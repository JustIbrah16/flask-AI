# Ejemplos de Uso - HR Platform API

## Flujo de Check-In / Check-Out

### 1. Empleado hace check-in (entrada)
```bash
curl -X POST http://localhost:5000/attendance/employee/1/check-in
```
**Response:**
```json
{
  "id": 1,
  "employee_id": 1,
  "check_in": "2025-11-25T08:00:00",
  "check_out": null,
  "worked_hours": 0,
  "attendance_date": "2025-11-25",
  "status": "present",
  "notes": null
}
```

### 2. Empleado hace check-out (salida)
```bash
curl -X POST http://localhost:5000/attendance/employee/1/check-out
```
**Response:**
```json
{
  "id": 1,
  "employee_id": 1,
  "check_in": "2025-11-25T08:00:00",
  "check_out": "2025-11-25T17:30:00",
  "worked_hours": 9.5,
  "attendance_date": "2025-11-25",
  "status": "present",
  "notes": null
}
```

### 3. Ver resumen de asistencia de un mes
```bash
curl -X GET "http://localhost:5000/attendance/employee/1/summary?from_date=2025-11-01&to_date=2025-11-30"
```
**Response:**
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
  "to_date": "2025-11-30"
}
```

## Flujo de Solicitudes de Vacaciones

### 1. Empleado envía solicitud de vacaciones
```bash
curl -X POST http://localhost:5000/vacations/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "start_date": "2025-12-01",
    "end_date": "2025-12-10",
    "reason": "Personal leave"
  }'
```
**Response:**
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

### 2. Agente aprueba la solicitud
```bash
curl -X PUT http://localhost:5000/vacations/1/approve
```
**Response:**
```json
{
  "id": 1,
  "employee_id": 1,
  "start_date": "2025-12-01",
  "end_date": "2025-12-10",
  "reason": "Personal leave",
  "status": "approved",
  "created_at": "2025-11-25T10:30:00"
}
```

### 3. Agente rechaza la solicitud
```bash
curl -X PUT http://localhost:5000/vacations/1/reject
```

### 4. Ver todas las solicitudes de un empleado
```bash
curl -X GET http://localhost:5000/vacations/employee/1
```

## Flujo de Reportes

### 1. Empleado envía un reporte
```bash
curl -X POST http://localhost:5000/reports/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "title": "Incident Report",
    "description": "Equipment malfunction in section A",
    "report_type": "incident",
    "status": "pending"
  }'
```
**Response:**
```json
{
  "id": 1,
  "employee_id": 1,
  "title": "Incident Report",
  "description": "Equipment malfunction in section A",
  "report_type": "incident",
  "status": "pending",
  "created_at": "2025-11-25T10:30:00",
  "updated_at": "2025-11-25T10:30:00"
}
```

### 2. Agente revisa y cambia status
```bash
curl -X PUT http://localhost:5000/reports/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "reviewed"
  }'
```

### 3. Ver todos los reportes de un empleado
```bash
curl -X GET http://localhost:5000/reports/employee/1
```

## Gestión de Empleados

### 1. Crear nuevo empleado
```bash
curl -X POST http://localhost:5000/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "role_id": 3,
    "password": "secure_password"
  }'
```

### 2. Editar empleado
```bash
curl -X PUT http://localhost:5000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated",
    "phone": "9876543210"
  }'
```

### 3. Inactivar empleado
```bash
curl -X DELETE http://localhost:5000/employees/1
```
**Response:**
```json
{
  "msg": "employee inactivated",
  "data": {
    "id": 1,
    "username": "john_doe",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "role_id": 3,
    "is_active": false,
    "created_at": "2025-11-25T08:00:00",
    "updated_at": "2025-11-25T18:00:00"
  }
}
```

### 4. Reactivar empleado
```bash
curl -X PUT http://localhost:5000/employees/1/toggle-status
```

### 5. Ver todos los empleados
```bash
curl -X GET http://localhost:5000/employees/
```

## Autenticación

### 1. Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password"
  }'
```
**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Usar token en peticiones protegidas
```bash
curl -X GET http://localhost:5000/auth/profile \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```
