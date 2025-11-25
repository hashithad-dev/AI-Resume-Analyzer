import re
from resume_analyzer import ResumeAnalyzer
from collections import Counter
import json

class EnhancedResumeAnalyzer(ResumeAnalyzer):
    def __init__(self):
        super().__init__()
        
        # Education keywords
        self.education_keywords = {
            'degrees': ['bachelor', 'master', 'phd', 'doctorate', 'mba', 'bs', 'ms', 'ba', 'ma'],
            'fields': ['computer science', 'engineering', 'business', 'marketing', 'finance', 'data science']
        }
        
        # Certification keywords
        self.certifications = ['aws', 'azure', 'google cloud', 'cisco', 'microsoft', 'oracle', 'pmp', 'scrum']
        
        # Job titles for experience matching
        self.job_titles = ['developer', 'engineer', 'manager', 'analyst', 'consultant', 'architect', 'lead', 'senior']
    
    def extract_education(self, text):
        """Extract education information"""
        text_lower = text.lower()
        found_education = {
            'degrees': [],
            'fields': [],
            'universities': []
        }
        
        # Find degrees
        for degree in self.education_keywords['degrees']:
            if degree in text_lower:
                found_education['degrees'].append(degree)
        
        # Find fields of study
        for field in self.education_keywords['fields']:
            if field in text_lower:
                found_education['fields'].append(field)
        
        # Find university patterns
        university_pattern = r'university|college|institute'
        universities = re.findall(r'\b\w+\s+(?:university|college|institute)\b', text_lower)
        found_education['universities'] = universities[:3]  # Limit to 3
        
        return found_education
    
    def extract_certifications(self, text):
        """Extract certifications"""
        text_lower = text.lower()
        found_certs = []
        
        for cert in self.certifications:
            if cert in text_lower:
                found_certs.append(cert)
        
        return found_certs
    
    def extract_job_titles(self, text):
        """Extract job titles and roles"""
        text_lower = text.lower()
        found_titles = []
        
        for title in self.job_titles:
            if title in text_lower:
                found_titles.append(title)
        
        return list(set(found_titles))
    

    
    def enhanced_analyze_resume(self, file_path):
        """Enhanced analysis with additional features"""
        # Get basic analysis
        basic_analysis = self.analyze_resume(file_path)
        
        if 'error' in basic_analysis:
            return basic_analysis
        
        # Extract text for additional analysis
        text = self.extract_text(file_path)
        
        # Add enhanced features
        basic_analysis.update({
            'education': self.extract_education(text),
            'certifications': self.extract_certifications(text),
            'job_titles': self.extract_job_titles(text),

        })
        
        return basic_analysis
    
    def generate_enhanced_report(self, analysis):
        """Generate enhanced report with new features"""
        if 'error' in analysis:
            return f"Error analyzing resume: {analysis['error']}"
        
        basic_report = self.generate_report(analysis)
        
        # Add enhanced sections
        enhanced_sections = f"""
EDUCATION:
- Degrees: {', '.join(analysis['education']['degrees']) if analysis['education']['degrees'] else 'Not detected'}
- Fields: {', '.join(analysis['education']['fields']) if analysis['education']['fields'] else 'Not detected'}
- Universities: {', '.join(analysis['education']['universities']) if analysis['education']['universities'] else 'Not detected'}

CERTIFICATIONS:
{', '.join(analysis['certifications']) if analysis['certifications'] else 'None detected'}

JOB TITLES/ROLES:
{', '.join(analysis['job_titles']) if analysis['job_titles'] else 'None detected'}

"""
        
        return basic_report + enhanced_sections