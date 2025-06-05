import datetime
from expense import Expense
import matplotlib.pyplot as plt

class Budget:
    def __init__(self):
        self.expenses = []
        self.cate = []
        self.cate_total = []

    def add_expense(self, category, description, amount):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount)
        self.expenses.append(expense)

        if category not in self.cate:
            self.cate.append(category)
            self.cate_total.append(0)
        
        idx = self.cate.index(category)
        self.cate_total[idx] += amount

        print("지출이 추가되었습니다.\n")

    def list_expenses(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        print("\n[지출 목록]")
        for idx, e in enumerate(self.expenses, 1):
            print(f"{idx}. {e}")
        print()

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"총 지출: {total:,}원\n")  

    def show_graph(self, path=None):
        fig = plt.figure(num="간단 가계부")
        wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 3}
        legend_labels = [f"{total:,}원" for total in self.cate_total]
        labels =[f"{cat}" for cat in self.cate]
        today = datetime.datetime.now()

        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        plt.title(today.strftime("<%Y년 %m월 가계부 카테고리별 지출 총액>"))
        plt.pie(self.cate_total, labels=labels, autopct='%.2f%%', wedgeprops=wedgeprops)
        plt.legend(legend_labels, title='카테고리별 지출 총액', fontsize=8, bbox_to_anchor=(0.9, 1.0))

        plt.show()