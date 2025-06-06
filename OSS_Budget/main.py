from budget import Budget

def main():
    budget = Budget()

    while True:
        print("==== 간단 가계부 ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("4. 가계부 저장 및 불러오기")
        print("5. 가계부 html 생성")
        print("6. 종료")
        choice = input("선택 > ")

        if choice == "1":
            category = input("카테고리 (예: 식비, 교통 등): ")
            description = input("설명: ")
            try:
                amount = int(input("금액(원): "))
                if (amount <= 0):
                    print("음수 혹은 0원은 입력할 수 없습니다.\n")
                    continue
            except ValueError:
                print("잘못된 금액입니다.\n")
                continue
            budget.add_expense(category, description, amount)

        elif choice == "2":
            budget.list_expenses()

        elif choice == "3":
            budget.total_spent()
        
        elif choice == "4":
            print("1. 저장")
            print("2. 불러오기")
            print("3. 돌아가기")
            select = input("선택 > ")

            if select == "1":
                if not budget.expenses:
                    print("가계부가 비어있습니다.\n")
                    continue
                budget.save_budget()
                print("가계부 저장을 완료했습니다.\n")

            elif select == "2":
                try:
                    f = open("budget.txt", 'r', encoding='utf-8')
                    budget.budget_clear()
                    while True:
                        line = f.readline()
                        if not line:
                            if not budget.expenses:
                                print("가계부 파일이 비어있습니다.\n")
                                break
                            print("가계부를 불러왔습니다.\n")
                            break
                        else:
                            if len(line.split()) != 4:
                                print("가계부 파일이 잘못되었습니다. 기존 가계부를 초기화합니다.\n")
                                budget.budget_clear()
                                break

                            today, category, description, amount_str = line.split()
                            amount = int(amount_str)

                            if (amount <= 0):
                                print("음수 혹은 0원은 입력할 수 없습니다. 기존 가계부를 초기화합니다.\n")
                                budget.budget_clear()
                                break
                            budget.load_budget(today, category, description, amount)
                            
                except FileNotFoundError:
                    print("파일을 찾을 수 없습니다. 초기 선택으로 돌아갑니다.\n")
                    continue

            elif select == "3":
                continue
            
            else:
                print("잘못된 선택입니다. 초기 선택으로 돌아갑니다.\n")

        elif choice == "5":
            budget.save_html()

        elif choice == "6":
            print("가계부를 종료합니다.")
            break

        else:
            print("잘못된 선택입니다.\n")

if __name__ == "__main__":
    main()