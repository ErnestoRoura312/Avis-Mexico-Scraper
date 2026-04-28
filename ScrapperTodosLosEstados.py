#region Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import re
import pandas as pd
import os
from datetime import datetime
import json
#endregion

#region Funciones
def pausa():
    sleep(random.uniform(1, 2))
#endregion

#region Codigo
serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv)
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_archivo_txt = os.path.join(ruta_script, "Recursos/EstadosMexico.txt")

driver.maximize_window()

precios = []
arreglo_estados = []

fecha_entrega = "2026-3-29" 
selectorFechaEntrega = f'[data-mdb-date="{fecha_entrega}"]'
fecha_devolucion = "2026-3-30" 
selectorFechaDevolucion = f'[data-mdb-date="{fecha_devolucion}"]'

with open(ruta_archivo_txt, 'r', encoding='utf-8') as archivo:
    arreglo_estados = [linea.strip() for linea in archivo if linea.strip()]

for estado in arreglo_estados:
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
            fechaEntrega.click()
            botonDiaEntrega = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selectorFechaEntrega))
            )
            botonDiaEntrega.click()
            fechaDevolucion.click()
            botonDiaDevolucion = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selectorFechaDevolucion))
            )
            botonDiaDevolucion.click()
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

carpeta_principal = "Resultados"
nombre_subcarpeta = f"precios_{timestamp}"

ruta_guardado = os.path.join(ruta_script, carpeta_principal, nombre_subcarpeta)

if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

ruta_json = os.path.join(ruta_guardado, "precios.json")

with open(ruta_json, 'w', encoding='utf-8') as f:
    json.dump(precios, f, ensure_ascii=False, indent=4)
#endregion

