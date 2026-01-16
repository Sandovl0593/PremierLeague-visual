from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import os, sys

# ===== Seasons =====
seasons = []
start_year = 2003
season_columns = ["season_id", "season_name", "start_year"]

count_year = 1
for year in range(start_year, datetime.now().year):   # hasta 2025-2026
    seasons.append([f"S{count_year}", f"{year}-{year + 1}", year])
    count_year += 1

df_seasons = pd.DataFrame(seasons, columns=season_columns)
df_seasons.to_csv("seasons.csv", index=False)

# ===== Directorios para data extraida =====
if not os.path.exists("teams"):
    os.makedirs("teams")
if not os.path.exists("registers"):
    os.makedirs("registers")

count_years = datetime.now().year - start_year
if len(os.listdir("teams")) == count_years:
    print("[+] Extracción ya completada previamente")
    sys.exit()

# ===== Setup Driver =====
url = lambda year: f"https://www.espn.com/soccer/standings/_/league/ENG.1/season/{year}" 

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-dev-shm-usage")

driver_path = r"C:\\chromedriver-win64\\chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=chromeOptions)
print("[+] Driver listo")


# ===== Extraccion de datos =====
def extract_data(table, has_headers=True):
    """
    Extrae los datos de una tabla de ESPN
    """
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) == 0:
            continue
        data.append([col.text.strip().replace("\n", "") for col in cols])
    
    if has_headers:
        header = table.find_elements(By.TAG_NAME, "th")
        headers = [header.text for header in header]
        return headers, data
    return data
    

for _, season in df_seasons.iterrows():
    step = f"-- ({season['season_name']})"
    if os.path.exists(f"teams/teams_{season['season_name']}.csv") or os.path.exists(f"registers/registers_{season['season_name']}.csv"):
        print(f"{step} Datos ya extraidos")
        continue

    try:
        print(f"\n{step} Obteniendo datos ...")
        driver.get(url(season["start_year"]))
        
        tables = driver.find_elements(By.CLASS_NAME, "Table")
        print(f"{step} Tables encontradas: {len(tables)}")

        if len(tables) < 2:
            raise Exception("No se encontraron tablas")
        
        data_team = extract_data(tables[0], False)     # Table Teams, sin headers
        df_teams = pd.DataFrame(data_team)
        
        headers_registers, data_registers = extract_data(tables[1])  # Table Registers (ESPN Stats), con headers
        df_registers = pd.DataFrame(data_registers, columns=headers_registers)

        df_teams.to_csv(f"teams/teams_{season['season_name']}.csv", index=False)
        print(f"{step} Guardado Teams")
        df_registers.to_csv(f"registers/registers_{season['season_name']}.csv", index=False)
        print(f"{step} Guardado Registers")
    
    except Exception as e:
        print(f"{step} Error al obtener datos:")
        print(e)
    finally:
        driver.refresh()
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Table"))
        )
