import requests
import datetime
import json

# Coordenades de Barcelona (pots canviar-les per qualsevol altra ciutat)
latitude = 41.3851
longitude = 2.1734

# Obtenir la data actual en format ISO i per al nom del fitxer
avui = datetime.date.today()
data_str = avui.strftime("%Y%m%d")

# URL de l'API Open-Meteo
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}&"
    f"hourly=temperature_2m&timezone=auto"
)

# Fer la petició a l'API
resposta = requests.get(url)
dades = resposta.json()

# Obtenir les temperatures horàries del dia d'avui
hores = dades["hourly"]["time"]
temperatures = dades["hourly"]["temperature_2m"]

# Filtrar només les temperatures del dia d'avui
temps_avui = [
    temp for hora, temp in zip(hores, temperatures)
    if hora.startswith(str(avui))
]

# Comprovar que tenim dades
if not temps_avui:
    print("No s'han trobat temperatures per avui.")
    exit()

# Calcular estadístiques
temp_max = max(temps_avui)
temp_min = min(temps_avui)
temp_mitjana = round(sum(temps_avui) / len(temps_avui), 2)

# Crear diccionari amb resultats
resultat = {
    "data": str(avui),
    "poblacio": "Barcelona",
    "temperatura_maxima": temp_max,
    "temperatura_minima": temp_min,
    "temperatura_mitjana": temp_mitjana,
}

# Escriure a un fitxer JSON
nom_fitxer = f"temp_{data_str}.json"
with open(nom_fitxer, "w", encoding="utf-8") as fitxer:
    json.dump(resultat, fitxer, indent=4)

print(f"Dades desades a {nom_fitxer}")
