from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    if not url.startswith("https://"):
        score += 1
        reasons.append("HTTPS not used")

    if re.search(r"(bit\.ly|tinyurl|t\.co|cutt\.ly)", url):
        score += 1
        reasons.append("URL shortener used")

    if re.search(r"(login|verify|secure|account|update)", url, re.I):
        score += 1
        reasons.append("Suspicious keywords found")

    if score == 0:
        risk = "Safe"
    elif score == 1:
        risk = "Low Risk"
    elif score == 2:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return risk, score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    risk = None
    score = None
    reasons = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            risk, score, reasons = analyze_url(url)

    return render_template(
        "index.html",
        risk=risk,
        score=score,
        reasons=reasons
    )


if __name__ == "__main__":
    app.run()
