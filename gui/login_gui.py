"""
Ventana de Inicio de Sesión - Midrash
"""
import customtkinter as ctk
import os

NAVY_BLUE = "#1A4FA0"
NAVY_DARK = "#143D80"
NAVY_LIGHT = "#2E6BD6"
WHITE = "#FFFFFF"
GRAY_LIGHT = "#F0F0F0"
RED_ERROR = "#D32F2F"

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color=WHITE)

        self.container = ctk.CTkFrame(root, fg_color=WHITE, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        self.center_frame = ctk.CTkFrame(self.container, fg_color=WHITE, corner_radius=0)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        if os.path.exists(logo_path):
            self.logo_image = ctk.CTkImage(
                light_image=__import__("PIL").Image.open(logo_path),
                dark_image=__import__("PIL").Image.open(logo_path),
                size=(60, 60)
            )
            self.logo_label = ctk.CTkLabel(self.center_frame, image=self.logo_image, text="")
            self.logo_label.pack(pady=(0, 5))

        self.title_label = ctk.CTkLabel(
            self.center_frame, text="MIDRASH",
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
            text_color=NAVY_BLUE
        )
        self.title_label.pack(pady=(5, 2))

        self.subtitle_label = ctk.CTkLabel(
            self.center_frame, text="Sistema de Gestión de Pacientes",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="#666666"
        )
        self.subtitle_label.pack(pady=(0, 30))

        self.user_label = ctk.CTkLabel(
            self.center_frame, text="Usuario",
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w"
        )
        self.user_label.pack(fill="x", padx=40, pady=(0, 4))

        self.user_entry = ctk.CTkEntry(
            self.center_frame, height=42,
            font=ctk.CTkFont(family="Roboto", size=14),
            corner_radius=8, border_color="#CCCCCC",
            placeholder_text="Ingresa tu usuario"
        )
        self.user_entry.pack(fill="x", padx=40, pady=(0, 15))

        self.pass_label = ctk.CTkLabel(
            self.center_frame, text="Contraseña",
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w"
        )
        self.pass_label.pack(fill="x", padx=40, pady=(0, 4))

        self.pass_entry = ctk.CTkEntry(
            self.center_frame, height=42,
            font=ctk.CTkFont(family="Roboto", size=14),
            corner_radius=8, border_color="#CCCCCC",
            show="*", placeholder_text="Ingresa tu contraseña"
        )
        self.pass_entry.pack(fill="x", padx=40, pady=(0, 10))

        self.error_label = ctk.CTkLabel(
            self.center_frame, text="",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color=RED_ERROR
        )
        self.error_label.pack(pady=(0, 5))

        self.login_btn = ctk.CTkButton(
            self.center_frame, text="Iniciar Sesión",
            font=ctk.CTkFont(family="Roboto", size=15, weight="bold"),
            height=44, corner_radius=8,
            fg_color=NAVY_BLUE, hover_color=NAVY_DARK,
            command=self._login
        )
        self.login_btn.pack(fill="x", padx=40, pady=(5, 0))

        self.user_entry.bind("<Return>", lambda e: self.pass_entry.focus())
        self.pass_entry.bind("<Return>", lambda e: self._login())

    def _login(self):
        user = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not user or not password:
            self.error_label.configure(text="Por favor, completa todos los campos")
            return
        if user == "admin" and password == "1234":
            self.error_label.configure(text="")
            self._open_dashboard()
        else:
            self.error_label.configure(text="Usuario o contraseña incorrectos")

    def _open_dashboard(self):
        self.root.destroy()
        from gui.dashboard_gui import DashboardApp
        dashboard = ctk.CTk()
        dashboard.title("Midrash - Panel de Pacientes")
        dashboard.state("zoomed")
        app = DashboardApp(dashboard)
        dashboard.mainloop()
