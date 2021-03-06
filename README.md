# MindTree Project
Team Member : 김수연, 김영민, 박태영, 장동기  
 
## 소개
MindTree는 사용자의 일기장을 저장하여 분석해주는 웹서비스입니다.  
 
## 기술set
Python 언어로 작성하고  
Flask App으로 개발하였으며  
git을 통한 버전관리와 업데이트를 하였습니다.  
 
## 기능구현내용
일기장을 분석하여 감정상태를 분석하여 웹페이지에 보여주는 기능을 구현하였습니다.  
일기장 작성 > 사진저장 > OCR분석 > 결과텍스트저장 or 직접 텍스트를 작성하여 저장  
일지저장목록 확인  
일기분석 > 일자별/기간별  
 
## 화면구성
메인 Page  
일기목록 Page  
업로드 Page  
분석결과 Page  
 
## Data Structure
-영구저장  
일기데이터저장객체(.json) > diaries/diary.json에 작성시간별로 추가  
-덮어쓰기/임시저장  
감정분석 실행 후 각 파일에 덮어쓰기  
감정분석객체(.json)생성 > report\sentiment.json에 덮어쓰기  
워드클라우드 이미지(.jpg)생성 > report\wordcloud.jpg에 덮어쓰기  
 
## Application Architecture  
 
API_key  
    key.json  
 
modules  
    OCR.py  
    request_sentiment.py  
    text_analysis.py  
    WordCloud.py  
 
results  
    user_diaryid.jpg  
    user_diaryid_ocr.txt  
    user_diaryid_sentiment.json  
    user_diaryid_wordcloud.jpg  
 
static  
    css  
        style.css  
    images  
        img.jpg  
    js  
        script.js  
 
utils  
    config.py  
    forms.py  
    models.py  
    routes.py  
    site.db  
    thread.py  
 
resources  
    testdata.jpg  
 
app.py  
