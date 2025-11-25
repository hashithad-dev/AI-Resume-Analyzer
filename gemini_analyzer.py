import os
import google.generativeai as genai
from dotenv import load_dotenv
from resume_analyzer import ResumeAnalyzer

class GeminiResumeAnalyzer(ResumeAnalyzer):
    def __init__(self):
        super().__init__()
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def ai_analyze_resume(self, text):
        """Use Gemini AI to analyze resume content"""
        prompt = f"""
        Analyze this resume and provide insights:
        
        {text}
        
        Please provide:
        1. Overall assessment (strengths/weaknesses)
        2. Career level estimation
        3. Skill gaps or recommendations
        4. Industry fit suggestions
        5. Resume improvement tips
        
        Keep response concise and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI analysis failed: {str(e)}"
    
    def enhanced_analyze_resume(self, file_path):
        """Enhanced analysis with AI insights"""
        # Get basic analysis
        basic_analysis = self.analyze_resume(file_path)
        
        if 'error' in basic_analysis:
            return basic_analysis
        
        # Extract text for AI analysis
        text = self.extract_text(file_path)
        
        # Add AI insights
        basic_analysis['ai_insights'] = self.ai_analyze_resume(text)
        
        return basic_analysis
    
    def generate_enhanced_report(self, analysis):
        """Generate report with AI insights"""
        basic_report = self.generate_report(analysis)
        
        if 'ai_insights' in analysis:
            ai_section = f"""
AI INSIGHTS:
{'='*50}
{analysis['ai_insights']}
"""
            return basic_report + ai_section
        
        return basic_report