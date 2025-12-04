-- ============================================================================
-- HR PLATFORM - SCRIPT DE DATOS DE PRUEBA
-- ============================================================================
-- Este script contiene datos de ejemplo para probar la API
-- ============================================================================

-- ============================================================================
-- Este archivo de documentación contiene el mismo seed que el principal, actualizado para usar las tablas maestras y los campos *_id.

-- (Se insertan los mismos datos que en `database_seed_test_data.sql`)

-- Ciudades
INSERT IGNORE INTO `cities` (`id`, `name`) VALUES
(1, 'Bogotá'),
(2, 'Medellín'),
(3, 'Cali'),
(4, 'Barranquilla'),
(5, 'Bucaramanga');

-- Cargos / positions
INSERT IGNORE INTO `positions` (`id`, `name`) VALUES
(1, 'Directora General'),
(2, 'Gerente de Recursos Humanos'),
(3, 'Coordinadora de Proyectos'),
(4, 'Ingeniero de Software'),
(5, 'Diseñadora Gráfica'),
(6, 'Contador');

-- Tipos de contrato
INSERT IGNORE INTO `contract_types` (`id`, `name`) VALUES
(1, 'Temporal'),
(2, 'Indefinido'),
(3, 'Prestación de servicios');

-- Bancos
INSERT IGNORE INTO `banks` (`id`, `name`) VALUES
(1, 'Bancolombia'),
(2, 'Davivienda'),
(3, 'Banco de Bogotá'),
(4, 'Banco Popular'),
(5, 'BBVA');

-- Proyectos
INSERT IGNORE INTO `projects` (`id`, `name`) VALUES
(1, 'Proyecto A'),
(2, 'Proyecto B'),
(3, 'Proyecto C'),
(4, 'Admin');

-- Géneros
INSERT IGNORE INTO `genders` (`id`, `name`) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Otro'),
(4, 'No especificado');

-- Áreas
INSERT IGNORE INTO `areas` (`id`, `name`) VALUES
(1, 'Administración'),
(2, 'RRHH'),
(3, 'Proyectos'),
(4, 'Tecnología'),
(5, 'Marketing'),
(6, 'Finanzas');

-- EPS (Empresas Promotoras de Salud)
INSERT IGNORE INTO `health_insurances` (`id`, `name`) VALUES
(1, 'Sanitas'),
(2, 'Axa Colpatria'),
(3, 'Coomeva'),
(4, 'SURA');

-- Tallas (para camisa y abrigo)
INSERT IGNORE INTO `sizes` (`id`, `name`) VALUES
(1, 'XS'),
(2, 'S'),
(3, 'M'),
(4, 'L'),
(5, 'XL'),
(6, 'XXL');

-- Estados civiles
INSERT IGNORE INTO `marital_statuses` (`id`, `name`) VALUES
(1, 'Soltero'),
(2, 'Casado'),
(3, 'Unión libre'),
(4, 'Divorciado'),
(5, 'Viudo');

INSERT INTO `arl_providers` (`id`, `name`) VALUES
(1,'ARL Sura'),
(2,'ARL Bolívar'),
(3,'ARL Colmena'),
(4,'ARL Positiva'),
(5,'ARL Seguros de Vida Alfa');
-- Empleados (documentación): mismos valores que el script principal
INSERT INTO `employees` (
  `id`, `identificacion`, `nombre`, `fecha_nacimiento`, `correo`, `contacto`,
  `direccion`, `ciudad_id`, `cargo_id`, `area_id`, `role_id`,
  `jefe_inmediato`, `tipo_contrato_id`, `banco_id`, `numero_cuenta_bancaria`,
  `salario`, `fecha_ingreso`, `proyecto_id`, `estado`,
  `genero_id`, `camisa_id`, `pantalon`, `zapatos`, `abrigo_id`, `eps_id`,
  `estudios`, `estado_civil_id`, `hijos`, `username`, `password`, `is_active`, `created_at`, `updated_at`
) VALUES
(1, 'ADM001', 'María González Rodríguez', '1985-03-20', 'maria.admin@company.com', '+57 1 2345001',
  'Calle Admin 100', 1, 1, 1, 1,
  'Junta Directiva', 2, 3, '100000001',
  5000000, '2020-01-15', 4, 'activo',
  2, 3, '34', '37', 3, 1,
  'Administración Empresarial - Universidad de los Andes', 2, 2, 'maria_admin', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', TRUE, NOW(), NOW()),

(2, 'AGE001', 'Carlos Mendez Silva', '1988-07-10', 'carlos.agente@company.com', '+57 1 2345002',
  'Calle Principal 200', 1, 2, 2, 2,
  'María González Rodríguez', 2, 5, '200000001',
  3500000, '2021-03-20', 1, 'activo',
  1, 4, '32', '42', 2, 2,
  'Psicología - Pontificia Universidad Javeriana', 1, 0, 'carlos_agente', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', TRUE, NOW(), NOW()),

(3, 'AGE002', 'Laura Fernández López', '1992-11-25', 'laura.agente@company.com', '+57 1 2345003',
  'Calle Secundaria 300', 2, 3, 3, 2,
  'María González Rodríguez', 2, 1, '300000001',
  3200000, '2022-06-10', 2, 'activo',
  2, 2, '26', '36', 2, 1,
  'Ingeniería de Proyectos - EAFIT', 4, 1, 'laura_agente', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', TRUE, NOW(), NOW()),

(4, 'EMP001', 'Juan David Pérez García', '1995-02-14', 'juan.perez@company.com', '+57 1 2345004',
  'Calle Tercera 400', 1, 4, 4, 3,
  'Carlos Mendez Silva', 2, 3, '400000001',
  2800000, '2023-01-15', 1, 'activo',
  1, 3, '30', '40', 2, 1,
  'Ingeniería de Sistemas - Universidad Nacional', 1, 0, 'juan_perez', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', TRUE, NOW(), NOW()),

(5, 'EMP002', 'Sofía Rodríguez Martínez', '1993-09-08', 'sofia.rodriguez@company.com', '+57 1 2345005',
  'Calle Cuarta 500', 1, 5, 5, 3,
  'Laura Fernández López', 1, 5, '500000001',
  2500000, '2023-06-01', 2, 'activo',
  2, 2, '28', '38', 1, 3,
  'Diseño Gráfico - SENA', 1, 0, 'sofia_rodriguez', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', TRUE, NOW(), NOW()),

(6, 'EMP003', 'Roberto Gutiérrez Ramírez', '1990-12-03', 'roberto.gutierrez@company.com', '+57 1 2345006',
  'Calle Quinta 600', 3, 6, 6, 3,
  'Carlos Mendez Silva', 2, 1, '600000001',
  2600000, '2022-03-15', 3, 'inactivo',
  1, 5, '34', '44', 4, 1,
  'Contabilidad - Universidad del Valle', 2, 3, 'roberto_gutierrez', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', FALSE, NOW(), NOW());
  'roberto_gutierrez', '$2b$12$gSvqqUPHg0sCNPPMdK2KCOYt8S.dh6j/QVz1z0K0.p0X.Z0zJ6BVm', FALSE
);

-- ============================================================================
-- INSERCIÓN DE SOLICITUDES DE VACACIONES DE PRUEBA
-- ============================================================================

INSERT INTO `vacation_requests` (
  `employee_id`, `start_date`, `end_date`, `reason`, `status`
) VALUES
(4, '2025-12-01', '2025-12-10', 'Vacaciones personales', 'pending'),
(4, '2025-12-20', '2025-12-31', 'Vacaciones de fin de año', 'approved'),
(5, '2025-11-28', '2025-11-30', 'Fin de semana largo', 'pending'),
(6, '2025-12-15', '2025-12-17', 'Asuntos personales', 'rejected');

-- ============================================================================
-- INSERCIÓN DE REPORTES DE PRUEBA
-- ============================================================================

INSERT INTO `reports` (
  `employee_id`, `title`, `description`, `report_type`, `status`
) VALUES
(4, 'Reporte Diario - Desarrollo API', 'Se completó la implementación del módulo de asistencia con cálculo automático de horas.', 'daily', 'reviewed'),
(5, 'Reporte Semanal - Diseño', 'Se diseñaron 5 nuevas pantallas para el módulo de reportes.', 'weekly', 'pending'),
(6, 'Reporte de Incidente', 'Problema con el servidor de base de datos en la mañana del 25 de noviembre.', 'incident', 'closed'),
(4, 'Reporte Mensual - Avances', 'Se completó el 85% de las tareas planificadas para noviembre.', 'monthly', 'pending');

-- ============================================================================
-- INSERCIÓN DE REGISTROS DE ASISTENCIA DE PRUEBA
-- ============================================================================

INSERT INTO `attendance` (
  `employee_id`, `check_in`, `check_out`, `worked_hours`, `attendance_date`, `status`, `notes`
) VALUES
(4, '2025-11-24 08:00:00', '2025-11-24 17:30:00', 9.5, '2025-11-24', 'present', 'Día normal'),
(4, '2025-11-25 08:15:00', '2025-11-25 17:45:00', 9.5, '2025-11-25', 'present', 'Llego 15 minutos tarde'),
(5, '2025-11-24 08:00:00', '2025-11-24 17:00:00', 9.0, '2025-11-24', 'present', 'Día normal'),
(5, '2025-11-25 08:30:00', NULL, 0, '2025-11-25', 'present', 'Aún en jornada laboral'),
(6, '2025-11-24 08:00:00', '2025-11-24 12:00:00', 4.0, '2025-11-24', 'half-day', 'Medio día'),
(6, NULL, NULL, 0, '2025-11-25', 'absent', 'No asistió');






-- Insertar EPS Providers
INSERT IGNORE INTO `eps_providers` (`id`, `name`) VALUES
(1, 'EPS SURA'),
(2, 'EPS Sanitas'),
(3, 'EPS Amedida'),
(4, 'EPS Colmedica'),
(5, 'EPS Coomeva'),
(6, 'EPS Famisanar'),
(7, 'EPS Nueva'),
(8, 'EPS Alianza'),
(9, 'EPS Servimos'),
(10, 'EPS Compensar');

-- ============================================================================
-- FIN DEL SCRIPT DE DATOS DE PRUEBA
-- ============================================================================

-- Notas:
-- 1. Las contraseñas están hasheadas con bcrypt. El valor mostrado es para la contraseña "password123"
-- 2. Todos los usuarios pueden usarse para login
-- 3. Los datos son solo para pruebas y deben ser reemplazados en producción
