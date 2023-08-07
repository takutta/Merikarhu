from tkinter import *
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os, sys, shutil, time
import titania as ti
import excel as ex
import pandas as pd
from tarvetaulukko import luo_tarvetaulukko
from io import StringIO


class GUI(Tk):
    def __init__(self):
        super().__init__()
        # watchdog
        self.watchdog = None
        self.watch_paths = [
            os.path.join(os.path.expanduser("~"), "merikarhu", "input"),
            r"c:\tyko2000\work",
        ]
        self.update_watch_paths()
        self.start_watchdog()

        self.title("Merikarhu")
        self.resizable(False, False)
        self.iconbitmap("merikarhu.ico")
        self.create_widgets()
        self.titaniat = []
        self.pvm_titania = ""
        self.peukku_id = None
        self.poista_txt()
        self.data = None

        # ruudun keskitys
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = 0
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        self.canvas = Canvas(self, width=800, height=600, bg="SystemButtonFace")
        self.canvas.pack(fill=BOTH, expand=True)

        self.background_image = PhotoImage(file="hylje.png")
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

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
        self.log("Haetaan Titania & Hoitoajat -tiedostoja kansioista:")

        button_frame = Frame(self.canvas)
        self.button = Button(
            button_frame,
            text="Klikkaa, kun tiedostot ovat löytyneet",
            font=("Segoe UI", 16),
            command=self.button_clicked,
        )
        self.button.pack(pady=0)
        self.canvas.create_window(400, 580, anchor=S, window=button_frame)
        self.button.config(state=DISABLED)

        for path in self.watch_paths:
            self.log(path)

    def log(self, message):
        self.log_text += f"\n{message}"
        self.canvas.itemconfig(self.log_text_id, text=self.log_text)

    def lisaa_peukku(self):
        img = PhotoImage(file="peukku.png")
        self.peukku_id = self.canvas.create_image(540, 240, anchor="nw", image=img)
        self.peukku = img

    def poista_peukku(self):
        if self.peukku_id is not None:
            self.canvas.delete(self.peukku_id)
            self.peukku_id = None

    def update_watch_paths(self):
        """Poista polut, jotka eivät ole olemassa"""
        self.watch_paths = [path for path in self.watch_paths if os.path.exists(path)]

    def start_watchdog(self):
        if self.watchdog is None:
            txt_maara = int(sys.argv[1]) if len(sys.argv) > 1 else 2
            self.watchdog = Watchdog(
                paths=self.watch_paths, logfunc=self.log, gui=self, txt_maara=txt_maara
            )
            self.watchdog.start()

    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log("Watchdog pysäytetty")
        else:
            self.log("Watchdog ei ole käynnissä")

    def receive_data(self, titaniat, pvm_titania):
        self.titaniat = titaniat
        self.pvm_titania = pvm_titania

    def poista_txt(self):
        [
            os.remove(os.path.join(r"c:\tyko2000\work", tiedostonimi))
            for tiedostonimi in os.listdir(r"c:\tyko2000\work")
            if os.path.isfile(os.path.join(r"c:\tyko2000\work", tiedostonimi))
            and tiedostonimi.endswith(".txt")
        ]

    def process_data(self):
        # titanioiden yhdistäminen
        if len(self.titaniat) > 1:
            titania_tt = ti.yhdista_tyontekijat(self.titaniat)
        else:
            titania_tt = self.titaniat[0]

        # excel-jsonin tallentaminen
        excel_data = ex.lataa_json(self.watchdog.excel_path)
        data = ex.tt_asetukset_synkka(titania_tt, excel_data)
        output_filepath = os.path.join(
            os.path.expanduser("~"), "merikarhu", "output", "merikarhu_output.json"
        )
        self.data = data
        ex.excel_export(self.data, output_filepath)

    def show_button(self):
        self.button.config(text="Aloita listojen luonti", state=NORMAL)

    def button_clicked(self):
        luo_tarvetaulukko(self.data, self.pvm_titania)


class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, paths=None, patterns="*", logfunc=print, gui=None, txt_maara=1):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.paths = paths or []
        self.setup_watchers()
        self.log = logfunc
        self.gui = gui
        self.txt_loytyi = 0
        self.txt_maara = txt_maara
        self.excel_loytyi = False
        self.excel_path = ""
        self.titaniat = []
        self.pvm_titania = ""

    def setup_watchers(self):
        # Poista polut, jotka eivät ole olemassa
        self.paths = [path for path in self.paths if os.path.exists(path)]
        for path in self.paths:
            self.schedule(self, path=path, recursive=False)

    def on_created(self, event):
        # Tiedoston luomistapahtuma
        self.process_file(event.src_path)

    def process_file(self, file_path):
        if file_path.endswith(".txt"):  # titania
            self.process_text_file(file_path)
        elif file_path.endswith(".json"):  # excel
            self.process_excel_file(file_path)

    def process_text_file(self, file_path):
        # Tiedostotyypin mukainen käsittely
        if self.txt_loytyi < self.txt_maara:
            self.txt_loytyi += 1
            self.log(f"Titania {self.txt_loytyi}/{self.txt_maara} löytyi: {file_path}")

            self.get_titania_data(file_path)
            self.check_files_and_show_button()

        elif self.txt_loytyi == self.txt_maara:
            self.txt_loytyi = 1
            self.log(
                f"Titania {self.txt_loytyi}/{self.txt_maara} korvattu: {file_path}"
            )
            self.titaniat = []
            self.get_titania_data(file_path)
            self.check_files_and_show_button()

    def get_titania_data(self, file_path):
        """kerätään titania data ja poistetaan tiedosto"""
        time.sleep(2)
        df, pvm_titania = ti.titania_import(file_path)
        self.pvm_titania = pvm_titania
        tt = ti.df_to_json(df)
        time.sleep(2)
        os.remove(file_path)
        self.titaniat.append(tt)

    def process_excel_file(self, file_path):
        # Tiedostotyypin mukainen käsittely
        if self.excel_loytyi:
            self.log(f"Uusi Excel tiedosto korvattu: {file_path}")
            self.excel_path = file_path
            pass
        else:
            self.excel_loytyi = True
            self.log(f"Excel löytyi: {file_path}")
            self.excel_path = file_path
            self.check_files_and_show_button()

    def check_files_and_show_button(self):
        if self.txt_loytyi == self.txt_maara and self.excel_loytyi:
            if self.txt_maara == 1:
                self.log("Molemmat tiedostot löytyivät.")
            else:
                self.log("Kaikki tiedostot löytyivät.")
            self.gui.receive_data(self.titaniat, self.pvm_titania)
            self.gui.process_data()
            self.gui.show_button()
            self.gui.lisaa_peukku()

        else:
            self.gui.button.config(state=DISABLED)
            self.gui.button.config(text="Klikkaa, kun tiedostot ovat löytyneet")
            self.gui.poista_peukku()


if __name__ == "__main__":
    GUI().mainloop()
