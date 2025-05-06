from flask import Flask, request, render_template_string
import pandas as pd
from difflib import get_close_matches
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)

# Load CSV
try:
    df = pd.read_csv("bristol_hs.csv")
    df = df.dropna(subset=["funding_per_student", "mcas_ela", "mcas_math", "mcas_science"], how="all")
except FileNotFoundError:
    df = None
    print("Error: bristol_hs.csv not found.")

def clean_school_name(name):
    if not isinstance(name, str):
        return ""
    return name.lower().replace("high school", "").strip()

def find_best_match(user_input, school_names):
    cleaned_input = clean_school_name(user_input)
    cleaned_list = [clean_school_name(name) for name in school_names]
    match = get_close_matches(cleaned_input, cleaned_list, n=1, cutoff=0.6)
    if match:
        index = cleaned_list.index(match[0])
        return school_names[index]
    return None

def analyze_school(school_name, df):
    matched_name = find_best_match(school_name, df["school_name"].tolist())
    if not matched_name:
        return f"<p>No close match found for '{school_name}'. Please check the spelling or try again.</p>"

    school_row = df[df["school_name"] == matched_name]
    other_schools = df[df["school_name"] != matched_name]

    comparisons = {
        "Funding per Student": ("funding_per_student", "${:,.2f}"),
        "MCAS ELA Score": ("mcas_ela", "{:.1f}"),
        "MCAS Math Score": ("mcas_math", "{:.1f}"),
        "MCAS Science Score": ("mcas_science", "{:.1f}")
    }

    comparison_text = f"<h2>Analyzing data for '{matched_name}'</h2>"

    # Percent Black Comparison
    if "percent_black" in school_row.columns:
        school_black = school_row["percent_black"].values[0]
        county_black = other_schools["percent_black"].mean()
        comparison_text += (
            f"<p><strong>Percent Black Students:</strong> {school_black:.1f}% "
            f"(vs County Average: {county_black:.1f}%)</p>"
        )
    else:
        comparison_text += "<p><strong>Percent Black Students:</strong> Not available.</p>"

    # Academic and funding comparisons
    available_metrics = {}
    for label, (col, fmt) in comparisons.items():
        school_val = school_row[col].values[0]
        avg_val = other_schools[col].mean()
        if pd.notna(school_val):
            comparison_text += f"<p><strong>{label}</strong>: {fmt.format(school_val)} vs County Average: {fmt.format(avg_val)}</p>"
            available_metrics[label] = (school_val, avg_val)
        else:
            comparison_text += f"<p><strong>{label}</strong>: Not enough information available.</p>"

    # Create chart if there is available data
    if available_metrics:
        categories = list(available_metrics.keys())
        school_vals = [v[0] for v in available_metrics.values()]
        avg_vals = [v[1] for v in available_metrics.values()]

        x = range(len(categories))
        width = 0.35
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar([i - width / 2 for i in x], school_vals, width=width, label=matched_name, color='#f9d342')
        ax.bar([i + width / 2 for i in x], avg_vals, width=width, label="All Other Schools", color='#888')

        ax.set_ylabel("Value")
        ax.set_title("School vs All Other Schools")
        ax.set_xticks(list(x))
        ax.set_xticklabels(categories)
        ax.legend()
        plt.tight_layout()

        filename = f"static/chart_{uuid.uuid4().hex}.png"
        plt.savefig(filename)
        plt.close()
        comparison_text += f"<img src='/{filename}' style='margin-top:20px; max-width:100%; border-radius:12px;'>"
    else:
        comparison_text += "<p>No chart available due to missing data for this school.</p>"

    return comparison_text

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        school_name = request.form.get("school_name")
        if df is not None:
            output = analyze_school(school_name, df)
        else:
            output = "<p>Error: Data not loaded.</p>"

    return render_template_string('''
        <html>
        <head>
            <style>
                body {
                    margin: 0;
                    font-family: 'Helvetica Neue', sans-serif;
                }
                .overlay {
                    background: rgba(0, 0, 0, 0.6);
                    min-height: 100vh;
                    padding: 60px 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: start;
                }
                h1 {
                    font-size: 2.8em;
                    margin-bottom: 30px;
                    color: #f9d342;
                    text-shadow: 2px 2px #222;
                }
                form {
                    margin-bottom: 30px;
                    background: rgba(255, 255, 255, 0.15);
                    padding: 20px;
                    border-radius: 15px;
                    backdrop-filter: blur(5px);
                }
                input[type="text"] {
                    padding: 10px;
                    width: 300px;
                    border: none;
                    border-radius: 8px;
                    font-size: 1em;
                    margin-right: 10px;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    background-color: #f9d342;
                    color: #333;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #f0c93b;
                }
                .result {
                    max-width: 800px;
                    text-align: left;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 15px;
                    backdrop-filter: blur(4px);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                }
                .result h2 {
                    color: #f9d342;
                }
            </style>
        </head>
        <body>
            <div class="overlay">
                <h1>Bristol County: Education Equity Analyzer</h1>
                <form method="post">
                    <input type="text" name="school_name" placeholder="Enter school name" required>
                    <input type="submit" value="Analyze">
                </form>
                <div class="result">{{ output|safe }}</div>
            </div>
        </body>
        </html>
    ''', output=output)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
