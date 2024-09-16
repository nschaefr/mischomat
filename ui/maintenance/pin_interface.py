import customtkinter


class PinCodeInterface(customtkinter.CTkFrame):
    def __init__(self, parent_app, customer, correct_pin="1234"):
        super().__init__(parent_app.frame_container)
        self.parent_app = parent_app
        self.correct_pin = correct_pin
        self.customer = customer
        self.entered_pin = ""

        self.pin_frame = customtkinter.CTkFrame(self)
        self.pin_frame.pack(fill="both", expand=True)

        if self.customer:
            back_button = customtkinter.CTkButton(
                self.pin_frame, text="Zurück", command=self.on_back_pressed, font=customtkinter.CTkFont(size=18), width=100, height=40
            )
            back_button.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

        self.pin_display = customtkinter.CTkLabel(
            self.pin_frame, text="____", font=customtkinter.CTkFont(size=30))
        if self.customer:
            self.pin_display.place(relx=0.465, rely=0.03)
        else:
            self.pin_display.pack(pady=(10, 5))

        button_frame = customtkinter.CTkFrame(self.pin_frame)
        button_frame.pack(pady=18)

        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]

        for (text, row, column) in buttons:
            button = customtkinter.CTkButton(button_frame, text=text, width=70, height=70,
                                             command=lambda num=text: self.append_pin(num), font=customtkinter.CTkFont(size=18))
            button.grid(row=row, column=column, padx=4, pady=4)

    def append_pin(self, num):
        if len(self.entered_pin) < 4:
            self.entered_pin += num
            self.update_pin_display()

            if len(self.entered_pin) == 4:
                self.check_pin()

    def update_pin_display(self):
        display_text = '*' * len(self.entered_pin) + \
            '_' * (4 - len(self.entered_pin))
        self.pin_display.configure(text=display_text)

    def check_pin(self):
        if self.entered_pin == self.correct_pin:
            self.parent_app.show_configuration_interface()
            self.reset_pin()
        else:
            self.reset_pin()

    def reset_pin(self):
        self.entered_pin = ""
        self.update_pin_display()

    def on_back_pressed(self):
        self.parent_app.show_customer_interface(False)
