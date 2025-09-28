# EmotionDetection/__init__.py
"""
Package initializer for EmotionDetection.

Exposes:
    emotion_detector(text: str) -> dict
"""

from .emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
