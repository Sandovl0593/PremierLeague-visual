import psycopg2
import os, sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
pass_db = os.getenv("PASS_DB")

# ==== Setup Database ====
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password=pass_db
    )
    cursor = conn.cursor()

    with open("model.psql", "r") as f:
        sql_script = f.read()
        cursor.execute(sql_script)
        conn.commit()
        print("[+] Base de datos creado correctamente")

except Exception as e:
    print("[-] No se pudo conectar a la base de datos por:", e)
    conn.rollback()
    if cursor:  cursor.close()
    if conn:    conn.close()
    sys.exit()


# ==== Insertar datos BY COPY ====
try:
    with open("teams.csv", 'r') as f:
        next(f)
        cursor.copy_from(f, "teams", sep=",")

    with open("seasons.csv", "r") as f:
        next(f)
        cursor.copy_from(f, "seasons", sep=",")

    with open("season_teams.csv", "r") as f:
        next(f)
        cursor.copy_from(f, "season_teams", sep=",")

    with open("stat_registers.csv", "r") as f:
        next(f)
        cursor.copy_from(f, "stat_registers", sep=",")
    
    conn.commit()
    print("[+] Datos insertados correctamente")

except Exception as e:
    print("[-] No se pudo insertar los datos por:", e)
    conn.rollback()

finally:
    if cursor:  cursor.close()
    if conn:    conn.close()