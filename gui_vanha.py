"""
Merikarhu
Version: 0.1
Creator: Jaakko Haavisto, takutta@gmail.com
Date: June, 2023
"""

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
import os, threading, logging, functools
from sys import argv  # arguments for launching file
from time import sleep  # for watchdog
from re import findall  # regex
from pathlib import Path  # path helper
import glob  # pathname patterns
from datetime import datetime, timedelta


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    # create the logging file handler (scriptname.log)
    fh = logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + ".log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # add consolehandler (stdout) to logger object
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def exception(error_text):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = f"{error_text}. Function: {func.__name__}"
                logger.exception(err)

            # re-raise the exception
            raise

        return wrapper

    return decorator


class TxtEventHandler(RegexMatchingEventHandler):
    """Etsitään uusia txt tiedostoja polusta C:\*.txt"""

    def __init__(self, src_path, regex):
        src_path = src_path.replace("\\", "\\\\")
        # self.regex = rf"^{re.escape(src_path)}\\.+\.txt$"
        # self.REGEX = [rf"^{src_path}.*\.txt$"]
        self.REGEX = [rf"^{src_path}{regex}$"]
        super().__init__(self.REGEX)

    def on_created(self, event):
        if event.is_directory:
            return
        # self.process(event)

        if any(event.src_path.endswith(ext) for ext in [".txt", ".info"]):
            if event.src_path.endswith(".txt"):
                self.process_txt(event.src_path)
            elif event.src_path.endswith(".info"):
                self.process_info(event.src_path)

    def process(self, event):
        main(event.src_path)
        log("debug", "Etsitään Titanian txt-tiedostoja")

    def process_txt(self, path):
        log("debug", "Txt tiedosto havaittu: %s", path)
        # prosessoi_txt(path)

    def process_info(self, path):
        log("debug", "Info tiedosto havaittu: %s", path)
        # prosessoi_info(path)


class TxtWatcher:
    """watchdog luokka uusien tiedostojen tarkkailua varten"""

    def __init__(self, src_path, regex):
        self.__src_path = src_path
        self.__event_handler = TxtEventHandler(src_path, regex)
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler, self.__src_path, recursive=True
        )


def main(source_path):
    """
    prosessoidaan txt
    """
    try:
        paths = get_paths(source_path)
        log("info", "Löydetty uusi txt: %s", paths["src"])
    except:
        pass


@exception("Virhe lokituksessa")
def log(level, message, *args):
    log_function = getattr(logger, level, None)
    log_function(message, *args)


@exception("Ongelmia tiedostojen löytämisessä")
def process_txts(src_path):
    p = Path(src_path)
    # Käydään läpi kaikki alikansiot
    for folder in [
        f / "in" for f in p.iterdir() if f.is_dir() and os.path.exists(f / "in")
    ]:
        # prosessoidaan kaikki txt-tiedostot
        for txt in sorted(folder.glob("*.txt")):
            main(txt)


@exception("Problem with creating paths")
def get_paths(source_path: str):
    """return dict of paths: source, destination, template, archive and error"""

    path = Path(source_path)
    dict = {}

    template_name = path.parents[1].name
    dict["src"] = path.absolute()

    dest_folder = path.parents[1].absolute() / "out"
    dict["dest_folder"] = dest_folder
    dest_name = path.stem
    dict["dest"] = Path(dest_folder, dest_name).with_suffix(".xml")

    log("debug", "Paths dict created")
    return dict


@exception("Can't move files to /in")
def publish(template: str, paths: dict):
    """write xml to /out"""

    with open(paths["dest"], "w") as file:
        file.write("".join(template))
    log("info", "XML has been published at: %s", paths["dest"])


if __name__ == "__main__":
    # start logging
    logger = create_logger()

    # Use current folder if argument not used
    txt_path = r"C:\Users\pampi\testi"
    info_path = r"C:\Users\pampi\testi2"
    # before starting watcher let's process all found JSONs first
    # process_txts(src_path)

    log("debug", "Etsitään tiedostoja")

    # file watcher launch
    # TxtWatcher(src_path).run()

    # create and start the first watcher with the desired regex
    watcher1 = TxtWatcher(txt_path, r".*\.txt")
    watcher1_thread = threading.Thread(target=watcher1.run)
    watcher1_thread.start()

    # create and start the second watcher with the desired regex
    watcher2 = TxtWatcher(info_path, r".*\.info")
    watcher2_thread = threading.Thread(target=watcher2.run)
    watcher2_thread.start()

    # wait for both watchers to finish
    watcher1_thread.join()
    watcher2_thread.join()
