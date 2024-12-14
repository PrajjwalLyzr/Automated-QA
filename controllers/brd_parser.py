from flask import Blueprint, request, render_template
from PyPDF2 import PdfReader
from markdown2 import markdown
import os
from models.qa_logic import parse_brd_with_llm, generate_test_cases

brd_parser = Blueprint("brd_parser", __name__)

@brd_parser.route("/upload", methods=["GET", "POST"])
def upload_brd():
    if request.method == "POST":
        file = request.files["brd_file"]
        if file and file.filename.endswith(".pdf"):
            try:
                # Read and extract text from PDF
                reader = PdfReader(file)
                brd_text = ""
                for page in reader.pages:
                    brd_text += page.extract_text()
                
                # Send text to GPT-4 for processing
                
                markdown_data = parse_brd_with_llm(brd_text)

                python_test_cases = generate_test_cases(user_stories=markdown_data)

                # Save the generated test cases to tests.py
                test_file_path = os.path.join("models", "tests.py")
                with open(test_file_path, "w") as test_file:
                    test_file.write("# Generated Test Cases\n\n")
                    test_file.write(python_test_cases)
                
                # Convert Markdown to HTML
                parsed_html = markdown(markdown_data)


                return render_template("results.html", parsed_html=parsed_html)
            except Exception as e:
                return render_template("error.html", message=f"Error: {str(e)}")
        else:
            return render_template("error.html", message="Please upload a valid PDF file.")
    return render_template("upload.html")


