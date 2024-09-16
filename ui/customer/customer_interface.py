import random
import customtkinter
from PIL import Image
from utils.json_operations import load_json
from ui.customer.strength_interface import StrengthInterface
from ui.customer.confirmation_interface import ConfirmationInterface


class CustomerInterface(customtkinter.CTkFrame):
    def __init__(self, parent_app):
        super().__init__(parent_app.frame_container)
        self.parent_app = parent_app

        self.left_frame = customtkinter.CTkFrame(self, width=1)
        self.left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        self.middle_frame = customtkinter.CTkScrollableFrame(
            self, label_text="Mischgetränke")
        self.middle_frame.pack(side="left", fill="both",
                               expand=True, padx=5, pady=10)

        self.right_frame = customtkinter.CTkScrollableFrame(
            self, label_text="Longdrinks")
        self.right_frame.pack(side="left", fill="both",
                              expand=True, padx=(5, 10), pady=10)

        self.settings_icon = customtkinter.CTkImage(
            Image.open('assets/setting.png'), size=(35, 35))
        settings_button = customtkinter.CTkButton(
            self.left_frame, image=self.settings_icon, text="", fg_color="transparent", border_width=2, width=62, height=50,
            command=self.on_settings_click
        )
        settings_button.pack()

        random_button = customtkinter.CTkButton(
            self.left_frame, text="Zufall", width=62, height=50, font=customtkinter.CTkFont(size=17),
            fg_color="#c4a439", hover_color="#806a25", command=self.on_random_button_click
        )
        random_button.pack(side="bottom", pady=0)

        self.create_buttons(self.middle_frame, "Mischgetränk")
        self.create_buttons(self.right_frame, "Longdrink")

    def create_buttons(self, frame, category):
        data = self.load_data(category)
        ingredient_data = load_json('database/liquids.json')
        row, col = 0, 0

        for key, drink in data.items():
            if self.is_button_enabled(drink, ingredient_data):
                text = drink['name']
                truncated_text = self.truncate_text(text)
                button = customtkinter.CTkButton(
                    frame, text=truncated_text, command=lambda d=drink['name'], c=category, i=drink['zutaten'], f=drink['gesamtmenge_ml']: self.on_button_click(
                        d, c, i, f),
                    font=customtkinter.CTkFont(size=17),
                    width=100, height=70
                )
                button.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

                col += 1
                if col > 1:
                    col = 0
                    row += 1

        frame.grid_columnconfigure((0, 1), weight=1)

    def truncate_text(self, text):
        if len(text) > 13:
            return text[:13] + "..."
        return text

    def is_button_enabled(self, drink, ingredient_data):
        for ingredient_id, percentage in drink['zutaten'].items():
            ingredient_info = ingredient_data.get(ingredient_id, None)

            if not ingredient_info:
                return False

            required_fill = percentage * drink['gesamtmenge_ml'] / 100
            actual_fill = ingredient_info['fuellstand_ml']

            if not (actual_fill >= required_fill and ingredient_info['gewaehlt'] == 1 and ingredient_info['anschlussplatz'] > 0):
                return False

        return True

    def update_buttons(self):
        self.create_buttons(self.middle_frame, "Mischgetränk")
        self.create_buttons(self.right_frame, "Longdrink")

    def on_random_button_click(self):
        category = random.choice(["Mischgetränk", "Longdrink"])
        data = self.load_data(category)

        available_drinks = [drink for key, drink in data.items(
        ) if self.is_button_enabled(drink, load_json('database/liquids.json'))]

        if available_drinks:
            drink = random.choice(available_drinks)
            drink_name = drink['name']

            self.on_button_click(drink_name, category, drink['zutaten'])

    def on_settings_click(self):
        self.parent_app.show_pin_code_interface(True)

    def on_button_click(self, drink_name, category, ingredients, fill):
        if category == "Mischgetränk":
            StrengthInterface(self.parent_app, drink_name, ingredients, fill)
        elif category == "Longdrink":
            ConfirmationInterface(
                self.parent_app, drink_name, ingredients, None, fill)

    def load_data(self, category):
        file_path = 'database/mix.json' if category == 'Mischgetränk' else 'database/longdrinks.json'
        return load_json(file_path)
