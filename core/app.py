import tkinter as tk
import helpers.constants as keys
import math


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = "0"
        self.memory = 0
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_label, self.label = self.create_display_labels()

        self.scientific_digits = {
            7: (4, 1), 8: (4, 2), 9: (4, 3),
            4: (5, 1), 5: (5, 2), 6: (5, 3),
            1: (6, 1), 2: (6, 2), 3: (6, 3),
            0: (7, 2), ".": (7, 3),
        }

        self.programmer_digits = {
            7: (3, 1), 8: (3, 2), 9: (3, 3),
            4: (4, 1), 5: (4, 2), 6: (4, 3),
            1: (5, 1), 2: (5, 2), 3: (5, 3),
            0: (6, 2), ".": (6, 3),
        }
        self.operators = {"/": "\u00F7", "*": "\u00D7",
                          "-": "\u2212", "+": "\u002B"}

        self.current_mode = 0

    # run the app
    def run(self):
        self.choose_buttons()
        self.bind_keys()
        self.window.mainloop()

    # choose buttons mode
    def choose_buttons(self):
        if self.current_mode == 0:
            self.window.geometry("350x550")
            self.buttons_frame.rowconfigure(0, weight=1)

            for x in range(1, 8):
                self.buttons_frame.rowconfigure(x, weight=1)
                self.buttons_frame.columnconfigure(x, weight=1)

            self.draw_scientific_buttons()
        else:
            self.window.geometry("350x480")
            self.buttons_frame.rowconfigure(0, weight=1)

            for x in range(1, 7):
                self.buttons_frame.rowconfigure(x, weight=1)
                self.buttons_frame.columnconfigure(x, weight=1)

            self.draw_programmer_buttons()

    # create the display frame
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=250,
                         width=400, bg=keys.LIGHT_GRAY)
        frame.pack(fill="both", expand=True)
        return frame

    # create the buttons frame
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True)
        return frame

    # create the display labels
    def create_display_labels(self):
        # total label
        total_label = tk.Label(self.display_frame, text=self.total_expression,
                               anchor=tk.E, font=keys.SMALL_FONT_STYLE, bg=keys.LIGHT_GRAY, fg=keys.BLACK_COLOR, padx=24)
        total_label.pack(fill="both", expand=True)

        # current label
        label = tk.Label(self.display_frame, text=self.current_expression,
                         anchor=tk.E, font=keys.BIG_FONT_STYLE, bg=keys.LIGHT_GRAY, fg=keys.BLACK_COLOR, padx=24)
        label.pack(fill="both", expand=True)

        return total_label, label

    # create custom button
    def draw_button(self, text, row, column, command, bg_color, fg_color, font_style):
        button = tk.Button(self.buttons_frame, text=text, font=font_style,
                           bg=bg_color, fg=fg_color, borderwidth=0, padx=24, pady=24, command=command)
        button.grid(row=row, column=column, sticky=tk.NSEW)

    # create the digit buttons
    def create_digit_buttons(self):
        digits = self.scientific_digits

        if self.current_mode == 1:
            digits = self.programmer_digits

        for key, value in digits.items():
            button = tk.Button(self.buttons_frame, text=key, font=keys.DIGITS_FONT_STYLE,
                               bg=keys.DIGIT_BG, fg=keys.BLACK_COLOR, borderwidth=0, padx=24, pady=24, command=lambda key=key: self.add_digit(key))
            button.grid(row=value[0], column=value[1], sticky=tk.NSEW)

    # create the operator buttons
    def create_operator_buttons(self):
        i = 3
        if self.current_mode == 1:
            i = 2

        for operator, symbol in self.operators.items():
            button = tk.Button(self.buttons_frame, text=symbol, font=keys.DEFAULT_FONT_STYLE,
                               bg=keys.LABEL_COLOR, fg=keys.BLACK_COLOR, borderwidth=0, padx=24, pady=24, command=lambda key=operator: self.append_operator(key))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    # create the equals button
    def create_equals_button(self):
        row = 7
        if self.current_mode == 1:
            row = 6

        button = tk.Button(self.buttons_frame, text="=", font=keys.DEFAULT_FONT_STYLE,
                           bg=keys.CUTE_BLUE, fg=keys.LABEL_COLOR, borderwidth=0, padx=24, pady=24, command=lambda: self.evaluate())
        button.grid(row=row, column=4, sticky=tk.NSEW)

    # create mode change buttons
    def create_mode_change_buttons(self):
        if self.current_mode == 0:
            s_bg = keys.CUTE_BLUE
            s_fg = keys.OFF_WHITE
            s_row = 0
            s_column = 0
            s_columnspan = 3
            p_bg = keys.LIGHT_GRAY
            p_fg = keys.BLACK_COLOR
            p_row = 0
            p_column = 3
            p_columnspan = 2
        else:
            s_bg = keys.LIGHT_GRAY
            s_fg = keys.BLACK_COLOR
            s_row = 0
            s_column = 0
            s_columnspan = 2
            p_bg = keys.CUTE_BLUE
            p_fg = keys.OFF_WHITE
            p_row = 0
            p_column = 2
            p_columnspan = 3

        button = tk.Button(self.buttons_frame, text="Scientific", font=keys.MEMORY_FONT_STYLE,
                           bg=s_bg, fg=s_fg, borderwidth=0, padx=24, pady=24, command=lambda: self.change_mode(0))
        button.grid(row=s_row, column=s_column,
                    columnspan=s_columnspan, sticky=tk.NSEW)

        button = tk.Button(self.buttons_frame, text="Programmer", font=keys.MEMORY_FONT_STYLE,
                           bg=p_bg, fg=p_fg, borderwidth=0, padx=24, pady=24, command=lambda: self.change_mode(1))
        button.grid(row=p_row, column=p_column,
                    columnspan=p_columnspan, sticky=tk.NSEW)

    # draw memory buttons
    def draw_memory_buttons(self):
        # draw MC button
        self.draw_button("MC", 1, 0, lambda: self.clear_memory(),
                         keys.LIGHT_GRAY, keys.BLACK_COLOR, keys.MEMORY_FONT_STYLE)

        # draw MR button
        self.draw_button("MR", 1, 1, lambda: self.recall_memory(),
                         keys.LIGHT_GRAY, keys.BLACK_COLOR, keys.MEMORY_FONT_STYLE)

        # draw M+ button
        self.draw_button("M+", 1, 2, lambda: self.add_to_memory(),
                         keys.LIGHT_GRAY, keys.BLACK_COLOR, keys.MEMORY_FONT_STYLE)

        # draw M- button
        self.draw_button("M-", 1, 3, lambda: self.subtract_from_memory(),
                         keys.LIGHT_GRAY, keys.BLACK_COLOR, keys.MEMORY_FONT_STYLE)

        # draw MS button
        self.draw_button("MS", 1, 4, lambda: self.memory_store(),
                         keys.LIGHT_GRAY, keys.BLACK_COLOR, keys.MEMORY_FONT_STYLE)

    # draw programmer buttons
    def draw_programmer_buttons(self):
        # draw mode change buttons
        self.create_mode_change_buttons()

        # draw memory buttons
        self.draw_memory_buttons()

        # draw bitwise left button
        self.draw_button("<<", 2, 0, lambda: self.bitwise_left(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw bitwise right button
        self.draw_button(">>", 2, 1, lambda: self.bitwise_right(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw binary conversion button
        self.draw_button("Bin", 3, 0, lambda: self.to_binary(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw octal conversion button
        self.draw_button("Oct", 4, 0, lambda: self.to_octal(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw hex conversion button
        self.draw_button("Hex", 5, 0, lambda: self.to_hex(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw clear button
        self.draw_button("C", 2, 2, lambda: self.clear(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw clear one button
        self.draw_button("\u232B", 2, 3, lambda: self.clear_one(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw negate button
        self.draw_button("+/-", 6, 1, lambda: self.negate(),
                         keys.DIGIT_BG, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw digit buttons
        self.create_digit_buttons()

        # draw operator buttons
        self.create_operator_buttons()

        # draw equals button
        self.create_equals_button()

    # draw scientific buttons
    def draw_scientific_buttons(self):
        # draw mode change buttons
        self.create_mode_change_buttons()

        # draw memory buttons
        self.draw_memory_buttons()

        # draw absolute value button
        self.draw_button("|x|", 2, 0, lambda: self.abs(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw square root button
        self.draw_button("\u221A", 2, 1, lambda: self.square_root(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw square button
        self.draw_button("x\u00B2", 2, 2, lambda: self.square(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw clear button
        self.draw_button("C", 2, 3, lambda: self.clear(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw clear one button
        self.draw_button("\u232B", 2, 4, lambda: self.clear_one(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw sinus button
        self.draw_button("sin", 3, 0, lambda: self.sin(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw left parenthesis button
        self.draw_button("(", 3, 1, lambda: self.append_parantheses(
            "("), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw right parenthesis button
        self.draw_button(")", 3, 2, lambda: self.append_parantheses(
            ")"), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw factorial button
        self.draw_button("n!", 3, 3, lambda: self.factorial(),
                         keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw cosine button
        self.draw_button("cos", 4, 0, lambda: self.cos(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw tangent button
        self.draw_button("tan", 5, 0, lambda: self.tan(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw cotangent button
        self.draw_button("cot", 6, 0, lambda: self.cot(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw natural logarihtm button
        self.draw_button("ln", 7, 0, lambda: self.ln(
        ), keys.LABEL_COLOR, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw negate button
        self.draw_button("+/-", 7, 1, lambda: self.negate(),
                         keys.DIGIT_BG, keys.BLACK_COLOR, keys.DEFAULT_FONT_STYLE)

        # draw digit buttons
        self.create_digit_buttons()

        # draw operator buttons
        self.create_operator_buttons()

        # draw equals button
        self.create_equals_button()

    # add digit to current expression
    def add_digit(self, digit):
        if self.total_expression == "0":
            self.total_expression = ""
        if self.current_expression == "0":
            self.current_expression = str(digit)
        elif self.current_expression.find('.') != -1 and digit == '.':
            return
        else:
            self.current_expression += str(digit)
        self.update_label()

    # clear one digit from current expression
    def clear_one(self):
        if self.current_expression == "0":
            return
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    # update total label
    def update_total_label(self):
        expression = self.total_expression

        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f' {symbol} ')

        self.total_label.config(text=expression)

    # update label
    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    # append operator
    def append_operator(self, operator):
        if self.current_expression != "":
            if operator == "\u00F7":
                self.current_expression += "/"
            elif operator == "\u00D7":
                self.current_expression += "*"
            else:
                self.current_expression += operator
            self.total_expression += self.current_expression
            self.current_expression = ""
            self.update_total_label()
            self.update_label()

    # append parantheses
    def append_parantheses(self, parantheses):
        if self.current_expression != "":
            if parantheses == "(":
                self.current_expression = "(" + self.current_expression
            else:
                self.current_expression += parantheses
            self.update_label()

    # clear all
    def clear(self):
        self.current_expression = "0"
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    # calcultae the expression
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    # calculate factorial
    def factorial(self):
        if self.current_expression == "" or int(self.current_expression) > 15:
            return
        self.total_expression = self.current_expression + "!"
        self.current_expression = str(
            math.factorial(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # calculate square
    def square(self):
        if self.current_expression == "":
            return
        self.total_expression = self.current_expression + "\u00B2"
        self.current_expression = str(
            int(self.current_expression)**2)
        self.update_total_label()
        self.update_label()

    # calculate square root
    def square_root(self):
        if self.current_expression == "":
            return
        self.total_expression = "\u221A" + self.current_expression
        self.current_expression = str(
            math.sqrt(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # calculate sin
    def sin(self):
        if self.current_expression == "":
            return
        self.total_expression = "sin(" + self.current_expression + ")"
        self.current_expression = str(
            math.sin(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # calculate cos
    def cos(self):
        if self.current_expression == "":
            return
        self.total_expression = "cos(" + self.current_expression + ")"
        self.current_expression = str(
            math.cos(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # calculate tan
    def tan(self):
        if self.current_expression == "":
            return
        self.total_expression = "tan(" + self.current_expression + ")"
        self.current_expression = str(
            math.tan(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # calculate cot
    def cot(self):
        if self.current_expression == "" or self.current_expression == "0":
            return
        self.total_expression = "cot(" + self.current_expression + ")"
        self.current_expression = str(
            1/math.tan(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # calculate ln
    def ln(self):
        if self.current_expression == "" or self.current_expression == "0":
            return
        self.total_expression = "ln(" + self.current_expression + ")"
        self.current_expression = str(
            math.log(int(self.current_expression), math.e))
        self.update_total_label()
        self.update_label()

    # negate number
    def negate(self):
        if self.current_expression == "":
            return
        self.current_expression = str(-int(self.current_expression))
        self.update_label()

    # add to memory
    def add_to_memory(self):
        if self.current_expression == "":
            return
        self.memory += int(self.current_expression)
        self.update_total_label()
        self.update_label()

    # clear memory
    def clear_memory(self):
        self.memory = 0
        self.update_total_label()
        self.update_label()

    # recall from memory
    def recall_memory(self):
        self.current_expression = str(self.memory)
        self.update_total_label()
        self.update_label()

    # subtract from memory
    def subtract_from_memory(self):
        if self.current_expression == "":
            return
        self.memory -= int(self.current_expression)
        self.update_total_label()
        self.update_label()

    # memory store
    def memory_store(self):
        self.memory = int(self.current_expression)
        self.update_total_label()
        self.update_label()

    # calculate absolute value
    def abs(self):
        if self.current_expression == "":
            return
        self.total_expression = "|" + self.current_expression + "|"
        self.current_expression = str(
            abs(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # change window mode
    def change_mode(self, mode):
        if self.current_mode == mode:
            return
        self.current_mode = mode
        self.buttons_frame.destroy()
        self.buttons_frame = self.create_buttons_frame()
        self.choose_buttons()

    # convert to binary
    def to_binary(self):
        if self.current_expression == "":
            return
        self.total_expression = "bin(" + self.current_expression + ")"
        self.current_expression = str(
            bin(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # convert to octal
    def to_octal(self):
        if self.current_expression == "":
            return
        self.total_expression = "oct(" + self.current_expression + ")"
        self.current_expression = str(
            oct(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # convert to hexadecimal
    def to_hex(self):
        if self.current_expression == "":
            return
        self.total_expression = "hex(" + self.current_expression + ")"
        self.current_expression = str(
            hex(int(self.current_expression)))
        self.update_total_label()
        self.update_label()

    # bitwise left
    def bitwise_left(self):
        if self.current_expression == "":
            return
        self.total_expression = "<< " + self.current_expression
        self.current_expression = str(
            int(self.current_expression) << 1)
        self.update_total_label()
        self.update_label()

    # bitwise right
    def bitwise_right(self):
        if self.current_expression == "":
            return
        self.total_expression = ">> " + self.current_expression
        self.current_expression = str(
            int(self.current_expression) >> 1)
        self.update_total_label()
        self.update_label()

    # bind keys

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.clear_one())
        self.window.bind("<Delete>", lambda event: self.clear())
        self.window.bind("=", lambda event: self.evaluate())
        for key in self.scientific_digits:
            self.window.bind(str(key), lambda event,
                             key=key: self.add_digit(key))
        for key in self.operators:
            self.window.bind(str(key), lambda event,
                             key=key: self.append_operator(key))
