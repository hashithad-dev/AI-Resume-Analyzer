from resume_analyzer import ResumeAnalyzer

def main():
    # Initialize the analyzer
    analyzer = ResumeAnalyzer()
    
    # Example usage
    print("Resume Analyzer - Example Usage")
    print("=" * 40)
    
    # Get file path from user
    file_path = input("Enter the path to your resume file (PDF or DOCX): ")
    
    try:
        # Analyze the resume
        print("\nAnalyzing resume...")
        analysis = analyzer.analyze_resume(file_path)
        
        # Generate and display report
        report = analyzer.generate_report(analysis)
        print(report)
        
        # Save report to file
        with open("resume_analysis_report.txt", "w") as f:
            f.write(report)
        print("\nReport saved to 'resume_analysis_report.txt'")
        
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()