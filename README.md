### 🐘 Aplicación Python con PostgreSQL y Pool de Conexiones

Este proyecto es una simulación de una aplicación cliente-servidor en Python que interactúa con una base de datos PostgreSQL utilizando un **pool de conexiones** (`psycopg2.pool.SimpleConnectionPool`), siguiendo buenas prácticas como el uso del patrón **Singleton** y la arquitectura **DAO (Data Access Object)**.
Además, incluye un test de carga concurrente con múltiples hilos para medir el comportamiento y rendimiento del pool.

---

### 📦 Estructura del Proyecto

```bash
tu_proyecto/
├── db/
│   └── connection_pool.py       # Singleton del pool de conexiones
├── dao/
│   └── pedido_dao.py            # DAO para manejar operaciones sobre la tabla pedido
├── test_concurrente.py          # Test de carga concurrente con hilos
├── main.py                      # Ejemplo de uso del DAO
└── docker-compose.yml           # Para levantar PostgreSQL con Docker
```

---

### 🐳 Levantar la Base de Datos con Docker Compose

La base de datos PostgreSQL utilizada en esta aplicación se levanta mediante Docker Compose.

#### 1. Contenido del `docker-compose.yml`

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

#### 2. Comando para levantar el contenedor

```bash
docker-compose up -d
```

Asegúrate de tener Docker y Docker Compose instalados.

---

### 🧾 Tabla usada: `pedido`

```sql
CREATE TABLE public.pedido (
	id serial PRIMARY KEY,
	cliente VARCHAR(50) NOT NULL,
	descripcion TEXT NOT NULL,
	fecha_pedido DATE NOT NULL
);
```

---

### 🚀 Uso del DAO

El archivo `main.py` muestra cómo insertar y listar pedidos con el DAO.

```bash
python main.py
```

Esto realiza inserciones en la tabla `pedido` utilizando el pool de conexiones.

---

### 🧪 Test de Carga Concurrente

Archivo: `test_concurrente.py`

Este script lanza múltiples hilos para insertar registros concurrentemente.

#### Parámetros simulados:
* Número de hilos: 10, 20, 50  
* Tamaño del pool: máximo 5 conexiones  
* Modo de prueba:  
  * Con liberación de conexión (`putconn()`)  
  * Sin liberación (para simular mal uso)

#### Ejecutar test con 50 hilos:

```bash
python test_concurrente.py
```

Puedes modificar la cantidad de hilos en el `main` del script.

---

### 📊 Resultados esperados

#### Cuando se libera la conexión (`putconn()`):
* Conexiones son reutilizadas correctamente.
* Operaciones lentas pero exitosas.
* Tiempo promedio aceptable.

#### Cuando NO se libera (`putconn()` omitido):
* El pool se queda sin conexiones disponibles.
* Algunos hilos se bloquean o fallan.
* Tiempo de respuesta incrementa drásticamente.

---

### ✅ Requisitos

* Python 3.8+
* Docker y Docker Compose
* psycopg2 → `pip install psycopg2`
* (opcional) matplotlib si deseas graficar resultados

---

### 📚 Buenas Prácticas Aplicadas

* Uso de pool de conexiones para escalabilidad.
* Separación de responsabilidades (DAO, conexión).
* Patrón Singleton para compartir el pool.
* Test concurrente realista para medir eficiencia.

---

### 📬 Contacto

Desarrollado por [Tu Nombre o Equipo]  
Inspirado en buenas prácticas de desarrollo backend con Python y PostgreSQL.
