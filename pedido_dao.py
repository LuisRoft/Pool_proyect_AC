from datetime import date

class PedidoDAO:
    def __init__(self, connection_pool):
        self.pool = connection_pool

    def insertar_pedido(self, cliente, descripcion, fecha_pedido: date):
        conn = None
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pedido (cliente, descripcion, fecha_pedido)
                VALUES (%s, %s, %s)
            """, (cliente, descripcion, fecha_pedido))
            conn.commit()
            cursor.close()
            print("Pedido insertado correctamente")
        except Exception as e:
            print("Error al insertar pedido:", e)
        finally:
            if conn:
                self.pool.putconn(conn)

    def listar_pedidos(self):
        conn = None
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, cliente, descripcion, fecha_pedido
                FROM pedido
                ORDER BY fecha_pedido DESC
            """)
            pedidos = cursor.fetchall()
            for p in pedidos:
                print(f"[{p[0]}] {p[1]} - {p[2]} ({p[3]})")
            cursor.close()
        except Exception as e:
            print("Error al listar pedidos:", e)
        finally:
            if conn:
                self.pool.putconn(conn)
