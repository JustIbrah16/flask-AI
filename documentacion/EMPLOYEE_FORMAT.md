# Formato de Datos para Crear Empleados

## POST /employees/ - Crear Nuevo Empleado

### Campos Requeridos:
- `identificacion` - Identificación única del empleado
- `nombre` - Nombre completo
- `correo` - Correo electrónico único
- `username` - Usuario para login
- `password` - Contraseña

### Campos Opcionales:
- `fecha_nacimiento` - Fecha en formato YYYY-MM-DD
- `contacto` - Teléfono
- `direccion` - Dirección residencial
- `ciudad` - Ciudad
- `cargo` - Cargo/Posición
- `area` - Área de trabajo
- `role_id` - ID del rol (1=Admin, 2=Agente, 3=Empleado)
- `jefe_inmediato` - Nombre del supervisor
- `tipo_contrato` - Tipo: Indefinido, Temporal, Prestación de servicios
- `banco` - Nombre del banco
- `numero_cuenta_bancaria` - Número de cuenta (único)
- `salario` - Salario mensual
- `fecha_ingreso` - Fecha de ingreso (YYYY-MM-DD)
- `proyecto_centro_costo` - Proyecto o centro de costo
- `genero` - Masculino/Femenino/Otro
- `camisa` - Talla: XS, S, M, L, XL, XXL
- `pantalon` - Talla: 28-54
- `zapatos` - Talla: 35-48
- `abrigo` - Talla: XS, S, M, L, XL, XXL
- `eps` - Empresa Promotora de Salud
- `estudios` - Información sobre educación
- `estado_civil` - Soltero, Casado, Divorciado, Viudo
- `hijos` - Número de hijos

## Ejemplos de Solicitud

### Ejemplo Mínimo (Campos Obligatorios)
```bash
curl -X POST http://localhost:5000/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "EMP001",
    "nombre": "John Doe",
    "correo": "john@example.com",
    "username": "john_doe",
    "password": "secure_password_123"
  }'
```

### Ejemplo Completo
```bash
curl -X POST http://localhost:5000/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "EMP001",
    "nombre": "John Doe",
    "fecha_nacimiento": "1990-05-15",
    "correo": "john@example.com",
    "contacto": "+57 1 2345678",
    "direccion": "Calle Principal 123, Apt 4B",
    "ciudad": "Bogotá",
    "cargo": "Ingeniero de Software",
    "area": "Tecnología",
    "role_id": 2,
    "jefe_inmediato": "Juan García",
    "tipo_contrato": "Indefinido",
    "banco": "Banco de Bogotá",
    "numero_cuenta_bancaria": "123456789012",
    "salario": 3500000.0,
    "fecha_ingreso": "2025-01-15",
    "proyecto_centro_costo": "Proyecto A",
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
    "username": "john_doe",
    "password": "secure_password_123"
  }'
```

## Respuesta Exitosa (201 Created)
```json
{
  "id": 1,
  "numero": "EMP001",
  "nombre": "John Doe",
  "fecha_nacimiento": "1990-05-15",
  "correo": "john@example.com",
  "contacto": "+57 1 2345678",
  "direccion": "Calle Principal 123, Apt 4B",
  "ciudad": "Bogotá",
  "cargo": "Ingeniero de Software",
  "area": "Tecnología",
  "role_id": 2,
  "jefe_inmediato": "Juan García",
  "tipo_contrato": "Indefinido",
  "banco": "Banco de Bogotá",
  "numero_cuenta_bancaria": "123456789012",
  "salario": 3500000.0,
  "fecha_ingreso": "2025-01-15",
  "proyecto_centro_costo": "Proyecto A",
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

## Errores Comunes

### 400 - Campos Requeridos Faltantes
```json
{
  "error": "Campos requeridos faltantes: numero, correo"
}
```

### 400 - Correo o Número Duplicado
```json
{
  "error": "Error: (psycopg2.IntegrityError) duplicate key value..."
}
```

### 404 - No Encontrado (al editar)
```json
{
  "msg": "not found"
}
```

## Endpoints Relacionados

- `GET /employees/` - Listar todos
- `GET /employees/<id>` - Obtener por ID
- `GET /employees/numero/<numero>` - Obtener por número
- `PUT /employees/<id>` - Editar
- `DELETE /employees/<id>` - Inactivar
- `PUT /employees/<id>/toggle-status` - Activar/Inactivar
