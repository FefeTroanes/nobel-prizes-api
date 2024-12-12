from fastapi import FastAPI, HTTPException
# import requests
import json

app = FastAPI()

laureates = []
prizes = []

# fastapi dev servidor.py

# //////////////   MODELS   //////////////
class Laureate:
    firstname: str
    surname: str
    motivation: str
    share: str

class Prize:
    year: str
    category: str
    laureates: [Laureate]


# //////////////   GET   //////////////
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/prizes")
def get_all_prizes():
    with open('prizes.json', 'r') as archivo:
    # Lee el contenido del archivo
        content = archivo.read()
        return {content}

@app.get("/prizes/{year}")
def get_prizes_by_year(year: int):
    """
    Devuelve los premios Nobel correspondientes a un año específico.
    """
    try:
        # Carga el archivo prizes.json
        with open("prizes.json", "r") as archivo:
            prizes = json.load(archivo)  # Convertir a diccionario

            # Filtrar premios por el año
            prizes_by_year = [
                {
                    "category": prize["category"],
                    "laureates": prize["laureates"]
                }
                for prize_id, prize in prizes.items()
                if prize.get("year") == str(year)  # Comparar el año como cadena
            ]

            if prizes_by_year:
                return {"year": year, "prizes": prizes_by_year}
            else:
                raise HTTPException(status_code=404, detail=f"No prizes found for year {year}")

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="File prizes.json not found")

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding prizes.json")

@app.get("/laureates")
def get_all_laureates():
    with open('laureates.json', 'r') as archivo:
    # Lee el contenido del archivo
        content = archivo.read()
        return {content}

@app.get("/laureates/search")
def search_laureates_by_name(firstname: str = None, surname: str = None):
    import json
    try:
        with open('laureates.json', 'r') as archivo:
            # Carga el contenido del archivo como un diccionario
            laureates = json.load(archivo)

            # Filtrar laureados por nombre y/o apellido
            results = [
                {"id": id, "details": details}
                for id, details in laureates.items()
                if (firstname is None or details.get("firstname", "").lower() == firstname.lower())
                and (surname is None or details.get("surname", "").lower() == surname.lower())
            ]

            if results:
                return {"results": results}
            else:
                raise HTTPException(status_code=404, detail="No laureates found with the given name(s)")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="File laureates.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding laureates.json")

@app.get("/laureates/{id}")
def get_laureate_by_id(id: int):
    """
    Busca un laureado por su ID en el archivo laureates.json.
    """
    try:
        # Abre el archivo laureates.json
        with open("laureates.json", "r") as archivo:
            laureates = json.load(archivo)  # Carga el contenido como un diccionario

            # Busca el laureado por su ID
            laureate = laureates.get(str(id))  # Convertir el ID a string para coincidir con las claves del JSON

            if laureate:
                return {"id": id, "details": laureate}
            else:
                # Si no se encuentra, lanza una excepción HTTP con un código 404
                raise HTTPException(status_code=404, detail=f"Laureate with ID {id} not found")

    except FileNotFoundError:
        # Si el archivo no existe
        raise HTTPException(status_code=500, detail="File laureates.json not found")

    except json.JSONDecodeError:
        # Si hay un error al decodificar el archivo JSON
        raise HTTPException(status_code=500, detail="Error decoding laureates.json")


# //////////////   POST   //////////////
@app.post("/laureates")
def create_laureates(laureate):
    laureates.append(laureate)
    return laureates

@app.get("/laureates/{id}")
def get_laureate(id: int):
    try:
        with open('laureates.json', 'r') as archivo:
            # Carga el contenido del archivo como un diccionario
            laureates = json.load(archivo)
            # Busca el laureado por el ID proporcionado
            laureate = laureates.get(str(id))  # Convierte `id` a string porque los IDs en JSON son cadenas
            if laureate:
                return {"id": id, "details": laureate}
            else:
                # Lanza una excepción HTTP con un código 404 si no se encuentra el laureado
                raise HTTPException(status_code=404, detail=f"Laureate with id {id} not found")
    except FileNotFoundError:
        # Excepción HTTP 500 si el archivo no existe
        raise HTTPException(status_code=500, detail="File laureates.json not found")
    except json.JSONDecodeError:
        # Excepción HTTP 500 si hay un error al decodificar el archivo JSON
        raise HTTPException(status_code=500, detail="Error decoding laureates.json")

@app.get("/laureates/search")
def search_laureates(firstname: str = None, surname: str = None):
    import json
    try:
        with open('laureates.json', 'r') as archivo:
            # Carga el contenido del archivo como un diccionario
            laureates = json.load(archivo)

            # Filtrar laureados por nombre y/o apellido
            results = [
                {"id": id, "details": details}
                for id, details in laureates.items()
                if (firstname is None or details.get("firstname", "").lower() == firstname.lower())
                and (surname is None or details.get("surname", "").lower() == surname.lower())
            ]

            if results:
                return {"results": results}
            else:
                raise HTTPException(status_code=404, detail="No laureates found with the given name(s)")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="File laureates.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding laureates.json")

@app.get("/testconeccion/")
def testconect():
    return {"200"}




# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#   with open('memoria.txt', 'r') as archivo:
#     # Lee el contenido del archivo
#     contenido = archivo.read()
#     contenido = json.loads(contenido)
#     if item_id < 0 or item_id >= len(contenido):
#         raise HTTPException(status_code=404, detail="Item not found")

#     retorna = str(json.dumps(contenido["prizes"][item_id]))
#     print(retorna)
#     # json.load(str)
#     print(json.loads(retorna))
#     return {retorna}



