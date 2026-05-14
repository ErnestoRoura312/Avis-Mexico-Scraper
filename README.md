# Avis Mexico Scraper

This is an automated scraper developed in **Python** using **Selenium**. Its goal is to extract vehicle pricing and availability data from the official Avis Mexico website, processing multiple states across the country sequentially.

## 📋 Features
* **Full Automation**: Navigates, searches, and extracts prices without manual intervention.
* **External Configuration**: Rental dates are managed through a `config.txt` file (Notepad).
* **Multiple Formats**: Generates detailed reports in **JSON**, **CSV**, and **Excel** (.xlsx) formats.

## 🛠️ Requirements
Before running the script, ensure you have the following installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [Google Chrome](https://www.google.com/chrome/)
* Python dependencies (see the installation section).

## Installation and Usage

1. **Clone the repository:**
   ```
   git clone https://github.com/ErnestoRoura312/Avis-Mexico-Scraper.git
   ```
2. **Navigate to the project folder:**
   ```
   cd Avis-Mexico-Scraper
   ```
3. **Install the required libraries:**
   ```
   pip install -r requirements.txt
   ```
4. **Configure your dates:**
   Edit the file Configuracion/config.txt using the following format:
   ```
   fechaEntrega: DD/MM/YY
   fechaDevolucion: DD/MM/YY
   ```
5. **Run the script:**
   ```
   python ScrapperTodosLosEstados.py
   ```
## ⚖️ Legal and Ethical Notice

This project was developed exclusively for **educational and data analysis purposes**. 

*   **Scraping Ethics**: The script is designed to perform requests respectfully, avoiding overloading the target website's servers.
*   **Intellectual Property**: All rights to the "Avis" brand and its data belong to their respective owners. This project has no official affiliation with the company.
