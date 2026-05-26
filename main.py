"""
Midrash - Sistema de Gestión de Pacientes
Centro de Rehabilitación
"""
import sys
import os

if sys.platform.startswith("linux"):
    os.environ["GDK_BACKEND"] = "x11"

import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

from gui.login_gui import LoginWindow

def main():
    try:
        app = ctk.CTk()
        app.title("Midrash - Inicio de Sesión")
        app.geometry("400x550")
        app.resizable(False, False)
        app.update_idletasks()
        x = (app.winfo_screenwidth() // 2) - (400 // 2)
        y = (app.winfo_screenheight() // 2) - (550 // 2)
        app.geometry(f"400x550+{x}+{y}")
        login = LoginWindow(app)
        app.mainloop()
    except Exception as e:
        import tkinter.messagebox as mb
        try:
            mb.showerror("Error", f"Ocurrió un error:\n{e}")
        except:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
