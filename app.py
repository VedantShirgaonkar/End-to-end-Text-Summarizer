from flask import Flask, render_template, request
from src.textSummarizer.pipeline.prediction import PredictionPipeline

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """
    Loads the main UI page.
    """
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Takes text from the form, generates a summary,
    and renders the page with the result.
    """
    try:
        text = request.form["text"]
        obj = PredictionPipeline()
        summary = obj.predict(text)
        return render_template("index.html", summary=summary, original_text=text)
    except Exception as e:
        return render_template("index.html", error=str(e))

if __name__ == "__main__":
    # Flask's default port is 5000, but you can change it to 80 for Azure
    app.run(host="0.0.0.0", port=80)