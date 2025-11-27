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
