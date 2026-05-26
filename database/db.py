"""
Conexión a Base de Datos - Midrash
MySQL con pymysql
"""
try:
    import pymysql
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False
    print("⚠️ pymysql no está instalado. Ejecuta: pip install pymysql")

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "MidrashDB"
DB_USER = "root"
DB_PASSWORD = ""

from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        yield conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        if conn: conn.rollback()
        raise
    finally:
        if conn:
            try: conn.close()
            except: pass

def _check_column_exists(cursor, table_name, column_name):
    try:
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s",
            (DB_NAME, table_name, column_name)
        )
        result = cursor.fetchone()
        return result["cnt"] > 0
    except:
        return False

def _ensure_sexo_column():
    if not PYMYSQL_AVAILABLE: return
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if not _check_column_exists(cursor, "Pacientes", "sexo"):
                cursor.execute("ALTER TABLE Pacientes ADD COLUMN sexo VARCHAR(20) NULL")
                conn.commit()
                print("✅ Columna 'sexo' añadida a la tabla Pacientes")
    except Exception as e:
        print(f"⚠️ No se pudo verificar/añadir columna sexo: {e}")

def obtener_pacientes():
    if not PYMYSQL_AVAILABLE: return []
    _ensure_sexo_column()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            has_sexo = _check_column_exists(cursor, "Pacientes", "sexo")
            sexo_col = "p.sexo," if has_sexo else ""
            query = f"""
                SELECT p.id_paciente, p.nombre, p.apellido_paterno,
                       p.apellido_materno, {sexo_col} p.telefono, p.direccion,
                       p.dia_nacimiento, p.mes_nacimiento, p.anio_nacimiento,
                       p.estado,
                       f.nombre AS familiar_nombre, f.parentesco AS familiar_parentesco,
                       f.telefono AS familiar_telefono, f.direccion AS familiar_direccion,
                       e.nombre AS encargado_nombre, e.cargo AS encargado_cargo,
                       e.telefono AS encargado_telefono,
                       i.motivo AS motivo_ingreso, i.observaciones,
                       i.dia AS dia_ingreso, i.mes AS mes_ingreso, i.anio AS anio_ingreso
                FROM Pacientes p
                LEFT JOIN Familiar f ON p.id_paciente = f.id_paciente
                LEFT JOIN Personal_Encargado e ON p.id_paciente = e.id_paciente
                LEFT JOIN Ingresos i ON p.id_paciente = i.id_paciente
                WHERE p.estado = 'Internado'
                ORDER BY p.id_paciente DESC
            """
            cursor.execute(query)
            pacientes = cursor.fetchall()
            for p in pacientes:
                if "sexo" not in p: p["sexo"] = ""
            return pacientes
    except Exception as e:
        print(f"❌ Error al obtener pacientes: {e}")
        return []

def buscar_pacientes(query_text):
    if not PYMYSQL_AVAILABLE: return []
    _ensure_sexo_column()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            has_sexo = _check_column_exists(cursor, "Pacientes", "sexo")
            sexo_col = "p.sexo," if has_sexo else ""
            search = f"%{query_text}%"
            query = f"""
                SELECT p.id_paciente, p.nombre, p.apellido_paterno,
                       p.apellido_materno, {sexo_col} p.telefono, p.direccion,
                       p.dia_nacimiento, p.mes_nacimiento, p.anio_nacimiento,
                       p.estado,
                       f.nombre AS familiar_nombre, f.parentesco AS familiar_parentesco,
                       f.telefono AS familiar_telefono, f.direccion AS familiar_direccion,
                       e.nombre AS encargado_nombre, e.cargo AS encargado_cargo,
                       e.telefono AS encargado_telefono,
                       i.motivo AS motivo_ingreso, i.observaciones,
                       i.dia AS dia_ingreso, i.mes AS mes_ingreso, i.anio AS anio_ingreso
                FROM Pacientes p
                LEFT JOIN Familiar f ON p.id_paciente = f.id_paciente
                LEFT JOIN Personal_Encargado e ON p.id_paciente = e.id_paciente
                LEFT JOIN Ingresos i ON p.id_paciente = i.id_paciente
                WHERE p.estado = 'Internado'
                  AND (p.nombre LIKE %s OR p.apellido_paterno LIKE %s OR p.apellido_materno LIKE %s)
                ORDER BY p.id_paciente DESC
            """
            cursor.execute(query, (search, search, search))
            pacientes = cursor.fetchall()
            for p in pacientes:
                if "sexo" not in p: p["sexo"] = ""
            return pacientes
    except Exception as e:
        print(f"❌ Error al buscar pacientes: {e}")
        return []

def obtener_paciente_por_id(patient_id):
    if not PYMYSQL_AVAILABLE: return None
    _ensure_sexo_column()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            has_sexo = _check_column_exists(cursor, "Pacientes", "sexo")
            sexo_col = "p.sexo," if has_sexo else ""
            query = f"""
                SELECT p.id_paciente, p.nombre, p.apellido_paterno,
                       p.apellido_materno, {sexo_col} p.telefono, p.direccion,
                       p.dia_nacimiento, p.mes_nacimiento, p.anio_nacimiento,
                       p.estado,
                       f.nombre AS familiar_nombre, f.parentesco AS familiar_parentesco,
                       f.telefono AS familiar_telefono, f.direccion AS familiar_direccion,
                       e.nombre AS encargado_nombre, e.cargo AS encargado_cargo,
                       e.telefono AS encargado_telefono,
                       i.motivo AS motivo_ingreso, i.observaciones,
                       i.dia AS dia_ingreso, i.mes AS mes_ingreso, i.anio AS anio_ingreso
                FROM Pacientes p
                LEFT JOIN Familiar f ON p.id_paciente = f.id_paciente
                LEFT JOIN Personal_Encargado e ON p.id_paciente = e.id_paciente
                LEFT JOIN Ingresos i ON p.id_paciente = i.id_paciente
                WHERE p.id_paciente = %s
            """
            cursor.execute(query, (patient_id,))
            paciente = cursor.fetchone()
            if paciente:
                if "sexo" not in paciente: paciente["sexo"] = ""
                return paciente
            return None
    except Exception as e:
        print(f"❌ Error al obtener paciente: {e}")
        return None

def insertar_paciente(data):
    if not PYMYSQL_AVAILABLE: return False
    _ensure_sexo_column()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            has_sexo = _check_column_exists(cursor, "Pacientes", "sexo")
            if has_sexo:
                cursor.execute("""
                    INSERT INTO Pacientes (nombre, apellido_paterno, apellido_materno, sexo,
                                          telefono, direccion, dia_nacimiento, mes_nacimiento, anio_nacimiento, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Internado')
                """, (data["nombre"], data["apellido_paterno"], data.get("apellido_materno", ""),
                      data.get("sexo"), data.get("telefono", ""), data.get("direccion", ""),
                      data.get("dia_nacimiento"), data.get("mes_nacimiento"), data.get("anio_nacimiento")))
            else:
                cursor.execute("""
                    INSERT INTO Pacientes (nombre, apellido_paterno, apellido_materno,
                                          telefono, direccion, dia_nacimiento, mes_nacimiento, anio_nacimiento, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Internado')
                """, (data["nombre"], data["apellido_paterno"], data.get("apellido_materno", ""),
                      data.get("telefono", ""), data.get("direccion", ""),
                      data.get("dia_nacimiento"), data.get("mes_nacimiento"), data.get("anio_nacimiento")))
            patient_id = cursor.lastrowid
            cursor.execute("INSERT INTO Familiar (id_paciente, nombre, parentesco, telefono, direccion) VALUES (%s, %s, %s, %s, %s)",
                (patient_id, data.get("familiar_nombre", ""), data.get("familiar_parentesco", ""),
                 data.get("familiar_telefono", ""), data.get("familiar_direccion", "")))
            cursor.execute("INSERT INTO Personal_Encargado (id_paciente, nombre, cargo, telefono) VALUES (%s, %s, %s, %s)",
                (patient_id, data.get("encargado_nombre", ""), data.get("encargado_cargo", ""),
                 data.get("encargado_telefono", "")))
            cursor.execute("INSERT INTO Ingresos (id_paciente, dia, mes, anio, motivo, observaciones) VALUES (%s, %s, %s, %s, %s, %s)",
                (patient_id, data.get("dia_ingreso"), data.get("mes_ingreso"), data.get("anio_ingreso"),
                 data.get("motivo_ingreso", ""), data.get("observaciones", "")))
            conn.commit()
            print(f"✅ Paciente registrado con ID: {patient_id}")
            return True
    except Exception as e:
        print(f"❌ Error al insertar paciente: {e}")
        return False

def eliminar_paciente(patient_id):
    if not PYMYSQL_AVAILABLE: return False
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Pacientes SET estado = 'Alta' WHERE id_paciente = %s", (patient_id,))
            from datetime import datetime
            now = datetime.now()
            cursor.execute("INSERT INTO Egresos (id_paciente, dia, mes, anio, motivo) VALUES (%s, %s, %s, %s, 'Alta del paciente')",
                (patient_id, now.day, now.month, now.year))
            conn.commit()
            print(f"✅ Paciente {patient_id} dado de alta")
            return True
    except Exception as e:
        print(f"❌ Error al dar de alta: {e}")
        return False

def actualizar_paciente(data):
    if not PYMYSQL_AVAILABLE: return False
    _ensure_sexo_column()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            patient_id = data["id_paciente"]
            has_sexo = _check_column_exists(cursor, "Pacientes", "sexo")
            if has_sexo:
                cursor.execute("""
                    UPDATE Pacientes SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, sexo=%s,
                                         telefono=%s, direccion=%s, dia_nacimiento=%s, mes_nacimiento=%s, anio_nacimiento=%s
                    WHERE id_paciente=%s
                """, (data["nombre"], data["apellido_paterno"], data.get("apellido_materno", ""),
                      data.get("sexo"), data.get("telefono", ""), data.get("direccion", ""),
                      data.get("dia_nacimiento"), data.get("mes_nacimiento"), data.get("anio_nacimiento"),
                      patient_id))
            else:
                cursor.execute("""
                    UPDATE Pacientes SET nombre=%s, apellido_paterno=%s, apellido_materno=%s,
                                         telefono=%s, direccion=%s, dia_nacimiento=%s, mes_nacimiento=%s, anio_nacimiento=%s
                    WHERE id_paciente=%s
                """, (data["nombre"], data["apellido_paterno"], data.get("apellido_materno", ""),
                      data.get("telefono", ""), data.get("direccion", ""),
                      data.get("dia_nacimiento"), data.get("mes_nacimiento"), data.get("anio_nacimiento"),
                      patient_id))
            cursor.execute("""
                UPDATE Familiar SET nombre=%s, parentesco=%s, telefono=%s, direccion=%s
                WHERE id_paciente=%s
            """, (data.get("familiar_nombre", ""), data.get("familiar_parentesco", ""),
                  data.get("familiar_telefono", ""), data.get("familiar_direccion", ""), patient_id))
            cursor.execute("""
                UPDATE Personal_Encargado SET nombre=%s, cargo=%s, telefono=%s
                WHERE id_paciente=%s
            """, (data.get("encargado_nombre", ""), data.get("encargado_cargo", ""),
                  data.get("encargado_telefono", ""), patient_id))
            cursor.execute("""
                UPDATE Ingresos SET dia=%s, mes=%s, anio=%s, motivo=%s, observaciones=%s
                WHERE id_paciente=%s
            """, (data.get("dia_ingreso"), data.get("mes_ingreso"), data.get("anio_ingreso"),
                  data.get("motivo_ingreso", ""), data.get("observaciones", ""), patient_id))
            conn.commit()
            print(f"✅ Paciente {patient_id} actualizado")
            return True
    except Exception as e:
        print(f"❌ Error al actualizar paciente: {e}")
        return False

# Variable de compatibilidad para dashboard_gui.py
PYODBC_AVAILABLE = PYMYSQL_AVAILABLE

if PYMYSQL_AVAILABLE:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print("✅ Conexión a MySQL exitosa")
    except Exception as e:
        print(f"⚠️ No se pudo conectar a MySQL: {e}")
        print("   La aplicación funcionará en modo sin conexión")