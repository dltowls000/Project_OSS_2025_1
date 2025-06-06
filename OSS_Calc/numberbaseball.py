import tkinter as tk
import random

class NumberBaseballGame:
    max_tries = 10

    def __init__(self, window, parent_app=None):
        self.window = window
        self.parent_app = parent_app
        self.window.title("숫자야구 게임")
        self.window.geometry("320x500")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.target = self.generate_number()
        self.tries = 0

        self.label = tk.Label(self.window, text=f"남은 시도 횟수: {self.max_tries}", font=("Arial", 14))
        self.label.pack(pady=5)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.window, font=("Arial", 24), justify="center", textvariable=self.entry_var, state="readonly")
        self.entry.pack(pady=10, ipadx=10, ipady=5)

        self.result = tk.Label(self.window, text="", font=("Arial", 14))
        self.result.pack(pady=5)

        self.build_keypad()

        self.action_frame = tk.Frame(self.window)
        self.restart_btn = tk.Button(self.action_frame, text="재시작", command=self.restart_game, font=("Arial", 12), state="disabled")
        self.close_btn = tk.Button(self.action_frame, text="닫기", command=self.on_close, font=("Arial", 12), state="normal")
        self.restart_btn.pack(side="left", padx=10)
        self.close_btn.pack(side="right", padx=10)
        self.action_frame.pack(pady=10)

    def build_keypad(self):
        keypad_frame = tk.Frame(self.window)
        keypad_frame.pack()

        digits = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['←', '0', '확인']
        ]

        for row in digits:
            row_frame = tk.Frame(keypad_frame)
            row_frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(row_frame, text=char, font=("Arial", 16), height=2, width=5,
                                command=lambda ch=char: self.on_keypad_click(ch))
                btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)

    def on_keypad_click(self, char):
        current = self.entry_var.get()

        if char == '←':
            self.entry_var.set(current[:-1])
        elif char == '확인':
            if len(current) != 4:
                self.result.config(text="4자리 숫자를 입력하세요")
                return
            if len(set(current)) != 4 or '0' in current:
                self.result.config(text="중복 혹은 0없이 1~9 숫자만 가능")
                return
            self.check_answer(current)
        else:
            if len(current) < 4 and char not in current:
                self.entry_var.set(current + char)

    def generate_number(self):
        return ''.join(map(str, random.sample(range(1, 10), 4)))

    def check_answer(self, guess):
        strike, ball = 0, 0
        self.tries += 1
        self.label.config(text=f"남은 시도 횟수: {self.max_tries - self.tries}")

        for i in range(4):
            if guess[i] == self.target[i]:
                strike += 1
            elif guess[i] in self.target:
                ball += 1

        if strike == 4:
            self.result.config(text=f"🎉 정답! {self.tries}번 만에 성공!")
            self.disable_input()
        elif self.tries >= self.max_tries:
            self.result.config(text=f"❌ 실패! 정답: {self.target}")
            self.disable_input()
        else:
            self.result.config(text=f"{strike} 스트라이크, {ball} 볼")
            self.restart_btn.config(state="normal")
            self.close_btn.config(state="normal")
            self.entry_var.set("")

    def disable_input(self):
        self.entry.config(state="disabled")
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Button):
                        btn.config(state="disabled")
        self.restart_btn.config(state="normal")
        self.close_btn.config(state="normal")
    def restart_game(self):
        self.target = self.generate_number()
        self.tries = 0
        self.label.config(text=f"남은 시도 횟수: {self.max_tries}")
        self.result.config(text="")
        self.entry_var.set("")
        self.entry.config(state="readonly")

        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Button):
                        btn.config(state="normal")

        self.restart_btn.config(state="disabled")

    def on_close(self):
        if self.parent_app:
            self.parent_app.clear_baseball_window()
        self.window.destroy()
