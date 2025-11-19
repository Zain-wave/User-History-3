import csv

def guardar_csv(inventario, ruta="inventario.csv", incluir_header=True):
    if not inventario:
        print("No hay productos para guardar en el inventario")
        return False
    
    try:
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            
            if incluir_header:
                writer.writerow(["nombre", "precio", "cantidad"])
            
            for producto in inventario:
                writer.writerow([producto["nombre"], producto["precio"], producto["cantidad"]])
        
        print(f"Inventario guardado correctamente en: {ruta}")
        return True
        
    except PermissionError:
        print("Sin permisos para escribir en el archivo")
        return False
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return False


def cargar_csv(ruta="inventario.csv"):
    inventario = []
    productos_cargados = 0
    filas_invalidas = 0
    
    try:
        with open(ruta, 'r', newline='', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            
            if encabezado := next(reader, None):
                if encabezado != ["nombre", "precio", "cantidad"]:
                    print("Encabezado del CSV no coincide con el formato esperado")
            else:
                print("Archivo CSV vacío")
                return [], 0, 0
            
            for num_fila, fila in enumerate(reader, start=2):
                if len(fila) != 3:
                    print(f"Fila {num_fila} omitida: Número incorrecto de columnas")
                    filas_invalidas += 1
                    continue
                
                nombre, str_precio, str_cantidad = fila
                
                try:
                    precio = float(str_precio)
                    cantidad = int(str_cantidad)
                    
                    if precio < 0 or cantidad < 0:
                        print(f"Fila {num_fila} omitida: Valores negativos no permitidos")
                        filas_invalidas += 1
                        continue
                    
                    inventario.append({"nombre": nombre.strip(), "precio": precio, "cantidad": cantidad})
                    productos_cargados += 1
                    
                except ValueError:
                    print(f"Fila {num_fila} omitida: Formato inválido en precio o cantidad")
                    filas_invalidas += 1
                    continue
    
    except FileNotFoundError:
        print(f"No se encontró el archivo {ruta}")
        return [], 0, 0
    except UnicodeDecodeError:
        print("Problema de codificación en el archivo")
        return [], 0, 0
    except Exception as e:
        print(f"Error inesperado al cargar el archivo: {e}")
        return [], 0, 0
    
    return inventario, productos_cargados, filas_invalidas


def fusionar_inventarios(inventario_actual, inventario_nuevo):
    from servicios import buscar_producto
    
    inventario_fusionado = inventario_actual.copy()
    
    for producto_nuevo in inventario_nuevo:
        if producto_existente := buscar_producto(inventario_fusionado, producto_nuevo["nombre"]):
            producto_existente["cantidad"] += producto_nuevo["cantidad"]
            producto_existente["precio"] = producto_nuevo["precio"]
            print(f"🔄 Producto '{producto_nuevo['nombre']}' actualizado")
        else:
            inventario_fusionado.append(producto_nuevo)
            print(f"Producto '{producto_nuevo['nombre']}' agregado")
    
    return inventario_fusionado