import threading
from utils.OCR import OCR
from utils.text_analysis import TextAnalysis
from utils.request_sentiment import SentimentAnalysis


class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread()

