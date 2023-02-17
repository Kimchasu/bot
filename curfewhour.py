import config
import gspread
import schedule
import time

#config에서 api값 출력
api = config.create_api()

# Sheet에서 Sheet 연동 출력
gc = gspread.service_account(filename='enduring-sign-375216-cb27ccd0264a.json')
wks = gc.open("업보_상점계")

#통금 공지
def printtime():
	api.update_status("▪︎ 귀기가 강해질 시간입니다. 다들 문을 굳건히 걸어잠그시기 바랍니다." + "\n\n" + "(퍼블트 및 상점 이용을 제한합니다.01:00~07:00)")

schedule.every().day.at("01:00").do(printtime)

#통금 해제 공지
def printtime2():
	api.update_status("▪︎ 귀기가 옅어질 시간입니다. 신을 모시기 위한 사당의 문이 열립니다." + "\n\n" + "(퍼블트 및 상점 이용이 가능합니다.)")

schedule.every().day.at("07:00").do(printtime2)

#식단 안내 문구_아침
def printtime3():
	api.update_status("전 리조트에 방송이 울려 퍼집니다.\n[아침식사 배식이 시작되오니 식사하실 각 기관분들께서는 식당으로 방문 바랍니다.]\n \n▪︎ 식단은 합격자 가이드 문서 및 진행계 마음함에서 확인하실 수 있습니다. ")

schedule.every().day.at("07:01").do(printtime3)

#식단 안내 문구_점심
def printtime4():
	api.update_status("전 리조트에 방송이 울려 퍼집니다.\n[점심식사 배식이 시작되오니 식사하실 각 기관분들께서는 식당으로 방문 바랍니다.]\n \n▪︎ 식단은 합격자 가이드 문서 및 진행계 마음함에서 확인하실 수 있습니다. ")

schedule.every().day.at("12:00").do(printtime4)

#식단 안내 문구_저녁
def printtime5():
	api.update_status("전 리조트에 방송이 울려 퍼집니다.\n[저녁식사 배식이 시작되오니 식사하실 각 기관분들께서는 식당으로 방문 바랍니다.]\n \n▪︎ 식단은 합격자 가이드 문서 및 진행계 마음함에서 확인하실 수 있습니다. ")

schedule.every().day.at("19:00").do(printtime5)

#스케줄 반복 및 날짜 설정(14일 후 자동 중지)
while True:
    schedule.run_pending()
    time.sleep(1)
