# EmotionDetection/emotion_detection.py
import requests

WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def _none_result():
    """Return the required dict with all values set to None."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

def emotion_detector(text_to_analyze: str) -> dict:
    """
    Call Watson Emotion Predict and return:
      { anger, disgust, fear, joy, sadness, dominant_emotion }
    For blank/invalid input (HTTP 400), return the same dict with all values None.
    """
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        resp = requests.post(
            WATSON_EMOTION_URL,
            headers=HEADERS,
            json=payload,
            timeout=20,
        )

        # ---- Task 7 requirement: use status_code to drive behavior ----
        if resp.status_code == 400:
            # System response for blank/invalid entries → all None
            return _none_result()

        resp.raise_for_status()  # raise for other non-200 errors

        data = resp.json()

        # Extract typical structure
        emotions = {}
        if "emotionPredictions" in data and data["emotionPredictions"]:
            emotions = data["emotionPredictions"][0].get("emotion", {})
        elif "emotion" in data:  # fallback if API shape differs
            emotions = data.get("emotion", {})

        # Build scores (as floats)
        anger   = float(emotions.get("anger",   0.0))
        disgust = float(emotions.get("disgust", 0.0))
        fear    = float(emotions.get("fear",    0.0))
        joy     = float(emotions.get("joy",     0.0))
        sadness = float(emotions.get("sadness", 0.0))

        scores = {
            "anger": anger,
            "disgust": disgust,
            "fear": fear,
            "joy": joy,
            "sadness": sadness,
        }
        dominant = max(scores, key=scores.get) if any(scores.values()) else None

        return {**scores, "dominant_emotion": dominant}

    except requests.RequestException:
        # Network/other errors: return None values as a safe fallback
        return _none_result()
