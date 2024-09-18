import customtkinter
from ui.maintenance.configuration_interface import ConfigurationInterface
from ui.maintenance.pin_interface import PinCodeInterface
from ui.customer.customer_interface import CustomerInterface
from ui.customer.preparation_interface import PreparationInterface

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mischomat")
        self.geometry("800x400")
        self.resizable(False, False)

        self.frame_container = customtkinter.CTkFrame(self)
        self.frame_container.pack(fill="both", expand=True)

        self.loading_frame = customtkinter.CTkFrame(self.frame_container)
        self.loading_frame.pack(fill="both", expand=True)
        loading_label = customtkinter.CTkLabel(
            self.loading_frame, text="Mischomat wird gestartet...", font=customtkinter.CTkFont(size=25))
        loading_label.pack(expand=True)

        # Frames einmalig erstellen, aber nicht direkt anzeigen
        self.pin_frame = PinCodeInterface(self, False)
        self.pin_frame_cust = PinCodeInterface(self, True)
        self.config_frame = ConfigurationInterface(self)
        self.customer_frame = CustomerInterface(self)
        self.prep_frame = PreparationInterface(self, None, None, None, None)

        # Starte mit dem PinCode Interface (customer=False)
        self.show_pin_code_interface(0)

    def show_configuration_interface(self):
        self.clear_frame()  # Versteckt alle anderen Frames
        self.config_frame.refresh_fuellstand_values()
        self.config_frame.pack(fill="both", expand=True)

    def show_pin_code_interface(self, customer):
        self.clear_frame()  # Versteckt alle anderen Frames

        if customer:  # Unterschiedliches Verhalten bei customer True/False
            # Erstelle den Pin-Code-Frame nur einmal, außer der Kundenstatus ändert sich
            self.pin_frame_cust.pack(fill="both", expand=True)
        else:
            self.pin_frame.pack(fill="both", expand=True)

    def show_customer_interface(self, config):
        self.clear_frame()  # Versteckt alle anderen Frames

        if config:
            self.customer_frame.update_buttons()
            self.customer_frame.pack(fill="both", expand=True)
        else:
            self.customer_frame.pack(fill="both", expand=True)

        self.loading_frame.pack_forget()

    def show_preparation_interface(self, drink_name, ingredients, strength, fill):
        self.clear_frame()
        self.prep_frame.update_values(drink_name, ingredients, strength, fill)
        self.prep_frame.pack(fill="both", expand=True)

    def clear_frame(self):
        # Versteckt alle Frames, aber zerstört sie nicht
        for widget in self.frame_container.winfo_children():
            widget.pack_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
