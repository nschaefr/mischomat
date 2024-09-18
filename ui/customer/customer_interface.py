import random
from tkinter import messagebox
import customtkinter
from PIL import Image
import sys  # For exiting the program
from utils.json_operations import load_json
from ui.customer.strength_interface import StrengthInterface
from ui.customer.confirmation_interface import ConfirmationInterface
from ui.customer.missing_interface import MissingInterface


class CustomerInterface(customtkinter.CTkFrame):
    def __init__(self, parent_app):
        super().__init__(parent_app.frame_container)
        self.parent_app = parent_app

        self.left_frame = customtkinter.CTkFrame(self, width=1)
        self.left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # Create a tab view for category selection
        self.tabview = customtkinter.CTkTabview(self, width=300)
        self.tabview.pack(side="left", fill="both",
                          expand=True, padx=5, pady=10)

        # Add tabs for Mischgetränke and Longdrinks
        self.tab_mischgetraenke = self.tabview.add("Mischgetränke")
        self.tab_longdrinks = self.tabview.add("Longdrinks")

        # Create scrollable frames for each tab
        self.scroll_frame_mischgetraenke = customtkinter.CTkScrollableFrame(
            self.tab_mischgetraenke)
        self.scroll_frame_mischgetraenke.pack(fill="both", expand=True)

        self.scroll_frame_longdrinks = customtkinter.CTkScrollableFrame(
            self.tab_longdrinks)
        self.scroll_frame_longdrinks.pack(fill="both", expand=True)

        # Exit button (red) for quitting the program
        exit_button = customtkinter.CTkButton(
            self.left_frame, text="Off", width=62, height=50, font=customtkinter.CTkFont(size=17),
            fg_color="#ff4d4d", hover_color="#cc0000", command=self.on_exit_button_click
        )
        exit_button.pack(pady=(0, 2))

        # Settings button
        self.settings_icon = customtkinter.CTkImage(
            Image.open('assets/setting.png'), size=(35, 35))
        settings_button = customtkinter.CTkButton(
            self.left_frame, image=self.settings_icon, text="", fg_color="transparent", border_width=2, width=62, height=50,
            command=self.on_settings_click
        )
        settings_button.pack()  # Add spacing between buttons

        # Random button
        random_button = customtkinter.CTkButton(
            self.left_frame, text="Zufall", width=62, height=50, font=customtkinter.CTkFont(size=17),
            fg_color="#c4a439", hover_color="#806a25", command=self.on_random_button_click
        )
        random_button.pack(side="bottom")

        # Create buttons for each category
        self.create_buttons(self.scroll_frame_mischgetraenke, "Mischgetränk")
        self.create_buttons(self.scroll_frame_longdrinks, "Longdrink")

    def create_buttons(self, frame, category):
        """Erstellt Buttons für die gegebene Kategorie im angegebenen Frame."""
        data = self.load_data(category)
        ingredient_data = load_json('database/liquids.json')

        # Clear existing widgets
        self.clear_frame(frame)

        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

        # Create new buttons
        row, col = 0, 0
        for key, drink in data.items():
            if self.is_button_enabled(drink, ingredient_data):
                text = drink['name']
                truncated_text = self.truncate_text(text)
                button = customtkinter.CTkButton(
                    frame, text=truncated_text, command=lambda d=drink['name'], c=category, i=drink['zutaten'], f=drink['gesamtmenge_ml']: self.on_button_click(
                        d, c, i, f),
                    font=customtkinter.CTkFont(size=17),
                    height=100
                )
                button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

                col += 1
                if col >= 4:  # 3 or 4 columns
                    col = 0
                    row += 1

        # Configure grid columns and rows
        for i in range(4):  # Number of columns
            frame.grid_columnconfigure(i, weight=1)
            frame.grid_rowconfigure(i, weight=1)

    def truncate_text(self, text):
        if len(text) > 13:
            return text[:13] + "\n" + text[13:]
        return text

    def is_button_enabled(self, drink, ingredient_data):
        for ingredient_id, percentage in drink['zutaten'].items():
            ingredient_info = ingredient_data.get(ingredient_id, None)

            if not ingredient_info:
                return False

            if not (ingredient_info['gewaehlt'] == 1 and ingredient_info['anschlussplatz'] > 0):
                return False

        return True

    def update_buttons(self):
        """Aktualisiert die Buttons in den Scroll-Frames."""
        self.create_buttons(self.scroll_frame_mischgetraenke, "Mischgetränk")
        self.create_buttons(self.scroll_frame_longdrinks, "Longdrink")

    def clear_frame(self, frame):
        """Löscht alle Widgets im gegebenen Frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def on_random_button_click(self):
        category = random.choice(["Mischgetränk", "Longdrink"])
        data = self.load_data(category)

        available_drinks = [drink for key, drink in data.items(
        ) if self.is_button_enabled(drink, load_json('database/liquids.json'))]

        if available_drinks:
            drink = random.choice(available_drinks)
            drink_name = drink['name']
            fill = drink["gesamtmenge_ml"]

            self.on_button_click(drink_name, category, drink['zutaten'], fill)

    def on_settings_click(self):
        self.parent_app.show_pin_code_interface(1)

    def on_button_click(self, drink_name, category, ingredients, fill):
        missing_ingredients = self.check_ingredients(ingredients, fill)

        if missing_ingredients:
            MissingInterface(self.parent_app, missing_ingredients)
        else:
            if category == "Mischgetränk":
                StrengthInterface(
                    self.parent_app, drink_name, ingredients, fill)
            elif category == "Longdrink":
                ConfirmationInterface(
                    self.parent_app, drink_name, ingredients, None, fill)

    def load_data(self, category):
        file_path = 'database/mix.json' if category == 'Mischgetränk' else 'database/longdrinks.json'
        return load_json(file_path)

    def check_ingredients(self, ingredients, fill):
        """Überprüft, ob alle benötigten Zutaten verfügbar sind."""
        missing_ingredients = []
        ingredient_data = load_json('database/liquids.json')

        for ingredient_id, percentage in ingredients.items():
            ingredient_info = ingredient_data.get(ingredient_id, None)

            # Wenn die Zutat nicht existiert oder nicht genug Füllstand hat oder nicht gewählt ist
            if not ingredient_info or ingredient_info['gewaehlt'] == 0 or ingredient_info['anschlussplatz'] == 0:
                missing_ingredients.append(
                    ingredient_info['name'] if ingredient_info else "Unbekannte Zutat")
            else:
                required_fill = (percentage + 5) * fill / 100
                actual_fill = ingredient_info['fuellstand_ml']

                if actual_fill < required_fill:
                    missing_ingredients.append(ingredient_info['name'])

        return missing_ingredients

    def on_exit_button_click(self):
        sys.exit()  # Closes the program
