# Data Access Object
# 데이터호출객체
import os
import json
import datetime
import VO

class DATA_OBJECT:
    def __init__(self):
        self.data = {}

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


# 디렉토리생성함수정의
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        print('Failed create directory')

# 디렉토리생성
createFolder('.\MindTree\diaries')

# 기능변수설정
diary_path = VO.diary_path
userid = VO.userid
userpw = VO.userpw
useremail = VO.useremail
diary_date = f"{datetime.datetime.now()}"
diary_data = VO.diary_data

# json_data생성 및 수정
json_data = {}
json_data[f"{userid}"] = {}
json_data[f"{userid}"]["userpw"] = f"{userpw}"
json_data[f"{userid}"]["useremail"] = f"{useremail}"
json_data[f"{userid}"]["username"] = "name"
json_data[f"{userid}"]["report"] = "sentiment"
json_data[f"{userid}"]["userdiary"] = {}
json_data[f"{userid}"]["userdiary"]["diarydate"] = f"{diary_date}"
json_data[f"{userid}"]["userdiary"]["diarydata"] = f"{diary_data}"

# json_data를 파일로 저장
with open(diary_path, 'w') as json_file:
    json.dump(json_data, json_file, indent="\t")

# json_data를 파일로부터 호출
with open(diary_path, "r") as json_file:
    json_data = json.load(json_file)
# print(json_data)
