import datetime
from expense import Expense
import matplotlib.pyplot as plt
import collections

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

    def create_graph(self, path=None):
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

        plt.savefig(path, bbox_inches='tight')
        plt.close()

    def load_budget(self, today, category, description, amount):
        expense = Expense(today, category, description, amount)
        self.expenses.append(expense)

        if category not in self.cate:
            self.cate.append(category)
            self.cate_total.append(0)
        
        idx = self.cate.index(category)
        self.cate_total[idx] += amount

    def save_budget(self):
        f = open("budget.txt", 'w', encoding='utf-8')
        for i, e in enumerate(self.expenses):
            date = e.date
            category = e.category
            description = e.description
            amount = e.amount
            f.write("{} {} {} {}\n".format(date, category, description, amount))


    def budget_clear(self):
        self.expenses = []
        self.cate = []
        self.cate_total = []

    def save_html(self, filename='budget_report.html'):
        if not self.expenses:
            print("지출 내역이 없어 HTML을 생성하지 않습니다.\n")
            return

        total = sum(e.amount for e in self.expenses)
        max_index = self.cate_total.index(max(self.cate_total))
        max_cate = self.cate[max_index]
        max_amount = self.cate_total[max_index]

        today = datetime.datetime.now()
        title = f"{today.year}년 {today.month}월 간단 가계부 기록"
        graph_img = 'budget_chart.png'

        self.create_graph(path=graph_img)

        sorted_expenses = sorted(self.expenses, key=lambda e: e.date)
        grouped_expenses = collections.defaultdict(list)
        for e in sorted_expenses:
            grouped_expenses[e.category].append(e)

        html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; }}
        table {{ border-collapse: collapse; width: 80%; margin: 20px auto; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        h2, p {{ text-align: center; }}
        h3 {{ margin-left: 10%; }}
        img {{ display: block; margin: 20px auto; width: 400px; }}
    </style>
</head>
<body>
    <h2>{title}</h2>
    <p><strong>총 지출:</strong> {total:,}원</p>
    <p><strong>가장 지출이 많은 카테고리:</strong> {max_cate} ({max_amount:,}원)</p>
    <img src="{graph_img}" alt="카테고리별 지출 그래프">
"""

        for category in sorted(grouped_expenses.keys()):
            categorys = grouped_expenses[category]
            if not categorys:
                continue

            html += f"<h3>{category}</h3>"
            html += """
    <table>
        <tr>
            <th>날짜</th>
            <th>설명</th>
            <th>금액</th>
        </tr>
"""
            for e in categorys:
                html += f"""
        <tr>
            <td>{e.date}</td>
            <td>{e.description}</td>
            <td>{e.amount:,}원</td>
        </tr>
"""
            html += "</table>"

        html += """
</body>
</html>
"""
        with open('budget_report.html', 'w', encoding='utf-8') as f:
                f.write(html)

        print(f"HTML 파일이 'budget_report.html'에 저장되었습니다.")