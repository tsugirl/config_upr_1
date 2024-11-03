import tkinter as tk
import configparser

class ShellEmulator:
    def __init__(self, master):
        self.master = master
        self.master.title("OS Shell Emulator")
        
        # Load config
        self.load_config()
        
        # Create simple GUI
        self.output_text = tk.Text(self.master, height=20, width=80, bg="black", fg="white")
        self.output_text.pack()
        
        self.input_field = tk.Entry(self.master, width=80)
        self.input_field.pack()
        self.input_field.bind("<Return>", self.execute_command)

    def load_config(self):
        # Load configuration file
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def execute_command(self, event):
        command = self.input_field.get()
        self.output_text.insert(tk.END, f"$ {command}\n")
        self.input_field.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    emulator = ShellEmulator(root)
    root.mainloop()
