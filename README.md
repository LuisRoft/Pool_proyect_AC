### 🐘 Proyecto Python con PostgreSQL y Pool de Conexiones

Este repositorio presenta una simulación de una aplicación cliente-servidor en Python que se conecta a una base de datos PostgreSQL utilizando un **pool de conexiones** (`psycopg2.pool.SimpleConnectionPool`). Se implementan buenas prácticas como el patrón **Singleton** y la arquitectura **DAO (Data Access Object)**.

También se incluye una prueba de concurrencia con múltiples hilos para evaluar el rendimiento y funcionamiento del pool.

---

### 📦 Organización del Proyecto

```bash
tu_proyecto/
├── db/
│   └── connection_pool.py       # Singleton para el pool de conexiones
├── dao/
│   └── pedido_dao.py            # DAO para operaciones sobre la tabla pedido
├── test_concurrente.py          # Prueba de concurrencia con hilos
├── main.py                      # Ejemplo de uso del DAO
└── docker-compose.yml           # Configuración de PostgreSQL con Docker
```

---

### 🐳 Inicializar la Base de Datos con Docker Compose

La base de datos PostgreSQL utilizada en este proyecto se levanta fácilmente con Docker Compose.

#### 1. Ejemplo de `docker-compose.yml`

```yaml
version: "3.8"
services:
  postgres:
    image: postgres:15
    container_name: postgres_pool
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: pool
    ports:
      - "5432:5432"
    volumes:
      - ./data:/var/lib/postgresql/data
```

#### 2. Comando para iniciar el contenedor

```bash
docker-compose up -d
```

Recuerda tener Docker y Docker Compose instalados previamente.

---

### 🧾 Estructura de la tabla `pedido`

```sql
CREATE TABLE public.pedido (
	id serial PRIMARY KEY,
	cliente VARCHAR(50) NOT NULL,
	descripcion TEXT NOT NULL,
	fecha_pedido DATE NOT NULL
);
```

---

### 🚀 Ejemplo de Uso del DAO

El archivo `main.py` contiene ejemplos para insertar y consultar pedidos usando el DAO.

```bash
python main.py
```

Esto insertará registros en la tabla `pedido` utilizando el pool de conexiones.

---

### 🧪 Prueba de Concurrencia

Archivo: `test_concurrente.py`

Este script ejecuta varios hilos para insertar datos de manera simultánea.

#### Parámetros de la simulación:

- Cantidad de hilos: 10, 20, 50
- Tamaño máximo del pool: 5 conexiones
- Modos de prueba:
  - Liberando la conexión (`putconn()`)
  - Sin liberar la conexión (para simular un mal uso)

#### Ejecutar la prueba con 50 hilos:

```bash
python test_concurrente.py
```

Puedes ajustar el número de hilos modificando el `main` del script.

---

### 📊 Qué resultados esperar

#### Si se libera la conexión (`putconn()`):

- Las conexiones se reutilizan correctamente.
- Las operaciones pueden ser más lentas, pero exitosas.
- El tiempo promedio es razonable.

#### Si NO se libera la conexión (sin `putconn()`):

- El pool se queda sin conexiones disponibles.
- Algunos hilos quedan bloqueados o fallan.
- El tiempo de respuesta aumenta considerablemente.

---

### ✅ Requisitos

- Python 3.8 o superior
- Docker y Docker Compose
- psycopg2 → `pip install psycopg2`

---

### 📚 Buenas Prácticas Implementadas

- Uso de pool de conexiones para mejorar la escalabilidad.
- Separación de responsabilidades (DAO, conexión).
- Patrón Singleton para compartir el pool de conexiones.
- Prueba concurrente realista para evaluar la eficiencia.
