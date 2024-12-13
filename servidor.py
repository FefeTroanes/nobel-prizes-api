from fastapi import FastAPI, HTTPException, Request
import requests
import json
import os

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

@app.get("/prizes/category/{category}")
def get_prizes_by_category(category: str):
    """
    Devuelve los premios Nobel de una categoría específica.
    """
    try:
        # Carga el archivo prizes.json
        with open("prizes.json", "r") as archivo:
            prizes = json.load(archivo)  # Convertir a diccionario

            # Filtrar premios por la categoría
            prizes_by_category = [
                {
                    "year": prize["year"],
                    "laureates": prize.get("laureates", [])  # Obtener 'laureates' o una lista vacía si no existe
                }
                for prize_id, prize in prizes.items()
                if prize.get("category", "").lower() == category.lower()  # Comparar ignorando mayúsculas/minúsculas
            ]

            if prizes_by_category:
                return {"category": category, "prizes": prizes_by_category}
            else:
                raise HTTPException(status_code=404, detail=f"No prizes found for category '{category}'")

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

# //////////////   POST   //////////////
@app.post("/laureates")
async def add_laureate(request: Request):
    """
    Agrega un nuevo laureado al archivo laureates.json con un ID auto incremental.
    """
    try:
        # Obtén los datos del cuerpo de la solicitud
        laureate_data = await request.json()

        # Validar campos requeridos excepto ID (será generado automáticamente)
        required_fields = {"firstname", "motivation", "share"}
        if not required_fields.issubset(laureate_data.keys()):
            raise HTTPException(status_code=400, detail="Missing required fields.")

        if not isinstance(laureate_data["share"], int):
            raise HTTPException(status_code=400, detail="'share' must be an integer.")
        if not isinstance(laureate_data["firstname"], str):
            raise HTTPException(status_code=400, detail="'firstname' must be a string.")

        # Verifica si el archivo existe
        if not os.path.exists("laureates.json"):
            raise HTTPException(status_code=500, detail="File laureates.json not found")

        # Carga el archivo laureates.json
        with open("laureates.json", "r") as archivo:
            laureates = json.load(archivo)

        # Determina el próximo ID disponible (auto incremental)
        next_id = max(map(int, laureates.keys())) + 1 if laureates else 1

        # Agregar el nuevo laureado con el ID generado
        laureates[str(next_id)] = {
            "id": str(next_id),
            "firstname": laureate_data["firstname"],
            "surname": laureate_data.get("surname", None),  # Campo opcional
            "motivation": laureate_data["motivation"],
            "share": str(laureate_data["share"])
        }

        # Guardar los cambios en el archivo
        with open("laureates.json", "w") as archivo:
            json.dump(laureates, archivo, indent=4)

        return {"message": f"Laureate with ID {next_id} added successfully."}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="File laureates.json not found")

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding laureates.json")

@app.post("/prizes")
def create_prize(prize: dict):
    try:
        # Leer el archivo prizes.json
        with open("prizes.json", "r") as f:
            prizes = json.load(f)

        # Generar un nuevo ID para el premio
        new_id = str(max(int(k) for k in prizes.keys()) + 1)

        # Validar que los datos del premio sean correctos
        if "year" not in prize or "category" not in prize:
            raise HTTPException(status_code=400, detail="El premio debe tener 'year' y 'category'.")

        # Validar y preparar la lista de laureados
        laureates = prize.get("laureates", [])
        if laureates:
            for laureate in laureates:
                if "firstname" not in laureate or "surname" not in laureate or "motivation" not in laureate or "share" not in laureate:
                    raise HTTPException(
                        status_code=400,
                        detail="Cada laureado debe tener 'firstname', 'surname', 'motivation' y 'share'."
                    )

        # Crear el nuevo premio
        new_prize = {
            "year": prize["year"],
            "category": prize["category"],
            "laureates": laureates
        }

        # Agregar el premio al archivo
        prizes[new_id] = new_prize
        with open("prizes.json", "w") as f:
            json.dump(prizes, f, indent=4)

        return {"message": f"Premio con ID {new_id} creado exitosamente."}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="No se encontró el archivo prizes.json.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



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



