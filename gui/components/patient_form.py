"""
Formulario de Paciente y Expediente - Midrash
"""
import customtkinter as ctk
from database.db import insertar_paciente, actualizar_paciente

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
    """Modal para registrar un nuevo paciente - 4 pasos"""
    STEPS = ["Datos Personales", "Datos del Familiar", "Personal Encargado", "Datos de Ingreso"]

    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.current_step = 0

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Nuevo Paciente")
        self.window.geometry("720x750")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (720 // 2)
        y = (self.window.winfo_screenheight() // 2) - (750 // 2)
        self.window.geometry(f"720x750+{x}+{y}")

        self._build_ui()
        self.window.focus_force()

    def _build_ui(self):
        # Header
        self.header = ctk.CTkFrame(self.window, fg_color=NAVY_BLUE, height=50, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.title_label = ctk.CTkLabel(self.header,
            text=f"Paso 1/4 — {self.STEPS[0]}",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color=WHITE)
        self.title_label.pack(side="left", padx=20, pady=12)

        # Step indicators
        self.steps_frame = ctk.CTkFrame(self.window, fg_color=WHITE, height=40, corner_radius=0)
        self.steps_frame.pack(fill="x")
        self.steps_frame.pack_propagate(False)

        self.step_labels = []
        for i, step in enumerate(self.STEPS):
            fg = NAVY_BLUE if i == 0 else GRAY_MED
            tc = WHITE if i == 0 else GRAY_TEXT
            lbl = ctk.CTkLabel(self.steps_frame, text=f"{i+1}. {step}",
                font=ctk.CTkFont(family="Roboto", size=11, weight="bold" if i == 0 else "normal"),
                text_color=tc, fg_color=fg, corner_radius=5, height=28, padx=10)
            lbl.pack(side="left", padx=5, pady=6)
            self.step_labels.append(lbl)

        # Scrollable content
        self.content = ctk.CTkScrollableFrame(self.window, fg_color=WHITE, corner_radius=0)
        self.content.pack(fill="both", expand=True, padx=0, pady=0)
        self._bind_mousewheel(self.content)

        # Footer
        self.footer = ctk.CTkFrame(self.window, fg_color=WHITE, height=55, corner_radius=0)
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)

        self.back_btn = ctk.CTkButton(self.footer, text="← Anterior",
            font=ctk.CTkFont(family="Roboto", size=13), height=38, width=120,
            corner_radius=8, fg_color=GRAY_MED, text_color="#333333",
            hover_color="#CCCCCC", command=self._prev_step)
        self.back_btn.pack(side="left", padx=20, pady=8)

        self.next_btn = ctk.CTkButton(self.footer, text="Siguiente →",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            height=38, width=140, corner_radius=8,
            fg_color=NAVY_BLUE, hover_color=NAVY_DARK, command=self._next_step)
        self.next_btn.pack(side="right", padx=20, pady=8)

        # Build all steps
        self.step_frames = []
        self._build_step1()
        self._build_step2()
        self._build_step3()
        self._build_step4()

        for frame in self.step_frames:
            frame.pack_forget()
        self.step_frames[0].pack(fill="both", expand=True, padx=20, pady=10)
        self.back_btn.configure(state="disabled")

    def _bind_mousewheel(self, widget):
        def _on_mousewheel(event):
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def _on_mousewheel_linux(event):
            if event.num == 4:
                widget._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                widget._parent_canvas.yview_scroll(1, "units")
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", _on_mousewheel_linux)
        widget.bind("<Button-5>", _on_mousewheel_linux)
        def _bind_to_children(event=None):
            for child in widget.winfo_children():
                child.bind("<MouseWheel>", _on_mousewheel)
                child.bind("<Button-4>", _on_mousewheel_linux)
                child.bind("<Button-5>", _on_mousewheel_linux)
                for grandchild in child.winfo_children():
                    grandchild.bind("<MouseWheel>", _on_mousewheel)
                    grandchild.bind("<Button-4>", _on_mousewheel_linux)
                    grandchild.bind("<Button-5>", _on_mousewheel_linux)
        widget.bind("<Configure>", _bind_to_children)

    def _make_entry_row(self, parent, label_text, placeholder="", show=None, prefill=""):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", pady=(8, 2))
        entry = ctk.CTkEntry(parent, height=38,
            font=ctk.CTkFont(family="Roboto", size=13),
            corner_radius=8, border_color=GRAY_MED,
            placeholder_text=placeholder, show=show)
        entry.pack(fill="x", pady=(0, 4))
        if prefill:
            entry.insert(0, str(prefill))
        return entry

    def _make_date_row(self, parent, label_text, prefill_d=None, prefill_m=None, prefill_a=None):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", pady=(8, 2))
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 4))

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

    def _build_step1(self):
        frame = ctk.CTkFrame(self.content, fg_color=WHITE)
        self.step_frames.append(frame)
        self.entry_nombre = self._make_entry_row(frame, "Nombre(s) *", "Nombre del paciente")
        self.entry_apellido_p = self._make_entry_row(frame, "Apellido Paterno *", "Apellido paterno")
        self.entry_apellido_m = self._make_entry_row(frame, "Apellido Materno", "Apellido materno")
        ctk.CTkLabel(frame, text="Sexo *",
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", pady=(8, 2))
        self.sexo_menu = ctk.CTkOptionMenu(frame, values=["Masculino", "Femenino"],
            height=38, font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        self.sexo_menu.set("Seleccionar...")
        self.sexo_menu.pack(fill="x", pady=(0, 4))
        self.entry_telefono = self._make_entry_row(frame, "Teléfono", "Teléfono de contacto")
        self.entry_direccion = self._make_entry_row(frame, "Dirección", "Dirección del paciente")
        self.dia_nac, self.mes_nac, self.anio_nac = self._make_date_row(frame, "Fecha de Nacimiento")

    def _build_step2(self):
        frame = ctk.CTkFrame(self.content, fg_color=WHITE)
        self.step_frames.append(frame)
        self.entry_fam_nombre = self._make_entry_row(frame, "Nombre del Familiar *", "Nombre completo")
        self.entry_fam_parentesco = self._make_entry_row(frame, "Parentesco *", "Ej: Madre, Padre, Hermano/a")
        self.entry_fam_telefono = self._make_entry_row(frame, "Teléfono del Familiar *", "Teléfono de contacto")
        self.entry_fam_direccion = self._make_entry_row(frame, "Dirección del Familiar", "Dirección")

    def _build_step3(self):
        frame = ctk.CTkFrame(self.content, fg_color=WHITE)
        self.step_frames.append(frame)
        self.entry_enc_nombre = self._make_entry_row(frame, "Nombre del Encargado *", "Nombre completo")
        self.entry_enc_cargo = self._make_entry_row(frame, "Cargo *", "Ej: Médico, Psicólogo")
        self.entry_enc_telefono = self._make_entry_row(frame, "Teléfono del Encargado *", "Teléfono de contacto")

    def _build_step4(self):
        frame = ctk.CTkFrame(self.content, fg_color=WHITE)
        self.step_frames.append(frame)
        self.dia_ing, self.mes_ing, self.anio_ing = self._make_date_row(frame, "Fecha de Ingreso *")
        self.entry_motivo = self._make_entry_row(frame, "Motivo de Ingreso *", "Descripción del motivo")
        self.entry_observaciones = self._make_entry_row(frame, "Observaciones", "Observaciones adicionales")

    def _update_step_ui(self):
        self.title_label.configure(text=f"Paso {self.current_step+1}/4 — {self.STEPS[self.current_step]}")
        for i, lbl in enumerate(self.step_labels):
            if i == self.current_step:
                lbl.configure(fg_color=NAVY_BLUE, text_color=WHITE,
                    font=ctk.CTkFont(family="Roboto", size=11, weight="bold"))
            else:
                lbl.configure(fg_color=GRAY_MED, text_color=GRAY_TEXT,
                    font=ctk.CTkFont(family="Roboto", size=11))
        for frame in self.step_frames:
            frame.pack_forget()
        self.step_frames[self.current_step].pack(fill="both", expand=True, padx=20, pady=10)
        self.back_btn.configure(state="normal" if self.current_step > 0 else "disabled")
        if self.current_step == 3:
            self.next_btn.configure(text="💾 Guardar", fg_color=GREEN, hover_color="#1B5E20")
        else:
            self.next_btn.configure(text="Siguiente →", fg_color=NAVY_BLUE, hover_color=NAVY_DARK)

    def _next_step(self):
        if self.current_step < 3:
            self.current_step += 1
            self._update_step_ui()
        else:
            self._save_patient()

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_step_ui()

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


class ExpedienteModal:
    """Modal para ver y editar el expediente completo de un paciente"""

    def __init__(self, parent, paciente, callback=None):
        self.parent = parent
        self.paciente = paciente
        self.callback = callback
        self.editing = False

        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Expediente - {paciente.get('nombre', '')} {paciente.get('apellido_paterno', '')}")
        self.window.geometry("720x750")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (720 // 2)
        y = (self.window.winfo_screenheight() // 2) - (750 // 2)
        self.window.geometry(f"720x750+{x}+{y}")

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

        # Botones del header (se reutilizan en ambos modos)
        estado = self.paciente.get("estado", "")

        self.close_btn = ctk.CTkButton(self.header, text="✕ Cerrar",
            font=ctk.CTkFont(family="Roboto", size=12), height=32, width=80,
            corner_radius=6, fg_color=RED, hover_color="#B71C1C",
            command=self.window.destroy)
        self.close_btn.pack(side="right", padx=15, pady=9)

        if estado == "Internado":
            self.alta_btn = ctk.CTkButton(self.header, text="🔴 Dar de Alta",
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), height=32, width=120,
                corner_radius=6, fg_color=ORANGE, hover_color="#BF360C",
                command=self._discharge_from_expediente)
            self.alta_btn.pack(side="right", padx=(0, 5), pady=9)

        self.edit_btn = ctk.CTkButton(self.header, text="✏️ Editar",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"), height=32, width=90,
            corner_radius=6, fg_color=GREEN, hover_color="#1B5E20",
            command=self._enter_edit_mode)
        self.edit_btn.pack(side="right", padx=(0, 5), pady=9)

    # =============================================
    # MODO VISTA (solo lectura)
    # =============================================
    def _build_view_mode(self):
        self.view_content = ctk.CTkScrollableFrame(self.window, fg_color=WHITE, corner_radius=0,
            scrollbar_button_color=NAVY_LIGHT, scrollbar_button_hover_color=NAVY_DARK)
        self.view_content.pack(fill="both", expand=True, padx=10, pady=10)
        self._bind_mousewheel(self.view_content)

        estado = self.paciente.get("estado", "")
        estado_color = GREEN if estado == "Internado" else RED
        estado_text = "● INTERNADO" if estado == "Internado" else "● DADO DE ALTA"
        ctk.CTkLabel(self.view_content, text=estado_text,
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            text_color=estado_color, fg_color=GRAY_LIGHT, corner_radius=8,
            height=36, padx=15).pack(pady=(5, 10))

        p = self.paciente
        self._add_section(self.view_content, "Datos Personales", [
            ("Nombre", p.get("nombre", "")),
            ("Apellido Paterno", p.get("apellido_paterno", "")),
            ("Apellido Materno", p.get("apellido_materno", "")),
            ("Sexo", p.get("sexo", "N/A")),
            ("Teléfono", p.get("telefono", "N/A")),
            ("Dirección", p.get("direccion", "N/A")),
            ("Fecha de Nacimiento", self._format_date(p.get("dia_nacimiento"), p.get("mes_nacimiento"), p.get("anio_nacimiento"))),
        ])
        self._add_section(self.view_content, "Datos del Familiar", [
            ("Nombre", p.get("familiar_nombre", "N/A")),
            ("Parentesco", p.get("familiar_parentesco", "N/A")),
            ("Teléfono", p.get("familiar_telefono", "N/A")),
            ("Dirección", p.get("familiar_direccion", "N/A")),
        ])
        self._add_section(self.view_content, "Personal Encargado", [
            ("Nombre", p.get("encargado_nombre", "N/A")),
            ("Cargo", p.get("encargado_cargo", "N/A")),
            ("Teléfono", p.get("encargado_telefono", "N/A")),
        ])
        self._add_section(self.view_content, "Datos de Ingreso", [
            ("Fecha de Ingreso", self._format_date(p.get("dia_ingreso"), p.get("mes_ingreso"), p.get("anio_ingreso"))),
            ("Motivo", p.get("motivo_ingreso", "N/A")),
            ("Observaciones", p.get("observaciones", "N/A")),
        ])

    # =============================================
    # MODO EDICIÓN
    # =============================================
    def _enter_edit_mode(self):
        self.editing = True
        # Ocultar vista
        self.view_content.pack_forget()
        # Cambiar botones del header
        self.edit_btn.pack_forget()
        if hasattr(self, 'alta_btn'):
            self.alta_btn.pack_forget()
        # Cambiar título
        self.header_title.configure(text="✏️ Editando Expediente")
        # Construir modo edición
        self._build_edit_mode()

    def _build_edit_mode(self):
        self.edit_content = ctk.CTkScrollableFrame(self.window, fg_color=WHITE, corner_radius=0,
            scrollbar_button_color=NAVY_LIGHT, scrollbar_button_hover_color=NAVY_DARK)
        self.edit_content.pack(fill="both", expand=True, padx=10, pady=10)
        self._bind_mousewheel(self.edit_content)

        # Footer con botones de guardar/cancelar
        self.edit_footer = ctk.CTkFrame(self.window, fg_color=WHITE, height=55, corner_radius=0)
        self.edit_footer.pack(fill="x", side="bottom")
        self.edit_footer.pack_propagate(False)

        ctk.CTkButton(self.edit_footer, text="← Cancelar",
            font=ctk.CTkFont(family="Roboto", size=13), height=38, width=120,
            corner_radius=8, fg_color=GRAY_MED, text_color="#333333",
            hover_color="#CCCCCC", command=self._cancel_edit).pack(side="left", padx=20, pady=8)

        ctk.CTkButton(self.edit_footer, text="💾 Guardar Cambios",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            height=38, width=160, corner_radius=8,
            fg_color=GREEN, hover_color="#1B5E20",
            command=self._save_edit).pack(side="right", padx=20, pady=8)

        p = self.paciente

        # --- Datos Personales ---
        self._add_edit_section_title(self.edit_content, "Datos Personales")
        self.edit_nombre = self._make_edit_entry(self.edit_content, "Nombre(s) *", p.get("nombre", ""))
        self.edit_apellido_p = self._make_edit_entry(self.edit_content, "Apellido Paterno *", p.get("apellido_paterno", ""))
        self.edit_apellido_m = self._make_edit_entry(self.edit_content, "Apellido Materno", p.get("apellido_materno", "") or "")

        ctk.CTkLabel(self.edit_content, text="Sexo *",
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=15, pady=(8, 2))
        self.edit_sexo = ctk.CTkOptionMenu(self.edit_content, values=["Masculino", "Femenino"],
            height=38, font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#1A1A1A",
            fg_color=WHITE, button_color=NAVY_LIGHT, button_hover_color=NAVY_DARK)
        sexo_val = p.get("sexo", "")
        self.edit_sexo.set(sexo_val if sexo_val and sexo_val != "N/A" else "Seleccionar...")
        self.edit_sexo.pack(fill="x", padx=15, pady=(0, 4))

        self.edit_telefono = self._make_edit_entry(self.edit_content, "Teléfono", p.get("telefono", "") or "")
        self.edit_direccion = self._make_edit_entry(self.edit_content, "Dirección", p.get("direccion", "") or "")
        self.edit_dia_nac, self.edit_mes_nac, self.edit_anio_nac = self._make_edit_date_row(
            self.edit_content, "Fecha de Nacimiento",
            p.get("dia_nacimiento"), p.get("mes_nacimiento"), p.get("anio_nacimiento"))

        # --- Datos del Familiar ---
        self._add_edit_section_title(self.edit_content, "Datos del Familiar")
        self.edit_fam_nombre = self._make_edit_entry(self.edit_content, "Nombre del Familiar *", p.get("familiar_nombre", "") or "")
        self.edit_fam_parentesco = self._make_edit_entry(self.edit_content, "Parentesco *", p.get("familiar_parentesco", "") or "")
        self.edit_fam_telefono = self._make_edit_entry(self.edit_content, "Teléfono del Familiar *", p.get("familiar_telefono", "") or "")
        self.edit_fam_direccion = self._make_edit_entry(self.edit_content, "Dirección del Familiar", p.get("familiar_direccion", "") or "")

        # --- Personal Encargado ---
        self._add_edit_section_title(self.edit_content, "Personal Encargado")
        self.edit_enc_nombre = self._make_edit_entry(self.edit_content, "Nombre del Encargado *", p.get("encargado_nombre", "") or "")
        self.edit_enc_cargo = self._make_edit_entry(self.edit_content, "Cargo *", p.get("encargado_cargo", "") or "")
        self.edit_enc_telefono = self._make_edit_entry(self.edit_content, "Teléfono del Encargado *", p.get("encargado_telefono", "") or "")

        # --- Datos de Ingreso ---
        self._add_edit_section_title(self.edit_content, "Datos de Ingreso")
        self.edit_dia_ing, self.edit_mes_ing, self.edit_anio_ing = self._make_edit_date_row(
            self.edit_content, "Fecha de Ingreso *",
            p.get("dia_ingreso"), p.get("mes_ingreso"), p.get("anio_ingreso"))
        self.edit_motivo = self._make_edit_entry(self.edit_content, "Motivo de Ingreso *", p.get("motivo_ingreso", "") or "")
        self.edit_observaciones = self._make_edit_entry(self.edit_content, "Observaciones", p.get("observaciones", "") or "")

    def _add_edit_section_title(self, parent, title):
        ctk.CTkLabel(parent, text=title,
            font=ctk.CTkFont(family="Roboto", size=15, weight="bold"),
            text_color=NAVY_BLUE, anchor="w").pack(fill="x", padx=15, pady=(15, 2))
        ctk.CTkFrame(parent, fg_color=NAVY_LIGHT, height=2).pack(fill="x", padx=15, pady=(0, 5))

    def _make_edit_entry(self, parent, label_text, prefill=""):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=15, pady=(8, 2))
        entry = ctk.CTkEntry(parent, height=38,
            font=ctk.CTkFont(family="Roboto", size=13),
            corner_radius=8, border_color=GRAY_MED)
        entry.pack(fill="x", padx=15, pady=(0, 4))
        if prefill and str(prefill) != "N/A":
            entry.insert(0, str(prefill))
        return entry

    def _make_edit_date_row(self, parent, label_text, prefill_d=None, prefill_m=None, prefill_a=None):
        ctk.CTkLabel(parent, text=label_text,
            font=ctk.CTkFont(family="Roboto", size=13),
            text_color="#333333", anchor="w").pack(fill="x", padx=15, pady=(8, 2))
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", padx=15, pady=(0, 4))

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
        self.edit_content.pack_forget()
        self.edit_footer.pack_forget()
        self.editing = False
        self.header_title.configure(text=f"📋 Expediente: {self.paciente.get('nombre', '')} {self.paciente.get('apellido_paterno', '')}")
        # Restaurar botones
        self.edit_btn.pack(side="right", padx=(0, 5), pady=9)
        if hasattr(self, 'alta_btn'):
            self.alta_btn.pack(side="right", padx=(0, 5), pady=9)
        # Mostrar vista de nuevo
        self.view_content.pack(fill="both", expand=True, padx=10, pady=10)

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
    # Métodos compartidos
    # =============================================
    def _bind_mousewheel(self, widget):
        def _on_mousewheel(event):
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def _on_mousewheel_linux(event):
            if event.num == 4: widget._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5: widget._parent_canvas.yview_scroll(1, "units")
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", _on_mousewheel_linux)
        widget.bind("<Button-5>", _on_mousewheel_linux)
        def _bind_to_children(event=None):
            for child in widget.winfo_children():
                child.bind("<MouseWheel>", _on_mousewheel)
                child.bind("<Button-4>", _on_mousewheel_linux)
                child.bind("<Button-5>", _on_mousewheel_linux)
                for gc in child.winfo_children():
                    gc.bind("<MouseWheel>", _on_mousewheel)
                    gc.bind("<Button-4>", _on_mousewheel_linux)
                    gc.bind("<Button-5>", _on_mousewheel_linux)
        widget.bind("<Configure>", _bind_to_children)

    def _add_section(self, parent, title, fields):
        section = ctk.CTkFrame(parent, fg_color=GRAY_LIGHT, corner_radius=10)
        section.pack(fill="x", pady=(5, 10), padx=5)
        ctk.CTkLabel(section, text=title,
            font=ctk.CTkFont(family="Roboto", size=15, weight="bold"),
            text_color=NAVY_BLUE, anchor="w").pack(fill="x", padx=15, pady=(12, 5))
        for label, value in fields:
            row = ctk.CTkFrame(section, fg_color=WHITE, corner_radius=6, height=32)
            row.pack(fill="x", padx=15, pady=2)
            row.pack_propagate(False)
            ctk.CTkLabel(row, text=label,
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
                text_color="#555555", anchor="w", width=160).pack(side="left", padx=(10, 5), pady=5)
            ctk.CTkLabel(row, text=str(value) if value else "N/A",
                font=ctk.CTkFont(family="Roboto", size=12),
                text_color="#333333", anchor="w").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        ctk.CTkFrame(section, fg_color=GRAY_LIGHT, height=8).pack()

    def _format_date(self, dia, mes, anio):
        if dia and mes and anio:
            return f"{dia}/{mes}/{anio}"
        return "N/A"

    def _get_date_value(self, dia_menu, mes_menu, anio_menu):
        d, m, a = dia_menu.get(), mes_menu.get(), anio_menu.get()
        if d.startswith("Día") or m.startswith("Mes") or a.startswith("Año"):
            return None, None, None
        return int(d), int(m), int(a)

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
