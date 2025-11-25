# 🔗 INTEGRACIÓN ANGULAR - BACKEND FLASK

## ✅ CONFIGURACIÓN INICIAL

### API Base URL
```
http://localhost:5000
```

### CORS
✅ Ya configurado para `localhost:3000`, `localhost:8080`, `127.0.0.1:3000`

Si tu Angular corre en **otro puerto**, notificame para actualizar `.env`

---

## 🔐 1. AUTENTICACIÓN JWT

### Interceptor HTTP (Angular)

**Crear: `src/app/interceptors/auth.interceptor.ts`**

```typescript
import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private router: Router) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // Agregar token en header
    const token = localStorage.getItem('access_token');
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        // Si token expira (401) → redirigir a login
        if (error.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_id');
          this.router.navigate(['/login']);
        }
        return throwError(() => error);
      })
    );
  }
}
```

**Registrar en `app.module.ts`:**

```typescript
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './interceptors/auth.interceptor';

@NgModule({
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
})
export class AppModule { }
```

---

## 🔐 2. AUTH SERVICE (Angular)

**Crear: `src/app/services/auth.service.ts`**

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, { username, password });
  }

  verify(): Observable<any> {
    return this.http.get(`${this.apiUrl}/auth/verify`);
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/logout`, {});
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  setToken(token: string, userId: number, username: string): void {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_id', userId.toString());
    localStorage.setItem('username', username);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  clearToken(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
  }
}
```

---

## 👥 3. EMPLEADOS - ENDPOINTS Y ANGULAR SERVICE

### 3.1 GET - Listar todos los empleados

```
GET http://localhost:5000/employees/

Response (200):
[
  {
    "id": 1,
    "nombre": "Juan García",
    "identificacion": "1234567890",
    "jefe_inmediato": "Carlos López",
    "proyecto": "Proyecto A",
    "area": "Desarrollo",
    "cargo": "Developer Senior"
  },
  ...
]
```

**Angular:**
```typescript
getEmployees(): Observable<any> {
  return this.http.get(`${this.apiUrl}/employees/`);
}
```

---

### 3.2 GET - Obtener empleado por ID

```
GET http://localhost:5000/employees/1

Response (200):
{
  "id": 1,
  "identificacion": "1234567890",
  "nombre": "Juan García",
  "fecha_nacimiento": "1990-05-15",
  "correo": "juan@example.com",
  "contacto": "3001234567",
  "direccion": "Calle 123",
  "ciudad": "Bogotá",
  "cargo": "Developer Senior",
  "area": "Desarrollo",
  "jefe_inmediato": "Carlos López",
  "salario": 3500000,
  "fecha_ingreso": "2020-01-15",
  "eps": "EPS Sanitas",
  "estado_civil": "Casado",
  "hijos": 2,
  "is_active": true,
  "created_at": "2024-11-01T10:30:00",
  "updated_at": "2024-11-20T15:45:00"
}

Response (404):
{
  "msg": "not found"
}
```

**Angular:**
```typescript
getEmployee(id: number): Observable<any> {
  return this.http.get(`${this.apiUrl}/employees/${id}`);
}
```

---

### 3.3 POST - Crear nuevo empleado

```
POST http://localhost:5000/employees/

Request Body (REQUERIDOS: identificacion, nombre, correo, username, password):
{
  "identificacion": "9876543210",
  "nombre": "María González",
  "correo": "maria@example.com",
  "username": "maria",
  "password": "securepass123",
  "contacto": "3009876543",
  "fecha_nacimiento": "1992-03-20",
  "ciudad_id": 1,
  "cargo_id": 2,
  "area_id": 1,
  "jefe_inmediato": "Juan García",
  "salario": 2500000,
  "fecha_ingreso": "2024-11-25"
}

Response (201 Created):
{
  "id": 2,
  "identificacion": "9876543210",
  "nombre": "María González",
  ...
}

Response (400 Bad Request):
{
  "error": "Campos requeridos faltantes: correo, password"
}
```

**Angular:**
```typescript
createEmployee(employee: any): Observable<any> {
  return this.http.post(`${this.apiUrl}/employees/`, employee);
}
```

---

### 3.4 PUT - Actualizar empleado

```
PUT http://localhost:5000/employees/1

Request Body (OPCIONAL: solo campos a actualizar):
{
  "salario": 4000000,
  "jefe_inmediato": "Carlos López",
  "cargo_id": 3
}

Response (200):
{
  "id": 1,
  "identificacion": "1234567890",
  "nombre": "Juan García",
  "salario": 4000000,
  ...
}

Response (404):
{
  "msg": "not found"
}
```

**Angular:**
```typescript
updateEmployee(id: number, employee: any): Observable<any> {
  return this.http.put(`${this.apiUrl}/employees/${id}`, employee);
}
```

---

### 3.5 DELETE - Inactivar empleado

```
DELETE http://localhost:5000/employees/1

Response (200):
{
  "msg": "employee inactivated",
  "data": {
    "id": 1,
    "nombre": "Juan García",
    "is_active": false,
    ...
  }
}

Response (404):
{
  "msg": "not found"
}
```

**Angular:**
```typescript
deleteEmployee(id: number): Observable<any> {
  return this.http.delete(`${this.apiUrl}/employees/${id}`);
}
```

---

### 3.6 PUT - Toggle Estado Empleado

```
PUT http://localhost:5000/employees/1/toggle-status

Response (200):
{
  "id": 1,
  "nombre": "Juan García",
  "is_active": true,
  ...
}
```

**Angular:**
```typescript
toggleEmployeeStatus(id: number): Observable<any> {
  return this.http.put(`${this.apiUrl}/employees/${id}/toggle-status`, {});
}
```

---

### 3.7 GET - Obtener empleado por Identificación

```
GET http://localhost:5000/employees/identificacion/1234567890

Response (200):
{
  "id": 1,
  "identificacion": "1234567890",
  "nombre": "Juan García",
  ...
}

Response (404):
{
  "msg": "not found"
}
```

**Angular:**
```typescript
getEmployeeByIdentification(identificacion: string): Observable<any> {
  return this.http.get(`${this.apiUrl}/employees/identificacion/${identificacion}`);
}
```

---

## 📅 4. ASISTENCIA - ENDPOINTS

### 4.1 GET - Listar asistencias

```
GET http://localhost:5000/attendance/?employee_id=1&fecha_inicio=2024-11-01&fecha_fin=2024-11-30

Response (200):
[
  {
    "id": 1,
    "employee_id": 1,
    "fecha": "2024-11-25",
    "hora_entrada": "08:30",
    "hora_salida": "17:30",
    "estado": "presente"
  },
  ...
]
```

**Angular:**
```typescript
getAttendance(employeeId: number, fechaInicio: string, fechaFin: string): Observable<any> {
  const params = new HttpParams()
    .set('employee_id', employeeId)
    .set('fecha_inicio', fechaInicio)
    .set('fecha_fin', fechaFin);
  return this.http.get(`${this.apiUrl}/attendance/`, { params });
}
```

---

### 4.2 POST - Registrar asistencia

```
POST http://localhost:5000/attendance/

Request Body (REQUERIDOS: employee_id, fecha, hora_entrada, hora_salida):
{
  "employee_id": 1,
  "fecha": "2024-11-25",
  "hora_entrada": "08:30",
  "hora_salida": "17:30",
  "estado": "presente"
}

Response (201 Created):
{
  "id": 1,
  "employee_id": 1,
  "fecha": "2024-11-25",
  "hora_entrada": "08:30",
  "hora_salida": "17:30",
  "estado": "presente"
}
```

**Angular:**
```typescript
createAttendance(attendance: any): Observable<any> {
  return this.http.post(`${this.apiUrl}/attendance/`, attendance);
}
```

---

## 🏖️ 5. VACACIONES - ENDPOINTS

### 5.1 GET - Listar solicitudes de vacaciones

```
GET http://localhost:5000/vacations/?employee_id=1

Response (200):
[
  {
    "id": 1,
    "employee_id": 1,
    "fecha_inicio": "2024-12-15",
    "fecha_fin": "2024-12-25",
    "cantidad_dias": 10,
    "estado": "aprobada",
    "observaciones": "Vacaciones de fin de año"
  },
  ...
]
```

**Angular:**
```typescript
getVacations(employeeId: number): Observable<any> {
  const params = new HttpParams().set('employee_id', employeeId);
  return this.http.get(`${this.apiUrl}/vacations/`, { params });
}
```

---

### 5.2 POST - Solicitar vacaciones

```
POST http://localhost:5000/vacations/

Request Body (REQUERIDOS: employee_id, fecha_inicio, fecha_fin, cantidad_dias):
{
  "employee_id": 1,
  "fecha_inicio": "2024-12-15",
  "fecha_fin": "2024-12-25",
  "cantidad_dias": 10,
  "observaciones": "Vacaciones de fin de año"
}

Response (201 Created):
{
  "id": 1,
  "employee_id": 1,
  "fecha_inicio": "2024-12-15",
  "fecha_fin": "2024-12-25",
  "cantidad_dias": 10,
  "estado": "pendiente",
  "observaciones": "Vacaciones de fin de año"
}
```

**Angular:**
```typescript
createVacation(vacation: any): Observable<any> {
  return this.http.post(`${this.apiUrl}/vacations/`, vacation);
}
```

---

## 📊 6. REPORTES - ENDPOINTS

### 6.1 POST - Generar reporte de nómina

```
POST http://localhost:5000/reports/payroll

Request Body:
{
  "fecha_inicio": "2024-11-01",
  "fecha_fin": "2024-11-30",
  "format": "pdf"
}

Response (200):
{
  "file_url": "/reports/payroll_2024-11.pdf",
  "total_empleados": 25,
  "total_pagado": 87500000
}
```

**Angular:**
```typescript
generatePayrollReport(fechaInicio: string, fechaFin: string, format: string = 'pdf'): Observable<any> {
  return this.http.post(`${this.apiUrl}/reports/payroll`, {
    fecha_inicio: fechaInicio,
    fecha_fin: fechaFin,
    format
  });
}
```

---

## 📋 7. EMPLOYEE SERVICE COMPLETO (Angular)

**Crear: `src/app/services/employee.service.ts`**

```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EmployeeService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  // CRUD Empleados
  getEmployees(): Observable<any> {
    return this.http.get(`${this.apiUrl}/employees/`);
  }

  getEmployee(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/employees/${id}`);
  }

  getEmployeeByIdentification(identificacion: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/employees/identificacion/${identificacion}`);
  }

  createEmployee(employee: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/employees/`, employee);
  }

  updateEmployee(id: number, employee: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/employees/${id}`, employee);
  }

  deleteEmployee(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/employees/${id}`);
  }

  toggleEmployeeStatus(id: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/employees/${id}/toggle-status`, {});
  }

  // Asistencia
  getAttendance(employeeId: number, fechaInicio: string, fechaFin: string): Observable<any> {
    const params = new HttpParams()
      .set('employee_id', employeeId)
      .set('fecha_inicio', fechaInicio)
      .set('fecha_fin', fechaFin);
    return this.http.get(`${this.apiUrl}/attendance/`, { params });
  }

  createAttendance(attendance: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/attendance/`, attendance);
  }

  // Vacaciones
  getVacations(employeeId: number): Observable<any> {
    const params = new HttpParams().set('employee_id', employeeId);
    return this.http.get(`${this.apiUrl}/vacations/`, { params });
  }

  createVacation(vacation: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/vacations/`, vacation);
  }

  // Reportes
  generatePayrollReport(fechaInicio: string, fechaFin: string, format: string = 'pdf'): Observable<any> {
    return this.http.post(`${this.apiUrl}/reports/payroll`, {
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
      format
    });
  }
}
```

---

## 🔑 8. HEADERS REQUERIDOS

**Todos los endpoints EXCEPTO `POST /auth/login` requieren:**

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

✅ El **interceptor** lo agrega automáticamente

---

## 📅 9. FORMATOS DE DATOS

| Campo | Formato | Ejemplo |
|-------|---------|---------|
| Fechas | YYYY-MM-DD | 2024-11-25 |
| Horas | HH:MM | 08:30 |
| Dinero | Float | 3500000 |
| IDs | Integer | 1, 2, 3 |
| Booleans | true/false | true |

---

## 🛡️ 10. MANEJO DE ERRORES EN ANGULAR

```typescript
this.employeeService.getEmployees().subscribe({
  next: (employees) => {
    console.log('Empleados cargados:', employees);
  },
  error: (error) => {
    if (error.status === 401) {
      console.error('No autorizado');
    } else if (error.status === 404) {
      console.error('Recurso no encontrado');
    } else if (error.status === 400) {
      console.error('Error en datos:', error.error.error);
    } else {
      console.error('Error del servidor:', error.error.msg);
    }
  }
});
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Interceptor HTTP configurado
- [ ] AuthService creado
- [ ] EmployeeService creado
- [ ] Login implementado
- [ ] Token guardado en localStorage
- [ ] Rutas protegidas implementadas
- [ ] Listado de empleados funcionando
- [ ] CRUD de empleados funcionando
- [ ] Asistencia funcionando
- [ ] Vacaciones funcionando
- [ ] Reportes funcionando
- [ ] Manejo de errores (401, 404, 400, 500)
- [ ] Testing end-to-end completado
