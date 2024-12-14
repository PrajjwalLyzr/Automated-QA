from flask import Flask, render_template
from controllers.brd_parser import brd_parser

app = Flask(__name__)
app.register_blueprint(brd_parser, url_prefix="/brd")

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

