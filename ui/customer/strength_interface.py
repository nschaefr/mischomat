import customtkinter
from ui.customer.confirmation_interface import ConfirmationInterface


class StrengthInterface(customtkinter.CTkToplevel):
    def __init__(self, parent_app, drink_name, ingredients, fill):
        super().__init__()
        self.parent_app = parent_app
        self.drink_name = drink_name
        self.ingredients = ingredients
        self.fill = fill

        self.title(f"Stärke für {self.drink_name}")
        self.geometry("300x200")  # Größe des Popups
        self.resizable(False, False)  # Größe nicht veränderbar

        # Fenster relativ zur Mitte des Hauptfensters öffnen
        self.transient(parent_app)

        self.setup_ui()

        # Fokus auf das Popup legen, nachdem es angezeigt wurde
        self.after(10, self.grab_focus)

    def grab_focus(self):
        self.grab_set()  # Legt den Fokus auf das Popup-Fenster, sobald es "sichtbar" ist

    def setup_ui(self):
        # Drei Buttons für die Stärke-Auswahl
        weak_button = customtkinter.CTkButton(
            self, text="Schwach", command=lambda: self.on_strength_selected("Schwach"),
            font=customtkinter.CTkFont(size=16), width=150, height=40
        )
        weak_button.pack(pady=(28, 5))

        medium_button = customtkinter.CTkButton(
            self, text="Mittel", command=lambda: self.on_strength_selected("Mittel"),
            font=customtkinter.CTkFont(size=16), width=150, height=40
        )
        medium_button.pack(pady=5)

        strong_button = customtkinter.CTkButton(
            self, text="Stark", command=lambda: self.on_strength_selected("Stark"),
            font=customtkinter.CTkFont(size=16), width=150, height=40
        )
        strong_button.pack(pady=5)

    def on_strength_selected(self, strength):
        """Aktion bei Auswahl der Stärke."""
        self.destroy()  # Popup schließen nach Auswahl

        ConfirmationInterface(
            self.parent_app, self.drink_name, self.ingredients, strength, self.fill)
