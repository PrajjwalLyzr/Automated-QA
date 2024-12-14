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
