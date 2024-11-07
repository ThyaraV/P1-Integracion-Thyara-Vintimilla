import os
import pandas as pd
from faker import Faker
import shutil
import random
from datetime import datetime

# Directorios simulados de SGP y SFP
directorio_sgp = "SGP"
directorio_sfp = "SFP"
os.makedirs(directorio_sgp, exist_ok=True)
os.makedirs(directorio_sfp, exist_ok=True)

def generar_archivo_csv_sgp():
    fake = Faker()
    datos = []
    num_facturas = 10  # Número de facturas en el archivo

    for _ in range(num_facturas):
        id_factura = fake.unique.random_number(digits=5)
        id_proveedor = fake.random_number(digits=3)
        fecha = fake.date_between(start_date='-1y', end_date='today')
        monto = round(random.uniform(100, 5000), 2)
        estado = 'pendiente'
        
        datos.append([id_factura, id_proveedor, fecha, monto, estado])

    df = pd.DataFrame(datos, columns=['IDFactura', 'IDProveedor', 'Fecha', 'Monto', 'Estado'])
    archivo_csv = os.path.join(directorio_sgp, f'facturas_{datetime.now().strftime("%Y%m%d")}.csv')
    df.to_csv(archivo_csv, index=False)
    print(f"Archivo CSV generado en {archivo_csv}")
    
    return archivo_csv

def transferir_archivo_csv(archivo_csv):
    archivo_destino = os.path.join(directorio_sfp, os.path.basename(archivo_csv))
    shutil.copy(archivo_csv, archivo_destino)
    print(f"Archivo transferido a {archivo_destino}")

def validar_archivo_csv_sfp():
    archivos_csv = [f for f in os.listdir(directorio_sfp) if f.endswith('.csv')]
    for archivo in archivos_csv:
        ruta_archivo = os.path.join(directorio_sfp, archivo)
        df = pd.read_csv(ruta_archivo)
        
        # Ejemplo de validación de duplicados y campos incompletos
        if df.duplicated(subset=['IDFactura']).any():
            print(f"Advertencia: Se encontraron duplicados en {archivo}")
        if df.isnull().values.any():
            print(f"Advertencia: Existen campos incompletos en {archivo}")
        else:
            print(f"{archivo} validado correctamente.")

# Generar y transferir el archivo
archivo_generado = generar_archivo_csv_sgp()
transferir_archivo_csv(archivo_generado)
validar_archivo_csv_sfp()
