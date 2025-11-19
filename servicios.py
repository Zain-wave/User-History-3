def agregar_producto(inventario, nombre, precio, cantidad):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            producto["cantidad"] += cantidad
            producto["precio"] = precio
            print(f"Producto '{nombre}' actualizado")
            return inventario
    
    inventario.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
    print(f"Producto '{nombre}' agregado al inventario.")
    return inventario


def mostrar_inventario(inventario):
    if not inventario:
        print("Inventario vacío.")
        return
    
    print("\nInventario actual:".center(50, "="))
    for producto in inventario:
        print(f" - {producto['nombre']} | Precio: ${producto['precio']:.2f} | Cantidad: {producto['cantidad']}")


def buscar_producto(inventario, nombre):
    return next((p for p in inventario if p["nombre"].lower() == nombre.lower()), None)


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    if producto := buscar_producto(inventario, nombre):
        if nuevo_precio is not None:
            producto["precio"] = nuevo_precio
        if nueva_cantidad is not None:
            producto["cantidad"] = nueva_cantidad
        print(f"Producto '{nombre}' actualizado correctamente.")
    else:
        print(f"Producto '{nombre}' no encontrado.")
    return inventario


def eliminar_producto(inventario, nombre):
    if producto := buscar_producto(inventario, nombre):
        inventario.remove(producto)
        print(f"Producto '{nombre}' eliminado.")
    else:
        print(f"Producto '{nombre}' no encontrado.")
    return inventario


def calcular_estadisticas(inventario):
    if not inventario:
        print("📭 Inventario vacío.")
        return None
    
    subtotal = lambda p: p["precio"] * p["cantidad"]
    
    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)
    
    print("\n📊 Estadísticas del inventario:".center(50, "="))
    print(f"• Unidades totales: {unidades_totales}")
    print(f"• Valor total: ${valor_total:,.2f}")
    
    if producto_mas_caro := max(inventario, key=lambda p: p["precio"], default=None):
        print(f"• Producto más caro: {producto_mas_caro['nombre']} (${producto_mas_caro['precio']:.2f})")
    
    if producto_mayor_stock := max(inventario, key=lambda p: p["cantidad"], default=None):
        print(f"• Producto con más stock: {producto_mayor_stock['nombre']} ({producto_mayor_stock['cantidad']} unidades)")
    
    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock
    }