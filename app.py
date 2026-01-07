from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            if url.startswith("http://") or url.startswith("https://"):
                result = "URL format looks valid"
            else:
                result = "Invalid URL format"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)