"""
Panel Principal (Dashboard) - Midrash
"""
import customtkinter as ctk
from tkinter import ttk, Menu
import os
from database.db import (
    obtener_pacientes, buscar_pacientes, eliminar_paciente,
    obtener_paciente_por_id, PYODBC_AVAILABLE
)
from gui.components.patient_form import PatientFormModal, ExpedienteModal

NAVY_BLUE = "#1A4FA0"
NAVY_DARK = "#0D3A7A"
NAVY_LIGHT = "#2E6BD6"
WHITE = "#FFFFFF"
GRAY_LIGHT = "#F5F5F5"
GRAY_MED = "#E0E0E0"
GRAY_TEXT = "#666666"
RED_LOGOUT = "#C62828"

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color=GRAY_LIGHT)
        self.root.minsize(900, 600)
        self._build_layout()
        self._load_patients()

    def _build_layout(self):
        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self.root, width=220, corner_radius=0, fg_color=NAVY_BLUE)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        if os.path.exists(logo_path):
            self.logo_image = ctk.CTkImage(
                light_image=__import__("PIL").Image.open(logo_path),
                dark_image=__import__("PIL").Image.open(logo_path),
                size=(40, 40)
            )
            self.logo_label = ctk.CTkLabel(self.sidebar, image=self.logo_image, text="")
            self.logo_label.pack(pady=(25, 0))

        ctk.CTkLabel(self.sidebar, text="MIDRASH",
            font=ctk.CTkFont(family="Roboto", size=22, weight="bold"),
            text_color=WHITE
        ).pack(pady=(8, 30))

        self.nav_pacientes = ctk.CTkFrame(self.sidebar, fg_color=NAVY_DARK, corner_radius=8, height=40)
        self.nav_pacientes.pack(fill="x", padx=15, pady=2)
        self.nav_pacientes.pack_propagate(False)
        ctk.CTkLabel(self.nav_pacientes, text="📋  Pacientes",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color=WHITE, anchor="w"
        ).pack(side="left", padx=15)

        ctk.CTkFrame(self.sidebar, fg_color=NAVY_BLUE, height=10).pack(fill="x")

        db_status = "🟢 Conectado" if PYODBC_AVAILABLE else "🔴 Sin conexión"
        ctk.CTkLabel(self.sidebar, text=f"BD: {db_status}",
            font=ctk.CTkFont(family="Roboto", size=11),
            text_color="#AAC4FF"
        ).pack(side="bottom", pady=(0, 20))

        self.logout_btn = ctk.CTkButton(self.sidebar, text="🚪  Cerrar Sesión",
            font=ctk.CTkFont(family="Roboto", size=13), height=38,
            corner_radius=8, fg_color=RED_LOGOUT, hover_color="#B71C1C",
            command=self._logout
        )
        self.logout_btn.pack(side="bottom", fill="x", padx=15, pady=(0, 10))

        # MAIN CONTENT
        self.main_area = ctk.CTkFrame(self.root, fg_color=GRAY_LIGHT, corner_radius=0)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Header
        self.header = ctk.CTkFrame(self.main_area, fg_color=WHITE, height=60, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        ctk.CTkLabel(self.header, text="Pacientes",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            text_color="#333333", anchor="w"
        ).pack(side="left", padx=25, pady=15)

        # NUEVO PACIENTE button - ONLY in header, NOT in sidebar
        self.new_btn = ctk.CTkButton(self.header, text="+ Nuevo Paciente",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            height=36, corner_radius=8, fg_color=NAVY_BLUE, hover_color=NAVY_DARK,
            command=self._new_patient
        )
        self.new_btn.pack(side="right", padx=25, pady=12)

        # Search bar
        self.search_frame = ctk.CTkFrame(self.main_area, fg_color=WHITE, height=50, corner_radius=0)
        self.search_frame.pack(fill="x", padx=20, pady=(15, 0))
        self.search_frame.pack_propagate(False)

        self.search_entry = ctk.CTkEntry(self.search_frame, height=36,
            font=ctk.CTkFont(family="Roboto", size=13), corner_radius=8,
            border_color=GRAY_MED, placeholder_text="Buscar paciente por nombre...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=7)
        self.search_entry.bind("<Return>", lambda e: self._search_patients())

        self.search_btn = ctk.CTkButton(self.search_frame, text="Buscar",
            font=ctk.CTkFont(family="Roboto", size=13), height=36, width=90,
            corner_radius=8, fg_color=NAVY_BLUE, hover_color=NAVY_DARK,
            command=self._search_patients)
        self.search_btn.pack(side="right", padx=(0, 15), pady=7)

        # Table
        self.table_frame = ctk.CTkFrame(self.main_area, fg_color=WHITE, corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background=WHITE, foreground="#333333",
            fieldbackground=WHITE, font=("Roboto", 12), rowheight=38)
        style.configure("Custom.Treeview.Heading", background=NAVY_BLUE,
            foreground=WHITE, font=("Roboto", 12, "bold"), relief="flat")
        style.map("Custom.Treeview.Heading", background=[("active", NAVY_LIGHT)])
        style.map("Custom.Treeview", background=[("selected", "#D6E4FF")])

        columns = ("id", "nombre", "apellido_p", "apellido_m", "sexo", "telefono", "estado")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings",
            style="Custom.Treeview", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido_p", text="Apellido P")
        self.tree.heading("apellido_m", text="Apellido M")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=150, anchor="w")
        self.tree.column("apellido_p", width=140, anchor="w")
        self.tree.column("apellido_m", width=140, anchor="w")
        self.tree.column("sexo", width=100, anchor="center")
        self.tree.column("telefono", width=130, anchor="center")
        self.tree.column("estado", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 5))

        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📋 Ver Expediente", command=self._view_patient)
        self.context_menu.add_command(label="🔴 Dar de Alta", command=self._discharge_patient)
        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Double-1>", lambda e: self._view_patient())

    def _load_patients(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        pacientes = obtener_pacientes()
        for p in pacientes:
            self.tree.insert("", "end", values=(
                p.get("id_paciente", ""), p.get("nombre", ""),
                p.get("apellido_paterno", ""), p.get("apellido_materno", ""),
                p.get("sexo", ""), p.get("telefono", ""), p.get("estado", "")
            ))

    def _search_patients(self):
        query = self.search_entry.get().strip()
        if not query:
            self._load_patients()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        pacientes = buscar_pacientes(query)
        for p in pacientes:
            self.tree.insert("", "end", values=(
                p.get("id_paciente", ""), p.get("nombre", ""),
                p.get("apellido_paterno", ""), p.get("apellido_materno", ""),
                p.get("sexo", ""), p.get("telefono", ""), p.get("estado", "")
            ))

    def _new_patient(self):
        PatientFormModal(self.root, callback=self._load_patients)

    def _show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def _view_patient(self):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        patient_id = item["values"][0]
        paciente = obtener_paciente_por_id(patient_id)
        if paciente:
            ExpedienteModal(self.root, paciente, callback=self._load_patients)

    def _discharge_patient(self):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        patient_id = item["values"][0]
        estado = item["values"][-1]
        if estado == "Alta":
            import tkinter.messagebox as mb
            mb.showinfo("Info", "El paciente ya fue dado de alta.")
            return
        import tkinter.messagebox as mb
        if mb.askyesno("Confirmar", "¿Dar de alta a este paciente?"):
            eliminar_paciente(patient_id)
            self._load_patients()

    def _logout(self):
        self.root.destroy()
        from gui.login_gui import LoginWindow
        login = ctk.CTk()
        login.title("Midrash - Inicio de Sesión")
        login.geometry("400x550")
        login.resizable(False, False)
        login.update_idletasks()
        x = (login.winfo_screenwidth() // 2) - (400 // 2)
        y = (login.winfo_screenheight() // 2) - (550 // 2)
        login.geometry(f"400x550+{x}+{y}")
        LoginWindow(login)
        login.mainloop()
