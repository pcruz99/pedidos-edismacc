from database.celular import (
    select_all_celulares,
    select_celular_for_codi,
    insert_celular,
    update_celular,
    delete_celular,
)

from database.cliente import (
    select_all_clientes,
    select_cliente_for_codi,
    insert_cliente,
    update_cliente,
    delete_cliente,
    select_cliente_codi_for_cedu_y_nomb,
)

from database.direccion_envio import (
    select_all_direccion_envio,
    select_direccion_envio_for_codi,
    insert_direccion_envio,
    update_direccion_envio,
    delete_direccion_envio,
    select_direccion_envio_codi_for_clpr_y_refe,
)

from database.pedido import (
    select_all_pedidos,
    select_pedido_for_codi,
    insert_pedido,
    update_pedido,
    delete_pedido,
    select_detalle_for_codi_pedi,
    select_pedido_codi_for_clie_y_dien,
    calcular_subtotal_producto, 
    calcular_iva,
)

from database.detalle import (
    select_all_detalles,
    select_detalle_for_codi,
    insert_detalle,
    update_detalle,
    delete_detalle,
)

from database.auth import select_user

__all__ = [
    "select_all_celulares",
    "select_celular_for_codi",
    "insert_celular",
    "update_celular",
    "delete_celular",
    "select_all_clientes",
    "select_cliente_for_codi",
    "insert_cliente",
    "update_cliente",
    "delete_cliente",
    "select_all_direccion_envio",
    "select_direccion_envio_for_codi",
    "insert_direccion_envio",
    "update_direccion_envio",
    "delete_direccion_envio",
    "select_all_pedidos",
    "select_pedido_for_codi",
    "insert_pedido",
    "update_pedido",
    "delete_pedido",
    "select_all_detalles",
    "select_detalle_for_codi",
    "insert_detalle",
    "update_detalle",
    "delete_detalle",
    "select_detalle_for_codi_pedi",
    "select_cliente_codi_for_cedu_y_nomb",
    "select_direccion_envio_codi_for_clpr_y_refe",
    "select_pedido_codi_for_clie_y_dien",
    "calcular_subtotal_producto",
    "calcular_iva",
    "select_user",
]
