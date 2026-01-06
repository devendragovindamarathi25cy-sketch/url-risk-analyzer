from flask import Flask, render_template, request
import re

app = Flask(__name__)

def url_risk(url):
    score = 0
    reasons = []
    url = url.lower()

    total_checks = 8  # total risk checks

    # 1. IP address check
    if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 1
        reasons.append("IP address used instead of domain")

    # 2. URL shortener check
    if re.search(r"(bit\.ly|tinyurl|t\.co|goo\.gl|is\.gd)", url):
        score += 1
        reasons.append("URL shortener detected")

    # 3. Suspicious keywords
    suspicious_words = [
        "login", "verify", "secure", "account",
        "update", "bank", "payment", "password"
    ]

    for word in suspicious_words:
        if word in url:
            score += 1
            reasons.append(f"Suspicious keyword found: {word}")
            break

    # 4. Too many dots
    if url.count(".") > 3:
        score += 1
        reasons.append("Too many dots in URL")

    # 5. Too many hyphens
    if url.count("-") > 2:
        score += 1
        reasons.append("Too many hyphens in URL")

    # 6. HTTPS missing
    if not url.startswith("https://"):
        score += 1
        reasons.append("HTTPS not used")

    # 7. Long URL
    if len(url) > 75:
        score += 1
        reasons.append("URL is unusually long")

    # 8. @ symbol trick
    if "@" in url:
        score += 1
        reasons.append("Uses @ symbol (redirect trick)")

    # Risk percentage calculation
    risk_percent = int((score / total_checks) * 100)

    # Risk level
    if risk_percent <= 20:
        risk = "Safe"
    elif risk_percent <= 40:
        risk = "Low Risk"
    elif risk_percent <= 70:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return risk, score, risk_percent, reasons


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        risk, score, risk_percent, reasons = url_risk(url)
        result = {
            "url": url,
            "risk": risk,
            "score": score,
            "risk_percent": risk_percent,
            "reasons": reasons
        }
    return render_template("index.html", result=result)


if __name__ == "__main__":
    # IMPORTANT FOR ANDROID / PYDROID
    app.run(host="0.0.0.0", port=5000, debug=True)