# test_emotion_detection.py
import unittest
from EmotionDetection import emotion_detector

TEST_CASES = [
    ("I am glad this happened",                      "joy"),
    ("I am really mad about this",                   "anger"),
    ("I feel disgusted just hearing about this",     "disgust"),
    ("I am so sad about this",                       "sadness"),
    ("I am really afraid that this will happen",     "fear"),
]

class TestEmotionDetection(unittest.TestCase):

    def test_dominant_emotions(self):
        for text, expected in TEST_CASES:
            with self.subTest(text=text, expected=expected):
                result = emotion_detector(text)

                # Basic structure checks
                self.assertIsInstance(result, dict, "Result should be a dict")
                self.assertIn("dominant_emotion", result)
                for k in ("anger", "disgust", "fear", "joy", "sadness"):
                    self.assertIn(k, result)

                # If your function returns 'error' on network issues, fail fast
                if "error" in result and result["error"]:
                    self.fail(f"API error while testing '{text}': {result['error']}")

                self.assertEqual(
                    result["dominant_emotion"], expected,
                    f"Text: {text}  | Expected: {expected}  | Got: {result['dominant_emotion']}"
                )

if __name__ == "__main__":
    unittest.main(verbosity=2)
