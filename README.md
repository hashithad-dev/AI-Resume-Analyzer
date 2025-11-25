# Resume Analyzer

A Python tool for analyzing resumes and extracting key information.

## Features

- Extract text from PDF and DOCX files
- Identify contact information (emails, phone numbers)
- Detect technical skills across multiple categories
- Estimate years of experience
- Generate detailed analysis reports
- Word frequency analysis

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```python
from resume_analyzer import ResumeAnalyzer

analyzer = ResumeAnalyzer()
analysis = analyzer.analyze_resume("path/to/resume.pdf")
report = analyzer.generate_report(analysis)
print(report)
```

### Interactive Usage
```bash
python example_usage.py
```

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx)

## Skills Categories

The analyzer detects skills in these categories:
- Programming languages
- Web technologies
- Databases
- Cloud platforms
- Data science tools