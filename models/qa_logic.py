from openai import OpenAI 
from selenium import webdriver
import pytest
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

MODEL="gpt-4o-mini"
OPENAI_API_KEY = os.getenv("OPENAIKEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def parse_brd_with_llm(brd_text):
    """Parse BRD using GPT-4 to generate user stories."""
    response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You're an expert QA analyst."}, 
                        {"role": "user", "content": f"Parse this BRD into actionable user stories and test criteria:\n{brd_text}"}  
                    ]
                    )
    
    return response.choices[0].message.content

def generate_test_cases(user_stories):
    """Generate Python test cases from user stories."""

    response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You're a QA automation expert."},
                        {"role": "user", "content": f"Generate Python test cases for the following user stories:\n{user_stories}. [!Important] Just proide clean and pure python code, nothing else. Don't provdide any note or text just python code."}
                    ]
                    )
    
    return response.choices[0].message.content
    

def execute_ui_test_cases(url):
    """Run UI tests using Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # Example test case
        assert "Example" in driver.title
        return "All UI tests passed"
    except AssertionError:
        return "UI Test Failed"
    finally:
        driver.quit()


def run_tests_and_generate_report():
    """Run all pytest test cases and generate an HTML report."""
    pytest_command = "pytest --html=reports/test_report.html --self-contained-html"
    process = subprocess.run(pytest_command, shell=True, capture_output=True, text=True)

    if process.returncode == 0:
        return "Tests executed successfully. Report generated."
    else:
        return f"Test execution failed:\n{process.stderr}"
