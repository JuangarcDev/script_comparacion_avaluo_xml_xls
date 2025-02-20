import pandas as pd
import xml.etree.ElementTree as ET

# Rutas de los archivos
ruta_excel = r'C:\ACC\CONSOLIDACION_MANZANAS\PRUEBA_19022025\VALIDACION_URBANO\liquidacion_18022025_urbana_manta.xlsx'
ruta_xml = r'C:\Users\juang\Downloads\predios.xml'

# Leer Excel (ambas hojas)
def leer_excel(ruta):
    df_hojas = pd.read_excel(ruta, sheet_name=None, dtype={'numero_predial': str})
    datos = []
    for hoja, df in df_hojas.items():
        df = df[['numero_predial', 'avaluo_catastral_2025']].dropna()
        for _, row in df.iterrows():
            datos.append((row['numero_predial'], float(row['avaluo_catastral_2025'])))
    return dict(datos)

# Leer XML
def leer_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    datos = {}
    for predio in root.findall('predio'):
        codigo_predial = predio.find('codigo_predial_nacional').text
        avaluo_elemento = predio.find(".//avaluo_catastral/avaluo")
        avaluo = float(avaluo_elemento.text) if avaluo_elemento is not None else 0
        datos[codigo_predial] = avaluo
    return datos

# Extraer datos
datos_excel = leer_excel(ruta_excel)
datos_xml = leer_xml(ruta_xml)

# Comparaciones
set_excel = set(datos_excel.keys())
set_xml = set(datos_xml.keys())

# Cantidad de registros
total_excel = len(set_excel)
total_xml = len(set_xml)

# Coincidencias y diferencias
comunes = set_excel & set_xml
solo_excel = set_excel - set_xml
solo_xml = set_xml - set_excel

# Comparación de valores de avalúo
diferencias = {}
for num_predial in comunes:
    if datos_excel[num_predial] != datos_xml[num_predial]:
        diferencias[num_predial] = datos_excel[num_predial] - datos_xml[num_predial]

# Reporte de resultados
print("REPORTE CONTRASTE DE AVALUOS:")
print(f"Total registros en Excel: {total_excel}")
print(f"Total registros en XML: {total_xml}")
print(f"Registros en ambas fuentes: {len(comunes)}")
print(f"Registros solo en Excel: {len(solo_excel)} ({', \n '.join(solo_excel)})")
print(f"Registros solo en XML: {len(solo_xml)} ({', \n '.join(solo_xml)})")
print(f"Diferencias en avalúo (en registros comunes con diferencia): {len(diferencias)}")


# Mostrar diferencias significativas
for predial, diferencia in diferencias.items():
    print(f"Número Predial: {predial}, Diferencia Avalúo: {diferencia}")

print(f"\n \n")
print(f"Diferencias en avalúo (en registros comunes con diferencia igual o superior a mil):")
# MOSTRAR DIFERENCIAS IGUALES O SUPERIORES A MIL
cont = 0
for predial, diferencia in diferencias.items():
    if diferencia >= 1000:
        print(f"Número Predial: {predial}, Diferencia Avalúo: {diferencia}")
        cont = cont + 1
    
print(f"Cantidad de predios con diferencia significativa (en registros comunes con diferencia igual o superior a mil): {cont}")


