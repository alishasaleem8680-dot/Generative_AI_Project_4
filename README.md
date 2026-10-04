# Intelligent Code Reviewer & Explainer

## Overview

Intelligent Code Reviewer & Explainer is a Generative AI application that analyzes Python source code and provides an automated code quality review.

The application reads a Python source file, sends the source code to Google Gemini, identifies potential bugs and code quality issues, and generates a refactored version of the code.

## Features

* Python source code analysis
* Bug detection
* Code quality review
* Refactored code generation
* AI response validation
* File error handling
* Gemini API integration
* Automatic API retry mechanism
* Rich Markdown terminal rendering

## Architecture

```text
Python Source File
        |
        v
File Reader
        |
        v
Raw Source Code
        |
        v
Gemini API
        |
        v
AI Code Analysis
        |
        +-------------------+
        |                   |
        v                   v
  BUG_REPORT       REFACTORED_CODE
        |                   |
        +---------+---------+
                  |
                  v
        Response Validation
                  |
                  v
        Rich Markdown Rendering
                  |
                  v
           Terminal Output
```

## Technologies Used

* Python
* Google Gemini API
* Google GenAI Python SDK
* python-dotenv
* Rich

## Project Structure

```text
Generative_AI_Project_4
|
+-- app
|   +-- code_reviewer.py
|
+-- sample_code
|   +-- buggy_code.py
|   +-- test_code.py
|
+-- .gitignore
+-- README.md
+-- requirements.txt
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Add:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

The API key must never be uploaded to GitHub.

## Usage

Run the reviewer with:

```powershell
python app\code_reviewer.py sample_code\buggy_code.py
```

Another example:

```powershell
python app\code_reviewer.py sample_code\test_code.py
```

## Error Handling

The application handles:

* FileNotFoundError
* PermissionError
* UnicodeDecodeError
* Empty source files
* Gemini API errors

The application automatically retries failed Gemini API requests up to three times.

## Output Validation

The AI response is accepted only when it contains both required sections:

```text
## BUG_REPORT
```

and:

```text
## REFACTORED_CODE
```

This prevents incomplete or incorrectly formatted AI responses from being accepted as valid reviews.

## Example Output

The reviewer provides:

1. A bug report
2. Code quality observations
3. A refactored Python implementation

## Testing

The application was tested using multiple Python source files.

### Test 1

`sample_code/buggy_code.py`

The reviewer successfully identified potential division-by-zero issues, input validation problems, and code quality concerns.

### Test 2

`sample_code/test_code.py`

The reviewer successfully identified the division-by-zero error and generated a safer refactored version.

### Test 3

Missing file path

The application handles missing input files without crashing.

## Future Improvements

* Support additional programming languages
* Add a graphical web interface
* Export code review reports to PDF
* Add automated unit testing
* Add GitHub repository integration
