from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_url(url):
    patterns = {
        "IP address in URL": r"https?://\d+\.\d+\.\d+\.\d+",
        "URL shortener used": r"(bit\.ly|tinyurl|t\.co)",
        "Suspicious words found": r"(login|verify|secure|account|update)",
        "Too many dots": r"\..*\..*\..*"
    }

    reasons = []
    score = 0

    for reason, pattern in patterns.items():
        if re.search(pattern, url.lower()):
            score += 1
            reasons.append(reason)

    risk_levels = ["Safe", "Low Risk", "Medium Risk", "High Risk"]
    risk = risk_levels[min(score, 3)]

    return {
        "risk": risk,
        "score": score,
        "risk_percent": score * 25,
        "reasons": reasons
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        result = analyze_url(url)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()