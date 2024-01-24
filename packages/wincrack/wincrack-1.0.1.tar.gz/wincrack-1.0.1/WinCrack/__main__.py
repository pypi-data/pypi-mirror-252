from pystyle import Write, Colors
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import subprocess
import ctypes
import sys
import webbrowser

os.system('clear' if os.name == 'posix' else 'cls')

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

class WinRarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("WinRar Cracker by.kami on discord")

        self.winrar_path = tk.StringVar(value="C:\\Program Files\\WinRAR\\WinRAR.exe")

        tk.Label(master, text="WinRar path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(master, textvariable=self.winrar_path, width=50).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Button(master, text="Browse", command=self.select_winrar_path).grid(row=0, column=2, padx=10, pady=10, sticky="w")

        tk.Button(master, text="Crack WinRar", command=self.move_file).grid(row=1, column=0, columnspan=3, pady=10)
        tk.Button(master, text="Open WinRar", command=self.open_winrar).grid(row=3, column=0, columnspan=3, pady=10)

        self.status_label = tk.Label(master, text="", fg="black")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def select_winrar_path(self):
        path = filedialog.askopenfilename(filetypes=[("KamiRAR", "*.exe")])
        if path:
            self.winrar_path.set(path)

    def move_file(self):
        file_content = """RAR registration data
Für Abonnenten von TheReatekker
Unlimited Company License
UID=4e6c1650cdf8ad615ffa
64122122505ffaae408f7ad66b8bb746f58d6fa12007f52f099ed4
6c1726e2317c46bb430560fce6cb5ffde62890079861be57638717
7131ced835ed65cc743d9777f2ea71a8e32c7e593cf66794343565
b41bcf56929486b8bcdac33d50ecf77399604752331f0c57e362ab
443f1c64352b57668957fe62d07b434a2813addb4dbd3642364647
103788926272ccc3fb675e8b657f8b66c671e01419e9e361603899
c5a2af5001dd92308cfe644830edafe109c0e6cdd5864023283383"""

        file_path = "rarreg.key"
        with open(file_path, "w") as file:
            file.write(file_content)

        self.close_winrar()

        destination_path = os.path.join(os.path.dirname(self.winrar_path.get()), "rarreg.key")
        shutil.move(file_path, destination_path)
        Write.Print(f"WinRar is now cracked.", Colors.red_to_green)

    def close_winrar(self):
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'WinRAR.exe'])
            os.system('clear' if os.name == 'posix' else 'cls')
            self.status_label.config(text="WinRAR has been successfully cracked.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Cannot find WinRar.exe.", fg="red")
            Write.Print(f"Error while closing WinRar : {e}", Colors.red_to_green)

    def open_winrar(self):
        try:
            subprocess.Popen(self.winrar_path.get())
        except Exception as e:
            self.status_label.config(text=f"Cannot open WinRar.", fg="red")
            Write.Print(f"Error while opening WinRar : {e}", Colors.red_to_green)

    def on_closing(self):
        self.close_winrar()
        self.open_link()
        sys.exit()

    def open_link(self):
        webbrowser.open("https://guns.lol/kami")

if __name__ == "__main__":
    run_as_admin()
    root = tk.Tk()
    app = WinRarApp(root)
    root.mainloop()
    WinRarApp()
