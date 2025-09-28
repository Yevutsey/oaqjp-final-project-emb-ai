"""
Flask web app for Emotion Detection (Skills Network final project)

- GET "/" renders the UI.
- /emotionDetector accepts GET or POST.
  * Reads input from querystring, form data, or JSON as "textToAnalyze".
  * Calls the EmotionDetection.emotion_detector() function.
  * If the function indicates invalid input (dominant_emotion is None),
    returns the message "Invalid text! Please try again!" with HTTP 200 so
    the front-end always displays it.
  * Otherwise returns the formatted plain-text result.
"""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector  # your package function

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """Endpoint used by the front-end to analyze text."""
    # Accept the text from query string (?textToAnalyze=...), form, or JSON.
    text = (
        request.args.get("textToAnalyze")
        or request.form.get("textToAnalyze")
        or (request.get_json(silent=True) or {}).get("textToAnalyze")
        or ""
    )

    # Run the analysis
    result = emotion_detector(text)

    # If the analysis signals invalid/blank input, show friendly message.
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!", 200, {
            "Content-Type": "text/plain; charset=utf-8"
        }

    # Build the formatted response expected by the assignment
    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )

    return response_text, 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    # Expose on 0.0.0.0:5000 so the lab preview can reach it
    app.run(host="0.0.0.0", port=5000, debug=True)
