from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 2
        reasons.append("IP address detected")

    if re.search(r"(bit\.ly|tinyurl|t\.co|goo\.gl)", url):
        score += 2
        reasons.append("URL shortener used")

    if re.search(r"(login|verify|secure|account|update)", url.lower()):
        score += 1
        reasons.append("Suspicious keywords found")

    if url.count('.') > 4:
        score += 1
        reasons.append("Too many dots in URL")

    if not url.startswith("https://"):
        score += 1
        reasons.append("HTTPS not used")

    if score == 0:
        risk = "Safe"
    elif score <= 2:
        risk = "Low Risk"
    elif score <= 4:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return risk, score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    score = ""
    reasons = []

    if request.method == "POST":
        url = request.form.get("url")
        result, score, reasons = analyze_url(url)

    return render_template(
        "index.html",
        result=result,
        score=score,
        reasons=reasons
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)