from connection_pool import ConnectionPool
from pedido_dao import PedidoDAO
from datetime import date

# Configuración de la base de datos
DB_CONFIG = {
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432",
    "database": "pool"
}

# Instanciar el pool y el DAO
pool_instance = ConnectionPool(DB_CONFIG)
pedido_dao = PedidoDAO(pool_instance)

# Insertar pedidos
pedido_dao.insertar_pedido("Juan López", "Compra de artículos escolares", date(2025, 6, 20))
pedido_dao.insertar_pedido("Marta Sánchez", "Pedido de oficina", date(2025, 6, 18))

# Listar pedidos
pedido_dao.listar_pedidos()

# Cerrar todas las conexiones
pool_instance.closeall()
print("Conexiones del pool cerradas")
