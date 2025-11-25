import re
import PyPDF2
import docx
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class ResumeAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        
        # Common skills and keywords
        self.tech_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'tableau', 'powerbi']
        }
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_text(self, file_path):
        """Extract text based on file extension"""
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Use PDF or DOCX.")
    
    def extract_contact_info(self, text):
        """Extract contact information"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        return {
            'emails': emails,
            'phones': phones
        }
    
    def extract_skills(self, text):
        """Extract technical skills from resume"""
        text_lower = text.lower()
        found_skills = {}
        
        for category, skills in self.tech_skills.items():
            found_skills[category] = []
            for skill in skills:
                if skill in text_lower:
                    found_skills[category].append(skill)
        
        return found_skills
    
    def calculate_experience_years(self, text):
        """Estimate years of experience"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in'
        ]
        
        years = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 0
    
    def analyze_resume(self, file_path):
        """Main analysis function"""
        try:
            text = self.extract_text(file_path)
            
            # Tokenize and clean text
            tokens = word_tokenize(text.lower())
            filtered_tokens = [word for word in tokens if word.isalpha() and word not in self.stop_words]
            
            analysis = {
                'file_path': file_path,
                'contact_info': self.extract_contact_info(text),
                'skills': self.extract_skills(text),
                'experience_years': self.calculate_experience_years(text),
                'word_count': len(filtered_tokens),
                'most_common_words': Counter(filtered_tokens).most_common(10),
                'text_length': len(text)
            }
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_report(self, analysis):
        """Generate a formatted report"""
        if 'error' in analysis:
            return f"Error analyzing resume: {analysis['error']}"
        
        report = f"""
RESUME ANALYSIS REPORT
{'='*50}

File: {analysis['file_path']}
Text Length: {analysis['text_length']} characters
Word Count: {analysis['word_count']} words
Estimated Experience: {analysis['experience_years']} years

CONTACT INFORMATION:
- Emails: {', '.join(analysis['contact_info']['emails']) if analysis['contact_info']['emails'] else 'Not found'}
- Phones: {', '.join(analysis['contact_info']['phones']) if analysis['contact_info']['phones'] else 'Not found'}

TECHNICAL SKILLS FOUND:
"""
        
        for category, skills in analysis['skills'].items():
            if skills:
                report += f"- {category.title()}: {', '.join(skills)}\n"
        
        report += f"\nMOST FREQUENT WORDS:\n"
        for word, count in analysis['most_common_words']:
            report += f"- {word}: {count}\n"
        
        return report

# Example usage
if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    
    # Example: analyze a resume file
    # analysis = analyzer.analyze_resume("path/to/resume.pdf")
    # print(analyzer.generate_report(analysis))
    
    print("Resume Analyzer created successfully!")
    print("Usage: analyzer.analyze_resume('path/to/resume.pdf')")