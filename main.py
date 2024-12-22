import os, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

cls()

fichier = "liste.txt"

pays = input(f"Code du pays (exemple : fr) -> ")
print(f"")

def fetch_data(offset):
    try:
        print(f"[{offset}] Récupération des données...")
        requete = requests.get(f"https://combot.org/api/chart/{pays}?limit=100&offset={offset}")
        requete.raise_for_status()
        data = requete.json()

        resultats = []
        if isinstance(data, list):
            for groupes in data:
                groupe = groupes.get("u")
                if groupe:
                    resultats.append(groupe)
        else:
            return None

        return resultats
    except:
        return None

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(fetch_data, offset) for offset in range(1, 1000)]
    for future in as_completed(futures):
        resultats = future.result()
        if resultats:
            with open(fichier, "a", encoding="utf-8") as f:
                for groupe in resultats:
                    f.write(groupe + "\n")

print(f"\n[+] Les données sauvegardées dans -> {fichier}")
