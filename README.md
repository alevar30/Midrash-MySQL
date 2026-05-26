# Midrash - Sistema de Gestión de Pacientes

Sistema de escritorio para la gestión de pacientes en un centro de rehabilitación de adicciones, desarrollado con **CustomTkinter** y **MySQL**.

---

## Requisitos del Sistema

- **Python 3.10+** (probado en Python 3.13)
- **MySQL** (XAMPP o instalación independiente)
- **Windows 10/11** (aplicación de escritorio)

---

## Instalación Paso a Paso

### 1. Instalar Python

Descargar desde [python.org](https://www.python.org/downloads/) e instalar.
Asegúrate de marcar la opción **"Add Python to PATH"** durante la instalación.

### 2. Instalar MySQL

**Opción A — XAMPP (Recomendado):**
1. Descargar XAMPP desde [apachefriends.org](https://www.apachefriends.org/)
2. Instalar y abrir el Panel de Control de XAMPP
3. Iniciar el módulo **MySQL** (debe quedar en verde/running)

**Opción B — MySQL independiente:**
1. Descargar MySQL Community Server desde [mysql.com](https://dev.mysql.com/downloads/mysql/)
2. Instalar con configuración estándar
3. Crear un usuario con los credenciales que usarás en la aplicación

### 3. Crear la Base de Datos

**Con phpMyAdmin (XAMPP):**
1. Abrir el navegador y visitar `http://localhost/phpmyadmin`
2. Ir a la pestaña **SQL**
3. Copiar y pegar el contenido del archivo `database/midrash_mysql.sql`
4. Presionar **Continuar** para ejecutar

**O desde la terminal:**
```bash
mysql -u root < database/midrash_mysql.sql
```

Esto creará automáticamente:
- La base de datos `MidrashDB`
- Las 5 tablas: `Pacientes`, `Familiar`, `Personal_Encargado`, `Ingresos`, `Egresos`
- La vista `vw_PacientesActivos`
- 3 pacientes de prueba con sus datos relacionados

### 4. Instalar las Dependencias de Python

Abrir una terminal (CMD o PowerShell) en la carpeta del proyecto y ejecutar:

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install customtkinter>=5.2.0
pip install Pillow>=10.0.0
pip install pymysql>=1.1.0
```

### 5. Ejecutar la Aplicación

```bash
python main.py
```

---

## Credenciales de Acceso

| Campo | Valor |
|-------|-------|
| Usuario | `admin` |
| Contraseña | `1234` |

---

## Configuración de Conexión a MySQL

La configuración de conexión está en `database/db.py`. Los valores por defecto para XAMPP son:

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "MidrashDB"
DB_USER = "root"
DB_PASSWORD = ""
```

Si tu MySQL tiene contraseña, modifícala en `DB_PASSWORD`. Si usas un puerto diferente, cámbialo en `DB_PORT`.

---

## Estructura del Proyecto

```
Midrash/
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── assets/
│   └── logo.png                     # Logo de la aplicación
├── database/
│   ├── __init__.py
│   ├── db.py                        # Conexión y operaciones MySQL
│   └── midrash_mysql.sql            # Script de creación de BD
└── gui/
    ├── __init__.py
    ├── login_gui.py                 # Ventana de inicio de sesión
    ├── dashboard_gui.py             # Panel principal con tabla de pacientes
    └── components/
        ├── __init__.py
        └── patient_form.py          # Formulario de registro y expediente
```

---

## Funcionalidades

- **Inicio de sesión** con credenciales de administrador
- **Dashboard** con tabla de pacientes internados y barra de búsqueda
- **Registro de pacientes** en 4 pasos:
  1. Datos personales (nombre, apellidos, sexo, teléfono, dirección, fecha de nacimiento)
  2. Datos del familiar (nombre, parentesco, teléfono, dirección)
  3. Personal encargado (nombre, cargo, teléfono)
  4. Datos de ingreso (fecha, motivo, observaciones)
- **Expediente completo** de cada paciente (doble clic o clic derecho → Ver Expediente)
- **Dar de alta** a pacientes (clic derecho → Dar de Alta) — no hay borrado físico, solo cambio de estado
- **Registro automático de egreso** al dar de alta un paciente
- **Indicador de conexión** a base de datos en el sidebar
- **Cierre de sesión** para volver al login

---

## Base de Datos — Tablas

| Tabla | Descripción |
|-------|-------------|
| `Pacientes` | Datos personales del paciente y estado (Internado/Alta) |
| `Familiar` | Datos del familiar responsable del paciente |
| `Personal_Encargado` | Personal médico/terapéutico asignado |
| `Ingresos` | Registro de ingresos con fecha, motivo y observaciones |
| `Egresos` | Registro de egresos con fecha y motivo |
| `vw_PacientesActivos` | Vista que une las 4 tablas principales (solo pacientes internados) |

---

## Notas Importantes

- No existe borrado físico de pacientes. Al "dar de alta" se cambia el estado a `Alta` y se registra un egreso automático.
- La columna `sexo` se maneja dinámicamente con `_ensure_sexo_column()` por compatibilidad hacia atrás.
- Los dropdowns de fecha usan `CTkOptionMenu` (no `CTkComboBox`) por compatibilidad con Windows.
- Los frames con scroll incluyen bindings explícitos de mousewheel para Windows.
- La aplicación funciona en modo sin conexión si no puede conectarse a MySQL (solo lectura de la interfaz, sin datos).

---

## Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| CustomTkinter | 5.2+ | Framework de interfaz gráfica |
| Pillow | 10.0+ | Procesamiento de imágenes (logo) |
| PyMySQL | 1.1+ | Conector MySQL |
| MySQL | 8.0+ | Base de datos |
| XAMPP | 3.3+ | Servidor MySQL local (opcional) |
