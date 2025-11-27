# HR Platform API Documentation

## Overview
Esta es una REST API para un sistema de Recursos Humanos con 3 roles:
- **Admin**: Solo visualización de toda la información
- **Agente**: Gestión completa de empleados, vacaciones y reportes
- **Empleado**: Enviar solicitudes de vacaciones y reportes

## Endpoints

### Authentication (`/auth`)
- `POST /auth/login` - Login con username/password
  ```json
  {"username": "...", "password": "..."}
  ```
  Retorna:
  ```json
  {
    "message": "Inicio de sesión exitoso",
    "access_token": "...",
    "user_id": 1,
    "username": "someuser"
  }
  ```

- `POST /auth/register` - Registrar nuevo usuario (solo admin/agente)
  ```json
  {"username": "...", "password": "...", "email": "...", "full_name": "...", "phone": "...", "role_id": 1}
  ```

- `GET /auth/profile` - Obtener perfil del usuario actual (requiere JWT)

### Employees (`/employees`)
- `GET /employees/` - Listar todos los empleados
- `POST /employees/` - Crear nuevo empleado (solo admin/agente)
- `GET /employees/<id>` - Obtener detalles de un empleado
- `PUT /employees/<id>` - Editar empleado (admin/agente)
- `DELETE /employees/<id>` - Inactivar empleado (no elimina, solo marca como inactivo)
- `PUT /employees/<id>/toggle-status` - Activar/inactivar empleado (admin/agente)

### Vacations (`/vacations`)
- `GET /vacations/` - Listar todas las solicitudes de vacaciones (admin/agente)
- `POST /vacations/` - Crear solicitud de vacaciones (empleado/agente)
- `GET /vacations/<id>` - Obtener detalles de una solicitud
- `PUT /vacations/<id>` - Actualizar solicitud
- `DELETE /vacations/<id>` - Eliminar solicitud
- `PUT /vacations/<id>/approve` - Aprobar solicitud (solo agente)
- `PUT /vacations/<id>/reject` - Rechazar solicitud (solo agente)
- `GET /vacations/employee/<employee_id>` - Obtener vacaciones de un empleado

### Reports (`/reports`)
- `GET /reports/` - Listar todos los reportes (admin/agente)
- `POST /reports/` - Crear reporte (empleado/agente)
- `GET /reports/<id>` - Obtener detalles de un reporte
- `PUT /reports/<id>` - Actualizar reporte (status: pending, reviewed, closed)
- `DELETE /reports/<id>` - Eliminar reporte
- `GET /reports/employee/<employee_id>` - Obtener reportes de un empleado
- `GET /reports/attendance-summary` - Resumen de asistencia

### Attendance (`/attendance`)
- `GET /attendance/` - Listar todos los registros de asistencia
- `POST /attendance/` - Crear registro manual de asistencia
- `GET /attendance/<id>` - Obtener detalles de un registro
- `GET /attendance/employee/<employee_id>` - Listar asistencia de un empleado (con filtros opcionales: `from_date`, `to_date`)
- `GET /attendance/employee/<employee_id>/today` - Obtener asistencia de hoy
- `POST /attendance/employee/<employee_id>/check-in` - Registrar entrada (check-in)
- `POST /attendance/employee/<employee_id>/check-out` - Registrar salida (check-out) y calcular horas trabajadas
- `GET /attendance/employee/<employee_id>/summary` - Resumen de asistencia y horas (requiere `from_date` y `to_date`)

### Certificates (`/certificates`)
- `GET /certificates/employee/<employee_id>` - Listar certificados de un empleado.
- `POST /certificates/employee/<employee_id>` - Solicitar un nuevo certificado (ej. laboral).
- `GET /certificates/<id>` - Descargar un certificado.

## Models

### Employee (Completo)
```json
{
  "id": 1,
  "identificacion": "EMP001",
  "nombre": "John Doe",
  "fecha_nacimiento": "1990-05-15",
  "correo": "john@example.com",
  "contacto": "1234567890",
  "direccion": "Calle Principal 123",
  "ciudad": "Bogotá",
  "cargo": "Ingeniero de Software",
  "area": "Tecnología",
  "role_id": 2,
  "jefe_inmediato": "Juan García",
  "tipo_contrato": "Indefinido",
  "banco": "Banco de Bogotá",
  "numero_cuenta_bancaria": "123456789",
  "salario": 3500000.0,
  "fecha_ingreso": "2025-01-15",
  "proyecto": "Proyecto A / CC-001",
  "estado": "activo",
  "genero": "Masculino",
  "camisa": "M",
  "pantalon": "32",
  "zapatos": "42",
  "abrigo": "L",
  "eps": "Sanitas",
  "estudios": "Ingeniería de Sistemas - Universidad Nacional",
  "estado_civil": "Casado",
  "hijos": 2,
  "is_active": true,
  "created_at": "2025-11-25T10:30:00",
  "updated_at": "2025-11-25T10:30:00"
}
```

### VacationRequest
```json
{
  "id": 1,
  "employee_id": 1,
  "start_date": "2025-12-01",
  "end_date": "2025-12-10",
  "reason": "Personal leave",
  "status": "pending",
  "created_at": "2025-11-25T10:30:00"
}
```

### Report
```json
{
  "id": 1,
  "employee_id": 1,
  "title": "Monthly Report",
  "description": "Report description...",
  "report_type": "monthly",
  "status": "pending",
  "created_at": "2025-11-25T10:30:00",
  "updated_at": "2025-11-25T10:30:00"
}
```

### Attendance
```json
{
  "id": 1,
  "employee_id": 1,
  "check_in": "2025-11-25T08:00:00",
  "check_out": "2025-11-25T17:30:00",
  "worked_hours": 9.5,
  "attendance_date": "2025-11-25",
  "status": "present",
  "notes": "Regular day",
  "created_at": "2025-11-25T08:00:00",
  "updated_at": "2025-11-25T17:30:00"
}
```

### Attendance Summary
```json
{
  "employee_id": 1,
  "total_days": 20,
  "total_hours": 190.5,
  "present_days": 19,
  "absent_days": 1,
  "late_days": 0,
  "average_hours_per_day": 9.53,
  "from_date": "2025-11-01",
  "to_date": "2025-11-25"
}
```

### Certificate
```json
{
  "id": 1,
  "employee_id": 1,
  "certificate_type": "laboral",
  "issue_date": "2025-11-26",
  "status": "generated",
  "url": "/certificates/1/download",
  "created_at": "2025-11-26T09:00:00"
}
```

## Status Codes

- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API disponible en: `http://localhost:5000`
Swagger docs en: `http://localhost:5000/docs`

## Resumen de Capacidades de la Plataforma

La plataforma de Recursos Humanos ofrece una solución integral para la gestión de personal, con funcionalidades específicas para diferentes roles dentro de la organización (Administrador, Agente y Empleado).

Las capacidades clave incluyen:

*   **Gestión de Empleados:** Creación, visualización, actualización y desactivación de perfiles de empleados. Almacena información detallada que va desde datos personales y de contacto hasta información contractual y salarial.
*   **Control de Vacaciones:** Los empleados pueden solicitar vacaciones, y los agentes pueden gestionar estas solicitudes (aprobar o rechazar), manteniendo un registro claro del historial de vacaciones de cada empleado.
*   **Sistema de Reportes:** Permite a los empleados enviar reportes (por ejemplo, reportes mensuales o de incidentes), que luego pueden ser revisados y gestionados por los agentes.
*   **Seguimiento de Asistencia:** Registra las horas de entrada y salida de los empleados, calcula las horas trabajadas y proporciona resúmenes de asistencia para un control eficiente del tiempo y la productividad.
*   **Generación de Certificados:** Permite a los empleados solicitar y descargar certificados (ej. laborales) de forma automática.
*   **Autenticación y Seguridad:** Sistema de autenticación basado en JWT para proteger los endpoints y garantizar que los usuarios solo accedan a la información y funcionalidades permitidas por su rol.

Esta API centraliza las operaciones de recursos humanos, facilitando la administración del personal y mejorando la comunicación entre los empleados y el departamento de RRHH.
