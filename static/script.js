document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select a file');
        return;
    }
    
    showLoading();
    hideError();
    hideResults();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
        } else {
            displayResults(data.analysis, data.report);
        }
    } catch (error) {
        showError('Upload failed: ' + error.message);
    } finally {
        hideLoading();
    }
});

function displayResults(analysis, report) {
    // Update summary
    document.getElementById('experience').textContent = analysis.experience_years + ' years';
    document.getElementById('wordCount').textContent = analysis.word_count;
    document.getElementById('email').textContent = analysis.contact_info.emails[0] || 'Not found';
    document.getElementById('phone').textContent = analysis.contact_info.phones[0] || 'Not found';
    
    // Update skills
    const skillsContent = document.getElementById('skillsContent');
    skillsContent.innerHTML = '';
    
    for (const [category, skills] of Object.entries(analysis.skills)) {
        if (skills.length > 0) {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'skills-category';
            
            const title = document.createElement('h4');
            title.textContent = category;
            categoryDiv.appendChild(title);
            
            skills.forEach(skill => {
                const skillTag = document.createElement('span');
                skillTag.className = 'skill-tag';
                skillTag.textContent = skill;
                categoryDiv.appendChild(skillTag);
            });
            
            skillsContent.appendChild(categoryDiv);
        }
    }
    

    
    // Store analysis data globally for export
    window.currentAnalysis = analysis;
    
    // Update education
    const educationContent = document.getElementById('educationContent');
    educationContent.innerHTML = `
        <div class="education-section">
            <h4>Degrees</h4>
            <p>${analysis.education.degrees.join(', ') || 'None detected'}</p>
        </div>
        <div class="education-section">
            <h4>Certifications</h4>
            <p>${analysis.certifications.join(', ') || 'None detected'}</p>
        </div>
        <div class="education-section">
            <h4>Job Titles</h4>
            <p>${analysis.job_titles.join(', ') || 'None detected'}</p>
        </div>
    `;
    

    
    // Update full report
    document.getElementById('fullReport').textContent = report;
    
    showResults();
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showResults() {
    document.getElementById('results').classList.remove('hidden');
}

// Enhanced file input handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const analyzeBtn = document.querySelector('.analyze-btn');
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });
    
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    function handleFileSelect(file) {
        const uploadContent = document.querySelector('.upload-content');
        uploadContent.innerHTML = `
            <i class="fas fa-file-check" style="color: #4c51bf;"></i>
            <h3 style="color: #4c51bf;">${file.name}</h3>
            <p>File selected successfully</p>
        `;
        analyzeBtn.disabled = false;
    }
});

function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

