from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os

# Configure API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use latest Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            prompt = request.form.get("prompt")

            if not prompt:
                return "Please enter a prompt."

            response = model.generate_content(prompt)

            if response and response.text:
                return response.text
            else:
                return "Gemini did not return a response."

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)