from concurrent import futures

# from .modules.OCR import OCR
from .modules.request_sentiment import SentimentAnalysis
from .modules.text_analysis import TextAnalysis
from .modules.util import get_time_str

from mindtree import db
from mindtree.models import Post


class Worker:
    def __init__(self):
        self._ocr = None
        self._text_analyzer = None
        self._sentiment_analyzer = None

        self.ocr = None
        self.text_analyzer = None
        self.sentiment_analyzer = None
        self.initialized = False

    def init_and_analyze(self, user_id, post_id):
        """main function"""
        self.init_analyzers()
        self.analysis(user_id, post_id)

    def is_initialized(self):
        print(f"{get_time_str()} is worker initialied? ----- {self.initialized}")
        return self.initialized

    def init_analyzers(self):
        with futures.ThreadPoolExecutor() as executor:
            # 각 객체를 초기화한다.
            self._ocr = executor.submit(OCR)
            self._text_analyzer = executor.submit(TextAnalysis)
            self._sentiment_analyzer = executor.submit(SentimentAnalysis)

            if True:  # for 문을 명백히 빠져나오는 것을 표현하려고 그냥 if 씀
                for f in futures.as_completed([self._ocr, self._text_analyzer, self._sentiment_analyzer]):
                    # 중복해서 담기긴 하지만 실행에는 문제 없어서 놔두기로함.
                    self.ocr = self._ocr.result()
                    self.text_analyzer = self._text_analyzer.result()
                    self.sentiment_analyzer = self._sentiment_analyzer.result()
                self.initialized = True

    def analysis(self, post_id):
        print("thread.analysis", post_id)
        with futures.ThreadPoolExecutor() as executor:
            # 1. OCR 시작. 끝날때까지 기다린다.
            f1_m = executor.submit(self.ocr.ocr_main, post_id)
            futures.wait([f1_m])

            # 1-2. 완료 로그찍기
            if f1_m.done():
                print("f1_m 완료")
            else:
                print("f1_m 오류발생")
                f1_m.cancel()

            # 2. 감성분석, 텍스트 분석 모두 실행.
            f2_m = executor.submit(self.text_analyzer.text_analysis, user_id, post_id)
            f3_m = executor.submit(self.sentiment_analyzer.sentiment_analysis, user_id, post_id)

            # 2-2. 완료되면 로그찍기
            i = 2
            for f in futures.as_completed([f2_m, f3_m]):
                if f.done():
                    print(i, "완료")
                    i += 1
                    continue
                else:
                    f.cancel()

        # 분석이 끝난 후 db에 완료 했음을 저장.
        post = Post.query.get(post_id)
        post.completed = True
        db.session.commit()

        return None


# 외부에서 바로 불러서 사용할 수 있도록 여기에 선언해둠.
worker = Worker()
