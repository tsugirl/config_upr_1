import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
import json
import datetime

# щагрузка конфигурационного файла
def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    vfs_path = config['paths']['virtual_filesystem']
    log_path = config['paths']['log_file']
    return vfs_path, log_path

# логгирование команд в JSON
def log_action(log_path, action):
    log_entry = {"action": action, "timestamp": str(datetime.datetime.now())}
    try:
        with open(log_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

# получение содержимого zip-архива
def load_virtual_filesystem(vfs_path):
    with zipfile.ZipFile(vfs_path, 'r') as z:
        return z.namelist()

# получение команд 
def handle_command(cmd, log_path, vfs):
    if cmd == 'ls':
        log_action(log_path, 'ls')
        return "\n".join(vfs)
    else:
        return "Unknown command"

# GUI
class ShellEmulatorApp(tk.Tk):
    def __init__(self, config_path):
        super().__init__()
        self.title("Shell Emulator")
        self.geometry("600x400")
        
        self.vfs_path, self.log_path = load_config(config_path)
        
        self.virtual_filesystem = load_virtual_filesystem(self.vfs_path)

        self.output = tk.Text(self, bg="black", fg="white", insertbackground="white", height=20, width=80)
        self.output.pack(expand=True, fill='both')

        self.output.bind("<Return>", self.run_command)

        self.output.insert(tk.END, "Welcome to Shell Emulator\n")
        self.output.insert(tk.END, "$ ") 

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_command(self, event):
        command_text = self.get_last_command()

        self.output.delete("insert-1c", tk.END)


        if command_text.strip() == "ls":
            result = handle_command("ls", self.log_path, self.virtual_filesystem)
        else:
            result = "Unknown command"

        self.output.insert(tk.END, f"\n{result}\n$ ")  
        self.output.see(tk.END)  
        return "break"  

    def get_last_command(self):
        input_text = self.output.get("1.0", tk.END)
        last_line = input_text.strip().split("\n")[-1]
        return last_line[2:] + "  "  

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    config_file = filedialog.askopenfilename(title="Select Config File", filetypes=[("INI files", "*.ini")])
    if config_file:
        app = ShellEmulatorApp(config_file)
        app.mainloop()
    else:
        messagebox.showerror("Error", "No config file selected!")
