"""
Formulario de Paciente, Expediente y Reinternación - Midrash
Usa CTkTabview en vez de CTkScrollableFrame para evitar problemas de scroll
"""
import customtkinter as ctk
from database.db import insertar_paciente, actualizar_paciente, reinternar_paciente

NAVY_BLUE = "#1A4FA0"
NAVY_DARK = "#0D3A7A"
NAVY_LIGHT = "#2E6BD6"
WHITE = "#FFFFFF"
GRAY_LIGHT = "#F5F5F5"
GRAY_MED = "#E0E0E0"
GRAY_TEXT = "#666666"
GREEN = "#2E7D32"
RED = "#C62828"
ORANGE = "#E65100"


class PatientFormModal:
    """Modal para registrar un nuevo paciente - con pestañas (sin scroll)"""

    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Nuevo Paciente")
        self.window.geometry("720x680")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (720 // 2)
        y = (self.window.winfo_screenheight() // 2) - (680 // 2)
        self.window.geometry(f"720x680+{x}+{y}")

        self._build_header()
        self._build_tabs()
        self._build_footer()
        self.window.focus_force()

    def _build_header(self):
        header = ctk.CTkFrame(self.window, fg_color=NAVY_BLUE, height=50, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="➕ Nuevo Paciente",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color=WHITE).pack(side="left", padx=20, pady=12)

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self.window,
            fg_color=WHITE,
            segmented_button_fg_color=GRAY_LIGHT,
            segmented_button_selected_color=NAVY_BLUE,
            segmented_button_unselected_color=GRAY_MED,
            segmented_button_selected_hover_color=NAVY_DARK,
            segmented_button_unselected_hover_color="#D0D0D0",
            text_color="white",
            text_color_disabled=GRAY_TEXT)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=10)

        # --- Tab 1: Datos Personales ---
        tab1 = self.tabview.add("Personales")
        self.entry_nombre = self._make_entry(tab1, "Nombre(s) *", "Nombre del paciente")
        self.entry_apellido_p = self._make_entry(tab1, "Apellido Paterno *", "Apellido paterno")
        self.entry_apellido_m = self._make_entry(tab1, "Apellido Materno", "Apellido materno")

        ctk.CTkLabel(tab1, text="Sexo *",
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=20, pady=(8, 2))
        self.sexo_menu = ctk.CTkOptionMenu(tab1, values=["Masculino", "Femenino"],
            height=38, font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        self.sexo_menu.set("Seleccionar...")
        self.sexo_menu.pack(fill="x", padx=20, pady=(0, 4))

        self.entry_telefono = self._make_entry(tab1, "Teléfono", "Teléfono de contacto")
        self.entry_direccion = self._make_entry(tab1, "Dirección", "Dirección del paciente")
        self.dia_nac, self.mes_nac, self.anio_nac = self._make_date_row(tab1, "Fecha de Nacimiento")

        # --- Tab 2: Familiar ---
        tab2 = self.tabview.add("Familiar")
        self.entry_fam_nombre = self._make_entry(tab2, "Nombre del Familiar *", "Nombre completo")
        self.entry_fam_parentesco = self._make_entry(tab2, "Parentesco *", "Ej: Madre, Padre, Hermano/a")
        self.entry_fam_telefono = self._make_entry(tab2, "Teléfono del Familiar *", "Teléfono de contacto")
        self.entry_fam_direccion = self._make_entry(tab2, "Dirección del Familiar", "Dirección")

        # --- Tab 3: Encargado ---
        tab3 = self.tabview.add("Encargado")
        self.entry_enc_nombre = self._make_entry(tab3, "Nombre del Encargado *", "Nombre completo")
        self.entry_enc_cargo = self._make_entry(tab3, "Cargo *", "Ej: Médico, Psicólogo")
        self.entry_enc_telefono = self._make_entry(tab3, "Teléfono del Encargado *", "Teléfono de contacto")

        # --- Tab 4: Ingreso ---
        tab4 = self.tabview.add("Ingreso")
        self.dia_ing, self.mes_ing, self.anio_ing = self._make_date_row(tab4, "Fecha de Ingreso *")
        self.entry_motivo = self._make_entry(tab4, "Motivo de Ingreso *", "Descripción del motivo")
        self.entry_observaciones = self._make_entry(tab4, "Observaciones", "Observaciones adicionales")

    def _build_footer(self):
        footer = ctk.CTkFrame(self.window, fg_color=WHITE, height=55, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkButton(footer, text="Cancelar",
            font=ctk.CTkFont(family="Roboto", size=13), height=38, width=120,
            corner_radius=8, fg_color=GRAY_MED, text_color="#333333",
            hover_color="#CCCCCC", command=self.window.destroy).pack(side="left", padx=20, pady=8)

        ctk.CTkButton(footer, text="💾 Guardar Paciente",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            height=38, width=170, corner_radius=8,
            fg_color=GREEN, hover_color="#1B5E20",
            command=self._save_patient).pack(side="right", padx=20, pady=8)

    # ── Helpers ──────────────────────────────────────
    def _make_entry(self, parent, label_text, placeholder="", prefill=""):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=20, pady=(8, 2))
        entry = ctk.CTkEntry(parent, height=38,
            font=ctk.CTkFont(family="Roboto", size=13),
            corner_radius=8, border_color=GRAY_MED,
            placeholder_text=placeholder)
        entry.pack(fill="x", padx=20, pady=(0, 4))
        if prefill:
            entry.insert(0, str(prefill))
        return entry

    def _make_date_row(self, parent, label_text, prefill_d=None, prefill_m=None, prefill_a=None):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=20, pady=(8, 2))
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=(0, 4))

        dia_vals = [str(i) for i in range(1, 32)]
        dia_menu = ctk.CTkOptionMenu(date_frame, values=dia_vals, width=80, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        dia_menu.set(str(prefill_d) if prefill_d else "Día")
        dia_menu.pack(side="left", padx=(0, 5))

        mes_vals = [str(i) for i in range(1, 13)]
        mes_menu = ctk.CTkOptionMenu(date_frame, values=mes_vals, width=80, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        mes_menu.set(str(prefill_m) if prefill_m else "Mes")
        mes_menu.pack(side="left", padx=5)

        anio_vals = [str(i) for i in range(2026, 1919, -1)]
        anio_menu = ctk.CTkOptionMenu(date_frame, values=anio_vals, width=100, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        anio_menu.set(str(prefill_a) if prefill_a else "Año")
        anio_menu.pack(side="left", padx=5)

        return dia_menu, mes_menu, anio_menu

    def _get_date_value(self, dia_menu, mes_menu, anio_menu):
        d, m, a = dia_menu.get(), mes_menu.get(), anio_menu.get()
        if d.startswith("Día") or m.startswith("Mes") or a.startswith("Año"):
            return None, None, None
        return int(d), int(m), int(a)

    def _save_patient(self):
        dia_nac, mes_nac, anio_nac = self._get_date_value(self.dia_nac, self.mes_nac, self.anio_nac)
        dia_ing, mes_ing, anio_ing = self._get_date_value(self.dia_ing, self.mes_ing, self.anio_ing)
        sexo = self.sexo_menu.get()
        if sexo == "Seleccionar...":
            sexo = None
        data = {
            "nombre": self.entry_nombre.get().strip(),
            "apellido_paterno": self.entry_apellido_p.get().strip(),
            "apellido_materno": self.entry_apellido_m.get().strip(),
            "sexo": sexo,
            "telefono": self.entry_telefono.get().strip(),
            "direccion": self.entry_direccion.get().strip(),
            "dia_nacimiento": dia_nac, "mes_nacimiento": mes_nac, "anio_nacimiento": anio_nac,
            "familiar_nombre": self.entry_fam_nombre.get().strip(),
            "familiar_parentesco": self.entry_fam_parentesco.get().strip(),
            "familiar_telefono": self.entry_fam_telefono.get().strip(),
            "familiar_direccion": self.entry_fam_direccion.get().strip(),
            "encargado_nombre": self.entry_enc_nombre.get().strip(),
            "encargado_cargo": self.entry_enc_cargo.get().strip(),
            "encargado_telefono": self.entry_enc_telefono.get().strip(),
            "dia_ingreso": dia_ing, "mes_ingreso": mes_ing, "anio_ingreso": anio_ing,
            "motivo_ingreso": self.entry_motivo.get().strip(),
            "observaciones": self.entry_observaciones.get().strip(),
        }
        import tkinter.messagebox as mb
        if not data["nombre"] or not data["apellido_paterno"]:
            mb.showwarning("Campos requeridos", "Nombre y Apellido Paterno son obligatorios."); return
        if not data["familiar_nombre"] or not data["familiar_parentesco"] or not data["familiar_telefono"]:
            mb.showwarning("Campos requeridos", "Los datos del familiar son obligatorios."); return
        if not data["encargado_nombre"] or not data["encargado_cargo"] or not data["encargado_telefono"]:
            mb.showwarning("Campos requeridos", "Los datos del personal encargado son obligatorios."); return
        if not data["dia_ingreso"] or not data["mes_ingreso"] or not data["anio_ingreso"]:
            mb.showwarning("Campos requeridos", "La fecha de ingreso es obligatoria."); return
        if not data["motivo_ingreso"]:
            mb.showwarning("Campos requeridos", "El motivo de ingreso es obligatorio."); return
        success = insertar_paciente(data)
        if success:
            mb.showinfo("Éxito", "Paciente registrado correctamente.")
            self.window.destroy()
            if self.callback:
                self.callback()
        else:
            mb.showerror("Error", "No se pudo registrar el paciente. Verifique la conexión a la base de datos.")


# ============================================================
# EXPEDIENTE MODAL - Ver y Editar con pestañas (sin scroll)
# ============================================================
class ExpedienteModal:
    """Modal para ver y editar el expediente completo de un paciente.
    Usa CTkTabview para evitar problemas de scroll en Windows."""

    def __init__(self, parent, paciente, callback=None):
        self.parent = parent
        self.paciente = paciente
        self.callback = callback
        self.editing = False

        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Expediente - {paciente.get('nombre', '')} {paciente.get('apellido_paterno', '')}")
        self.window.geometry("720x700")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (720 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"720x700+{x}+{y}")

        self._build_header()
        self._build_view_mode()
        self.window.focus_force()

    def _build_header(self):
        self.header = ctk.CTkFrame(self.window, fg_color=NAVY_BLUE, height=50, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        nombre = f"{self.paciente.get('nombre', '')} {self.paciente.get('apellido_paterno', '')} {self.paciente.get('apellido_materno', '')}"
        self.header_title = ctk.CTkLabel(self.header, text=f"📋 Expediente: {nombre}",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color=WHITE)
        self.header_title.pack(side="left", padx=20, pady=12)

        # Botón cerrar siempre visible
        self.close_btn = ctk.CTkButton(self.header, text="✕ Cerrar",
            font=ctk.CTkFont(family="Roboto", size=12), height=32, width=80,
            corner_radius=6, fg_color=RED, hover_color="#B71C1C",
            command=self.window.destroy)
        self.close_btn.pack(side="right", padx=15, pady=9)

        # Botón dar de alta / reinternar según estado
        estado = self.paciente.get("estado", "")
        if estado == "Internado":
            self.alta_btn = ctk.CTkButton(self.header, text="🔴 Dar de Alta",
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), height=32, width=130,
                corner_radius=6, fg_color=ORANGE, hover_color="#BF360C",
                command=self._discharge_from_expediente)
            self.alta_btn.pack(side="right", padx=(0, 5), pady=9)
        elif estado == "Alta":
            self.reinternar_btn = ctk.CTkButton(self.header, text="🟢 Reinternar",
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), height=32, width=120,
                corner_radius=6, fg_color=GREEN, hover_color="#1B5E20",
                command=self._reinternar_from_expediente)
            self.reinternar_btn.pack(side="right", padx=(0, 5), pady=9)

        # Botón editar siempre visible
        self.edit_btn = ctk.CTkButton(self.header, text="✏️ Editar",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), height=32, width=90,
            corner_radius=6, fg_color="#1565C0", hover_color="#0D47A1",
            command=self._enter_edit_mode)
        self.edit_btn.pack(side="right", padx=(0, 5), pady=9)

    # =============================================
    # MODO VISTA (solo lectura) - Pestañas
    # =============================================
    def _build_view_mode(self):
        p = self.paciente
        estado = p.get("estado", "")
        estado_color = GREEN if estado == "Internado" else RED
        estado_text = "● INTERNADO" if estado == "Internado" else "● DADO DE ALTA"

        # Etiqueta de estado arriba del tabview
        status_frame = ctk.CTkFrame(self.window, fg_color=WHITE, height=40, corner_radius=0)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)
        ctk.CTkLabel(status_frame, text=estado_text,
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            text_color=estado_color, fg_color=GRAY_LIGHT, corner_radius=8,
            height=30, padx=15).pack(pady=5)

        # Tabview
        self.view_tabview = ctk.CTkTabview(self.window,
            fg_color=WHITE,
            segmented_button_fg_color=GRAY_LIGHT,
            segmented_button_selected_color=NAVY_BLUE,
            segmented_button_unselected_color=GRAY_MED,
            segmented_button_selected_hover_color=NAVY_DARK,
            segmented_button_unselected_hover_color="#D0D0D0",
            text_color="white",
            text_color_disabled=GRAY_TEXT)
        self.view_tabview.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        # Tab: Datos Personales
        tab1 = self.view_tabview.add("Personales")
        self._add_field_row(tab1, "Nombre", p.get("nombre", ""))
        self._add_field_row(tab1, "Apellido Paterno", p.get("apellido_paterno", ""))
        self._add_field_row(tab1, "Apellido Materno", p.get("apellido_materno", ""))
        self._add_field_row(tab1, "Sexo", p.get("sexo", "N/A"))
        self._add_field_row(tab1, "Teléfono", p.get("telefono", "N/A"))
        self._add_field_row(tab1, "Dirección", p.get("direccion", "N/A"))
        self._add_field_row(tab1, "Fecha de Nacimiento",
            self._format_date(p.get("dia_nacimiento"), p.get("mes_nacimiento"), p.get("anio_nacimiento")))

        # Tab: Familiar
        tab2 = self.view_tabview.add("Familiar")
        self._add_field_row(tab2, "Nombre", p.get("familiar_nombre", "N/A"))
        self._add_field_row(tab2, "Parentesco", p.get("familiar_parentesco", "N/A"))
        self._add_field_row(tab2, "Teléfono", p.get("familiar_telefono", "N/A"))
        self._add_field_row(tab2, "Dirección", p.get("familiar_direccion", "N/A"))

        # Tab: Encargado
        tab3 = self.view_tabview.add("Encargado")
        self._add_field_row(tab3, "Nombre", p.get("encargado_nombre", "N/A"))
        self._add_field_row(tab3, "Cargo", p.get("encargado_cargo", "N/A"))
        self._add_field_row(tab3, "Teléfono", p.get("encargado_telefono", "N/A"))

        # Tab: Ingreso
        tab4 = self.view_tabview.add("Ingreso")
        self._add_field_row(tab4, "Fecha de Ingreso",
            self._format_date(p.get("dia_ingreso"), p.get("mes_ingreso"), p.get("anio_ingreso")))
        self._add_field_row(tab4, "Motivo", p.get("motivo_ingreso", "N/A"))
        self._add_field_row(tab4, "Observaciones", p.get("observaciones", "N/A"))

        # Tab: Egreso (solo si fue dado de alta)
        if estado == "Alta":
            tab5 = self.view_tabview.add("Egreso")
            self._add_field_row(tab5, "Fecha de Egreso",
                self._format_date(p.get("dia_egreso"), p.get("mes_egreso"), p.get("anio_egreso")))
            self._add_field_row(tab5, "Motivo de Egreso", p.get("motivo_egreso", "N/A"))

    def _add_field_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color=WHITE, corner_radius=6, height=36)
        row.pack(fill="x", padx=20, pady=3)
        row.pack_propagate(False)
        ctk.CTkLabel(row, text=label,
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
            text_color="#555555", anchor="w", width=180).pack(side="left", padx=(10, 5), pady=6)
        ctk.CTkLabel(row, text=str(value) if value else "N/A",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color="#333333", anchor="w").pack(side="left", padx=5, pady=6, fill="x", expand=True)

    # =============================================
    # MODO EDICIÓN - Pestañas con campos editables
    # =============================================
    def _enter_edit_mode(self):
        self.editing = True
        # Destruir vista
        self.view_tabview.destroy()
        # Ocultar botones del header
        self.edit_btn.pack_forget()
        if hasattr(self, 'alta_btn'):
            self.alta_btn.pack_forget()
        if hasattr(self, 'reinternar_btn'):
            self.reinternar_btn.pack_forget()
        # Cambiar título
        self.header_title.configure(text="✏️ Editando Expediente")
        # Construir modo edición
        self._build_edit_mode()

    def _build_edit_mode(self):
        p = self.paciente

        # Tabview de edición
        self.edit_tabview = ctk.CTkTabview(self.window,
            fg_color=WHITE,
            segmented_button_fg_color=GRAY_LIGHT,
            segmented_button_selected_color=NAVY_BLUE,
            segmented_button_unselected_color=GRAY_MED,
            segmented_button_selected_hover_color=NAVY_DARK,
            segmented_button_unselected_hover_color="#D0D0D0",
            text_color="white",
            text_color_disabled=GRAY_TEXT)
        self.edit_tabview.pack(fill="both", expand=True, padx=15, pady=(10, 5))

        # --- Tab: Datos Personales ---
        tab1 = self.edit_tabview.add("Personales")
        self.edit_nombre = self._make_edit_entry(tab1, "Nombre(s) *", p.get("nombre", ""))
        self.edit_apellido_p = self._make_edit_entry(tab1, "Apellido Paterno *", p.get("apellido_paterno", ""))
        self.edit_apellido_m = self._make_edit_entry(tab1, "Apellido Materno", p.get("apellido_materno", "") or "")

        ctk.CTkLabel(tab1, text="Sexo *",
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=20, pady=(8, 2))
        self.edit_sexo = ctk.CTkOptionMenu(tab1, values=["Masculino", "Femenino"],
            height=38, font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        sexo_val = p.get("sexo", "")
        self.edit_sexo.set(sexo_val if sexo_val and sexo_val != "N/A" else "Seleccionar...")
        self.edit_sexo.pack(fill="x", padx=20, pady=(0, 4))

        self.edit_telefono = self._make_edit_entry(tab1, "Teléfono", p.get("telefono", "") or "")
        self.edit_direccion = self._make_edit_entry(tab1, "Dirección", p.get("direccion", "") or "")
        self.edit_dia_nac, self.edit_mes_nac, self.edit_anio_nac = self._make_edit_date_row(
            tab1, "Fecha de Nacimiento",
            p.get("dia_nacimiento"), p.get("mes_nacimiento"), p.get("anio_nacimiento"))

        # --- Tab: Familiar ---
        tab2 = self.edit_tabview.add("Familiar")
        self.edit_fam_nombre = self._make_edit_entry(tab2, "Nombre del Familiar *", p.get("familiar_nombre", "") or "")
        self.edit_fam_parentesco = self._make_edit_entry(tab2, "Parentesco *", p.get("familiar_parentesco", "") or "")
        self.edit_fam_telefono = self._make_edit_entry(tab2, "Teléfono del Familiar *", p.get("familiar_telefono", "") or "")
        self.edit_fam_direccion = self._make_edit_entry(tab2, "Dirección del Familiar", p.get("familiar_direccion", "") or "")

        # --- Tab: Encargado ---
        tab3 = self.edit_tabview.add("Encargado")
        self.edit_enc_nombre = self._make_edit_entry(tab3, "Nombre del Encargado *", p.get("encargado_nombre", "") or "")
        self.edit_enc_cargo = self._make_edit_entry(tab3, "Cargo *", p.get("encargado_cargo", "") or "")
        self.edit_enc_telefono = self._make_edit_entry(tab3, "Teléfono del Encargado *", p.get("encargado_telefono", "") or "")

        # --- Tab: Ingreso ---
        tab4 = self.edit_tabview.add("Ingreso")
        self.edit_dia_ing, self.edit_mes_ing, self.edit_anio_ing = self._make_edit_date_row(
            tab4, "Fecha de Ingreso *",
            p.get("dia_ingreso"), p.get("mes_ingreso"), p.get("anio_ingreso"))
        self.edit_motivo = self._make_edit_entry(tab4, "Motivo de Ingreso *", p.get("motivo_ingreso", "") or "")
        self.edit_observaciones = self._make_edit_entry(tab4, "Observaciones", p.get("observaciones", "") or "")

        # Footer con botones
        self.edit_footer = ctk.CTkFrame(self.window, fg_color=WHITE, height=55, corner_radius=0)
        self.edit_footer.pack(fill="x", side="bottom")
        self.edit_footer.pack_propagate(False)

        ctk.CTkButton(self.edit_footer, text="← Cancelar",
            font=ctk.CTkFont(family="Roboto", size=13), height=38, width=120,
            corner_radius=8, fg_color=GRAY_MED, text_color="#333333",
            hover_color="#CCCCCC", command=self._cancel_edit).pack(side="left", padx=20, pady=8)

        ctk.CTkButton(self.edit_footer, text="💾 Guardar Cambios",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            height=38, width=170, corner_radius=8,
            fg_color=GREEN, hover_color="#1B5E20",
            command=self._save_edit).pack(side="right", padx=20, pady=8)

    def _make_edit_entry(self, parent, label_text, prefill=""):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=20, pady=(8, 2))
        entry = ctk.CTkEntry(parent, height=38,
            font=ctk.CTkFont(family="Roboto", size=13),
            corner_radius=8, border_color=GRAY_MED)
        entry.pack(fill="x", padx=20, pady=(0, 4))
        if prefill and str(prefill) != "N/A":
            entry.insert(0, str(prefill))
        return entry

    def _make_edit_date_row(self, parent, label_text, prefill_d=None, prefill_m=None, prefill_a=None):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=20, pady=(8, 2))
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=(0, 4))

        dia_vals = [str(i) for i in range(1, 32)]
        dia_menu = ctk.CTkOptionMenu(date_frame, values=dia_vals, width=80, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        dia_menu.set(str(prefill_d) if prefill_d else "Día")
        dia_menu.pack(side="left", padx=(0, 5))

        mes_vals = [str(i) for i in range(1, 13)]
        mes_menu = ctk.CTkOptionMenu(date_frame, values=mes_vals, width=80, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        mes_menu.set(str(prefill_m) if prefill_m else "Mes")
        mes_menu.pack(side="left", padx=5)

        anio_vals = [str(i) for i in range(2026, 1919, -1)]
        anio_menu = ctk.CTkOptionMenu(date_frame, values=anio_vals, width=100, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        anio_menu.set(str(prefill_a) if prefill_a else "Año")
        anio_menu.pack(side="left", padx=5)

        return dia_menu, mes_menu, anio_menu

    def _cancel_edit(self):
        self.edit_tabview.destroy()
        self.edit_footer.destroy()
        self.editing = False
        nombre = f"{self.paciente.get('nombre', '')} {self.paciente.get('apellido_paterno', '')}"
        self.header_title.configure(text=f"📋 Expediente: {nombre}")
        # Restaurar botones
        self.edit_btn.pack(side="right", padx=(0, 5), pady=9)
        if hasattr(self, 'alta_btn'):
            self.alta_btn.pack(side="right", padx=(0, 5), pady=9)
        if hasattr(self, 'reinternar_btn'):
            self.reinternar_btn.pack(side="right", padx=(0, 5), pady=9)
        # Reconstruir vista
        self._build_view_mode()

    def _save_edit(self):
        dia_nac, mes_nac, anio_nac = self._get_date_value(self.edit_dia_nac, self.edit_mes_nac, self.edit_anio_nac)
        dia_ing, mes_ing, anio_ing = self._get_date_value(self.edit_dia_ing, self.edit_mes_ing, self.edit_anio_ing)
        sexo = self.edit_sexo.get()
        if sexo == "Seleccionar...":
            sexo = None

        data = {
            "id_paciente": self.paciente.get("id_paciente"),
            "nombre": self.edit_nombre.get().strip(),
            "apellido_paterno": self.edit_apellido_p.get().strip(),
            "apellido_materno": self.edit_apellido_m.get().strip(),
            "sexo": sexo,
            "telefono": self.edit_telefono.get().strip(),
            "direccion": self.edit_direccion.get().strip(),
            "dia_nacimiento": dia_nac, "mes_nacimiento": mes_nac, "anio_nacimiento": anio_nac,
            "familiar_nombre": self.edit_fam_nombre.get().strip(),
            "familiar_parentesco": self.edit_fam_parentesco.get().strip(),
            "familiar_telefono": self.edit_fam_telefono.get().strip(),
            "familiar_direccion": self.edit_fam_direccion.get().strip(),
            "encargado_nombre": self.edit_enc_nombre.get().strip(),
            "encargado_cargo": self.edit_enc_cargo.get().strip(),
            "encargado_telefono": self.edit_enc_telefono.get().strip(),
            "dia_ingreso": dia_ing, "mes_ingreso": mes_ing, "anio_ingreso": anio_ing,
            "motivo_ingreso": self.edit_motivo.get().strip(),
            "observaciones": self.edit_observaciones.get().strip(),
        }

        import tkinter.messagebox as mb
        if not data["nombre"] or not data["apellido_paterno"]:
            mb.showwarning("Campos requeridos", "Nombre y Apellido Paterno son obligatorios."); return
        if not data["familiar_nombre"] or not data["familiar_parentesco"] or not data["familiar_telefono"]:
            mb.showwarning("Campos requeridos", "Los datos del familiar son obligatorios."); return
        if not data["encargado_nombre"] or not data["encargado_cargo"] or not data["encargado_telefono"]:
            mb.showwarning("Campos requeridos", "Los datos del personal encargado son obligatorios."); return
        if not data["dia_ingreso"] or not data["mes_ingreso"] or not data["anio_ingreso"]:
            mb.showwarning("Campos requeridos", "La fecha de ingreso es obligatoria."); return
        if not data["motivo_ingreso"]:
            mb.showwarning("Campos requeridos", "El motivo de ingreso es obligatorio."); return

        success = actualizar_paciente(data)
        if success:
            mb.showinfo("Éxito", "Paciente actualizado correctamente.")
            self.window.destroy()
            if self.callback:
                self.callback()
        else:
            mb.showerror("Error", "No se pudo actualizar el paciente. Verifique la conexión a la base de datos.")

    # =============================================
    # Acciones del expediente
    # =============================================
    def _discharge_from_expediente(self):
        import tkinter.messagebox as mb
        patient_id = self.paciente.get("id_paciente")
        if not patient_id:
            return
        if mb.askyesno("Confirmar", "¿Dar de alta a este paciente?"):
            from database.db import eliminar_paciente
            if eliminar_paciente(patient_id):
                mb.showinfo("Éxito", "Paciente dado de alta correctamente.")
                self.window.destroy()
                if self.callback:
                    self.callback()
            else:
                mb.showerror("Error", "No se pudo dar de alta al paciente.")

    def _reinternar_from_expediente(self):
        """Abre el modal de reinternación."""
        ReinternarModal(self.parent, self.paciente, callback=self.callback)
        self.window.destroy()

    # =============================================
    # Helpers compartidos
    # =============================================
    def _get_date_value(self, dia_menu, mes_menu, anio_menu):
        d, m, a = dia_menu.get(), mes_menu.get(), anio_menu.get()
        if d.startswith("Día") or m.startswith("Mes") or a.startswith("Año"):
            return None, None, None
        return int(d), int(m), int(a)

    def _format_date(self, dia, mes, anio):
        if dia and mes and anio:
            return f"{dia}/{mes}/{anio}"
        return "N/A"


# ============================================================
# MODAL DE REINTERNACIÓN
# ============================================================
class ReinternarModal:
    """Modal para reinternar a un paciente dado de alta."""

    def __init__(self, parent, paciente, callback=None):
        self.parent = parent
        self.paciente = paciente
        self.callback = callback

        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Reinternar - {paciente.get('nombre', '')} {paciente.get('apellido_paterno', '')}")
        self.window.geometry("520x480")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (520 // 2)
        y = (self.window.winfo_screenheight() // 2) - (480 // 2)
        self.window.geometry(f"520x480+{x}+{y}")

        self._build_header()
        self._build_form()
        self._build_footer()
        self.window.focus_force()

    def _build_header(self):
        header = ctk.CTkFrame(self.window, fg_color=GREEN, height=50, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        nombre = f"{self.paciente.get('nombre', '')} {self.paciente.get('apellido_paterno', '')}"
        ctk.CTkLabel(header, text=f"🟢 Reinternar: {nombre}",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color=WHITE).pack(side="left", padx=20, pady=12)

    def _build_form(self):
        form = ctk.CTkFrame(self.window, fg_color=WHITE, corner_radius=0)
        form.pack(fill="both", expand=True, padx=20, pady=20)

        # Info del paciente
        estado = self.paciente.get("estado", "")
        ctk.CTkLabel(form, text=f"Estado actual: {'Dado de Alta' if estado == 'Alta' else estado}",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color=RED if estado == "Alta" else GRAY_TEXT,
            fg_color=GRAY_LIGHT, corner_radius=6, height=30, padx=10).pack(fill="x", pady=(0, 15))

        # Fecha de reingreso
        self.dia_reing, self.mes_reing, self.anio_reing = self._make_date_row(form, "Fecha de Reingreso *")
        self.entry_motivo = self._make_entry(form, "Motivo de Reinternación *", "Motivo de la reinternación")
        self.entry_observaciones = self._make_entry(form, "Observaciones", "Observaciones adicionales")

    def _make_entry(self, parent, label_text, placeholder=""):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        entry = ctk.CTkEntry(parent, height=38,
            font=ctk.CTkFont(family="Roboto", size=13),
            corner_radius=8, border_color=GRAY_MED,
            placeholder_text=placeholder)
        entry.pack(fill="x", padx=5, pady=(0, 4))
        return entry

    def _make_date_row(self, parent, label_text):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", padx=5, pady=(0, 4))

        from datetime import datetime
        now = datetime.now()

        dia_vals = [str(i) for i in range(1, 32)]
        dia_menu = ctk.CTkOptionMenu(date_frame, values=dia_vals, width=80, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=GREEN, button_hover_color="#1B5E20")
        dia_menu.set(str(now.day))
        dia_menu.pack(side="left", padx=(0, 5))

        mes_vals = [str(i) for i in range(1, 13)]
        mes_menu = ctk.CTkOptionMenu(date_frame, values=mes_vals, width=80, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=GREEN, button_hover_color="#1B5E20")
        mes_menu.set(str(now.month))
        mes_menu.pack(side="left", padx=5)

        anio_vals = [str(i) for i in range(2026, 1919, -1)]
        anio_menu = ctk.CTkOptionMenu(date_frame, values=anio_vals, width=100, height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=GREEN, button_hover_color="#1B5E20")
        anio_menu.set(str(now.year))
        anio_menu.pack(side="left", padx=5)

        return dia_menu, mes_menu, anio_menu

    def _build_footer(self):
        footer = ctk.CTkFrame(self.window, fg_color=WHITE, height=55, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkButton(footer, text="Cancelar",
            font=ctk.CTkFont(family="Roboto", size=13), height=38, width=120,
            corner_radius=8, fg_color=GRAY_MED, text_color="#333333",
            hover_color="#CCCCCC", command=self.window.destroy).pack(side="left", padx=20, pady=8)

        ctk.CTkButton(footer, text="🟢 Reinternar Paciente",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            height=38, width=180, corner_radius=8,
            fg_color=GREEN, hover_color="#1B5E20",
            command=self._save_reinternar).pack(side="right", padx=20, pady=8)

    def _get_date_value(self, dia_menu, mes_menu, anio_menu):
        d, m, a = dia_menu.get(), mes_menu.get(), anio_menu.get()
        if d.startswith("Día") or m.startswith("Mes") or a.startswith("Año"):
            return None, None, None
        return int(d), int(m), int(a)

    def _save_reinternar(self):
        dia, mes, anio = self._get_date_value(self.dia_reing, self.mes_reing, self.anio_reing)
        motivo = self.entry_motivo.get().strip()
        observaciones = self.entry_observaciones.get().strip()

        import tkinter.messagebox as mb
        if not dia or not mes or not anio:
            mb.showwarning("Campos requeridos", "La fecha de reingreso es obligatoria."); return
        if not motivo:
            mb.showwarning("Campos requeridos", "El motivo de reinternación es obligatorio."); return

        data = {
            "dia_ingreso": dia, "mes_ingreso": mes, "anio_ingreso": anio,
            "motivo_ingreso": motivo, "observaciones": observaciones,
        }
        patient_id = self.paciente.get("id_paciente")
        success = reinternar_paciente(patient_id, data)
        if success:
            mb.showinfo("Éxito", "Paciente reinternado correctamente.")
            self.window.destroy()
            if self.callback:
                self.callback()
        else:
            mb.showerror("Error", "No se pudo reinternar al paciente. Verifique la conexión a la base de datos.")
