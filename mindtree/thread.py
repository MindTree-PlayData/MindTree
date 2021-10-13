# import threading
from concurrent import futures
from .utils.OCR import OCR
from .utils.text_analysis import TextAnalysis
from .utils.request_sentiment import SentimentAnalysis


def analysis_threading(user_id):
    with futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(OCR)
        f2 = executor.submit(TextAnalysis)
        f3 = executor.submit(SentimentAnalysis)

        for f in futures.as_completed([f1, f2, f3]):
            f1_m = executor.submit(f1.result().ocr_main, user_id)
            futures.wait([f1_m])

        f2_m = executor.submit(f2.result().text_mining, user_id)
        f3_m = executor.submit(f3.result().sentiment_analysis, user_id)

    return None

