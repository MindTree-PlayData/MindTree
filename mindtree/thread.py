# import threading
from concurrent import futures
from .utils.OCR import OCR
from .utils.text_analysis import TextAnalysis
from .utils.request_sentiment import SentimentAnalysis


def analysis_threading(user_id):

    with futures.ThreadPoolExecutor() as executor:
        # 각 객체를 초기화한다.
        f1 = executor.submit(OCR)
        f2 = executor.submit(TextAnalysis)
        f3 = executor.submit(SentimentAnalysis)

        # 1. OCR 시작. 끝날때까지 기다린다.
        futures.as_completed([f1])  # f1 완료 되면..
        f1_m = executor.submit(f1.result().ocr_main, user_id)
        futures.wait([f1_m])

        if f1_m.done():
            print("f1_m 완료")
        else:
            print("f1_m 오류발생")
            f1_m.cancel()

        # 2. 감성분석, 텍스트 분석 모두 실행.
        f2_m = executor.submit(f2.result().text_mining, user_id)
        f3_m = executor.submit(f3.result().sentiment_analysis, user_id)

        # 완료되면 로그찍기
        i = 2
        for f in futures.as_completed([f2_m, f3_m]):
            if f.done():
                print(i, "완료")
                i += 1
                continue
            else:
                f.cancel()


    return None

