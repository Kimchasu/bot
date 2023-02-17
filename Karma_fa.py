import time
import random
import gspread
import pprint
import config

# config에서 api값 출력
api = config.create_api()

# Sheet에서 Sheet 연동 출력
gc = gspread.service_account(filename='enduring-sign-375216-cb27ccd0264a.json')
wks = gc.open("업보_상점계")

# 주술청 연동
worksheetju = wks.worksheet('주술청')
memberlistju = worksheetju.get_all_records()

# 위령청 연동
worksheetye = wks.worksheet('위령청')
memberlistye = worksheetye.get_all_records()

# 퇴마청 연동
worksheetma = wks.worksheet('퇴마청')
memberlistma = worksheetma.get_all_records()

# 전인원 연동
worksheetup = wks.worksheet('업보')
memberlistup = worksheetup.get_all_records()

# 코인정산시트 연동
worksheetco = wks.worksheet('코인정산시트')
worksheetshop = wks.worksheet('상점물품')
worksheetlucky = wks.worksheet('오늘의운세')
Luckysheetlist = worksheetlucky.get_all_records()
Shop_List = worksheetshop.get_all_records()

# 멘답하는 봇 만들기
bot = api.verify_credentials() # 봇의 user obj 반환
bot_id = bot.id # 봇 id (고유값, 주소)
timeline_list = api.user_timeline(user_id=bot_id)
last_reply_id = timeline_list[0].id_str
keywords = ['주사위', '퇴마청', '위령청', '주술청', '아침출석', '저녁출석', '사정정산', '상점','홀짝','업보','노래방점수']  # 키워드


# 주의!!! 리트윗과 멘션 합해서 3시간에 300개 가능 (트위터 API 정책)

# 새 멘션 확인하는 함수
def check_new_mention():
    print("! 멘션을 확인하는 함수를 호출합니다")
    global last_reply_id
    mention_return = api.mentions_timeline(since_id=last_reply_id) # since_id 이후의 트윗만 가져온다.
    mention_return_length = len(mention_return) # 받아온 새 멘션의 개수

    if mention_return_length > 0:
        print('! 키워드를 체크하는 함수를 호출합니다.')
        check_keyword(mention_return_length, mention_return)  # 키워드 체크하는 함수. 새 멘션 개수와, 새 멘션들을 매개변수로 넘긴다.
        print('! 다음 동작 시간을 기다립니다')
        return  # return을 만났으니 44줄로는 가지 않고 mention_return_length 함수를 빠져나간다

    print('! 새 멘션이 없습니다.')

def check_keyword(mention_return_length, mention_return):
    for i in range(mention_return_length - 1, -1, -1):  # 최신 멘션부터 불러오기 때문에 거꾸로 순회
        mention = mention_return[i]  # 현재 보고 있는 멘션
        mention_text = mention.text  # 의 내용
        keyword_type = -1

        # 키워드 체크 함수

        try:
            if mention.author.id != bot_id:  # 내가 보낸 멘션이 아닐때만 답멘
                # [] 가 존재하나?
                start = mention_text.find('[')
                end = mention_text.find(']')

                if (start != -1 and end != -1) and start < end:  # [] 조건 찾기. [, ]가 존재해야 하고, 닫는 괄호가 여는 괄호보다 앞에 있으면 안됨
                    mention_keyword = mention_text[start + 1:end].strip().split('/')  # '/' 기준으로 멘션 키워드 나누기
                    first_keyword = mention_keyword[0].strip()  # 상점은 키워드 [상점/구매물품/개수] 로 들어가니 나눠놓기!!

                    ###################### 키워드 별 함수 호출. 키워드가 늘어나면 여기가 길어진다. ######################

                    if first_keyword in keywords:  # 준비된 키워드 내용 중 키워드가 있다면

                        if first_keyword == '주사위':  # 첫번째 키워드가 '주사위' 라면
                            print('! 1d100을 호출합니다.')
                            keyword_action_return = str(random.randint(1, 100))  # 1-100 랜덤컨택
                            print(keyword_action_return)
                            keyword_type = 2

                        elif first_keyword == '홀짝':  # 첫번째 키워드가 '주사위' 라면
                            print('! 홀짝을 호출합니다.')
                            YN = ['홀','짝']
                            keyword_action_return = str(random.choice(YN)) # 홀짝 랜덤컨택
                            print(keyword_action_return)
                            keyword_type = 2

                        elif first_keyword == '퇴마청':  # 키워드 '퇴마청' 일 경우
                            print('! 퇴마청 랜덤 함수를 불러옵니다')
                            keyword_action_return = random_pick(memberlistma)  # 스프레드 시트 내의 퇴마청 목록 호출
                            keyword_type = 2  # 별도 문구 없이 답변출력

                        elif first_keyword == '위령청':  # 키워드 '위령청' 일 경우
                            print('! 위령청 랜덤 함수를 불러옵니다')
                            keyword_action_return = random_pick(memberlistye)  # 스프레드 시트 내 위령청 목록 호출
                            keyword_type = 2

                        elif first_keyword == '주술청':  # 키워드 '위령청' 일 경우
                            print('! 다이스 랜덤 함수를 불러옵니다')
                            keyword_action_return = random_pick(memberlistju)  # 스프레드 시트 내의 상점 데이터를 확인하고 후처리하는 함수
                            keyword_type = 2

                        elif first_keyword == '업보':  # 키워드 '위령청' 일 경우
                            print('! 다이스 랜덤 함수를 불러옵니다')
                            keyword_action_return = random_pick(memberlistup)  # 스프레드 시트 내의 상점 데이터를 확인하고 후처리하는 함수
                            keyword_type = 2

                        elif first_keyword == '아침출석':
                            print('! 아침출석을 확인합니다.')
                            keyword_action_return = " "
                            keyword_type = attu(mention, 17, 9)

                        elif first_keyword == '저녁출석':
                            print('! 저녁출석을 확인합니다.')
                            keyword_action_return = " "
                            keyword_type = attu(mention, 18, 10)

                        elif first_keyword == '사정정산':
                            print('! 사정정산을 확인합니다.')
                            keyword_action_return = " "
                            keyword_type = Sajung(mention, 11)

                        elif first_keyword == '노래방점수':
                            print('! 노래방점수를 확인합니다.')
                            keyword_action_return = str(Song(mention))
                            keyword_type = 7

                        elif first_keyword == '상점':
                            print('! 상점을 구동합니다.')
                            item = mention_keyword[1].strip()
                            print(item)
                            if item == '운세종이' :
                                colorli = ['적색','흑색','백색','청색','황색','녹색','유황색','벽색','자색','홍색']
                                directionli = ['동쪽','서쪽','남쪽','북쪽','우주','망라','산','바다','심해,''사막']
                                woterli = ['이각형','삼각형','사각형','오각형','육각형','칠각형','팔각형','구각형','십각형']
                                Lukli = ['애정운','금전운','도박운','건강운','불운','행운','터주신','귀신']
                                drinkli = ['소주','맥주','와인','백탁의...','커피','벌주','젓갈','뱀주']
                                conditionli = ['날카로운,''진중한','소심한','지혜로운','호탕한','밝히는','아름다운','지혜로운']
                                lucky = random_pick(Luckysheetlist)
                                luckysentence = '\n\n' + '<' + lucky.format(color=random.choice(colorli),
                                                                            direction=random.choice(directionli),
                                                                            woter=random.choice(woterli),
                                                                            Lucky=random.choice(Lukli),
                                                                            drink=random.choice(drinkli),condition=random.choice(conditionli)) + '>'

                                keyword_action_return = Store_sen(item)+str(luckysentence)


                            else:
                                keyword_action_return = Store_sen(item)

                            keyword_type = shop_system(mention, mention_keyword)
                            print(keyword_type)

                    #################################################################################################

                if keyword_type != -1:  # 키워드 오류가 없으면
                    reply_content = make_reply_content(mention, keyword_type,
                                                       keyword_action_return)  # 타입, 키워드 별 함수의 호출의 결과(리턴)값을 매개변수로 넣어 답멘 내용을 만드는 함수 호출

                # 답멘하는 함수
                reply_function(mention, reply_content)  # 현재 보고 있는 멘션, 만든 답멘 내용
                print('! 답멘이 완료되었습니다.')
        except:
            print('! 키워드 체크 도중 오류가 발생했습니다.')


# 출석 확인 함수
def attu(mention, day, coin_day):
    cell = worksheetco.find(mention.user.screen_name)
    print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

    check1 = "Y"
    Price = 3

    for i in range(1, 19):
        print(worksheetco.cell(cell.row, i).value, end=' ')
        if i == int(day):
            # 시트 내 출석초기화 란이 False 상태일 경우 체크 + [ 출석 확인 ] 출력
            if str(worksheetco.cell(cell.row, i).value) == "N":
                worksheetco.update_cell(cell.row, i, check1)
                print(">", worksheetco.cell(cell.row, i).value, end=' ')

                # 그리고 출석 란에 Price 3의 가격을 더한다

                for i in range(1, 18):
                    print(worksheetco.cell(cell.row, i).value, end=' ')

                    if i == int(coin_day):
                        coin = int(worksheetco.cell(cell.row, i).value)
                        worksheetco.update_cell(cell.row, i, coin + Price)

                keyword_type_all = 1

            # 시트 내 출석 란에 체크가 되어 있을 경우 [ 이미 출석처리 되었습니다. 내일 다시 시도해주세요. ] 출력
            else:
                worksheetco.update_cell(cell.row, i, check1)
                print(">", worksheetco.cell(cell.row, i).value, end=' ')

                keyword_type_all = 3

    return keyword_type_all

#사정 정산
def Sajung(mention,coin_day):
    cell = worksheetco.find(mention.user.screen_name)
    print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

    Price = 3

    for i in range(1, 19):
        print(worksheetco.cell(cell.row, i).value, end=' ')

        if i == int(coin_day):
            coin = int(worksheetco.cell(cell.row, i).value)
            worksheetco.update_cell(cell.row, i, coin + Price)

            keyword_type_all = 6


    return keyword_type_all


# 시트 랜덤 호출 함수
def random_pick(ma):
    ma_len = len(ma)  # 전체 레코드의 개수
    print('숫자 : ', ma_len)
    rand_idx = random.randrange(0, ma_len)
    print('랜덤하게 뽑은 key : ', rand_idx)
    pick_record = ma[rand_idx]
    print('랜덤하게 뽑은 value : ', pick_record)
    pick_content = pick_record['내용']
    print('답멘으로 줄 내용 :', pick_content)

    return pick_content


# 상점
def shop_system(mention, mention_keyword):
    cell = worksheetco.find(mention.user.screen_name)  # 멘션보낸 사람 ID값 확인
    print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))  # 정보 호출

    for i in range(1, 19):
        print(worksheetco.cell(cell.row, i).value, end=' ')

        if i == 15:
            # 코인총액 변수 저장
            item = str(mention_keyword[1].strip())
            item2 = int(mention_keyword[2].strip())
            coin_all = int(worksheetco.cell(cell.row, i).value)
            item_Price = Store(item, item2)

            if coin_all >= int(item_Price):  # 코인의 총액이 가격보다 높거나 같다면
                for i in range(1, 19):
                    if i == 13:
                        AccurePrice = int(worksheetco.cell(cell.row, i).value)
                        worksheetco.update_cell(cell.row, i, AccurePrice + item_Price)  # 코인정산 시트의 사용코인에 가격 업로드
                keyword_type_all = 4

            elif coin_all < int(item_Price):
                keyword_type_all = 5

    return keyword_type_all


# 상점 가격 : 물품리스트에서 리턴
def Store(item, item2):
    worksheetshop = wks.worksheet('상점물품')
    Shop_List = worksheetshop.get_all_records()

    for i in range(len(Shop_List)):
        if (Shop_List[i]['2']) == item:
            Price = int(Shop_List[i]['4']) * int(item2)

    return int(Price)


# 상점 설명 : 물품리스트에서 리턴
def Store_sen(item):
    worksheetshop = wks.worksheet('상점물품')
    Shop_List = worksheetshop.get_all_records()

    for i in range(len(Shop_List)):
        if (Shop_List[i]['2']) == item:
            condomlist = ['초박형', '딸기향', '돌기형', '형광노랑야광', '굴곡형', '사정지연']
            sleeplist = ['흰색 쥐', '무난한 회색', '분홍색 토끼', '초록색 공룡', '갈색 곰돌이', '노란색 오리', '무난한 네이비', '생활한복']
            earmuffslist = ['소음방지 귀마개', '토끼 귀도리', '강아지 귀마개', '펭귄 귀마개', '기압조절 귀마개', '고양이 귀마개', '오리 귀마개']
            AcolL = ['맥주', '양주', '고량주', '사케', '막걸리', '위스키', '럼', '와인', '벌주', '뱀주', '스타킹', '치파오']
            DrinkL = ['딸기우유', '초코우유', '콜라', '사이다', '오렌지주스', '육각수', '커피', '젓갈', '란제리']
            BreadL = ['크림빵', '단팥빵', '소금빵', '종합과자세트', '고급쿠키세트', '버터쿠키', '초코쿠키', '소시지', '닭가슴살', '목줄']
            JunL = ['젤리', '캬라멜', '컵라면', '아이스크림', '껌', '사탕', '와플', '냉동만두']
            KingL = ['반쯤 남은 두루마리 휴지', '나무젓가락', '반쯤 구겨진 떡메모지', '누군가 사용하던 볼펜', '라이터', '성냥', '건전지', '반지']
            Sentence = Shop_List[i]['3'].format(condom=random.choice(condomlist), sleep=random.choice(sleeplist),
                                                earmuffs=random.choice(earmuffslist),Acol=random.choice(AcolL),Drink=random.choice(DrinkL),Bread=random.choice(BreadL),Jun=random.choice(JunL),King=random.choice(KingL))
            print(Sentence)

    return str(Sentence)

#노래방 설명
def Song(score) :

    score = random.randint(1, 100)

    if 0 < score <= 20 :
        Evaluation = str(score)+ "점!" + "\n\n" + "바람은 바람이요, 산은 산이고, 물은 물이다... 공기 중에 흩어지는 저것은 누군가의 목소리겠지... 노래가 전혀 감동을 일으키지 못했다..."
    elif 20 < score <= 40 :
        Evaluation = str(score)+ "점!" + "\n\n" +"귓가에 간질이는 바람 정도는 된 듯 하다. 적당히 시간을 때울 만한 것은 되려나. 다시 듣고 싶은 지는... 미지수다."
    elif 40 < score <= 60 :
        Evaluation = str(score)+ "점!" + "\n\n" +"여기저기서 잔잔한 박수 소리가 들린다. 열심히 노래를 부른 보람을 느낄 수 있다. 한 곡 더 부르면 잘 부를 수 있을까?"
    elif 60 < score <= 80 :
        Evaluation = str(score)+ "점!" + "\n\n" +"음정과 박자가 살아있는 무대였다. 이 정도면 노래방에서 분위기를 잡는 것도 가능할지도! 모두가 고개를 끄덕일 실력이다."
    elif 80 < score <= 100 :
        Evaluation = str(score)+ "점!" + "\n\n" +"이런 존재가 리조트에 있었다니...! 누구나 인정하는 신이 내린 목소리, 그야말로 <가왕> 이다. 주변의 자연물마저 감응하며 실력을 칭송한다!"

    return Evaluation


# 답멘 내용 만드는 함수
def make_reply_content(mention, type_of_keyword, keyword_action_return):
    print('! 답멘 내용 만드는 함수를 호출합니다.')
    global last_reply_id
    reply_content = ''
    try:
        if type_of_keyword == 1:  # 키워드 타입이 출석일 경우
            cell = worksheetco.find(mention.author.screen_name)
            print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

            for i in range(1, 19):
                if i == 3:
                    name = str(worksheetco.cell(cell.row, i).value)
                if i == 15:
                    coin_all = int(worksheetco.cell(cell.row, i).value)

            reply_content = "[출석 확인]" + "\n\n" + "현재 " + str(name) + "님의 잔여 백당전은 총 " + str(coin_all) + "전 입니다."

        elif type_of_keyword == 2:  # 키워드 타입이 랜덤출력일 경우
            reply_content = keyword_action_return

        elif type_of_keyword == 3:
            reply_content = "[이미 출석처리 되었습니다. 내일 다시 시도해주세요.]"

        elif type_of_keyword == 4:
            Sentence2 = keyword_action_return
            cell = worksheetco.find(mention.author.screen_name)
            print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

            for i in range(1, 19): #상점 구매확인
                if i == 3:
                    name = str(worksheetco.cell(cell.row, i).value)
                if i == 15:
                    coin_all = int(worksheetco.cell(cell.row, i).value)

            reply_content = "[구매 확인]" + "\n\n" + str(Sentence2) + "\n\n" + "현재 " + str(name) + "님의 잔여 백당전은 총 " + str(
                coin_all) + "전 입니다."

        elif type_of_keyword == 5: #구입백당전 부족 시
            cell = worksheetco.find(mention.author.screen_name)
            print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

            for i in range(1, 19):
                if i == 3:
                    name = str(worksheetco.cell(cell.row, i).value)
                if i == 15:
                    coin_all = int(worksheetco.cell(cell.row, i).value)

            reply_content = "[보유 백당전이 부족합니다.]" + "\n\n" + "현재 " + str(name) + "님의 잔여 백당전은 총 " + str(coin_all) + "전 입니다."

        elif type_of_keyword == 6: #사정정산
            cell = worksheetco.find(mention.author.screen_name)
            print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

            for i in range(1, 19):
                if i == 3:
                    name = str(worksheetco.cell(cell.row, i).value)
                if i == 15:
                    coin_all = int(worksheetco.cell(cell.row, i).value)

            reply_content = "[정산확인]" + "\n\n" + "현재 " + str(name) + "님의 잔여 백당전은 총 " + str(coin_all) + "전 입니다."

        elif type_of_keyword == 7:  # 노래방점수
            Ev = keyword_action_return
            cell = worksheetco.find(mention.author.screen_name)
            print("%s행 %s열에서 찾았습니다." % (cell.row, cell.col))

            for i in range(1, 19):
                if i == 3:
                    name = str(worksheetco.cell(cell.row, i).value)

            reply_content = "과연... " + str(name) + " 님의 점수는?!?!" + "\n\n" + "두구두구두구......" + "\n\n" + str(Ev)

    except:
        print('! 오류가 발생했습니다.')
        pass

    return reply_content


# 답멘 하는 함수
def reply_function(mention, reply_content):
    print('! 답멘하는 함수를 호출합니다.')

    global last_reply_id
    reply_to = "@" + mention.author.screen_name + ' '  # 맨 앞에 붙일 @아이디
    total_reply_content = reply_to + reply_content  # 전체 답멘 내용은 @답멘대상 답멘내용
    try:
        api.update_status(total_reply_content, in_reply_to_status_id=mention.id_str)  # 답멘 하는 함수
        last_reply_id = mention.id_str  # 어디까지 답멘했나 확인
    except:
        print("! 답멘하는 함수에서 발생한에러입니다")
        pass
    return


while True:
    check_new_mention()
    time.sleep(60)
