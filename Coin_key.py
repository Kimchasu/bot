import tweepy
import config
import gspread
import time
import schedule

# config에서 api값 출력
api = config.create_api()

# Sheet에서 Sheet 연동 출력
gc = gspread.service_account(filename='enduring-sign-375216-cb27ccd0264a.json')
wks = gc.open("업보_상점계")

#해야되는거 > 저 씬네임에 행전체 훑어서 그걸 리스트로 불러온 다음 그거 for문으로 돌리게 하기

# 트윗수 코인 자동 정산
def tweet_calculate1():
    worksheet2 = wks.worksheet("코인정산시트")  # 코인정산시트 연동
    IDLIST = worksheet2.range('B3:B14') # ID Key값 위치 변환
    print(IDLIST)
    for IDLO in IDLIST: #지정 위치에서 각 셀값(ID) 가져오기
        ID = [IDLO.value]
        print(ID)

        for member in ID:  # 아이디 리스트에 인원 행으로 훑어서 넣기~!

            screen_name = str(member)
            user = api.get_user(id=screen_name)  # 유저 아이디값을 가지고 온다?
            cell2 = worksheet2.find(screen_name)
            statuses_count = user.statuses_count
            print(screen_name, "트윗 수 : " + str(statuses_count))

            current_count = user.statuses_count
            prev_count = int(worksheet2.cell(cell2.row, 4).value)
            changetweet = int(statuses_count // 10)
            print(prev_count)

            # print("현재 : ", current_count, "이전 : ", prev_count)

            for i in range(1, 16):
                if i == 4:  # 트윗 정산(D열)
                    worksheet2.update_cell(cell2.row, i, statuses_count)
                if i == 5:  # 정산된 트윗의 개수(E열)
                    a = int(statuses_count // 10)
                    worksheet2.update_cell(cell2.row, i, changetweet * 10)
                '''if i == 6:  # 변환된 코인의 개수(F열)
                    worksheet2.update_cell(cell2.row, i, statuses_count / 10 - statuses_count % 10)'''
                if i == 7:  # 오늘 내가 새로한 트윗의 개수
                    print(current_count - prev_count)
                    worksheet2.update_cell(cell2.row, i, current_count - prev_count)
                if i == 8:  # 오늘 내가 그래서 번 코인의 개수
                    newtweet = prev_count % 10 + (current_count - prev_count)
                    worksheet2.update_cell(cell2.row, i, newtweet // 10)

def tweet_calculate2():
    worksheet2 = wks.worksheet("코인정산시트")  # 코인정산시트 연동
    IDLIST = worksheet2.range('B15:B28') # ID Key값 위치 변환
    print(IDLIST)
    for IDLO in IDLIST: #지정 위치에서 각 셀값(ID) 가져오기
        ID = [IDLO.value]
        print(ID)

        for member in ID:  # 아이디 리스트에 인원 행으로 훑어서 넣기~!

            screen_name = str(member)
            user = api.get_user(id=screen_name)  # 유저 아이디값을 가지고 온다?
            cell2 = worksheet2.find(screen_name)
            statuses_count = user.statuses_count
            print(screen_name, "트윗 수 : " + str(statuses_count))

            current_count = user.statuses_count
            prev_count = int(worksheet2.cell(cell2.row, 4).value)
            changetweet = int(statuses_count // 10)
            print(prev_count)

            # print("현재 : ", current_count, "이전 : ", prev_count)

            for i in range(1, 16):
                if i == 4:  # 트윗 정산(D열)
                    worksheet2.update_cell(cell2.row, i, statuses_count)
                if i == 5:  # 정산된 트윗의 개수(E열)
                    a = int(statuses_count // 10)
                    worksheet2.update_cell(cell2.row, i, changetweet*10 )
                '''if i == 6:  # 변환된 코인의 개수(F열)
                    worksheet2.update_cell(cell2.row, i, statuses_count / 10 - statuses_count % 10)'''
                if i == 7:  # 오늘 내가 새로한 트윗의 개수
                    print(current_count - prev_count)
                    worksheet2.update_cell(cell2.row, i, current_count - prev_count)
                if i == 8:  # 오늘 내가 그래서 번 코인의 개수
                    newtweet = prev_count % 10 + (current_count - prev_count)
                    worksheet2.update_cell(cell2.row, i, newtweet // 10)


schedule.every().day.at("00:05").do(tweet_calculate1) #매일 5분에 1차 실행'''
schedule.every().day.at("00:07").do(tweet_calculate2) #매일 7분에 2차 실행

while True:
    schedule.run_pending()
    time.sleep(1)