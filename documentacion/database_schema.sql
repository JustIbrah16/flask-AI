-- ============================================================================
-- HR PLATFORM - SCRIPT DE CREACIÓN DE TABLAS
-- ============================================================================
-- Base de datos: project
-- Sistema: Flask + SQLAlchemy
-- Fecha: 2025-11-25
-- ============================================================================

-- ============================================================================
-- 1. TABLA: roles
-- ============================================================================
CREATE TABLE IF NOT EXISTS `roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. TABLA: employees (Empleados)
-- ============================================================================
-- Añadimos tablas maestras necesarias para normalizar datos (ciudades, cargos, bancos, etc.)
CREATE TABLE IF NOT EXISTS `cities` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `positions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `contract_types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `banks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `projects` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `genders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `sizes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `areas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `eps_providers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `marital_statuses` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla employees con referencias a las tablas maestras (campos *_id)
CREATE TABLE IF NOT EXISTS `employees` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `identificacion` BIGINT UNIQUE,
  `nombre` VARCHAR(120) NOT NULL,
  `fecha_nacimiento` DATE,
  `correo` VARCHAR(120) UNIQUE,
  `contacto` BIGINT,
  `direccion` VARCHAR(255),
  `ciudad_id` INT,
  `cargo_id` INT,
  `area_id` INT,
  `role_id` INT,
  `jefe_inmediato` VARCHAR(120),
  `tipo_contrato_id` INT,
  `banco_id` INT,
  `numero_cuenta_bancaria` BIGINT UNIQUE,
  `salario` FLOAT,
  `fecha_ingreso` DATE,
  `proyecto_id` INT,
  `estado` VARCHAR(20) DEFAULT 'activo',
  `genero_id` INT,
  `camisa_id` INT,
  `pantalon` INT,
  `zapatos` INT,
  `abrigo_id` INT,
  `eps_id` INT,
  `estudios` TEXT,
  `estado_civil_id` INT,
  `hijos` INT DEFAULT 0,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `password` VARCHAR(200),
  `is_active` INT DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_identificacion` (`identificacion`),
  KEY `idx_correo` (`correo`),
  KEY `idx_username` (`username`),
  KEY `idx_is_active` (`is_active`),
  CONSTRAINT `fk_employees_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `fk_employees_cities` FOREIGN KEY (`ciudad_id`) REFERENCES `cities` (`id`),
  CONSTRAINT `fk_employees_positions` FOREIGN KEY (`cargo_id`) REFERENCES `positions` (`id`),
  CONSTRAINT `fk_employees_areas` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`),
  CONSTRAINT `fk_employees_contract_types` FOREIGN KEY (`tipo_contrato_id`) REFERENCES `contract_types` (`id`),
  CONSTRAINT `fk_employees_banks` FOREIGN KEY (`banco_id`) REFERENCES `banks` (`id`),
  CONSTRAINT `fk_employees_projects` FOREIGN KEY (`proyecto_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `fk_employees_genders` FOREIGN KEY (`genero_id`) REFERENCES `genders` (`id`),
  CONSTRAINT `fk_employees_camisa_sizes` FOREIGN KEY (`camisa_id`) REFERENCES `sizes` (`id`),
  CONSTRAINT `fk_employees_abrigo_sizes` FOREIGN KEY (`abrigo_id`) REFERENCES `sizes` (`id`),
  CONSTRAINT `fk_employees_eps_providers` FOREIGN KEY (`eps_id`) REFERENCES `eps_providers` (`id`),
  CONSTRAINT `fk_employees_marital_statuses` FOREIGN KEY (`estado_civil_id`) REFERENCES `marital_statuses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. TABLA: vacation_requests (Solicitudes de Vacaciones)
-- ============================================================================
CREATE TABLE IF NOT EXISTS `vacation_requests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_id` INT NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `reason` VARCHAR(255) NOT NULL,
  `status` VARCHAR(20) DEFAULT 'pending',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_employee_id` (`employee_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_vacation_requests_employees` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. TABLA: reports (Reportes)
-- ============================================================================
CREATE TABLE IF NOT EXISTS `reports` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `report_type` VARCHAR(50),
  `status` VARCHAR(20) DEFAULT 'pending',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_employee_id` (`employee_id`),
  KEY `idx_status` (`status`),
  KEY `idx_report_type` (`report_type`),
  CONSTRAINT `fk_reports_employees` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 5. TABLA: attendance (Asistencia)
-- ============================================================================
CREATE TABLE IF NOT EXISTS `attendance` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_id` INT NOT NULL,
  `check_in` DATETIME,
  `check_out` DATETIME,
  `worked_hours` FLOAT DEFAULT 0,
  `attendance_date` DATE NOT NULL,
  `status` VARCHAR(20) DEFAULT 'present',
  `notes` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_employee_id` (`employee_id`),
  KEY `idx_attendance_date` (`attendance_date`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_attendance_employees` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================================
-- MIGRACIÓN: agregar tablas para certificados
-- Fecha: 2025-11-27
-- ============================================================================

CREATE TABLE IF NOT EXISTS `certificate_types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL UNIQUE,
  `description` VARCHAR(255),
  `template` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `certificates` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `certificate_type_id` INT,
  `created_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `subject_name` VARCHAR(200) NOT NULL,
  `subject_identificacion` BIGINT,
  `subject_email` VARCHAR(120),
  `certificate_content` TEXT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_certificates_types` FOREIGN KEY (`certificate_type_id`) REFERENCES `certificate_types` (`id`),
  CONSTRAINT `fk_certificates_employees` FOREIGN KEY (`created_by`) REFERENCES `employees` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- FIN MIGRACIÓN

-- ============================================================================
-- INSERCIÓN DE DATOS INICIALES
-- ============================================================================

-- Insertar Roles
INSERT IGNORE INTO `roles` (`id`, `name`) VALUES
(1, 'admin'),
(2, 'agente'),
(3, 'empleado');

-- Insertar EPS Providers
INSERT IGNORE INTO `eps_providers` (`id`, `name`) VALUES
(1, 'EPS SURA'),
(2, 'EPS Sanitas'),
(3, 'EPS Amedida'),
(4, 'EPS Colmedica'),
(5, 'EPS Coomeva'),
(6, 'EPS Famisanar');

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
