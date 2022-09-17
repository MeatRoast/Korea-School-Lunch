import pymysql
import requests
from bs4 import BeautifulSoup
import time

# DB 접속
host = ''
port = int('')
user = ''
pw = ''
db = ''
con = pymysql.connect(host=host, port=port, user=user, password=pw, database=db, charset='utf8')
cur = con.cursor()
print('[INFO] [ DB 연결이 완료되었습니다. ]')

#학교검색
arg1 = input("학교를 입력해주세요: ")

#DB 찾기
sql = "SELECT * FROM school_db where school_name = %s"

cur.execute(sql,(arg1))
rows = cur.fetchall()
print(rows)

# 데이터 가져옴
for row in rows:
    print(row[0], row[1], row[2])
    koreaS_code = row[1]
    school_code = row[2]

time1 = time.strftime('%Y%m%d')
sch2 = f'{arg1}'
surl = "https://open.neis.go.kr/hub/mealServiceDietInfo?"
test = f"ATPT_OFCDC_SC_CODE={koreaS_code}&SD_SCHUL_CODE={school_code}&MMEAL_SC_CODE=2&MLSV_YMD={time1}"
url = surl + test
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
rlist = soup.findAll('row')

#가져온 데이터 정리
for r in rlist:
    dd = r.find('ddish_nm').text
    dd2 = dd.replace("<br/>", "\n")+"\n\n"

print(dd2)