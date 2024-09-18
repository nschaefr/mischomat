import customtkinter
from utils.json_operations import load_json, save_json


class PreparationInterface(customtkinter.CTkFrame):
    def __init__(self, parent_app, drink_name, ingredient_numbers, strength, fill):
        super().__init__(parent_app.frame_container)
        self.parent_app = parent_app
        self.drink_name = drink_name
        self.ingredient_numbers = ingredient_numbers
        self.strength = strength
        self.fill = fill

        self.configure(bg_color="white", corner_radius=0)
        self.setup_ui()

    def setup_ui(self):
        self.label = customtkinter.CTkLabel(
            self, text=f"Dein Getränk wird zubereitet",
            font=customtkinter.CTkFont(size=26)
        )
        self.label.pack(pady=(135, 5))

        self.sub_label = customtkinter.CTkLabel(
            self, text=f"Wir bitten um etwas Geduld",
            font=customtkinter.CTkFont(size=18)
        )
        self.sub_label.pack(pady=(5, 5))

        self.progress_bar = customtkinter.CTkProgressBar(
            self, orientation="horizontal", mode="indeterminate", height=12
        )
        self.progress_bar.pack(pady=30, padx=20)
        self.max_width = 300
        self.progress_bar.configure(width=self.max_width)

    def update_values(self, drink_name, ingredient_numbers, strength, fill):
        self.drink_name = drink_name
        self.ingredient_numbers = ingredient_numbers
        self.strength = strength
        self.fill = fill

        data = load_json("database/liquids.json")

        if strength != None:
            for ingredient_id, percentage in self.ingredient_numbers.items():
                if (data[ingredient_id]["alcohol"] == 1):
                    self.percentage_alc = self.ingredient_numbers[ingredient_id]
                    if (self.strength == "Schwach"):
                        self.percentage_alc -= 5
                    if (self.strength == "Stark"):
                        self.percentage_alc += 5
                else:
                    self.percentage_filler = self.ingredient_numbers[ingredient_id]
                    if (self.strength == "Schwach"):
                        self.percentage_filler += 5
                    if (self.strength == "Stark"):
                        self.percentage_filler -= 5

        self.start_dispensing()

    def start_dispensing(self):
        self.progress_bar.start()

        # raspberryHardwareFunctionMix(self.percentage_alc, self.percentage_filler, self.ingredient_numbers, self.fill)
        # raspberryHardwareFunctionLong(self.ingredient_numbers, self.fill)

        # while !getFunctionFromRaspberry():
        #   pass

        self.after(10000, self.finish_preparation)

    def finish_preparation(self):
        self.parent_app.show_customer_interface(False)
        self.update_liquids()
        self.progress_bar.stop()

    def update_liquids(self):
        data = load_json("database/liquids.json")

        for ingredient_id, percentage in self.ingredient_numbers.items():
            if ingredient_id in data:
                if self.strength != None:
                    if data[ingredient_id]["alcohol"] == 0:
                        percentage = self.percentage_filler
                    else:
                        percentage = self.percentage_alc
                ingredient_info = data[ingredient_id]
                required_fill = percentage * self.fill / 100
                ingredient_info['fuellstand_ml'] = int(
                    ingredient_info['fuellstand_ml'] - required_fill)

        save_json("database/liquids.json", data)
