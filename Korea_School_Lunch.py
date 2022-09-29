# V. 2.1.5 ( 2022.09.29 )
# 조식/중식/석식 선택이 추가되었습니다.
# 검색 시스템이 개선 되었습니다.
# DB에 학교 정보가 없으면 예외 변수가 표시됩니다.
# 급식 식단이 없으면 예외 변수가 표시됩니다.
# 나이스 API로 제작되었습니다 ( https://open.neis.go.kr/ )


# 모듈
import pymysql
import time
import requests
from bs4 import BeautifulSoup

# 검색
학교입력 = input("조회하실 학교를 입력해주세요: ")
급식_선택 = input("조식/중식/석식 중 선택해주세요: ")


# DB접속
host = ''
port = int('')
user = ''
pw = ''
db = 'school'
con = pymysql.connect(host=host, port=port, user=user, password=pw, database=db, charset='utf8')
cur = con.cursor()
print('[INFO] [ 학교 정보 DB 연결이 완료되었습니다. ]')
sql = "SELECT * FROM school_db where school_name = %s"
cur.execute(sql,(학교입력))
rows = cur.fetchall()
print(rows)
#DB검색이안될경우
if rows == ():
    print("해당 학교의 DB정보를 찾을수 없습니다.\n( 오류이유: 오타, 신설학교 ) \nV.2022.09.29")

# 검색이되면
else:
    # DB에서 가져온 데이터 정리
    for row in rows:
        print(row[0], row[1], row[2])
        koreacode = row[1]
        schoolcode= row[2]
        # 오늘날짜
        time1 = time.strftime('%Y%m%d')
        # API URL 기본
        surl = "https://open.neis.go.kr/hub/mealServiceDietInfo?"

        # 중식 부분
        if 급식_선택 == "중식":
            # API URL 세부
            test = f"ATPT_OFCDC_SC_CODE={koreacode}&SD_SCHUL_CODE={schoolcode}&MMEAL_SC_CODE=2&MLSV_YMD={time1}"
            # API URL
            url = surl + test
            # URL 콘솔창 표시
            print(url)
            # 급식 데이터 가져오기
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            rlist = soup.findAll('row')
            # 해당 학교 급식정보가 없을 경우
            if rlist == []:
                print(f"{학교입력} 급식 정보가 없습니다.")
            # 급식정보가 있을경우
            else:
                for r in rlist:
                    # 테스트로 저장    
                    dd = r.find('ddish_nm').text
                    # 데이터 정리
                    dd2 = dd.replace("<br/>", "\n")+"\n\n"
                    #급식 정보 표시
                    print(f"{학교입력} 급식정보입니다")
                    print("중식\n")
                    print(dd2)

        # 조식 부분 위와 형식 같음
        if 급식_선택 == "조식":
            test = f"ATPT_OFCDC_SC_CODE={koreacode}&SD_SCHUL_CODE={schoolcode}&MMEAL_SC_CODE=1&MLSV_YMD={time1}"
            url = surl + test
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            rlist = soup.findAll('row')
            if rlist == []:
                print(f"{학교입력} 급식 정보가 없습니다.")
            else:
                for r in rlist:
                    dd = r.find('ddish_nm').text
                    dd2 = dd.replace("<br/>", "\n")+"\n\n"
                    
                    print(f"{학교입력} 급식정보입니다")
                    print("조식\n")
                    print(dd2)

        # 서식 부분 위와 형식 같음
        if 급식_선택 == "석식":
            surl = "https://open.neis.go.kr/hub/mealServiceDietInfo?"
            test = f"ATPT_OFCDC_SC_CODE={koreacode}&SD_SCHUL_CODE={schoolcode}&MMEAL_SC_CODE=3&MLSV_YMD={time1}"
            url = surl + test
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            rlist = soup.findAll('row')
            if rlist == []:
                print(f"{학교입력} 급식 정보가 없습니다.")
            else:
                for r in rlist:
                    dd = r.find('ddish_nm').text
                    dd2 = dd.replace("<br/>", "\n")+"\n\n"
                    
                    print(f"{학교입력} 급식정보입니다")
                    print("석식\n")
                    print(dd2)
