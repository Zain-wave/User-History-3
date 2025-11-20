from servicios import (
    agregar_producto, mostrar_inventario, buscar_producto,
    actualizar_producto, eliminar_producto, calcular_estadisticas
)
from archivos import guardar_csv, cargar_csv, fusionar_inventarios

menu = {
    1: "Agregar Producto",
    2: "Mostrar Inventario", 
    3: "Buscar Producto",
    4: "Actualizar Producto",
    5: "Eliminar Producto",
    6: "Estadisticas",
    7: "Guardar CSV",
    8: "Cargar CSV",
    9: "Salir",
}


def mostrar_menu():
    print("\n\033[33m MENU PRINCIPAL \033[0m")
    for i in range(1, len(menu) + 1):
        print(f"{i}. {menu[i]}")
    print("=" * 50)


def validar_entrada(msg, tipo="float", min_val=0.0):
    while True:
        try:
            n = float(input(msg)) if tipo == "float" else int(input(msg))
            return n if n >= min_val else print(f"❌ Debe ingresar un número mayor o igual que {min_val}")
        except ValueError:
            print("El dato ingresado es inválido, intente nuevamente")


def main():
    inventario = []
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opción (1-9): ").strip()
            
            if opcion == "1":
                print("\nAGREGAR PRODUCTO")
                if nombre := input("Nombre del producto: ").strip():
                    cantidad = validar_entrada("Cantidad: ", "int", 0)
                    precio = validar_entrada("Precio: $", "float", 0)
                    inventario = agregar_producto(inventario, nombre, precio, cantidad)
                else:
                    print("El nombre no puede estar vacío")

            elif opcion == "2":
                mostrar_inventario(inventario)

            elif opcion == "3":
                print("\n🔍 BUSCAR PRODUCTO")
                if nombre := input("Nombre del producto a buscar: ").strip():
                    if producto := buscar_producto(inventario, nombre):
                        print(f"Encontrado: {producto['nombre']} | Precio: ${producto['precio']:.2f} | Cantidad: {producto['cantidad']}")
                    else:
                        print("Producto no encontrado")

            elif opcion == "4":
                print("\nACTUALIZAR PRODUCTO")
                if nombre := input("Nombre del producto a actualizar: ").strip():
                    if producto := buscar_producto(inventario, nombre):
                        print("Deje en blanco (Enter) para mantener el valor actual")
                        nuevo_precio_input = input(f"Nuevo precio (actual: ${producto['precio']:.2f}): ").strip()
                        nueva_cantidad_input = input(f"Nueva cantidad (actual: {producto['cantidad']}): ").strip()
                        
                        nuevo_precio = float(nuevo_precio_input) if nuevo_precio_input else None
                        nueva_cantidad = int(nueva_cantidad_input) if nueva_cantidad_input else None
                        
                        inventario = actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)
                    else:
                        print("Producto no encontrado")

            elif opcion == "5":
                print("\nELIMINAR PRODUCTO")
                if nombre := input("Nombre del producto a eliminar: ").strip():
                    inventario = eliminar_producto(inventario, nombre)

            elif opcion == "6":
                calcular_estadisticas(inventario)

            elif opcion == "7":
                print("\nGUARDAR CSV")
                ruta = input("Ruta del archivo (Enter para 'inventario.csv'): ").strip()
                guardar_csv(inventario, ruta or "inventario.csv")

            elif opcion == "8":
                print("\nCARGAR CSV")
                ruta = input("Ruta del archivo (Enter para 'inventario.csv'): ").strip()
                
                if inventario_cargado := cargar_csv(ruta or "inventario.csv"):
                    productos_cargados, filas_invalidas = inventario_cargado[1], inventario_cargado[2]
                    
                    if productos_cargados > 0:
                        print("\nResumen de carga:")
                        print(f"• Productos cargados: {productos_cargados}")
                        print(f"• Filas inválidas omitidas: {filas_invalidas}")
                        
                        if inventario:
                            print("\n¿Qué desea hacer con el inventario actual?")
                            print("1. Sobrescribir (reemplazar todo)")
                            print("2. Fusionar (combinar ambos inventarios)")
                            
                            if opcion_carga := input("Seleccione (1-2): ").strip():
                                inventario = inventario_cargado[0] if opcion_carga == "1" else fusionar_inventarios(inventario, inventario_cargado[0])
                                print("Inventario sobrescrito" if opcion_carga == "1" else "✅ Inventarios fusionados")
                        else:
                            inventario = inventario_cargado[0]
                            print("Inventario cargado")

            elif opcion == "9":
                print("\nSaliendo del programa...")
                break

            else:
                print("Opción no válida, intente nuevamente")
        
        except KeyboardInterrupt:
            print("\n\nUse la opción 9 para salir correctamente.")
        except Exception as e:
            print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()