function exportToPDF() {
    const reportContent = document.getElementById('fullReport').textContent;
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume_analysis_report.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function exportToJSON() {
    if (window.currentAnalysis) {
        const dataStr = JSON.stringify(window.currentAnalysis, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resume_analysis_data.json';
        a.click();
        URL.revokeObjectURL(url);
    }
}

function compareResumes() {
    document.getElementById('compareModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('compareModal').style.display = 'none';
}