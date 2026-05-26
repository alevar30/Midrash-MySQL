-- ============================================
-- Midrash - Script de creación de base de datos
-- MySQL (XAMPP)
-- Ejecutar desde phpMyAdmin o terminal:
--   mysql -u root < midrash_mysql.sql
-- ============================================

CREATE DATABASE IF NOT EXISTS MidrashDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE MidrashDB;

-- ============================================
-- Tabla: Pacientes
-- ============================================
CREATE TABLE IF NOT EXISTS Pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NULL,
    sexo VARCHAR(20) NULL CHECK (sexo IN ('Masculino', 'Femenino')),
    telefono VARCHAR(20) NULL,
    direccion VARCHAR(255) NULL,
    dia_nacimiento INT NULL CHECK (dia_nacimiento BETWEEN 1 AND 31),
    mes_nacimiento INT NULL CHECK (mes_nacimiento BETWEEN 1 AND 12),
    anio_nacimiento INT NULL CHECK (anio_nacimiento BETWEEN 1900 AND 2100),
    estado VARCHAR(20) DEFAULT 'Internado' CHECK (estado IN ('Internado', 'Alta'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: Familiar
-- ============================================
CREATE TABLE IF NOT EXISTS Familiar (
    id_familiar INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NULL,
    direccion VARCHAR(255) NULL,
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: Personal_Encargado
-- ============================================
CREATE TABLE IF NOT EXISTS Personal_Encargado (
    id_encargado INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NULL,
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: Ingresos
-- ============================================
CREATE TABLE IF NOT EXISTS Ingresos (
    id_ingreso INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    dia INT NOT NULL CHECK (dia BETWEEN 1 AND 31),
    mes INT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INT NOT NULL CHECK (anio BETWEEN 1900 AND 2100),
    motivo VARCHAR(500) NOT NULL,
    observaciones VARCHAR(500) NULL,
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Tabla: Egresos
-- ============================================
CREATE TABLE IF NOT EXISTS Egresos (
    id_egreso INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    dia INT NOT NULL CHECK (dia BETWEEN 1 AND 31),
    mes INT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INT NOT NULL CHECK (anio BETWEEN 1900 AND 2100),
    motivo VARCHAR(500) NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Vista: vw_PacientesActivos
-- ============================================
CREATE OR REPLACE VIEW vw_PacientesActivos AS
SELECT
    p.id_paciente, p.nombre, p.apellido_paterno, p.apellido_materno, p.sexo,
    p.telefono, p.direccion, p.dia_nacimiento, p.mes_nacimiento, p.anio_nacimiento, p.estado,
    f.nombre AS familiar_nombre, f.parentesco AS familiar_parentesco, f.telefono AS familiar_telefono,
    e.nombre AS encargado_nombre, e.cargo AS encargado_cargo, e.telefono AS encargado_telefono,
    i.motivo AS motivo_ingreso, i.dia AS dia_ingreso, i.mes AS mes_ingreso, i.anio AS anio_ingreso
FROM Pacientes p
LEFT JOIN Familiar f ON p.id_paciente = f.id_paciente
LEFT JOIN Personal_Encargado e ON p.id_paciente = e.id_paciente
LEFT JOIN Ingresos i ON p.id_paciente = i.id_paciente
WHERE p.estado = 'Internado';

-- ============================================
-- Datos de prueba (solo si la tabla está vacía)
-- ============================================
INSERT INTO Pacientes (nombre, apellido_paterno, apellido_materno, sexo, telefono, direccion, dia_nacimiento, mes_nacimiento, anio_nacimiento, estado)
SELECT 'Juan', 'García', 'López', 'Masculino', '555-1234', 'Calle Principal 123', 15, 6, 1988, 'Internado'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Pacientes LIMIT 1);

INSERT INTO Familiar (id_paciente, nombre, parentesco, telefono, direccion)
SELECT 1, 'María López', 'Madre', '555-5678', 'Calle Principal 123'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Familiar WHERE id_paciente = 1);

INSERT INTO Personal_Encargado (id_paciente, nombre, cargo, telefono)
SELECT 1, 'Dr. Carlos Ramírez', 'Médico', '555-9012'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Personal_Encargado WHERE id_paciente = 1);

INSERT INTO Ingresos (id_paciente, dia, mes, anio, motivo, observaciones)
SELECT 1, 10, 1, 2025, 'Adicción a sustancias', 'Paciente referido por centro de salud'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Ingresos WHERE id_paciente = 1);

INSERT INTO Pacientes (nombre, apellido_paterno, apellido_materno, sexo, telefono, direccion, dia_nacimiento, mes_nacimiento, anio_nacimiento, estado)
SELECT 'Ana', 'Martínez', 'Hernández', 'Femenino', '555-3456', 'Avenida Central 456', 22, 3, 1995, 'Internado'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Pacientes WHERE id_paciente = 2);

INSERT INTO Familiar (id_paciente, nombre, parentesco, telefono, direccion)
SELECT 2, 'Pedro Martínez', 'Padre', '555-7890', 'Avenida Central 456'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Familiar WHERE id_paciente = 2);

INSERT INTO Personal_Encargado (id_paciente, nombre, cargo, telefono)
SELECT 2, 'Dra. Laura Sánchez', 'Psicóloga', '555-2345'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Personal_Encargado WHERE id_paciente = 2);

INSERT INTO Ingresos (id_paciente, dia, mes, anio, motivo, observaciones)
SELECT 2, 5, 2, 2025, 'Dependencia de alcohol', 'Paciente voluntaria'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Ingresos WHERE id_paciente = 2);

INSERT INTO Pacientes (nombre, apellido_paterno, apellido_materno, sexo, telefono, direccion, dia_nacimiento, mes_nacimiento, anio_nacimiento, estado)
SELECT 'Roberto', 'Díaz', 'Flores', 'Masculino', '555-6789', 'Boulevard Norte 789', 8, 11, 1990, 'Internado'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Pacientes WHERE id_paciente = 3);

INSERT INTO Familiar (id_paciente, nombre, parentesco, telefono, direccion)
SELECT 3, 'Sofía Flores', 'Esposa', '555-0123', 'Boulevard Norte 789'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Familiar WHERE id_paciente = 3);

INSERT INTO Personal_Encargado (id_paciente, nombre, cargo, telefono)
SELECT 3, 'Lic. Miguel Torres', 'Trabajador Social', '555-4567'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Personal_Encargado WHERE id_paciente = 3);

INSERT INTO Ingresos (id_paciente, dia, mes, anio, motivo, observaciones)
SELECT 3, 20, 3, 2025, 'Adicción a estupefacientes', 'Remitido por juzgado'
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM Ingresos WHERE id_paciente = 3);
