import customtkinter
import sys
from utils.json_operations import load_json, save_json


class ConfigurationInterface(customtkinter.CTkFrame):
    def __init__(self, parent_app):
        super().__init__(parent_app.frame_container)
        self.parent_app = parent_app

        # Daten nur einmal laden
        self.longdrink_data = load_json("database/longdrinks.json")
        self.mix_data = load_json("database/mix.json")
        self.drinks_data = load_json("database/liquids.json")

        # Main container frame
        self.container_frame = customtkinter.CTkFrame(self)
        self.container_frame.pack(fill="both", expand=True)

        # Layout config
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(1, weight=3)

        # Frame for longdrinks and mix options
        self.frame = customtkinter.CTkFrame(self.container_frame)
        self.frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Longdrink and mix options
        self.create_drink_options()

        # Scrollable frame for drink selection
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.container_frame, label_text="Getränkewahl")
        self.scrollable_frame.grid(
            row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        # Drink options
        self.create_drink_widgets()

    def create_drink_options(self):
        """Erstellt die Longdrink- und Mischgetränk-Auswahloptionen."""
        self.longdrink_label = customtkinter.CTkLabel(
            self.frame, text="Longdrinks", font=customtkinter.CTkFont(size=19))
        self.longdrink_label.pack(pady=(14, 6))

        self.longdrink_option = customtkinter.CTkOptionMenu(
            self.frame, values=["250ml", "300ml", "350ml", "400ml", "450ml", "500ml"])
        self.longdrink_option.pack(pady=0)
        self.longdrink_option.set(
            str(self.longdrink_data["1"]["gesamtmenge_ml"]) + "ml")

        self.mix_label = customtkinter.CTkLabel(
            self.frame, text="Mischgetränke", font=customtkinter.CTkFont(size=19))
        self.mix_label.pack(pady=(14, 6))

        self.mix_option = customtkinter.CTkOptionMenu(
            self.frame, values=["250ml", "300ml", "350ml", "400ml", "450ml", "500ml"])
        self.mix_option.pack()
        self.mix_option.set(str(self.mix_data["1"]["gesamtmenge_ml"]) + "ml")

        self.button = customtkinter.CTkButton(
            self.frame, command=self.size_button_event, text="Weiter", font=customtkinter.CTkFont(size=16), width=120, height=40)
        self.button.pack(side="bottom", pady=14)

    def create_drink_widgets(self):
        """Erstellt die Getränkeauswahl-Widgets."""
        for drink_id, drink_info in self.drinks_data.items():
            drink_frame = customtkinter.CTkFrame(self.scrollable_frame)
            drink_frame.pack(pady=5, fill="x")

            drink_frame.drink_id = drink_id

            drink_name = drink_info["name"]

            check_var = customtkinter.BooleanVar(
                value=self.drinks_data[drink_id]["gewaehlt"] == 1)
            check_box = customtkinter.CTkCheckBox(
                drink_frame,
                text="",
                variable=check_var,
                command=lambda var=check_var, frame=drink_frame, id=drink_id: self.toggle_option_menu(
                    var, frame, id)
            )
            check_box.configure(width=20, height=20)
            check_box.pack(side="left", padx=0)

            drink_label = customtkinter.CTkLabel(
                drink_frame, text=drink_name, font=customtkinter.CTkFont(size=16))
            drink_label.pack(side="left", padx=10)

            anschlussplatz_value = str(
                self.drinks_data[drink_id]["anschlussplatz"])
            option_menu = customtkinter.CTkOptionMenu(
                drink_frame,
                values=self.get_anschlussplatz_values(drink_info),
                width=60,
                command=lambda event, frame=drink_frame, id=drink_id: self.update_place(
                    frame, id, 1)
            )
            option_menu.set(
                anschlussplatz_value if anschlussplatz_value != "0" else "-")

            fuellstand_value = str(
                self.drinks_data[drink_id]["fuellstand_ml"]) + "ml"
            fuellstand_menu = customtkinter.CTkOptionMenu(
                drink_frame,
                values=self.get_fuellstand_values(drink_info),
                width=100,
                command=lambda value, id=drink_id: self.update_fuellstand(
                    id, value)
            )
            fuellstand_menu.set(fuellstand_value)

            if self.drinks_data[drink_id]["gewaehlt"] == 1:
                option_menu.pack(side="right", padx=0)
                fuellstand_menu.pack(side="right", padx=10)
            else:
                option_menu.pack_forget()
                fuellstand_menu.pack_forget()

            drink_frame.option_menu = option_menu
            drink_frame.fuellstand_menu = fuellstand_menu
            drink_frame.check_var = check_var

    def get_fuellstand_values(self, drink_info):
        """Bestimmt die verfügbaren Füllstandswerte basierend auf belegungswert."""
        if drink_info["belegungswert"] == 1:
            return [str(i) + "ml" for i in range(250, 1500, 250)]
        else:
            return [str(i) + "ml" for i in range(2000, 2100, 100)]

    def size_button_event(self):
        """Speichert die gewählten Größen und navigiert zur nächsten Seite."""
        longdrink_size = self.longdrink_option.get()
        mix_size = self.mix_option.get()

        longdrink_size_ml = int(longdrink_size.replace("ml", ""))
        mix_size_ml = int(mix_size.replace("ml", ""))

        # Speichern der Longdrinks
        for drink in self.longdrink_data:
            self.longdrink_data[drink]['gesamtmenge_ml'] = longdrink_size_ml
        save_json('database/longdrinks.json', self.longdrink_data)

        # Speichern der Mischgetränke
        for drink in self.mix_data:
            self.mix_data[drink]['gesamtmenge_ml'] = mix_size_ml
        save_json('database/mix.json', self.mix_data)

        self.parent_app.show_customer_interface(True)

    def toggle_option_menu(self, check_var, frame, drink_id):
        """Aktualisiert die Anzeige der OptionMenu und Füllstand basierend auf der Auswahl."""
        if check_var.get():
            self.drinks_data[drink_id]["gewaehlt"] = 1
            frame.option_menu.pack(side="right", padx=0)
            frame.option_menu.set(
                str(self.drinks_data[drink_id]["anschlussplatz"]) if self.drinks_data[drink_id]["anschlussplatz"] != 0 else "-")
            frame.fuellstand_menu.set(
                str(self.drinks_data[drink_id]["fuellstand_ml"]) + "ml")
            if (self.drinks_data[drink_id]["anschlussplatz"] != 0) & (self.drinks_data[drink_id]["belegungswert"] == 1):
                frame.fuellstand_menu.pack(side="right", padx=10)
            else:
                frame.fuellstand_menu.pack_forget()
        else:
            self.drinks_data[drink_id]["gewaehlt"] = 0
            frame.option_menu.pack_forget()
            frame.fuellstand_menu.pack_forget()

            frame.option_menu.set("-")
            frame.fuellstand_menu.set("250ml")
            self.drinks_data[drink_id]["anschlussplatz"] = 0
            if self.drinks_data[drink_id]["belegungswert"] == 1:
                self.drinks_data[drink_id]["fuellstand_ml"] = 250

        save_json("database/liquids.json", self.drinks_data)
        self.refresh_option_menus()

    def update_place(self, frame, drink_id, check_var):
        """Aktualisiert den Anschlussplatz basierend auf der Auswahl."""
        value = int(frame.option_menu.get()) if (check_var == 1) & (
            frame.option_menu.get() != "-") else 0
        if value != 0:
            frame.fuellstand_menu.pack(side="right", padx=10)
        else:
            frame.fuellstand_menu.pack_forget()

        if drink_id in self.drinks_data:
            self.drinks_data[drink_id]["anschlussplatz"] = value
            save_json("database/liquids.json", self.drinks_data)

        self.refresh_option_menus()

    def get_anschlussplatz_values(self, drink_info):
        """Bestimmt die verfügbaren Anschlussplatzwerte basierend auf belegungswert und filtert belegte Plätze."""
        # Alle belegten Plätze sammeln
        belegte_plaetze = {self.drinks_data[drink]["anschlussplatz"]
                           for drink in self.drinks_data if self.drinks_data[drink]["anschlussplatz"] != 0}

        # Festlegen der Anschlussplatzbereiche
        if drink_info["belegungswert"] == 0:
            moegliche_plaetze = set(range(1, 10))  # Bereich 1-9
        else:
            moegliche_plaetze = set(range(10, 20))  # Bereich 10-19

        # Verfügbare Plätze, indem belegte Plätze ausgeschlossen werden
        verfuegbare_plaetze = moegliche_plaetze - belegte_plaetze

        # Rückgabe als Liste von Strings, "-" für keinen Platz
        return ["-"] + [str(platz) for platz in sorted(verfuegbare_plaetze)]

    def update_fuellstand(self, drink_id, value):
        """Aktualisiert den Füllstand des Getränks."""
        fuellstand_value = int(value.replace("ml", ""))
        if drink_id in self.drinks_data:
            self.drinks_data[drink_id]["fuellstand_ml"] = fuellstand_value
            save_json("database/liquids.json", self.drinks_data)

    def refresh_fuellstand_values(self):
        """Aktualisiert die Füllstandswerte für alle ausgewählten Getränke."""
        # Lade aktuelle Daten aus der JSON-Datei neu
        self.drinks_data = load_json("database/liquids.json")

        # Iteriere durch alle Getränke im scrollable_frame und aktualisiere deren Füllstände
        for drink_frame in self.scrollable_frame.winfo_children():
            drink_id = drink_frame.drink_id

            # Falls das Getränk als gewählt markiert ist, aktualisiere die Füllstandswerte
            if self.drinks_data[drink_id]["gewaehlt"] == 1:
                fuellstand_value = str(
                    self.drinks_data[drink_id]["fuellstand_ml"]) + "ml"
                drink_frame.fuellstand_menu.set(fuellstand_value)

    def refresh_option_menus(self):
        """Aktualisiert die OptionMenus für alle Getränke basierend auf den belegten Plätzen."""
        for drink_frame in self.scrollable_frame.winfo_children():
            drink_id = drink_frame.drink_id
            anschlussplatz_value = str(
                self.drinks_data[drink_id]["anschlussplatz"])

            # Aktualisiere die verfügbaren Anschlussplatzoptionen
            option_values = self.get_anschlussplatz_values(
                self.drinks_data[drink_id])
            drink_frame.option_menu.configure(values=option_values)
