from concurrent import futures

from mindtree.modules.OCR import OCR
from mindtree.modules.sentiment_analysis import SentimentAnalysis
from mindtree.modules.text_analysis import TextAnalysis
from mindtree.utils.util import get_time_str

from mindtree import db
from mindtree.models import Post


class ThreadedAnalysis:
    def __init__(self):
        self._ocr = None
        self._text_analyzer = None
        self._sentiment_analyzer = None

        self.ocr = None
        self.text_analyzer = None
        self.sentiment_analyzer = None
        self.initialized = False

    def init_and_analyze(self, post_id: int):
        """main function"""
        self.init_analyzers()
        self.analysis(post_id)

    def is_initialized(self):
        print(f"{get_time_str()} is worker initialied? ----- {self.initialized}")
        return self.initialized

    def init_analyzers(self):
        with futures.ThreadPoolExecutor() as executor:
            # 각 객체를 초기화한다.
            self._ocr = executor.submit(OCR)
            self._text_analyzer = executor.submit(TextAnalysis)
            self._sentiment_analyzer = executor.submit(SentimentAnalysis)

            if futures.wait([self._ocr, self._text_analyzer, self._sentiment_analyzer]):
                """ 세 futures 객체가 일을 마칠때 까지 기다린다. 
                    실제로 위 wait 메서드의 return 값은 각 객체가 일을 마칠때 까지 반환되지 않기 때문에,
                    if 문으로 바로 검증되지 않고 wait()가 return 될때까지 기다린다. 
                    True가 리턴되면 아래와 같이 각 분석 객체를 변수에 담는다."""

                self.ocr = self._ocr.result()
                self.text_analyzer = self._text_analyzer.result()
                self.sentiment_analyzer = self._sentiment_analyzer.result()

                print("[init_analyzers] initialization 완료")
                self.initialized = True

            return self

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
            f2_m = executor.submit(self.text_analyzer.text_analysis, post_id)
            f3_m = executor.submit(self.sentiment_analyzer.sentiment_analysis, post_id)

            futures.wait([f2_m, f3_m], timeout=10)

            try:
                post = Post.query.get_or_404(post_id)
                if f2_m.done():
                    if f3_m.done():
                        print('[analysis] f2_m 완료, f3_m 완료')
                        post.completed = True
                        post.error = False
                    else:
                        print('[analysis] f2_m 완료, f3_m 에러')
                        post.error = True
                elif f3_m.done():
                    print('[analysis] f2_m 에러, f3_m 완료')
                    post.error = True
                else:
                    print('[analysis] f2_m 에러, f3_m 에러')
                    post.error = True
            except Exception as e:
                """ thread 관련 오류든, 분석 모듈 관련 오류든, db 쿼리 관련 오류든
                어쨌든 오류이기 때문에 에러 플래그를 반영시킨다. """
                print('[analysis] ', e)
                post.error = True
            finally:
                db.session.commit()


if __name__ == '__main__':
    thr = ThreadedAnalysis()
    thr.init_and_analyze(3)
