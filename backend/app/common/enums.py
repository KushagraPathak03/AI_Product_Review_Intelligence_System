from enum import Enum


class ProductCategory(str, Enum):
    SMARTPHONE = "Smartphone"
    LAPTOP = "Laptop"
    SMARTWATCH = "Smartwatch"
    EARBUDS = "Earbuds"
    HEADPHONES = "Headphones"
    BLUETOOTH_SPEAKER = "Bluetooth Speaker"
    CAMERA = "Camera"
    TABLET = "Tablet"
    MONITOR = "Monitor"
    KEYBOARD = "Keyboard"
    MOUSE = "Mouse"
    POWER_BANK = "Power Bank"
    CHARGER = "Charger"


class ReviewSource(str, Enum):
    AMAZON = "Amazon"
    FLIPKART = "Flipkart"
    YOUTUBE = "YouTube"
    REDDIT = "Reddit"


class SentimentLabel(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"