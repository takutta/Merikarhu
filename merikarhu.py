from tkinter import *
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os


class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, paths=None, patterns="*", logfunc=print, gui=None):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.paths = paths or []
        self.setup_watchers()
        self.log = logfunc
        self.gui = gui
        self.txt_loytyi = False
        self.excel_loytyi = False

    def setup_watchers(self):
        for path in self.paths:
            self.schedule(self, path=path, recursive=False)

    def on_created(self, event):
        # Tiedoston luomistapahtuma
        self.process_file(event.src_path)

    def process_file(self, file_path):
        # Tiedoston käsittely tiedostotyypin perusteella
        if file_path.endswith(".txt"):
            self.process_text_file(file_path)
        elif file_path.endswith(".xls"):
            self.process_excel_file(file_path)
        # Lisää tarvittaessa muita tiedostotyyppejä ja niiden käsittelyfunktioita

    def process_text_file(self, file_path):
        # Tiedostotyypin mukainen käsittely
        self.txt_loytyi = True
        self.log(f"Titania löytyi: {file_path}")
        self.check_files_and_show_button()

    def process_excel_file(self, file_path):
        # Tiedostotyypin mukainen käsittely
        self.excel_loytyi = True
        self.log(f"Excel löytyi: {file_path}")
        self.check_files_and_show_button()

    def check_files_and_show_button(self):
        if self.txt_loytyi and self.excel_loytyi:
            self.log("Molemmat tiedostot löytyivät.")
            self.gui.show_button()


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.watchdog = None
        self.watch_paths = [
            r"C:\Users\pampi\testi",
            r"C:\Users\pampi\testi2",
        ]  # Aseta haluamasi oletuskansiot tähän
        self.title("Merikarhu")
        self.resizable(False, False)
        self.create_widgets()
        self.start_watchdog()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Laske ikkunan leveys ja korkeus
        window_width = 800
        window_height = 600

        # Laske ikkunan sijainti
        x = (screen_width - window_width) // 2
        y = 0
        # Aseta ikkunan sijainti
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        # Luo Canvas-olio ja aseta se taustalle
        self.canvas = Canvas(self, width=800, height=600, bg="SystemButtonFace")
        self.canvas.pack(fill=BOTH, expand=True)

        # Lataa taustakuva ja aseta se Canvas-olion taustalle
        self.background_image = PhotoImage(file="hylje.png")
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

        # Luo lokitus tekstiä varten
        self.log_text = ""
        self.log_text_id = self.canvas.create_text(
            5,
            0,
            text=self.log_text,
            font=("Segoe UI", 14),
            fill="black",
            anchor="nw",
            width=780,
        )

        # Luo nappulan Frame-olio
        button_frame = Frame(self.canvas)

        # Luo nappula
        self.button = Button(
            button_frame,
            text="Klikkaa, kun tiedostot ovat löytyneet",
            font=("Segoe UI", 16),
            command=self.button_clicked,
        )
        self.button.pack(pady=0)

        # Lisää nappula Canvasiin
        self.canvas.create_window(400, 580, anchor=S, window=button_frame)

        self.button.config(state=DISABLED)

    def start_watchdog(self):
        if self.watchdog is None:
            self.watchdog = Watchdog(paths=self.watch_paths, logfunc=self.log, gui=self)
            self.watchdog.start()
            self.log("Haetaan Titania & Hoitoajat -tiedostoja kansioista:")
            self.log(f"{self.watch_paths[0]} ja {self.watch_paths[1]}\n")

    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log("Watchdog stopped")
        else:
            self.log("Watchdog is not running")

    def log(self, message):
        self.log_text += f"\n{message}"
        self.canvas.itemconfig(self.log_text_id, text=self.log_text)

    def show_button(self):
        self.button.config(text="Aloita listojen luonti", state=NORMAL)

    def button_clicked(self):
        # Nappulan painalluksen käsittely
        self.log("Nappulaa painettiin!")


if __name__ == "__main__":
    GUI().mainloop()
