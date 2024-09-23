import customtkinter


class MissingInterface(customtkinter.CTkToplevel):
    def __init__(self, parent_app, ingredients):
        super().__init__()
        self.parent_app = parent_app
        self.ingredients = ingredients

        self.title("Hinweis")
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
        # Zutatenliste als Stichpunkte erstellen
        ingredients_text = "Es fehlen Zutaten für dieses Getränk, bitte geben Sie jemandem Bescheid.\n\n" + "\n".join(
            [f"- {ingredient}" for ingredient in self.ingredients])

        # Label mit den fehlenden Zutaten als Stichpunkte
        missing_label = customtkinter.CTkLabel(
            self, text=f"{ingredients_text}",
            font=customtkinter.CTkFont(size=16), wraplength=250
        )
        missing_label.pack(pady=(15, 15))

        # Button: "Ok"
        ok_button = customtkinter.CTkButton(
            self, text="Ok", command=self.on_confirm,
            font=customtkinter.CTkFont(size=16), width=120, height=40
        )
        ok_button.pack(side="bottom", pady=(10, 20))

    def on_confirm(self):
        """Aktion bei Bestätigung."""
        self.destroy()  # Popup schließen nach Bestätigung
