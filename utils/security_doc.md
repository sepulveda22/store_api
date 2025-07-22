# Documentación Detallada de security.py

Este documento proporciona una explicación detallada del archivo `security.py`, que maneja la seguridad en la aplicación FastAPI. Este módulo es fundamental para la gestión de autenticación y seguridad, implementando el manejo de contraseñas y tokens JWT.

## Propósito del Módulo

El módulo `security.py` tiene tres responsabilidades principales:
1. Gestión segura de contraseñas (hashing y verificación)
2. Generación de tokens JWT para autenticación
3. Manejo de tiempos de expiración de sesiones

## Importaciones
```python
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from functions import read_data
```

- `passlib.context`: Proporciona el contexto de encriptación para el manejo seguro de contraseñas
- `jwt`: Biblioteca para manejar JSON Web Tokens
- `datetime`, `timedelta`, `timezone`: Utilizados para manejar fechas y tiempos de expiración
- `Optional`: Tipo de datos para parámetros opcionales
- `read_data`: Función personalizada para leer la configuración

## Configuración
```python
config = read_data()
SECRET_KEY = config['secret_key']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Explicación Detallada de la Configuración:

1. **Lectura de Configuración**:
   ```python
   config = read_data()
   ```
   - La función `read_data()` lee la configuración desde un archivo externo
   - Esto permite mantener las credenciales y configuraciones sensibles fuera del código
   - Buena práctica de seguridad: separación de configuración y código

2. **Clave Secreta**:
   ```python
   SECRET_KEY = config['secret_key']
   ```
   - Clave utilizada para firmar los tokens JWT
   - CRUCIAL: Debe ser una cadena larga y aleatoria
   - Nunca debe compartirse o versionarse en git
   - Si se compromete, todos los tokens deben ser invalidados

3. **Algoritmo de Encriptación**:
   ```python
   ALGORITHM = "HS256"
   ```
   - HS256 = HMAC con SHA-256
   - Algoritmo simétrico: la misma clave se usa para firmar y verificar
   - Ventajas:
     * Rápido y eficiente
     * Ampliamente soportado
     * Seguro para la mayoría de aplicaciones

4. **Tiempo de Expiración**:
   ```python
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```
   - Define cuánto tiempo es válido un token
   - Balance entre seguridad y experiencia de usuario
   - 30 minutos es un valor común para aplicaciones web
   - Se puede ajustar según necesidades específicas:
     * Menor tiempo = más seguro pero más molestos reingresos
     * Mayor tiempo = mejor UX pero más riesgo si el token se compromete

## Contexto de Encriptación
```python
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
```

### Explicación del Contexto de Encriptación:

1. **CryptContext**:
   - Objeto principal para manejar el hashing de contraseñas
   - Provee una capa de abstracción sobre los algoritmos de hash
   - Permite actualizar esquemas de hash sin romper compatibilidad

2. **Bcrypt**:
   - ¿Por qué bcrypt?
     * Diseñado específicamente para contraseñas
     * Protección contra ataques de fuerza bruta
     * Parámetro de costo ajustable
     * Salt incorporado automáticamente
   - Ventajas sobre otros algoritmos:
     * Más lento que MD5/SHA (esto es bueno para seguridad)
     * Salt único por contraseña
     * Resistente a ataques con tablas rainbow

3. **Configuración `deprecated="auto"`**:
   - Maneja automáticamente esquemas de hash obsoletos
   - Permite actualización gradual de hashes antiguos
   - Proceso:
     1. Verifica contraseña con hash actual
     2. Si usa esquema obsoleto, rehash automático
     3. Actualiza hash en próxima autenticación

## Funciones de Seguridad

### 1. validate_password
```python
def validate_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
```

#### Explicación Detallada de validate_password:

1. **Propósito**:
   - Verifica si una contraseña proporcionada coincide con su hash almacenado
   - Usado en el proceso de login/autenticación
   - Nunca compara contraseñas en texto plano

2. **Parámetros**:
   - `plain_password`: 
     * Contraseña en texto plano proporcionada por el usuario
     * Ejemplo: "MiContraseña123"
   - `hashed_password`:
     * Hash almacenado en la base de datos
     * Ejemplo: "$2b$12$LQT7FJM/XB4FxU2G6JMOqeIL9CRjXVq9IesWgYgLui74xOruHJ.Fy"

3. **Proceso Interno**:
   1. Extrae el salt del hash almacenado
   2. Aplica el mismo proceso de hashing a la contraseña proporcionada
   3. Compara los hashes de manera segura (comparación de tiempo constante)

4. **Retorno**:
   - `True`: La contraseña es correcta
   - `False`: La contraseña es incorrecta

5. **Ejemplo de Uso**:
   ```python
   # Ejemplo de verificación de contraseña
   stored_hash = "$2b$12$LQT7FJM/XB4FxU2G6JMOqeIL9CRjXVq9IesWgYgLui74xOruHJ.Fy"
   is_valid = validate_password("MiContraseña123", stored_hash)
   # is_valid será True si la contraseña es correcta
   ```

### 2. get_password_hash
```python
def get_password_hash(password):
    return pwd_context.hash(password)
```

#### Explicación Detallada de get_password_hash:

1. **Propósito**:
   - Convierte una contraseña en texto plano a un hash seguro
   - Usado en registro de usuarios y cambios de contraseña
   - Implementa las mejores prácticas de hashing de contraseñas

2. **Parámetro**:
   - `password`: 
     * Contraseña en texto plano a hashear
     * Ejemplo: "MiContraseña123"

3. **Proceso de Hashing**:
   1. Generación de salt aleatorio único
   2. Aplicación del algoritmo bcrypt
   3. Combinación de salt y hash en un único string

4. **Formato del Hash Resultante**:
   ```
   $2b$12$LQT7FJM/XB4FxU2G6JMOqeIL9CRjXVq9IesWgYgLui74xOruHJ.Fy
   ```
   Donde:
   - `$2b$`: Identificador de versión de bcrypt
   - `12`: Factor de costo (2^12 rondas)
   - El resto: Salt y hash combinados

5. **Ejemplo de Uso**:
   ```python
   # Ejemplo de generación de hash
   password = "MiContraseña123"
   hashed = get_password_hash(password)
   # hashed será algo como:
   # "$2b$12$LQT7FJM/XB4FxU2G6JMOqeIL9CRjXVq9IesWgYgLui74xOruHJ.Fy"
   ```

6. **Características de Seguridad**:
   - Salt único por contraseña
   - Resistente a ataques de diccionario
   - Resistente a ataques de fuerza bruta
   - No reversible (one-way hash)

### 3. create_access_token
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

#### Explicación Detallada de create_access_token:

1. **Propósito**:
   - Genera tokens JWT para autenticación de usuarios
   - Permite acceso seguro a recursos protegidos
   - Implementa autenticación sin estado (stateless)

2. **Parámetros**:
   - `data` (dict):
     * Información a incluir en el token
     * Ejemplo: `{"sub": "usuario@email.com", "role": "admin"}`
   - `expires_delta` (Optional[timedelta]):
     * Tiempo de vida del token
     * Si no se proporciona, usa 15 minutos por defecto

3. **Proceso Detallado**:
   ```python
   # 1. Copia segura de datos
   to_encode = data.copy()  # Evita modificar el diccionario original
   
   # 2. Cálculo de expiración
   if expires_delta:
       expire = datetime.now(timezone.utc) + expires_delta
   else:
       expire = datetime.now(timezone.utc) + timedelta(minutes=15)
   
   # 3. Actualización del payload
   to_encode.update({"exp": expire})  # Agrega timestamp de expiración
   
   # 4. Generación del token
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   ```

4. **Estructura del Token JWT**:
   El token resultante tiene tres partes:
   ```
   header.payload.signature
   ```
   - Header: `{"alg": "HS256", "typ": "JWT"}`
   - Payload: Tus datos + expiración
   - Signature: HMAC-SHA256 del header y payload

5. **Ejemplo de Uso**:
   ```python
   # Crear token para un usuario
   user_data = {
       "sub": "usuario@email.com",
       "role": "admin",
       "user_id": 123
   }
   expiration = timedelta(hours=1)
   token = create_access_token(user_data, expiration)
   ```

6. **Consideraciones de Seguridad**:
   - Uso de UTC para evitar problemas de zona horaria
   - Tokens con tiempo de vida limitado
   - Firma criptográfica para prevenir manipulación
   - No almacena información sensible en el payload

## Consideraciones de Seguridad y Mejores Prácticas

### 1. Hashing de Contraseñas con Bcrypt
- **Características de Seguridad**:
  * Algoritmo seguro y resistente a ataques de fuerza bruta
  * Salt único por contraseña (16 bytes)
  * Factor de costo ajustable (actualmente 12 rondas)
  * Diseñado específicamente para contraseñas

- **Ventajas sobre Otros Algoritmos**:
  * Más lento que MD5/SHA (beneficioso para la seguridad)
  * Protección contra ataques de tabla rainbow
  * Resistente a ataques de hardware especializado (GPU/ASIC)

### 2. Autenticación con JWT
- **Características del Token**:
  * Firmado criptográficamente con HMAC-SHA256
  * Tiempo de expiración configurable
  * Basado en UTC para consistencia global

- **Seguridad del Token**:
  * No almacena información sensible en el payload
  * Tokens invalidables mediante tiempo de expiración
  * Firma verificable para prevenir manipulación

### 3. Manejo de Sesiones
- **Tiempo de Expiración**:
  * Default: 30 minutos (configurable)
  * Balance entre seguridad y experiencia de usuario
  * Renovación de tokens implementada

- **Consideraciones de Implementación**:
  * Uso de UTC para evitar problemas de zona horaria
  * Validación de tiempo de expiración en cada request
  * Posibilidad de invalidación manual de tokens

### 4. Buenas Prácticas Implementadas
- **Almacenamiento Seguro**:
  * No se guardan contraseñas en texto plano
  * Hashes únicos por usuario
  * Separación de datos sensibles y código

- **Configuración**:
  * Variables de entorno para datos sensibles
  * Clave secreta fuera del código
  * Configuración modular y flexible

- **Manejo de Errores**:
  * Mensajes de error genéricos (no revelan información sensible)
  * Logging seguro de eventos
  * Manejo consistente de fallos de autenticación

### 5. Recomendaciones de Uso
- **Para Desarrolladores**:
  * Mantener SECRET_KEY segura y única por ambiente
  * Rotar claves periódicamente
  * Implementar rate limiting en endpoints de autenticación

- **Para Administradores**:
  * Monitorear intentos de autenticación fallidos
  * Mantener las dependencias actualizadas
  * Realizar auditorías de seguridad periódicas
