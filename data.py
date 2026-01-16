import csv
import pandas as pd
import os, sys

seasons = pd.read_csv("seasons.csv")
team_seasons_columns = ["steam_id", "team_name","season_id", "position", "points"]
stat_registers_columns = ["stat_id", "steam_id", "games_played", "n_wins", "n_draws", "n_losses", "goals_for", "goals_against", "goals_diff"]

# ==== Data Cleaning ====
team_file = lambda year: f"teams/teams_{year}-{year + 1}.csv"
register_file = lambda year: f"registers/registers_{year}-{year + 1}.csv"

reg_count = 0
df_joint_seasons = pd.DataFrame()
df_joint_registers = pd.DataFrame()

for season_idx, row in seasons.iterrows():
    year = row['start_year']
    # === Teams ===
    with open(team_file(year), "r") as f:
        content = f.read().split("\n")[1:-1]
    
    only_team = [l.lstrip("0123456789").strip() for l in content]
    df_team = pd.DataFrame(only_team, columns=["team_name"])

    df_stat_registers = pd.read_csv(register_file(year), header=0)
    df_stat_registers.rename(columns={
        'GP': 'games_played',
        'W': 'n_wins',
        'L': 'n_losses',
        'D': 'n_draws',
        'F': 'goals_for',
        'A': 'goals_against',
        'GD': 'goals_diff',
        'P': 'points'
    }, inplace=True)

    register_info = df_stat_registers.iterrows()

    # add columns
    df_stat_registers["stat_id"] = 0
    df_stat_registers["steam_id"] = 0
    
    team_seasons = []
    for pos, register in register_info:
        team_name = df_team.iloc[pos]["team_name"]
        
        df_stat_registers.at[pos,"stat_id"] = reg_count + 1
        df_stat_registers.at[pos,"steam_id"] = reg_count + 1
        team_seasons.append([reg_count + 1, team_name, f"S{season_idx + 1}", pos + 1, register["points"]])
        reg_count += 1
    
    df_team_seasons = pd.DataFrame(team_seasons, columns=team_seasons_columns)

    df_stat_registers.drop(columns=["points"], inplace=True)

    df_joint_seasons = pd.concat([df_joint_seasons, df_team_seasons], ignore_index=True)
    df_joint_registers = pd.concat([df_joint_registers, df_stat_registers], ignore_index=True)

# reorder columns
df_joint_seasons = df_joint_seasons[team_seasons_columns]
df_joint_registers = df_joint_registers[stat_registers_columns]

df_joint_seasons.to_csv("season_teams.csv", index=False)
df_joint_registers.to_csv("stat_registers.csv", index=False)

print("[+] Datos limpiados y ordenados")

# ==== Clear prev data ====
for file in os.listdir("registers"):
    os.remove(os.path.join("registers", file))
for file in os.listdir("teams"):
    os.remove(os.path.join("teams", file))

os.removedirs("registers")
os.removedirs("teams")