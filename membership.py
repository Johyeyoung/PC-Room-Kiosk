import pymysql


class Member:
    def __init__(self):
        self.memberDB = []
        self.nonMemberDB = []

    # 멤버쉽과 비멤버쉽요금 반환
    def bringMemberDB(self, database, table):

        conn = pymysql.connect(host='localhost', user='root', password='root',
                               db= database, charset='utf8')
        curs = conn.cursor()
        command = "SELECT * FROM " + table
        curs.execute(command)
        if table == 'member':  # 회원이면 여기 리스트에 담고
            self.memberDB = curs.fetchall()
        else:  # 비회원이면
            self.nonMemberDB = curs.fetchall()
        conn.close()




   # findBox = QGroupBox("▶ID 조회")  # 결제방식 카드/현금
        #         #
        #         # paymentLayout = QGridLayout()
        #         # paymentLayout.addWidget(QLabel("ID 입력 후 Enter를 누르세요."), 0, 0)
        #         # enterID = QLineEdit()
        #         # paymentLayout.addWidget(enterID, 1, 0)
        #         # enterBtn = QPushButton("Enter")  # Enter버튼
        #         # paymentLayout.addWidget(enterBtn, 1, 1)
        #         # resetBtn = QPushButton("초기화")  # 초기화버튼
        #         # paymentLayout.addWidget(resetBtn, 1, 2)
        #         #
        #         # findBox.setLayout(paymentLayout)






if __name__ == '__main__':
    member = Member()
