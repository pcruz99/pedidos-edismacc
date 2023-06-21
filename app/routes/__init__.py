from app.routes.jindex import index
from app.routes.celular import celular
from app.routes.cliente import cliente
from app.routes.direccion_envio import direccion_envio
from app.routes.pedido import pedido
from app.routes.auth import auth


__all__ = [
    "index",
    "celular",
    "cliente",
    "direccion_envio",
    "pedido",
    "auth",
]