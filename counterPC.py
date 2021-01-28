from PyQt5.QtCore import Qt
from mysql import DB
from logGrid import *
from logNT import *
from Tab import *
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QTableWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton, QLayout, QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QComboBox
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout

class Button(QToolButton):  # 클릭시 메소드와 연결하는 함수

    def __init__(self, text, callback):  # 넘겨받은 callback 함수를 인자로 받음
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred) # 버튼의 사이즈를 유동적으로
        self.setText(text)
        self.clicked.connect(callback)  # 한번 클릭시는 메인화면에 간단 정보

    def sizeHint(self):  # 버튼의 사이즈를 맞춤
        size = super(Button, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(size.height()+20)
        return size
class Button2(QToolButton):  # 클릭시 메소드와 연결하는 함수

    def __init__(self, text, callback):  # 넘겨받은 callback 함수를 인자로 받음
        super().__init__()
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum) # 버튼의 사이즈를 유동적으로
        self.clicked.connect(callback)  # 한번 클릭시는 메인화면에 간단 정보

class CounterPC(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.database = DB() # DB객체 생성
        # 기본창 띄우기
        mainLayout = QHBoxLayout()  # 왼쪽과 오른쪽으로 구획을 나눔
        self.loginList = []


        #left.................................. 카테고리, 좌석배치도실시간 리스트, 고객조회, 회원정보, 로그인된 인원수
        self.left_layout = QVBoxLayout()

        # ▶실시간 현황
        self.customerBox1 = QGroupBox("▶실시간 현황")
        self.customerLayout1 = QGridLayout()
        self.totalNum = QLabel(str(len(self.loginList)) + "/71석")
        self.totalNum.setStyleSheet('font: bold 18px')
        self.customerLayout1.addWidget(self.totalNum, 0, 0)
        self.customerLayout1.addWidget(QTextEdit(), 1, 0) # 여기에 리스트 반환
        select = '발생일시, ID,  회원명 , 카드번호, PC번호,  결제요금,  PC로그항목, 결제방식'  # DB 에서 전체말고 부분만
        select = '*'
        profile2 = self.database.bringDB('log', 'status', select, '')
        print(profile2)  # data from DB
        loglist = MyGrid(select, profile2)
        self.mychargelst = loglist.makeListOfStatus()  # Q리스트를 돌려준다
        self.customerLayout1.addWidget(self.mychargelst, 1, 0)

        self.customerBox1.setLayout(self.customerLayout1)

        # ▶회원정보
        customerBox3 = QGroupBox("▶회원정보")  # 클릭한 회원정보
        customerLayout = QGridLayout()
        self.pcNum = QLabel("       ")
        self.pcNum.setStyleSheet('font: bold 18px')
        customerLayout.addWidget(self.pcNum, 0, 0)
        self.customerprofile = QLabel("  ⚬ Name(ID):  \n\n  ⚬ 카드번호:  \n\n"
                                     "  ⚬ 시작일시:  \n\n  ⚬ 남은시간:  \n")
        customerLayout.addWidget(self.customerprofile, 1, 0)
        customerBox3.setLayout(customerLayout)

        self.left_layout.addWidget(self.customerBox1)
        self.left_layout.addWidget(customerBox3)




        # Right.................................. 카테고리(탭으로 표시하기), 좌석배치도
        rigthLayout = QVBoxLayout()

        # 1. 카테고리 QComboBox (맨상위)
        # Initialize tab screen
        self.tabs = QTabWidget()  # 모든 텝들을 커버하는 탭윈도우창
        self.tab1 = QWidget()  # 각 탭마다의 윈도우창을 설정
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.addTab(self.tab1, "죄석배치")  # Add tabs
        self.tabs.addTab(self.tab2, "회원조회")
        self.tabs.addTab(self.tab3, "매출확인")  # Add tabs
        self.tabs.addTab(self.tab4, "매장관리")
        self.tabs.addTab(self.tab5, "취소/환불")
        self.tab1SubLayout = QGridLayout()
        self.tab2SubLayout = QGridLayout()
        self.tab3SubLayout = QGridLayout()
        self.tab4SubLayout = QVBoxLayout()
        self.tab5SubLayout = QGridLayout()
        self.tab1.setLayout(self.tab1SubLayout)
        self.tab2.setLayout(self.tab2SubLayout)
        self.tab3.setLayout(self.tab3SubLayout)
        self.tab4.setLayout(self.tab4SubLayout)
        self.tab5.setLayout(self.tab5SubLayout)

        rigthLayout.addWidget(self.tabs)


        # tab1. 좌석 배치도
        self.seatBox = QGroupBox('▶좌석배치도')
        self.seatBox.setStyleSheet('background:lightgray')
        self.seatLayout = QGridLayout()
        self.seatBox.setLayout(self.seatLayout)
        cal = 0
        row = 0
        for num in range(1, 72):
            seat_num = Button(str(num), self.showResult)
            state = QLabel()
            if num in self.loginList:  # 로그인된 자리
                state = QLabel("☜")
                seat_num.setStyleSheet('color:white; background: lightblue')
            cal += 1
            self.seatLayout.addWidget(state, row, (2 * cal) + 1)  # 비어있는지 check
            self.seatLayout.addWidget(seat_num, row, (2 * cal))  # 좌석넘버
            if cal == 9:
                cal = 0
                row += 1
        self.tab1SubLayout.addWidget(self.seatBox, 0,0)  # tab에 Group Box배치


        # tab2. 회원조회
        self.findResult = QLabel('\n▶ \" ID를 입력한 뒤 \'조회하기\'버튼을 눌러주세요.\n')
        self.findResult.setStyleSheet('font: bold 18px')
        self.tab2SubLayout.addWidget(self.findResult, 0, 0, 1, 2)
        self.tab2SubLayout.addWidget(QLabel("아이디(ID) : "), 1, 0)  # ID로 조회
        self.insertID = QLineEdit()
        self.tab2SubLayout.addWidget(self.insertID, 1, 1)
        self.tab2SubLayout.addWidget(QLabel("이   름 : "), 2, 0)  # 이름으로 조회
        self.insertName = QLineEdit()
        self.tab2SubLayout.addWidget(self.insertName, 2, 1)
        enterBtn = Button("조회하기", self.showResult)  # 조회하기 button
        self.tab2SubLayout.addWidget(enterBtn, 3, 1, 1, 2)
        resetBtn = Button("초기화", self.showResult)  # 초기화 button
        self.tab2SubLayout.addWidget(resetBtn, 4, 1, 1, 2)
        self.tab2SubLayout.addWidget(QLabel('▼ 회원 정보 '),5, 0)
        self.tab2SubLayout.addWidget(QTextEdit(), 6, 0, 1, 2)
        self.tab2SubLayout.addWidget(QLabel('▼ 회원 기록 '),7, 0)
        self.tab2SubLayout.addWidget(QTextEdit(), 8, 0, 1, 2)


        # tab3. 매출확인
        self.calculate = QComboBox()

        self.calculate.addItems(['일간', '주간', '월간'])
        self.tab3SubLayout.addWidget(self.calculate, 0, 0)
        enterBtn = Button("매출조회", self.showResult)  # 조회하기 button
        self.tab3SubLayout.addWidget(enterBtn, 0, 1)
        self.tab3SubLayout.addWidget(QLabel("▶ 조회내역"), 1, 0)  # 조회 결과창
        eoeo = QTextEdit("날짜를 선택후 조회버튼을 눌러주세요.")
        eoeo.resize(eoeo.sizeHint())
        self.tab3SubLayout.addWidget(eoeo, 2, 0, 1, 2)


        # tab4. 매장관리 : 요금제변경
        chargeBox = QGroupBox("▼ 요금제 변경")
        self.chargeLayout = QGridLayout()
        self.mychargelst = QListWidget()
        self.chargeLayout.addWidget(QTextEdit("조회를 윈하시면 조회버튼을 눌러주세요."), 0, 0, 3, 2)
        checkBtn = Button2("조회하기", self.revise)  # 요금제 수정 버튼
        self.chargeLayout.addWidget(checkBtn, 0, 4)
        changeBtn = Button2("변경하기", self.revise)  # 요금제 수정 버튼
        self.chargeLayout.addWidget(changeBtn, 1, 4)
        deleteBtn = Button2("삭제하기", self.revise)  # 요금제 수정 버튼
        self.chargeLayout.addWidget(deleteBtn, 2, 4)
        # 요금제 추가 &  버튼
        self.chargeLayout.addWidget(QLabel("▶\'상품명/가격/시간(분)\' 순으로 입력해주세요."), 3, 0, 1, 2)
        self.addcharge = QLineEdit()
        self.chargeLayout.addWidget(self.addcharge, 4, 0)
        addBtn = Button2("추가하기", self.revise)
        self.chargeLayout.addWidget(addBtn, 3, 4)
        chargeBox.setLayout(self.chargeLayout)
        self.tab4SubLayout.addWidget(chargeBox)


        # tab4. 매장관리 : 고객 로그인/로그아웃 담당
        managerBox = QGroupBox("▼ 고객로그인/로그아웃")
        self.manageLayout = QGridLayout()
        self.mychargelst = QListWidget()
        self.loginID = QLineEdit()
        self.loginName = QLineEdit()
        self.loginPC = QLineEdit()
        self.manageLayout.addWidget(QLabel("아이디(ID) :"), 0, 0)
        self.manageLayout.addWidget(QLabel("이   름 :"), 1, 0)
        self.manageLayout.addWidget(QLabel("PC 좌석 :"), 2, 0)
        self.manageLayout.addWidget(self.loginID, 0, 1)
        self.manageLayout.addWidget(self.loginName, 1, 1)
        self.manageLayout.addWidget(self.loginPC, 2, 1)
        checkBtn = Button2("로그인하기", self.loginManager)  # 요금제 수정 버튼
        self.manageLayout.addWidget(checkBtn, 0, 4)
        changeBtn = Button2("로그아웃하기", self.loginManager)  # 요금제 수정 버튼
        self.manageLayout.addWidget(changeBtn, 1, 4)
        changeBtn = Button2("초기화", self.loginManager)  # 요금제 수정 버튼
        self.manageLayout.addWidget(changeBtn, 2, 4)
        notice = QLabel("\n※회원의 경우: 아이디, 이름, 좌석번호\n"
                                           "   비회원의 경우: 카드번호, 죄석번호를 기입해주세요.※")
        notice.setStyleSheet('color:blue;')
        self.manageLayout.addWidget(notice, 4, 0)
        self.loginResult = QLabel() # 로그인/ 로그아웃 결과창
        self.loginResult.setStyleSheet('color:red; font: bold 18px')
        self.manageLayout.addWidget(self.loginResult, 5, 0)
        managerBox.setLayout(self.manageLayout)
        self.tab4SubLayout.addWidget(managerBox)





        #tab5 취소/환불
        self.refundResult = QLabel('\n▶ \" ID를 입력한 뒤 \'조회하기\'버튼을 눌러주세요.\n')
        self.refundResult.setStyleSheet('font: bold 18px')
        self.tab5SubLayout.addWidget(self.refundResult, 0, 0, 1, 2)
        self.tab5SubLayout.addWidget(QLabel("아이디(ID) 또는 카드번호 : "), 1, 0)  # ID로 조회
        self.refundID = QLineEdit()
        self.tab5SubLayout.addWidget(self.refundID, 1, 1)
        self.tab5SubLayout.addWidget(QLabel("이   름 : "), 2, 0)  # 이름
        self.refundName = QLineEdit()
        self.tab5SubLayout.addWidget(self.refundName, 2, 1)
        self.tab5SubLayout.addWidget(QLabel("남은 시간 : "), 3, 0)  # 남은시간
        self.refundTime = QLineEdit()
        self.tab5SubLayout.addWidget(self.refundTime, 3, 1)
        self.tab5SubLayout.addWidget(QLabel("환불가능금액 : "), 4, 0)  # 환불가능한 돈
        self.ableMoney = QLineEdit()
        self.tab5SubLayout.addWidget(self.ableMoney, 4, 1)
        enterBtn = Button("조회하기", self.refundManager)  # 조회하기 button
        self.tab5SubLayout.addWidget(enterBtn, 5, 1)
        resetBtn = Button("초기화", self.refundManager)  # 초기화 button
        self.tab5SubLayout.addWidget(resetBtn, 6, 1)
        self.tab5SubLayout.addWidget(QLabel('▼ 취소할 금액을 입력해주세요(천원단위) '), 5, 0, 3, 1)
        self.refundMoney = QLineEdit()
        self.tab5SubLayout.addWidget(self.refundMoney, 7, 0)
        refundBtn = Button("환불하기", self.refundManager)  # 환불 button
        self.tab5SubLayout.addWidget(refundBtn, 7, 1)
        self.tab5SubLayout.addWidget(QLabel('▼ 회원 정보 '), 9, 0)
        self.tab5SubLayout.addWidget(QTextEdit(), 8, 0, 1, 2)




        self.tab5SubLayout.addWidget(QTextEdit(), 8, 0, 1, 2)


        #----------------------------- 윈도우창에 배치
        mainLayout.addLayout(self.left_layout)
        mainLayout.addLayout(rigthLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle('Counter PC')

    # 버튼에 써있는 텍스트를 가져와서 케이스별 상황을 만든다
    # 매출조회, 회원조회,
    def showResult(self):
        sender = self.sender()
        text = sender.text()
        if text == '매출조회':  # 고객DB에 저장 및 실시간 로그DB에도 저장
            select = '발생일시, ID, 회원명, 카드번호, 결제방식,  결제요금'  # DB에서 전체말고 부분만
            if self.calculate.currentText() == '일간':
                string = ' where 결제방식 in (\'카드결제\', \'현금결제\')'
            elif self.calculate.currentText() == '주간':
                string = ''
            elif self.calculate.currentText() == '월간':
                string = ''

            profile = self.database.bringDB('log', 'status', select, string)
            print(profile)
            loglist = MyGrid(select, profile)
            mytable = loglist.makeTable()
            self.tab3SubLayout.addWidget(mytable, 2, 0, 1, 2)
        elif text == '조회하기':  # DB에서 검색한다
            try:
                select = '발생일시,ID,회원명,PC번호,PC로그항목,남은시간,총이용요금'  # DB에서 가져올 항목
                # 회원정보
                profile1 = self.database.bringDB('customer', 'member', select,
                                                ' where ID = \'{}\''.format(self.insertID.text()))
                print(profile1)  # ('0000-00-00 00:00:00', 'missenergy', '조혜영', '113ssd', 0, 0, 918, 95000, None)
                self.insertName.setText(profile1[0][2])  # 이름
                loglist = MyGrid(select, profile1)
                mytable = loglist.makeTable() # 표를 돌려준다
                self.tab2SubLayout.addWidget(mytable, 6, 0, 1, 2)
                # 회원기록
                select = '발생일시,ID,회원명,PC번호,PC로그항목,결제요금,결제방식'  # DB에서 전체말고 부분만
                profile2 = self.database.bringDB('log', 'status', select,
                                                 ' where ID = \'{}\''.format(self.insertID.text()))
                print(profile2)  # ('0000-00-00 00:00:00', 'missenergy', '조혜영', '113ssd', 0, 0, 918, 95000, None)
                loglist = MyGrid(select, profile2)
                mychargetable = loglist.makeTable()  # 표를 돌려준다
                self.tab2SubLayout.addWidget(mychargetable, 8, 0, 1, 2)

                if len(profile2) == 0:
                    print("\"일치하는 아이디가 없습니다.\"")
            except:
                self.findResult.clear()
                self.findResult.setStyleSheet('color:red; font: bold 18px')
                self.findResult.setText('\n▶ \"일치하는 아이디가 없습니다.\"\n')
        elif text == '초기화':
            self.insertID.clear()
            self.insertName.clear()
            self.findResult.clear()
            self.findResult.setStyleSheet("color:black; font:bold 18px ")
            self.findResult.setText('\n▶ \" ID를 입력한 뒤 \'조회하기\'버튼을 눌러주세요.\n')
            self.tab2SubLayout.addWidget(QTextEdit(), 6, 0, 1, 2)
            self.tab2SubLayout.addWidget(QTextEdit(), 8, 0, 1, 2)
        elif type(int(text)) == int: # 좌석에 해당되는 번호가 들어오면 그좌석 고객정보
            try:
                self.pcNum.clear()
                self.pcNum.setStyleSheet("color:red; font:bold 18px")
                self.pcNum.setText("  ▒▒▒▒▶ {}번 PC ◀▒▒▒▒  ".format(text))
                string = ' where PC번호 = \'{}\'' .format(int(text))
                select1 = '발생일시, ID, 회원명, 남은시간'
                profile1 = self.database.bringDB('customer', 'member', select1, string)
                select2 = '발생일시, 카드번호, 남은시간'
                profile2 = self.database.bringDB('customer', 'nonmember', select2, string)
                profile = profile1[0] if len(profile2) == 0 else profile2[0]
                print(profile)
                self.customerprofile.clear()
                self.customerprofile.setText("  ⚬ Name(ID):  {}({})\n\n  ⚬ 카드번호:  \n\n"
                                         "  ⚬ 시작일시:  {}\n\n  ⚬ 남은시간:  {}분\n".format(profile[2],profile[1], str(profile[0]), profile[3]))
            except:
                self.pcNum.setStyleSheet("color:black; font:bold 18px")
                self.pcNum.setText("  ▒▒▒▒▶ {}번 PC ◀▒▒▒▒  ".format(text))
                self.customerprofile.clear()
                self.customerprofile.setText("  ⚬ Name(ID):  \n\n  ⚬ 카드번호:  \n\n"
                                              "  ⚬ 시작일시:  \n\n  ⚬ 남은시간:  \n")
        else:
            word = text.split("\n")
            self.choosePrice = word[1][:-1]
            self.result.clear()
            self.result.setText("선불요금 " + word[1] + "이 선택되었습니다.\n 아이디를 입력해 주세요")

    # 요금제 변경 함수
    def revise(self):
        sender = self.sender()
        text = sender.text()
        if text == '조회하기':
            select = '상품명, 가격, 시간'  # DB 에서 전체말고 부분만
            profile2 = self.database.bringDB('charge', 'charge', select, '')
            print(profile2)  # data from DB
            loglist = MyGrid(select, profile2)
            self.mychargelst= loglist.makeListOfCharge()  # 표를 돌려준다
            self.chargeLayout.addWidget(self.mychargelst, 0, 0, 3, 2)
        elif text == '삭제하기': # lineEdit과 DB모두 저장
            try:
                edit = self.mychargelst.currentItem().text().split(' ')  # 선택된거 text가져와 ' '기준으로 나눔
                print(edit[1])
                self.mychargelst.takeItem(self.mychargelst.currentRow())
                self.database.deleteDB('charge', 'charge', ' where 상품명 = \'{}\''.format(edit[1]))
            except:
                pass
        elif text == '추가하기':
            try:
                edit = self.addcharge.text().split('/')
                self.mychargelst.addItem("▶상품명: {}     가격: {}원    시간: {}분".format(edit[0],edit[1],edit[2]))
                dic = {'상품명': edit[0], '가격': edit[1], '시간': edit[2]}
                self.database.storeDB('charge', 'charge', dic)
            except:

                print("다시입력!")

    # 취소/환불 함수
    def refundManager(self):
        sender = self.sender()
        text = sender.text()
        if text == '조회하기':
            try:
                select = '발생일시,ID,회원명,결제요금,결제방식,카드번호,PC로그항목'  # DB에서 가져올 항목
                # 회원정보
                id ='카드번호' if len(self.refundID.text())== 4 else 'ID'
                profile1 = self.database.bringDB('log', 'status', select,
                                                ' where {} = \'{}\' and 결제방식 in (\'현금결제\', \'카드결제\')'.format(id, self.refundID.text()))
                profile2 = self.database.bringDB('customer', 'member', '남은시간',
                                                 ' where ID = \'{}\''.format( self.refundID.text()))
                print(profile2[0][0])
                self.refundName.setText(profile1[0][2])  # 이름
                self.refundTime.setText(str(profile2[0][0]))  # 남은시간
                self.ableMoney.setText(str(profile2[0][0]//50*1000))  # 환불가능 돈
                loglist = MyGrid(select, profile1)
                mychargetable = loglist.makeTable()  # 표를 돌려준다
                self.tab5SubLayout.addWidget(mychargetable, 8, 0, 1, 2)

            except:
                self.refundResult.clear()
                self.refundResult.setStyleSheet('color:red; font: bold 18px')
                self.refundResult.setText('\n▶ \"일치하는 아이디가 없습니다.\"\n')
        elif text == '환불하기':
            # 회원기록
            dic = {'총이용요금': -(int(self.refundMoney.text())), '남은시간': -(int(self.refundMoney.text()[:-3])*50)}
            print(dic)
            self.database.updateDB('customer', 'member', dic,
                                              ' where ID = \'{}\''.format(self.refundID.text()))
            self.refundResult.clear()
            self.refundResult.setStyleSheet("color:red; font:20px")
            self.refundResult.setText("환불이 완료되었습니다.")

    # 매장관리 탭에서 고객의 정보를 이용하여 로그인/로그아웃 담당
    # + 좌석배치 탭의 정보를 바꾸는 역할
    def loginManager(self):
        sender = self.sender()
        text = sender.text()
        if text == '로그인하기':
            try:
                self.manager = PClog(self.loginPC.text(), self.loginID.text(), self.loginName.text())  # 로그인담당 매니저 생성
                self.manager.login()
                self.loginResult.setText("로그인 성공")
                # 로그인좌석 배열에 좌석추가
                self.loginList.append(int(self.loginPC.text()))
                # 전체 인원수 update
                self.totalNum.clear()
                self.totalNum.setText(str(len(self.loginList)) + "/71석")
                # 좌석 배열 새로 만들기
                self.seatBox = QGroupBox('▶좌석배치도')
                self.seatBox.setStyleSheet('background:lightgray')
                self.seatLayout = QGridLayout()
                self.seatBox.setLayout(self.seatLayout)
                cal = 0
                row = 0
                for num in range(1, 72):
                    seat_num = Button(str(num), self.showResult)
                    state = QLabel()
                    if num in self.loginList:  # 로그인된 자리
                        state = QLabel("☜")
                        seat_num.setStyleSheet('color:white; background: lightblue')
                    cal += 1
                    self.seatLayout.addWidget(state, row, (2 * cal) + 1)  # 비어있는지 check
                    self.seatLayout.addWidget(seat_num, row, (2 * cal))  # 좌석넘버

                    if cal == 9:
                        cal = 0
                        row += 1
                self.tab1SubLayout.addWidget(self.seatBox, 0, 0)  # tab에 Group Box배치
            except:
                self.loginResult.setText("로그인 실패")
        elif text == '로그아웃하기':
            try:

                self.manager = PClog(self.loginPC.text(), self.loginID.text(), self.loginName.text())  # 로그인담당 매니저 생성
                self.manager.logout()
                self.loginResult.setText("로그아웃 성공")

                # 로그인좌석 배열에 좌석 제거
                self.loginList.remove(int(self.loginPC.text()))
                # 전체 인원수 update
                self.totalNum.clear()
                self.totalNum.setText(str(len(self.loginList)) + "/71석")
                # 좌석 배열 새로 만들기
                self.seatBox = QGroupBox('▶좌석배치도')
                self.seatBox.setStyleSheet('background:lightgray')
                self.seatLayout = QGridLayout()
                self.seatBox.setLayout(self.seatLayout)
                cal = 0
                row = 0
                for num in range(1, 72):
                    seat_num = Button(str(num), self.showResult)
                    state = QLabel()
                    if num in self.loginList:  # 로그인된 자리
                        state = QLabel("☜")
                        seat_num.setStyleSheet('color:white; background: lightblue')
                    print(self.loginList)

                    cal += 1
                    self.seatLayout.addWidget(state, row, (2 * cal) + 1)  # 비어있는지 check
                    self.seatLayout.addWidget(seat_num, row, (2 * cal))  # 좌석넘버

                    if cal == 9:
                        cal = 0
                        row += 1
                self.tab1SubLayout.addWidget(self.seatBox, 0, 0)  # tab에 Group Box배치

            except:
                self.loginResult.setText("로그아웃 실패")
        elif text == '초기화':
            self.loginID.setText('')
            self.loginName.setText('')
            self.loginPC.setText('')



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    calc = CounterPC()
    calc.show()
    sys.exit(app.exec_())()