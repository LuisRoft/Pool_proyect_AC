import threading
import time
from datetime import date
from connection_pool import ConnectionPool
from pedido_dao import PedidoDAO

DB_CONFIG = {
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432",
    "database": "pool"
}

# Singleton del pool
pool_instance = ConnectionPool(DB_CONFIG)
pedido_dao = PedidoDAO(pool_instance)

# Métricas
tiempos_insercion = []
conexion_activas = 0
conexion_maximas = 0
lock = threading.Lock()

# -------- CAMBIA ESTA BANDERA PARA VER COMPARACIONES ----------
LIBERAR_CONEXION = True  # ✅ True = usar putconn(), ❌ False = omitir

def tarea_insertar(id_hilo):
    global conexion_activas, conexion_maximas

    start_time = time.time()

    conn = pool_instance.getconn()
    with lock:
        conexion_activas += 1
        if conexion_activas > conexion_maximas:
            conexion_maximas = conexion_activas

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedido (cliente, descripcion, fecha_pedido)
            VALUES (%s, %s, %s)
        """, (f"Cliente {id_hilo}", f"Simulacion concurrente {id_hilo}", date.today()))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"[ERROR hilo {id_hilo}]:", e)
    finally:
        if LIBERAR_CONEXION:
            pool_instance.putconn(conn)
            with lock:
                conexion_activas -= 1

        end_time = time.time()
        with lock:
            tiempos_insercion.append(end_time - start_time)

def ejecutar_test_concurrente(num_hilos):
    print(f"\n⏱ Ejecutando test con {num_hilos} hilos. Pool limitado a 5 conexiones. LIBERAR_CONEXION = {LIBERAR_CONEXION}\n")
    hilos = []

    for i in range(num_hilos):
        t = threading.Thread(target=tarea_insertar, args=(i+1,))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    promedio = sum(tiempos_insercion) / len(tiempos_insercion)
    print(f"\n📊 RESULTADOS:\n")
    print(f"🧵 Hilos totales: {num_hilos}")
    print(f"⏱ Tiempo promedio de inserción: {promedio:.4f} segundos")
    print(f"🔝 Conexiones máximas concurrentes: {conexion_maximas}")
    print(f"📌 Conexiones activas finales: {conexion_activas}")

    pool_instance.closeall()
    print("✔️ Conexiones del pool cerradas.\n")


# test_concurrente.py
if __name__ == "__main__":
    ejecutar_test_concurrente(50)
