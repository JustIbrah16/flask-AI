# Guía de Instalación de Base de Datos

## 📁 Archivos SQL Disponibles

1. **`database_schema.sql`** - Crear tablas (REQUERIDO)
2. **`database_seed_test_data.sql`** - Datos de prueba (OPCIONAL)

## 🚀 Instalación Paso a Paso

### Opción 1: Usando MySQL Command Line

#### 1. Seleccionar la base de datos
```bash
mysql -u root -p
```
```sql
USE project;
```

#### 2. Ejecutar el script de tablas
```sql
SOURCE /ruta/a/database_schema.sql;
```

#### 3. (Opcional) Ejecutar datos de prueba
```sql
SOURCE /ruta/a/database_seed_test_data.sql;
```

### Opción 2: Usando Línea de Comandos

#### 1. Crear tablas
```bash
mysql -u root -p project < database_schema.sql
```

#### 2. (Opcional) Agregar datos de prueba
```bash
mysql -u root -p project < database_seed_test_data.sql
```

### Opción 3: Usando MySQL Workbench

1. Abrir MySQL Workbench
2. Seleccionar la conexión a tu servidor
3. File → Open SQL Script → Seleccionar `database_schema.sql`
4. Ejecutar (Ctrl + Shift + Enter o ⌘ + Shift + Enter)
5. Repetir para `database_seed_test_data.sql` si deseas datos de prueba

### Opción 4: Usando phpMyAdmin

1. Acceder a phpMyAdmin en tu servidor
2. Seleccionar la base de datos `project`
3. Click en "Import" o "Importar"
4. Seleccionar `database_schema.sql`
5. Click en "Go" o "Ejecutar"
6. Repetir para `database_seed_test_data.sql` si deseas

## 📊 Estructura de Tablas Creadas

### 1. **roles** (3 registros)
- id, name
- Valores: admin, agente, empleado

### 2. **employees** (5-6 registros de prueba)
- Información personal, laboral, bancaria
- Autenticación (username, password)
- Estado (activo/inactivo)

### 3. **vacation_requests** (4 registros de prueba)
- Solicitudes de vacaciones
- Estados: pending, approved, rejected

### 4. **reports** (4 registros de prueba)
- Reportes de empleados
- Tipos: daily, weekly, monthly, incident
- Estados: pending, reviewed, closed

### 5. **attendance** (6 registros de prueba)
- Registros de asistencia
- Check-in/Check-out
- Horas trabajadas calculadas

## 🔐 Credenciales de Prueba

Todos los usuarios de prueba usan la contraseña: **`password123`**

| Username | Rol | Email |
|----------|-----|-------|
| maria_admin | Admin | maria.admin@company.com |
| carlos_agente | Agente | carlos.agente@company.com |
| laura_agente | Agente | laura.agente@company.com |
| juan_perez | Empleado | juan.perez@company.com |
| sofia_rodriguez | Empleado | sofia.rodriguez@company.com |
| roberto_gutierrez | Empleado (Inactivo) | roberto.gutierrez@company.com |

## ✅ Verificar Instalación

### Ver todas las tablas
```sql
SHOW TABLES;
```

### Ver estructura de una tabla
```sql
DESCRIBE employees;
```

### Contar registros
```sql
SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM roles;
SELECT COUNT(*) FROM vacation_requests;
SELECT COUNT(*) FROM reports;
SELECT COUNT(*) FROM attendance;
```

### Listar todos los empleados
```sql
SELECT numero, nombre, correo, cargo, is_active FROM employees;
```

### Listar roles
```sql
SELECT * FROM roles;
```

## 🔄 Limpiar Base de Datos

### Eliminar todos los datos (mantiene tablas)
```sql
DELETE FROM attendance;
DELETE FROM reports;
DELETE FROM vacation_requests;
DELETE FROM employees;
DELETE FROM roles;
```

### Eliminar tablas completamente
```sql
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS vacation_requests;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS roles;
```

## 🐛 Solución de Problemas

### Error: "Access Denied for user 'root'@'localhost'"
```bash
mysql -u root -p project < database_schema.sql
# Ingresa tu contraseña cuando se solicite
```

### Error: "Unknown database 'project'"
Primero crea la base de datos:
```sql
CREATE DATABASE IF NOT EXISTS project;
USE project;
SOURCE database_schema.sql;
```

### Error: "Duplicate entry for key"
Los scripts usan `INSERT IGNORE`, así que es seguro ejecutarlos múltiples veces.

### Contraseñas hasheadas no funcionan
Las contraseñas en `database_seed_test_data.sql` están hasheadas con bcrypt.
Usar la contraseña original: `password123`

## 📝 Notas Importantes

1. **Backup:** Siempre hacer backup antes de ejecutar scripts en producción
2. **Prueba primero:** Ejecuta los scripts en un ambiente de desarrollo primero
3. **Caracteres especiales:** Las tablas usan UTF-8 para soporte de caracteres españoles
4. **Índices:** Se crearon índices en campos de búsqueda frecuente para mejor rendimiento
5. **Foreign Keys:** Todas las relaciones tienen constraints para integridad referencial

## 🔗 Próximos Pasos

1. ✅ Ejecutar `database_schema.sql`
2. ✅ Ejecutar `database_seed_test_data.sql` (opcional, para pruebas)
3. ✅ Iniciar la aplicación Flask: `python app.py`
4. ✅ Acceder a Swagger: `http://localhost:5000/docs`
5. ✅ Login con credenciales de prueba

## 📞 Soporte

Si tienes problemas:
1. Verifica que MySQL está corriendo
2. Verifica que tienes permisos en la BD
3. Revisa los logs de MySQL
4. Intenta ejecutar el script en partes
