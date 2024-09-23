import customtkinter


class ConfirmationInterface(customtkinter.CTkToplevel):
    def __init__(self, parent_app, drink_name, ingredients, strength, fill):
        super().__init__()
        self.parent_app = parent_app
        self.drink_name = drink_name
        self.ingredients = ingredients
        self.strength = strength
        self.fill = fill

        self.title("Bestätigung")
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
        # Label mit der Frage
        question_label = customtkinter.CTkLabel(
            self, text=f"{self.drink_name}\nzubereiten?",
            font=customtkinter.CTkFont(size=20), wraplength=250
        )
        question_label.pack(pady=(15, 15))

        # Zwei Buttons: "Ja" und "Abbrechen"
        yes_button = customtkinter.CTkButton(
            self, text="Ja", command=self.on_confirm,
            font=customtkinter.CTkFont(size=16), width=120, height=40
        )
        yes_button.pack(pady=(5, 10))

        cancel_button = customtkinter.CTkButton(
            self, text="Abbrechen", command=self.on_cancel,
            font=customtkinter.CTkFont(size=16), width=120, height=40
        )
        cancel_button.pack(pady=2)

    def on_confirm(self):
        """Aktion bei Bestätigung."""
        self.destroy()  # Popup schließen nach Bestätigung

        # Zeige das "Bitte warten"-Popup an, beginnt die Zubereitung
        self.parent_app.show_preparation_interface(
            self.drink_name, self.ingredients, self.strength, self.fill
        )

    def on_cancel(self):
        """Aktion bei Abbruch."""
        self.destroy()  # Popup schließen nach Abbruch
