from gemini_analyzer import GeminiResumeAnalyzer

def main():
    try:
        # Initialize the AI-enhanced analyzer
        analyzer = GeminiResumeAnalyzer()
        
        print("AI-Enhanced Resume Analyzer")
        print("=" * 40)
        
        # Get file path from user
        file_path = input("Enter the path to your resume file (PDF or DOCX): ")
        
        print("\nAnalyzing resume with AI insights...")
        
        # Enhanced analysis with AI
        analysis = analyzer.enhanced_analyze_resume(file_path)
        
        # Generate enhanced report
        report = analyzer.generate_enhanced_report(analysis)
        print(report)
        
        # Save report
        with open("ai_resume_analysis_report.txt", "w", encoding='utf-8') as f:
            f.write(report)
        print("\nEnhanced report saved to 'ai_resume_analysis_report.txt'")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()