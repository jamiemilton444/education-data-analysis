from flask import Flask, request, render_template_string
import pandas as pd
from difflib import get_close_matches

app = Flask(__name__)

# Load your CSV once when the server starts
df = pd.read_csv("bristol_hs.csv")

# Paste your functions below (clean_school_name, find_best_match, analyze_school)
# ...

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        school_name = request.form.get("school_name")
        output = analyze_school(school_name, df)

    return render_template_string('''
        <h1>Education Equity Analyzer</h1>
        <form method="post">
            <input type="text" name="school_name" placeholder="Enter your school name" required>
            <input type="submit" value="Analyze">
        </form>
        <div>{{ output|safe }}</div>
    ''', output=output)

if __name__ == "__main__":
    app.run(debug=True)
