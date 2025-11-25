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

## 3️⃣ ESTRUCTURA DE RESPUESTAS

### Login (200 OK):
```json
{
  "access_token": "eyJ0eXA...",
  "user_id": 1,
  "username": "juan"
}
```

### Error (401 Unauthorized):
```json
{
  "msg": "Invalid credentials",
  "code": "INVALID_CREDENTIALS"
}
```

### Empleados - Listado (200 OK):
```json
[
  {
    "id": 1,
    "nombre": "Juan García",
    "identificacion": "1234567890",
    "jefe_inmediato": "Carlos López",
    "proyecto": "Proyecto A",
    "area": "Desarrollo",
    "cargo": "Developer Senior"
  }
]
```

### Empleados - Detalle (200 OK):
```json
{
  "id": 1,
  "identificacion": "1234567890",
  "nombre": "Juan García",
  "correo": "juan@example.com",
  "contacto": "3001234567",
  "ciudad": "Bogotá",
  "cargo": "Developer Senior",
  "area": "Desarrollo",
  "salario": 3500000,
  "is_active": true,
  "created_at": "2024-11-01T10:30:00",
  "updated_at": "2024-11-20T15:45:00"
  // ... más campos
}
```

---

## 4️⃣ VALIDACIÓN DE DATOS

### Campos Requeridos por Endpoint:

**POST /auth/login**
- `username` (string)
- `password` (string)

**POST /employees/**
- `identificacion` (string)
- `nombre` (string)
- `correo` (string)
- `username` (string)
- `password` (string)

**POST /attendance/**
- `employee_id` (integer)
- `fecha` (date: YYYY-MM-DD)
- `hora_entrada` (time: HH:MM)
- `hora_salida` (time: HH:MM)

**POST /vacations/**
- `employee_id` (integer)
- `fecha_inicio` (date: YYYY-MM-DD)
- `fecha_fin` (date: YYYY-MM-DD)
- `cantidad_dias` (integer)

---

## 5️⃣ FLUJOS ESPECÍFICOS

### Flujo de Login

```
Usuario escribe credenciales
    ↓
Frontend valida formato (email, password no vacío)
    ↓
POST /auth/login { username, password }
    ↓
Backend valida en BD
    ↓
¿Válido? 
  SÍ → Devuelve { access_token, user_id, username }
  NO → Devuelve { msg, code } con status 401
    ↓
Frontend guarda token en localStorage
    ↓
Frontend redirige a /dashboard
```

### Flujo de Crear Empleado

```
Usuario completa formulario
    ↓
Frontend valida campos requeridos
    ↓
Frontend envía POST /employees/ con:
  - Headers: Authorization: Bearer <token>
  - Body: { id, username, nombre, correo, ... }
    ↓
Backend valida JWT
    ↓
Backend valida datos (requeridos, formatos)
    ↓
¿Válido?
  SÍ → Crea en BD, devuelve 201 + datos
  NO → Devuelve 400 + error
    ↓
Frontend muestra confirmación o error
```

---

## 6️⃣ TESTING RECOMENDADO

### Antes de integrar a producción:

1. **Test de Autenticación**
   - Login con credenciales correctas ✅
   - Login con credenciales incorrectas ✅
   - Acceder endpoint protegido sin token → debe rechazar ✅
   - Token expirado → debe redirigir a login ✅

2. **Test de CRUD Empleados**
   - GET /employees/ → lista 200+ empleados ✅
   - GET /employees/1 → devuelve detalles ✅
   - POST /employees/ → crea nuevo ✅
   - PUT /employees/1 → actualiza ✅
   - DELETE /employees/1 → inactiva ✅

3. **Test de Errores**
   - Error 400: campos faltantes ✅
   - Error 401: sin autorización ✅
   - Error 404: recurso no existe ✅
   - Error 500: error servidor ✅

---

## 7️⃣ HEADER REQUERIDO

**Todos los endpoints excepto `/auth/login` requieren:**

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Sin este header → Respuesta 401

---

## 8️⃣ TIPOS DE DATOS

### Fechas
- Formato: `YYYY-MM-DD` (ISO 8601)
- Ejemplo: `2024-11-25`
- Backend acepta string y convierte a date

### Horas
- Formato: `HH:MM` (24 horas)
- Ejemplo: `08:30`, `17:45`

### Números
- Dinero: Float con 2 decimales
- IDs: Integer
- Teléfono: String (puede tener caracteres especiales)

### Booleanos
- `true` / `false` (JSON)
- No usar strings `"true"` / `"false"`

---

## 9️⃣ PERFORMANCE & LIMITACIONES

### Rate Limiting
- No implementado en este backend (considerar agregar)
- Recomendación: Max 100 requests/minuto por IP

### Paginación
- Por implementar en endpoints de listado
- Recomendación: Agregar `page` y `limit` parameters

### Caching
- Considerar cachear GET /employees/ (datos relativamente estáticos)
- Usar headers: `Cache-Control: max-age=300` (5 minutos)

---

## 🔟 DOCKER COMPOSE (Opcional)

Para ejecutar todo con Docker:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: project
      MYSQL_ROOT_PASSWORD: password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build: ./restapi-flask
    ports:
      - "5000:5000"
    environment:
      DATABASE_URI: mysql+pymysql://root:password@mysql/project
      FLASK_ENV: development
    depends_on:
      - mysql

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:5000
    depends_on:
      - backend

volumes:
  mysql_data:
```

Ejecutar:
```bash
docker-compose up
```

---

## 📋 RESUMEN

✅ Backend: Listo en `http://localhost:5000`
✅ CORS: Configurado para `localhost:3000` y `localhost:8080`
✅ JWT: Habilitado con tokens de 1 hora
✅ Endpoints: Documentados en `/docs`
✅ Autenticación: Bearer token required (excepto login)

Tu frontend debe:
1. Configurar cliente HTTP con interceptores
2. Manejar JWT en localStorage
3. Redirigir a login si token expira
4. Validar datos antes de enviar
5. Mostrar errores al usuario apropiadamente
