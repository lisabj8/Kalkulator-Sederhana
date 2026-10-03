import math
import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator")
        self.root.geometry("340x470")
        self.root.resizable(False, False)
        self.root.configure(bg="#15191f")

        self.current = "0"
        self.stored = None
        self.pending = None
        self.reset_next = False

        self.display = tk.Label(
            root,
            text=self.current,
            anchor="e",
            padx=20,
            bg="#15191f",
            fg="#f4f6f8",
            font=("Segoe UI", 34),
        )
        self.display.pack(fill="both", ipady=28)

        grid = tk.Frame(root, bg="#15191f")
        grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        buttons = [
            ["AC", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["⌫", "0", ".", "="],
        ]

        for row_index, row in enumerate(buttons):
            grid.rowconfigure(row_index, weight=1)
            for column_index, label in enumerate(row):
                grid.columnconfigure(column_index, weight=1)
                color = self.button_color(label)
                button = tk.Button(
                    grid,
                    text=label,
                    command=lambda value=label: self.press(value),
                    bg=color,
                    fg="#f4f6f8",
                    activebackground="#59616d",
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    font=("Segoe UI", 17),
                    cursor="hand2",
                )
                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=4,
                    pady=4,
                )

        self.root.bind("<Key>", self.handle_key)

    def button_color(self, label):
        if label == "=":
            return "#168c80"
        if label in {"÷", "×", "−", "+"}:
            return "#315c70"
        if label in {"AC", "±", "%", "⌫"}:
            return "#343b45"
        return "#232a33"

    def update_display(self):
        self.display.config(text=self.current)

    def press(self, value):
        if value.isdigit():
            self.enter_digit(value)
        elif value == ".":
            self.enter_decimal()
        elif value in {"÷", "×", "−", "+"}:
            self.choose_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "AC":
            self.clear()
        elif value == "⌫":
            self.backspace()
        elif value == "±":
            self.toggle_sign()
        elif value == "%":
            self.percentage()

    def enter_digit(self, digit):
        if self.current == "Error" or self.reset_next:
            self.current = digit
            self.reset_next = False
        elif self.current == "0":
            self.current = digit
        else:
            self.current += digit
        self.update_display()

    def enter_decimal(self):
        if self.current == "Error" or self.reset_next:
            self.current = "0."
            self.reset_next = False
        elif "." not in self.current:
            self.current += "."
        self.update_display()

    def choose_operator(self, operator):
        if self.current == "Error":
            return

        if self.pending and not self.reset_next:
            self.calculate()
            if self.current == "Error":
                return
        else:
            self.stored = float(self.current)

        self.pending = operator
        self.reset_next = True

    def calculate(self):
        if self.pending is None or self.stored is None:
            return

        first = self.stored
        second = float(self.current)

        try:
            if self.pending == "+":
                result = first + second
            elif self.pending == "−":
                result = first - second
            elif self.pending == "×":
                result = first * second
            else:
                result = first / second

            if not math.isfinite(result):
                raise ArithmeticError

            self.current = f"{result:.10g}"
            self.stored = None
            self.pending = None
            self.reset_next = True
        except (ZeroDivisionError, ArithmeticError):
            self.current = "Error"
            self.stored = None
            self.pending = None
            self.reset_next = True

        self.update_display()

    def clear(self):
        self.current = "0"
        self.stored = None
        self.pending = None
        self.reset_next = False
        self.update_display()

    def backspace(self):
        if self.current == "Error":
            self.clear()
        elif not self.reset_next:
            self.current = self.current[:-1] or "0"
            if self.current == "-":
                self.current = "0"
            self.update_display()

    def toggle_sign(self):
        if self.current != "Error" and float(self.current) != 0:
            self.current = (
                self.current[1:] if self.current.startswith("-")
                else "-" + self.current
            )
            self.update_display()

    def percentage(self):
        if self.current != "Error":
            self.current = f"{float(self.current) / 100:.10g}"
            self.update_display()

    def handle_key(self, event):
        key_map = {
            "*": "×",
            "/": "÷",
            "-": "−",
            "+": "+",
            "Return": "=",
            "KP_Enter": "=",
            "BackSpace": "⌫",
            "Escape": "AC",
        }

        if event.char.isdigit() or event.char == ".":
            self.press(event.char)
        elif event.keysym in key_map:
            self.press(key_map[event.keysym])
        return "break"


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()