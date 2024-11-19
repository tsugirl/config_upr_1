import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
import json
import datetime

# чтение конфиг. файла
def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    vfs_path = config['paths']['virtual_filesystem']
    log_path = config['paths']['log_file']
    script_path = config['paths']['start_script']
    return vfs_path, log_path, script_path

# логгирование
def log_action(log_path, action):
    log_entry = {"action": action, "timestamp": str(datetime.datetime.now())}
    try:
        with open(log_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

# получаю список директорий и файлов
def load_virtual_filesystem(vfs_path):
    with zipfile.ZipFile(vfs_path, 'r') as z:
        return z.namelist()

# обработка команд тут
class ShellEmulator:
    def __init__(self, vfs):
        self.current_dir = "" 
        self.vfs = vfs

    def ls(self):
        files_in_dir = [
            f[len(self.current_dir):].split('/')[0]
            for f in self.vfs
            if f.startswith(self.current_dir) and len(f) > len(self.current_dir)
        ]
        return "\n" + "\n".join(sorted(set(files_in_dir))) or "No files found"

    def cd(self, path):
        if path == "":
            self.current_dir = ""
            return "\nReturned to root directory"
        elif path == "..":
            if self.current_dir:
                self.current_dir = "/".join(self.current_dir.strip("/").split("/")[:-1]) + "/"
                if self.current_dir == "/":
                    self.current_dir = ""
            return f"\nMoved to parent directory"
        else:
            potential_path = os.path.join(self.current_dir, path).replace("\\", "/") + "/"
            if any(f.startswith(potential_path) for f in self.vfs):
                self.current_dir = potential_path
                return f"\nChanged directory to {path}"
            else:
                return "\nDirectory not found"

    def date(self):
        return "\n" + str(datetime.datetime.now())

    def echo(self, message):
        return "\n" + message

    def chown(self, args): 
        return f"\nChanged ownership of {args[0]}"

# GUI
class ShellEmulatorApp(tk.Tk):
    def __init__(self, config_path):
        super().__init__()
        self.title("Shell Emulator")
        self.geometry("600x400")
        
        self.vfs_path, self.log_path, self.script_path = load_config(config_path)
        
        self.virtual_filesystem = load_virtual_filesystem(self.vfs_path)
        self.shell = ShellEmulator(self.virtual_filesystem)

        self.output = tk.Text(self, bg="black", fg="white", insertbackground="white", height=20, width=80)
        self.output.pack(expand=True, fill='both')

        self.output.bind("<Return>", self.run_command)

        self.output.insert(tk.END, "Welcome to Shell Emulator\n")
        self.output.insert(tk.END, "$ ")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_command(self, event):
        command_text = self.get_last_command()

        self.output.delete("insert-1c", tk.END)

        parts = command_text.split()
        cmd = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == 'ls':
            result = self.shell.ls()
        elif cmd == 'cd':
            result = self.shell.cd(args[0] if args else "")
        elif cmd == 'date':
            result = self.shell.date()
        elif cmd == 'echo':
            result = self.shell.echo(" ".join(args))
        elif cmd == 'chown':
            result = self.shell.chown(args)
        elif cmd == 'exit':
            self.on_close()
            return
        else:
            result = "\nUnknown command"

        # вывод команд
        self.output.insert(tk.END, f"{result}\n")
        self.output.insert(tk.END, "$ ")  
        self.output.see(tk.END)  # автоскролл в конец
        return "break"

    def get_last_command(self):
        input_text = self.output.get("1.0", tk.END)
        last_line = input_text.strip().split("\n")[-1]
        return last_line[2:]

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    config_file = filedialog.askopenfilename(title="Select Config File", filetypes=[("INI files", "*.ini")])
    if config_file:
        app = ShellEmulatorApp(config_file)
        app.mainloop()
    else:
        messagebox.showerror("Error", "No config file selected!")
