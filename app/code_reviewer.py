import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

console = Console()

MODEL_NAME = "gemini-3.8-flash"
MAX_RETRIES = 3
RETRY_DELAY = 5


def read_source_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        console.print("[bold red]File not found:[/bold red] " + file_path)
        return None

    except PermissionError:
        console.print("[bold red]Permission denied:[/bold red] " + file_path)
        return None

    except UnicodeDecodeError:
        console.print("[bold red]Unable to decode file:[/bold red] " + file_path)
        return None

    except OSError as error:
        console.print("[bold red]File error:[/bold red] " + str(error))
        return None


def validate_response(response_text):
    if not response_text:
        return False

    if "## BUG_REPORT" not in response_text:
        return False

    if "## REFACTORED_CODE" not in response_text:
        return False

    return True


def build_prompt(source_code):

    prompt = (
        "Review the following Python source code as a senior code "
        "quality assurance engineer.\n\n"
        "SOURCE CODE:\n\n"
        "```python\n"
        + source_code
        + "\n```\n\n"
        "Your task is to identify bugs, potential runtime errors, "
        "logical problems, missing validation, and code quality issues.\n\n"
        "Then provide an improved and refactored version of the code.\n\n"
        "IMPORTANT OUTPUT RULES:\n\n"
        "1. Do not greet the user.\n"
        "2. Do not say Sure or I'd be happy to help.\n"
        "3. Be direct, analytical, and technical.\n"
        "4. Your response MUST contain these two sections:\n\n"
        "## BUG_REPORT\n\n"
        "Use concise bullet points describing the detected problems.\n\n"
        "## REFACTORED_CODE\n\n"
        "Provide the complete improved Python code inside ONE Markdown "
        "python code block.\n\n"
        "5. Do not add another major section.\n"
        "6. Do not invent problems that are not relevant to the supplied code.\n"
        "7. The refactored code must remain functional Python code."
    )

    return prompt


def review_code(source_code):

    if not API_KEY:
        console.print(
            "[bold red]ERROR:[/bold red] GEMINI_API_KEY was not found."
        )
        console.print(
            "Please add GEMINI_API_KEY to your .env file."
        )
        return None

    try:
        client = genai.Client(api_key=API_KEY)

    except Exception as error:
        console.print(
            "[bold red]Could not initialize Gemini client:[/bold red] "
            + str(error)
        )
        return None

    prompt = build_prompt(source_code)

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            console.print(
                "[yellow]Sending code for AI review "
                "(attempt "
                + str(attempt)
                + "/"
                + str(MAX_RETRIES)
                + ")...[/yellow]"
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a cold, analytical senior code quality "
                        "assurance engineer. "
                        "Do not behave like a conversational chatbot. "
                        "Focus on software defects, code quality, "
                        "validation, reliability, and refactoring."
                    ),
                    temperature=0.2,
                    max_output_tokens=4000,
                ),
            )

            response_text = response.text

            if validate_response(response_text):
                return response_text

            console.print(
                "[bold red]Invalid AI response:[/bold red] "
                "Required sections are missing."
            )

            return None

        except Exception as error:

            console.print(
                "[bold red]Gemini API error:[/bold red] "
                + str(error)
            )

            if attempt < MAX_RETRIES:
                console.print(
                    "[yellow]Retrying in "
                    + str(RETRY_DELAY)
                    + " seconds...[/yellow]"
                )

                time.sleep(RETRY_DELAY)

    console.print(
        "[bold red]All Gemini API attempts failed.[/bold red]"
    )

    return None


def main():

    if len(sys.argv) != 2:

        console.print("[bold yellow]Usage:[/bold yellow]")

        console.print(
            "python app\\code_reviewer.py sample_code\\buggy_code.py"
        )

        return

    file_path = sys.argv[1]

    console.print()
    console.print("=" * 60)
    console.print("       INTELLIGENT CODE REVIEWER")
    console.print("=" * 60)
    console.print()

    console.print(
        "[bold cyan]Analyzing:[/bold cyan] " + file_path
    )

    console.print()

    source_code = read_source_file(file_path)

    if source_code is None:
        return

    if not source_code.strip():
        console.print(
            "[bold red]Error:[/bold red] The source file is empty."
        )
        return

    response = review_code(source_code)

    if response is None:
        console.print(
            "[bold red]Code review could not be completed.[/bold red]"
        )
        return

    console.print()
    console.print("=" * 60)
    console.print("                  AI REVIEW")
    console.print("=" * 60)
    console.print()

    console.print(Markdown(response))

    console.print()
    console.print("=" * 60)
    console.print("              REVIEW COMPLETED")
    console.print("=" * 60)


if __name__ == "__main__":
    main()