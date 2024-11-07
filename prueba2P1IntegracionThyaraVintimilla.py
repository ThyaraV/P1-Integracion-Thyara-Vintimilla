import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configuración de la conexión a la base de datos
engine = create_engine('mysql+mysqlconnector://T%40vs2022@localhost/pruebaintegracion')

# Directorio donde se encuentran los archivos CSV generados por el SGP
directorio_sgp = "SGP"

def guardar_datos_csv_en_bd():
    # Verificar si el directorio SGP existe
    if not os.path.exists(directorio_sgp):
        print(f"El directorio {directorio_sgp} no existe.")
        return

    # Obtener los archivos CSV en el directorio SGP
    archivos_csv = [archivo for archivo in os.listdir(directorio_sgp) if archivo.endswith('.csv')]
    if not archivos_csv:
        print(f"No se encontraron archivos CSV en el directorio {directorio_sgp}.")
        return
    
    print(f"Archivos CSV encontrados: {archivos_csv}")

    for archivo_csv in archivos_csv:
        ruta_archivo = os.path.join(directorio_sgp, archivo_csv)
        print(f"Leyendo archivo: {ruta_archivo}")
        
        # Leer el archivo CSV en un DataFrame de pandas
        try:
            df = pd.read_csv(ruta_archivo)
            print(f"Contenido del archivo {archivo_csv}:")
            print(df.head())  # Mostrar las primeras filas del DataFrame

            # Ajustar tipos de datos
            df['IDFactura'] = df['IDFactura'].astype(int)
            df['IDProveedor'] = df['IDProveedor'].astype(int)
            df['Monto'] = df['Monto'].astype(float)
            df['Estado'] = df['Estado'].astype(str)
            df['FechaCreacion'] = pd.to_datetime(df['FechaCreacion']).dt.date

            # Insertar datos fila por fila usando una consulta SQL
            with engine.connect() as connection:
                for _, row in df.iterrows():
                    try:
                        insert_query = f"""
                        INSERT INTO Facturas (IDFactura, IDProveedor, Monto, Estado, FechaCreacion)
                        VALUES ({row['IDFactura']}, {row['IDProveedor']}, {row['Monto']}, '{row['Estado']}', '{row['FechaCreacion']}')
                        """
                        connection.execute(insert_query)
                        print(f"Insertado: IDFactura={row['IDFactura']}")
                    except SQLAlchemyError as e:
                        print(f"Error al insertar la fila con IDFactura={row['IDFactura']}: {e}")
        
        except Exception as e:
            print(f"Error al procesar el archivo {archivo_csv}: {e}")

# Ejecutar la función para guardar los datos en la base de datos
guardar_datos_csv_en_bd()
