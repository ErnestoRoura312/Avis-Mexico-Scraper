#region Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from openpyxl.utils import get_column_letter
from time import sleep
import random
import pandas as pd
import os
from datetime import datetime, timedelta
import json
import sys
#endregion

#region Funciones
def pausa():
    sleep(random.uniform(1, 2))

def leerConfiguracion(rutaArchivo):
    config = {}
    if not os.path.exists(rutaArchivo):
        sys.exit(f"ERROR - No se encontró el archivo de configuracion")
    
    with open(rutaArchivo, "r") as f:
        for linea in f:
            if ":" in linea:
                clave, valor = linea.split(":")
                config[clave.strip()] = valor.strip()
    return config
#endregion

#region Codigo
serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv)
rutaScript = os.path.dirname(os.path.abspath(__file__))
rutaArchivoEstados = os.path.join(rutaScript, "Recursos/EstadosMexico.txt")
rutaArchivoConfiguracion = os.path.join(rutaScript, "Configuracion/config.txt")

driver.maximize_window()

precios = []
arreglo_estados = []

config = leerConfiguracion(rutaArchivoConfiguracion)
fechaEntregaStr = config.get("fechaEntrega")
fechaDevolucionStr = config.get("fechaDevolucion")

if not fechaEntregaStr or not fechaDevolucionStr:
    sys.exit("ERROR - Faltan fechas en el archivo de configuración.")

hoy = datetime.now()
fechaLimite = hoy + timedelta(days=365)
horaLimite = hoy.replace(hour=23, minute=30, second=0, microsecond=0)

try:
    fEntrega = datetime.strptime(fechaEntregaStr, "%d/%m/%y")
    fDevolucion = datetime.strptime(fechaDevolucionStr, "%d/%m/%y")
    
    if fEntrega.date() < hoy.date():
        sys.exit(f"ERROR - Fecha invalida: La fecha de entrega ya paso.")

    if fEntrega > fechaLimite or fDevolucion > fechaLimite:
        sys.exit("ERROR - Fecha invalida: Las fechas no pueden ser mayores a un año desde hoy.")

    if fDevolucion < fEntrega:
        sys.exit("ERROR - Fecha invalida: La fecha de devolución no puede ser anterior a la de entrega.")

    if fDevolucion > fEntrega + timedelta(days=30):
        sys.exit("ERROR - Fecha invalida: La fecha de devolución no puede ser mayor de 30 dias a la fecha de entrega.")
except ValueError:
    sys.exit("ERROR - Formato de fecha invalido: El formato debe ser DD/MM/YY (ej: 30/04/26).")

try:
    fEntrega = datetime.strptime(fechaEntregaStr, "%d/%m/%y")
    fDevolucion = datetime.strptime(fechaDevolucionStr, "%d/%m/%y")
    
    if fEntrega.date() == hoy.date():
        horaEntrega = hoy + timedelta(hours=4)
        if fDevolucion.date == hoy.date():
            horaDevolucion = hoy + timedelta(hours=7)
        else:
            horaDevolucion = fDevolucion.replace(hour=16, minute=0)
        
        if horaEntrega > horaLimite:
            sys.exit(f"ERROR - No hay tiempo suficiente para generar la renta antes de las 11:30 PM.")
            
    else:
        horaEntrega = fEntrega.replace(hour=12, minute=0)
        horaDevolucion = fDevolucion.replace(hour=16, minute=0)

    horaEntregaStr = horaEntrega.strftime("%I:%M %p")
    horaDevolucionStr = horaDevolucion.strftime("%I:%M %p")
except ValueError:
    sys.exit("ERROR - No es posible hacer la/las reservas.")

with open(rutaArchivoEstados, 'r', encoding='utf-8') as archivo:
    arregloEstados = [linea.strip() for linea in archivo if linea.strip()]

for estado in arregloEstados:
    driver.get('https://avis.mx/')
    pausa()

    try:

        barraBusquedaOficina = driver.find_element(By.ID, 'TxtOficinaRenta')
        barraBusquedaOficina.clear()
        barraBusquedaOficina.send_keys(Keys.CONTROL + "a")
        barraBusquedaOficina.send_keys(Keys.BACKSPACE)

        fechaEntrega = driver.find_element(By.ID, 'Frenta')
        fechaEntrega.clear()
        fechaEntrega.send_keys(Keys.CONTROL + "a")
        fechaEntrega.send_keys(Keys.BACKSPACE)

        fechaDevolucion = driver.find_element(By.ID, 'Fdev')
        fechaDevolucion.clear()
        fechaEntrega.send_keys(Keys.CONTROL + "a")
        fechaEntrega.send_keys(Keys.BACKSPACE)

        horaEntrega = driver.find_element(By.ID, 'Hrenta')
        horaEntrega.clear()
        horaEntrega.send_keys(Keys.CONTROL + "a")
        horaEntrega.send_keys(Keys.BACKSPACE)

        horaDevolucion = driver.find_element(By.ID, 'Hdev')
        horaDevolucion.clear()
        horaDevolucion.send_keys(Keys.CONTROL + "a")
        horaDevolucion.send_keys(Keys.BACKSPACE)

        pausa()

        barraBusquedaOficina.send_keys(estado)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'autocomplete-dropdown-autocomplete-oficina-inicia'))
        )

        pausa()

        primeraOpcion = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#autocomplete-dropdown-autocomplete-oficina-inicia li:first-child"))
        )
        if primeraOpcion.text == "No se encontró la sucursal":
            datosSucursal = {
                "Estado": estado,
                "Sucursal": "No hay sucursal",
                "Listado_Precios": "No hay precios"
            }

            precios.append(datosSucursal)
            continue
        else:
            textoOpcion = primeraOpcion.text
            datosSucursal = {
                "Estado": estado,
                "Sucursal": textoOpcion,
                "Listado_Precios": []
            }

            primeraOpcion.click()
            fechaEntrega.send_keys(fechaEntregaStr)
            horaEntrega.send_keys(horaEntregaStr)
            fechaDevolucion.send_keys(fechaDevolucionStr)
            horaDevolucion.send_keys(horaDevolucionStr)
            botonBuscar = driver.find_element(By.ID, 'elegirAutoDesk').click()
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'stepper-head'))
            )

            totalAutos = driver.find_elements(By.CSS_SELECTOR, '.accordion-item.border-0')

            for i in range(len(totalAutos)):
                autos = driver.find_elements(By.CSS_SELECTOR, '.accordion-item.border-0')
                auto = autos[i]
                fullId = auto.find_element(By.TAG_NAME, "button").get_attribute("id")
                letraAuto = fullId.split('-')[1] 

                posicion = auto.location['y']
                driver.execute_script(f"window.scrollTo(0, {posicion - 200});")

                paquete = auto.find_element(By.CSS_SELECTOR, '.h4.mb-0.font-bold').text
                modelo = auto.find_element(By.CSS_SELECTOR, '.fw-semibold.mb-1.text-muted').text
                botonAuto = auto.find_element(By.CSS_SELECTOR, '.btn.btn-red.rounded-5.btn-lg.font-semibold.shadow-none')
                
                infoAuto = {"Paquete": paquete, "Modelo": modelo, "Tarifas": []}
                
                botonAuto.click()
                
                id_detalle = f"detalle-grupo-{letraAuto}"
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, id_detalle))
                )

                pausa()

                selectorTarifas = f'[id*="card-paquete-"][id$="-{letraAuto}"]'
                tarifas = driver.find_elements(By.CSS_SELECTOR, selectorTarifas)
                for tarifa in tarifas:
                    nombreTarifa = tarifa.find_element(By.CSS_SELECTOR, '.h4.font-bold.text-red.mb-0').text
                    precioTarifa = tarifa.find_element(By.CSS_SELECTOR, '.fs-1.font-semibold.mb-0').text
                    datos_tarifa = {
                        nombreTarifa: precioTarifa
                    }
                    infoAuto["Tarifas"].append(datos_tarifa)

                selectorCerrar = f'button.btn-close[data-mdb-target="#{id_detalle}"]'
                botonCerrar = driver.find_element(By.CSS_SELECTOR, selectorCerrar)
                botonCerrar.click()
                
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, id_detalle))
                )
                
                datosSucursal["Listado_Precios"].append(infoAuto)
                driver.execute_script("window.scrollBy(0, -100);")
                pausa()

    except:

        datosSucursal = {
            "Estado": estado,
            "Sucursal": "No hay sucursal",
            "Listado_Precios": "No hay precios"
        }
                    
        precios.append(datosSucursal)
        continue
    
    precios.append(datosSucursal)
    pausa()

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

carpetaPrincipal = "Resultados"
nombreSubcarpeta = f"precios_{timestamp}"

rutaGuardado = os.path.join(rutaScript, carpetaPrincipal, nombreSubcarpeta)

if not os.path.exists(rutaGuardado):
    os.makedirs(rutaGuardado)

rutaJSON = os.path.join(rutaGuardado, "precios.json")

with open(rutaJSON, 'w', encoding='utf-8') as f:
    json.dump(precios, f, ensure_ascii=False, indent=4)

rows = []
for entry in precios:
    estado = entry['Estado']
    sucursal = entry['Sucursal']
    
    if isinstance(entry['Listado_Precios'], str):
        rows.append({
            'Estado': estado,
            'Sucursal': sucursal,
            'Paquete': 'N/A',
            'Modelo': 'N/A',
            'Tarifa Basic': 'N/A',
            'Tarifa Smart': 'N/A',
            'Tarifa Plus': 'N/A'
        })
        continue

    for item in entry['Listado_Precios']:
        row = {
            'Estado': estado,
            'Sucursal': sucursal,
            'Paquete': item['Paquete'],
            'Modelo': item['Modelo']
        }
        for tarifa in item['Tarifas']:
            row.update(tarifa)
        rows.append(row)

df = pd.DataFrame(rows)

rutaCSV = os.path.join(rutaGuardado, f"precios.csv")
rutaExcel = os.path.join(rutaGuardado, f"precios.xlsx")

df.to_csv(rutaCSV, index=False, encoding='utf-8-sig')

with pd.ExcelWriter(rutaExcel, engine='openpyxl') as writer:
    nombreHoja = 'PreciosAvis'
    df.to_excel(writer, index=False, sheet_name=nombreHoja)
    
    worksheet = writer.sheets[nombreHoja]
    
    for idx, col in enumerate(df.columns):
        largoDatos = max(len(str(val)) for val in df[col])
        largoCabecera = len(str(col))
        
        maxLen = max(largoDatos, largoCabecera) + 3
        colLetter = get_column_letter(idx + 1)
        
        worksheet.column_dimensions[colLetter].width = maxLen
#endregion

