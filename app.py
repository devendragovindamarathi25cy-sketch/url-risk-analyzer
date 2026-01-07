from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    # Rule 1: HTTPS check
    if not url.startswith("https://"):
        score += 1
        reasons.append("HTTPS not used")

    # Rule 2: URL shorteners
    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl"]
    if any(s in url for s in shorteners):
        score += 1
        reasons.append("URL shortener used")

    # Rule 3: Suspicious words
    suspicious_words = ["login", "verify", "secure", "account", "update"]
    if any(word in url.lower() for word in suspicious_words):
        score += 1
        reasons.append("Suspicious keyword found")

    # Rule 4: IP-based URL
    if re.match(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 1
        reasons.append("IP address used instead of domain")

    # Risk level
    if score <= 1:
        risk = "Low Risk"
    elif score <= 3:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return risk, score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    risk = score = reasons = None

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
    app.run(host="0.0.0.0", port=10000)
