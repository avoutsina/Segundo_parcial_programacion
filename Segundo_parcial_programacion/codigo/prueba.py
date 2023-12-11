import json
with open("niveles.json", "r") as archivo:
    niveles = json.load(archivo)
listan_niveles = niveles["niveles"]

print(listan_niveles)