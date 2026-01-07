import re
from flask import Flask, render_template, request

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 1
        reasons.append("IP address used instead of domain")

    if re.search(r"(bit\.ly|tinyurl|t\.co|cutt\.ly)", url):
        score += 1
        reasons.append("URL shortener detected")

    if not url.startswith("https://"):
        score += 1
        reasons.append("HTTPS not used")

    if re.search(r"(login|verify|secure|account|update|bank)", url.lower()):
        score += 1
        reasons.append("Suspicious keywords found")

    if url.count('.') >= 4:
        score += 1
        reasons.append("Too many dots in URL")

    if score == 0:
        level = "Safe"
    elif score <= 2:
        level = "Low Risk"
    elif score <= 4:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return level, score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    score = None
    reasons = []
    url = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            result, score, reasons = analyze_url(url)

    return render_template(
        "index.html",
        result=result,
        score=score,
        reasons=reasons,
        url=url
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
