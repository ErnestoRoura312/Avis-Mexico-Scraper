# Avis Mexico Scraper

Este es un scraper automatizado desarrollado en **Python** utilizando **Selenium**. Su objetivo es extraer información de precios y disponibilidad de vehículos de la web oficial de Avis México, procesando múltiples estados de la república de forma secuencial.

## 📋 Características
*   **Automatización Completa**: Navega, busca y extrae precios sin intervención manual.
*   **Configuración Externa**: Las fechas de renta se gestionan desde un archivo `config.txt` (Notepad).
*   **Múltiples Formatos**: Genera reportes detallados en formatos **JSON**, **CSV** y **Excel** (.xlsx).

## 🛠️ Requisitos
Antes de ejecutar el script, asegúrate de tener instalado:
*   [Python 3.10+](https://www.python.org/downloads/)
*   [Google Chrome](https://www.google.com/chrome/)
*   Dependencias de Python (ver sección de instalación).

## Instalación y Uso

1. **Clona el repositorio:**
   ```
   git clone https://github.com/ErnestoRoura312/Avis-Mexico-Scraper.git
   cd Avis-Mexico-Scraper
   ```
2. **Dirigete a la carpeta del proyecto:**
   ```
   cd Avis-Mexico-Scraper
   ```
3. **Instala las librerías necesarias:**
   ```
   pip install -r requirements.txt
   ```
4. **Configura tus fechas:**
   Edita el archivo Configuracion/config.txt con el siguiente formato:
   ```
   fechaEntrega: DD/MM/YY
   fechaDevolucion: DD/MM/YY
   ```
5. **Ejecuta el script:**
   ```
   python ScrapperTodosLosEstados.py
   ```
## ⚖️ Aviso Legal y Ético

Este proyecto fue desarrollado exclusivamente con **fines educativos y de análisis de datos**. 

*   **Ética de Scraping**: El script ha sido diseñado para realizar peticiones de forma respetuosa, evitando saturar los servidores del sitio web objetivo.
*   **Propiedad Intelectual**: Todos los derechos sobre la marca "Avis" y sus datos pertenecen a sus respectivos dueños. Este proyecto no tiene afiliación oficial con la empresa.
