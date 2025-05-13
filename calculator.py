import customtkinter as ctk
import math

# Set appearance for the calculator (dark mode)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Main calculator class
class MyCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Title and size of the calculator window
        self.title("Simple Calculator")
        self.geometry("360x610")
        self.resizable(False, False)
        self.configure(fg_color="#1e1e1e")

        # Some initial variables
        self.calculator_type = "Normal"  # Start with Normal mode
        self.saved_number = 0
        self.history = []  # To store calculation history
        self.history_visible = False  # To track if history is shown

        # Create all widgets for the calculator
        self.make_all_widgets()

        # Bind keyboard keys to calculator functions
        self.bind("<Key>", self.keyboard_press)
        self.bind("<Return>", lambda event: self.when_button_clicked("="))
        self.bind("<BackSpace>", lambda event: self.when_button_clicked("⌫"))

    def make_all_widgets(self):
        # Create main frame for calculator
        self.main_frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True)

        # Create frame for calculator buttons
        self.calculator_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e")
        self.calculator_frame.pack(side="left", fill="both", expand=True)

        # Create mode selection buttons (Standard or Scientific)
        self.mode_area = ctk.CTkFrame(self.calculator_frame, fg_color="#1e1e1e")
        self.mode_area.pack(pady=5, padx=10, fill="x")

        self.normal_mode_button = ctk.CTkButton(
            self.mode_area, text="Standard", width=150, height=35,
            fg_color="#2d2d2d", hover_color="#3d3d3d",
            command=self.switch_to_normal
        )
        self.normal_mode_button.pack(side="left", padx=5)

        self.advanced_mode_button = ctk.CTkButton(
            self.mode_area, text="Scientific", width=150, height=35,
            fg_color="#2d2d2d", hover_color="#3d3d3d",
            command=self.switch_to_advanced
        )
        self.advanced_mode_button.pack(side="right", padx=5)

        # Label above input area (shows current expression or error)
        self.label_frame = ctk.CTkFrame(self.calculator_frame, fg_color="#1e1e1e")
        self.label_frame.pack(padx=15, pady=(0, 0), fill="x")

        # History button
        self.history_button = ctk.CTkButton(
            self.label_frame, text="📜", width=30, height=25, font=("Segoe UI", 14),
            fg_color="#1e1e1e", hover_color="#3d3d3d", text_color="gray",
            command=self.toggle_history
        )
        self.history_button.pack(side="left")
        self.history_button.pack_forget()  # Hide history initially

        # Label for showing the expression above the input box
        self.label_above_input = ctk.CTkLabel(
            self.label_frame, text="", font=("Segoe UI", 16),
            text_color="gray", anchor="e", height=20
        )
        self.label_above_input.pack(side="right", fill="x", expand=True)

        # Input box for numbers and expressions
        self.input_box = ctk.CTkEntry(
            self.calculator_frame, font=("Segoe UI", 28), justify="right",
            height=70, corner_radius=10, fg_color="#1e1e1e", text_color="white"
        )
        self.input_box.pack(padx=10, pady=10, fill="x")
        self.input_box.insert(0, "0")

        # Buttons for the calculator (numbers, operators, etc.)
        self.buttons_area = ctk.CTkFrame(self.calculator_frame, fg_color="#1e1e1e")
        self.buttons_area.pack(padx=10, pady=10, fill="both", expand=True)

        # History dropdown panel (hidden initially)
        self.history_dropdown = ctk.CTkFrame(self, fg_color="#2a2a2a", width=220, height=180, corner_radius=8)
        self.history_textbox = ctk.CTkTextbox(self.history_dropdown, wrap="none", font=("Segoe UI", 13), text_color="white")
        self.history_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.history_dropdown.place_forget()  # Hide history initially

        # Show the buttons on the calculator
        self.show_buttons()

    def show_buttons(self):
        # Clear any existing buttons from the previous screen
        for widget in self.buttons_area.winfo_children():
            widget.destroy()

        # Get the list of buttons based on the mode (standard or scientific)
        button_list = self.get_buttons_to_show()

        # Create buttons for each row and column
        for row_index, row in enumerate(button_list):
            for col_index, symbol in enumerate(row):
                is_scientific = self.calculator_type == "Scientific" and row_index < 4
                main_color = "#2d2d2d" if not is_scientific else "#292929"
                hover_color = "#3d3d3d" if not is_scientific else "#383838"
                height = 60 if not is_scientific else 45
                font_size = 20 if not is_scientific else 18

                # Special color for the "=" button
                if symbol == "=":
                    main_color = "#f57f17"
                    hover_color = "#ff9100"
                    height = 60

                # Create each button
                button = ctk.CTkButton(
                    self.buttons_area,
                    text=symbol,
                    font=("Segoe UI", font_size),
                    fg_color=main_color,
                    hover_color=hover_color,
                    text_color="white",
                    width=70,
                    height=height,
                    corner_radius=12,
                    command=lambda x=symbol: self.when_button_clicked(x)
                )
                button.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="nsew")

        # Configure the grid so buttons resize properly
        for i in range(len(button_list)):
            self.buttons_area.grid_rowconfigure(i, weight=1)
        for j in range(len(button_list[0])):
            self.buttons_area.grid_columnconfigure(j, weight=1)

    def get_buttons_to_show(self):
        # Buttons for standard mode
        standard_buttons = [
            ["MC", "MR", "M+", "M-"],
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]
        # Buttons for scientific mode
        scientific_buttons = [
            ["sin", "cos", "tan", "π"],
            ["log", "ln", "√", "^"],
            ["(", ")", "!", "e"],
            ["deg", "rad", "abs", "exp"]
        ]
        # Return either scientific or standard buttons
        return scientific_buttons + standard_buttons if self.calculator_type == "Scientific" else standard_buttons

    def switch_to_normal(self):
        self.calculator_type = "Normal"  # Switch to normal mode
        self.show_buttons()

    def switch_to_advanced(self):
        self.calculator_type = "Scientific"  # Switch to scientific mode
        self.show_buttons()

    def when_button_clicked(self, key_text):
        self.hide_history()  # Hide history when pressing any button
        try:
            if key_text == "C":
                self.input_box.delete(0, "end")
                self.input_box.insert("end", "0")
                self.label_above_input.configure(text="")
            elif key_text == "⌫":
                current = self.input_box.get()[:-1]
                self.input_box.delete(0, "end")
                self.input_box.insert("end", current if current else "0")
            elif key_text == "=":
                formula = self.input_box.get().replace("π", str(math.pi)).replace("^", "**").replace("√", "math.sqrt")
                try:
                    answer = eval(formula)
                except:
                    answer = "Error"
                self.label_above_input.configure(text="")
                expression = self.input_box.get()
                self.history.append(f"{expression} = {answer}")
                self.update_history_display()
                self.history_button.pack(side="left")
                self.input_box.delete(0, "end")
                self.input_box.insert("end", str(answer))
            elif key_text == "±":
                number = float(self.input_box.get())
                self.input_box.delete(0, "end")
                self.input_box.insert("end", str(-number))
            elif key_text in ["sin", "cos", "tan", "log", "ln", "!", "e", "deg", "rad", "abs", "exp"]:
                self.label_above_input.configure(text=f"{key_text}({self.input_box.get()})")
                self.handle_scientific_button(key_text)
            elif key_text == "MR":
                self.label_above_input.configure(text="MR")
                self.input_box.delete(0, "end")
                self.input_box.insert("end", str(self.saved_number))
            elif key_text == "MC":
                self.saved_number = 0
                self.label_above_input.configure(text="MC")
            elif key_text == "M+":
                try:
                    self.saved_number += float(self.input_box.get())
                    self.label_above_input.configure(text="M+")
                except:
                    pass
            elif key_text == "M-":
                try:
                    self.saved_number -= float(self.input_box.get())
                    self.label_above_input.configure(text="M-")
                except:
                    pass
            else:
                existing_text = self.input_box.get()
                if existing_text == "0":
                    existing_text = ""

                if key_text in "+-*/":
                    if existing_text and existing_text[-1] in "+-*/":
                        if existing_text[-1] == key_text:
                            return
                        else:
                            existing_text = existing_text[:-1]
                    self.label_above_input.configure(text=existing_text + key_text)

                self.input_box.delete(0, "end")
                self.input_box.insert("end", existing_text + key_text)
        except:
            self.input_box.delete(0, "end")
            self.input_box.insert("end", "Error")
            self.label_above_input.configure(text="")

    def handle_scientific_button(self, func_name):
        # Handle scientific operations
        try:
            value = float(self.input_box.get())
            result = 0
            if func_name == "sin":
                result = math.sin(math.radians(value))
            elif func_name == "cos":
                result = math.cos(math.radians(value))
            elif func_name == "tan":
                result = math.tan(math.radians(value))
            elif func_name == "log":
                result = math.log10(value)
            elif func_name == "ln":
                result = math.log(value)
            elif func_name == "√":
                result = math.sqrt(value)
            elif func_name == "!":
                result = math.factorial(int(value))
            elif func_name == "e":
                result = math.e
            elif func_name == "deg":
                result = math.degrees(value)
            elif func_name == "rad":
                result = math.radians(value)
            elif func_name == "abs":
                result = abs(value)
            elif func_name == "exp":
                result = math.exp(value)
        except:
            result = "Error"

        self.input_box.delete(0, "end")
        self.input_box.insert("end", str(result))

    def update_history_display(self):
        # Update history panel with recent calculations
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        for line in reversed(self.history[-20:]):
            self.history_textbox.insert("end", line + "\n")
        self.history_textbox.configure(state="disabled")

    def toggle_history(self):
        # Show or hide history dropdown panel
        if self.history_visible:
            self.hide_history()
        else:
            x = self.history_button.winfo_rootx() - self.winfo_rootx()
            y = self.history_button.winfo_rooty() - self.winfo_rooty() + 30
            self.history_dropdown.place(x=x, y=y)
            self.history_visible = True

    def hide_history(self):
        # Hide the history panel
        if self.history_visible:
            self.history_dropdown.place_forget()
            self.history_visible = False

    def keyboard_press(self, event):
        self.hide_history()  # Hide history on key press
        typed = event.char
        key_converter = {
            "\r": "=",
            "\n": "=",
            "\x08": "⌫",
            ".": ".",
            ",": ".",
            "-": "-",
            "+": "+",
            "*": "*",
            "/": "/",
            "%": "%",
            "(": "(",
            ")": ")"
        }

        if typed in "0123456789":
            self.when_button_clicked(typed)
        elif typed in key_converter:
            self.when_button_clicked(key_converter[typed])

# Run the calculator application
if __name__ == "__main__":
    app = MyCalculator()
    app.mainloop()
