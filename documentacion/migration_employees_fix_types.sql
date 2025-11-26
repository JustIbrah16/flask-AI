-- ============================================================================
-- SCRIPT DE MIGRACIÓN: CORREGIR TIPOS DE DATOS EN TABLA EMPLOYEES
-- ============================================================================
-- Fecha: 2025-11-26
-- Descripción: Cambiar campos que fueron mal definidos como VARCHAR/STRING
--              a sus tipos correctos (INTEGER, BIGINT)
-- ============================================================================

-- Paso 1: Convertir columnas de tipos de datos
-- Convertir identificacion de VARCHAR(50) a BIGINT
ALTER TABLE `employees` 
MODIFY COLUMN `identificacion` BIGINT UNIQUE;

-- Convertir contacto de VARCHAR(20) a BIGINT
ALTER TABLE `employees` 
MODIFY COLUMN `contacto` BIGINT NULL;

-- Convertir numero_cuenta_bancaria de VARCHAR(50) a BIGINT
ALTER TABLE `employees` 
MODIFY COLUMN `numero_cuenta_bancaria` BIGINT UNIQUE;

-- Convertir pantalon de VARCHAR(10) a INT
ALTER TABLE `employees` 
MODIFY COLUMN `pantalon` INT NULL;

-- Convertir zapatos de VARCHAR(10) a INT
ALTER TABLE `employees` 
MODIFY COLUMN `zapatos` INT NULL;

-- Convertir is_active de BOOLEAN a INT (valores: 0=inactivo, 1=activo, 2=licencia)
ALTER TABLE `employees` 
MODIFY COLUMN `is_active` INT DEFAULT 1;

-- Paso 2: Recrear índices si es necesario
-- (Los índices se mantienen automáticamente)

-- ============================================================================
-- FIN DE LA MIGRACIÓN
-- ============================================================================
-- NOTAS IMPORTANTES:
-- 1. Los datos de pantalon y zapatos ahora son números enteros (INT)
-- 2. identificacion, contacto y numero_cuenta_bancaria ahora son BIGINT
-- 3. is_active ahora es INT: 0=inactivo, 1=activo, 2=licencia
-- 4. Asegúrate de hacer BACKUP de tu BD antes de ejecutar este script
-- 5. Después de ejecutar, verifica que los datos sean correctos con: DESC employees;
-- ============================================================================

