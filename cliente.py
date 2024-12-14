from pydantic import BaseModel
from fastapi import FastAPI
import requests
import json

class Laureate(BaseModel):
    id: int
    firstname: str | None = None
    surname: str | None = None
    motivation: str | None = None
    share: str | None = None

class Prize(BaseModel):
    category: str | None = None
    year: str | None = None

ip_address = ""

def print_response(response):
    if isinstance(response, dict):
        for key, value in response.items():
            if isinstance(value, dict):  # Si el valor es otro diccionario
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
    else:
        print("Response is not a valid dictionary")

def get_all_laureates(api_url: str):
    response = requests.get(f"{api_url}/laureates")
    if response.status_code == 200:
        # return response.json()  # Devuelve el JSON como un diccionario
        # print(response.status_code)
        return print(response.json())  # Devuelve el JSON como un diccionario
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def get_laureate_by_id(laureate_id: int):
    response = requests.get(f"{ip_address}/laureates/{laureate_id}")
    if response.status_code == 200:
        # return print(response.json())  # Devuelve los datos del laureado
        return print_response(response.json()["details"])
    elif response.status_code == 404:
        # response_data = response.json()
        print(response.json()["detail"])
        # return f"Laureate with ID {laureate_id} not found"
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def search_laureates_by_name(firstname: str = None, surname: str = None):
    params = {}
    if firstname:
        params['firstname'] = firstname
    if surname:
        params['surname'] = surname

    response = requests.get(f"{ip_address}/laureates/search", params=params)
    if response.status_code == 200:
        data = response.json()
        # print(data['results'])
        for result in data['results']:
            print(f'ID: {result['details']['id']}')
            print(f'Nombre: {result['details']['firstname']} {result['details']['surname']}')
            print(f'Motivacion: {result['details']['motivation']}')
            print(f'Shares: {result['details']['share']}')
            print(' ')
        # return print(response.json()["results"])  # Devuelve la lista de laureados que coinciden
        # return print_response(response.json())
    elif response.status_code == 404:
        # return print("No laureates found with the given criteria")
        print(response.json()["detail"])
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def get_prizes_by_year(year: int):
    """
    Consulta los premios Nobel por año desde el servidor.
    """
    response = requests.get(f"{ip_address}/prizes/{year}")
    if response.status_code == 200:
        data = response.json()
        print(f"Prizes for the year {data['year']}:\n")
        for prize in data["prizes"]:
            print(f"Category: {prize['category']}")
            print("Laureates:")
            for laureate in prize["laureates"]:
                name = laureate.get("firstname", "") + " " + laureate.get("surname", "")
                print(f"  - {name.strip()} ({laureate['motivation']})")
            print()
    elif response.status_code == 404:
        print(response.json()["detail"])
    else:
        print(f"Error {response.status_code}: {response.text}")

def get_prizes_by_category(category: str):
    """
    Consulta los premios Nobel por categoría desde el servidor.
    """
    response = requests.get(f"{ip_address}/prizes/category/{category}")
    if response.status_code == 200:
        data = response.json()
        print(f"Prizes for the category '{data['category']}':\n")
        for prize in data["prizes"]:
            print(f"Year: {prize['year']}")
            print("Laureates:")
            for laureate in prize["laureates"]:
                name = laureate.get("firstname", "") + " " + laureate.get("surname", "")
                print(f"  - {name.strip()} ({laureate['motivation']})")
            print()
    elif response.status_code == 404:
        print(response.json()["detail"])
    else:
        print(f"Error {response.status_code}: {response.text}")

def create_laureate():
    # Solicitar los datos del laureado
    firstname = input("Ingrese el nombre del laureado: ")
    surname = input("Ingrese el apellido del laureado: ")
    motivation = input("Ingrese la motivación del laureado: ")
    while True:
        try:
            share = int(input("Ingrese el share (debe ser un número): "))
            break
        except ValueError:
            print("El valor de 'share' debe ser un número entero.")

    # Crear un diccionario con los datos
    laureate_data = {
        "firstname": firstname,
        "surname": surname,
        "motivation": motivation,
        "share": share
    }

    # Realizar la solicitud POST al servidor
    url = "http://localhost:8000/laureates"
    response = requests.post(url, json=laureate_data)

    # Verificar la respuesta del servidor
    if response.status_code == 200:
        print(f"Laureado agregado exitosamente: {response.json()['message']}")
    else:
        print(f"Error al agregar el laureado: {response.json()['detail']}")

def create_prize():
    # Solicitar los datos del premio
    year = input("Ingrese el año del premio: ")
    category = input("Ingrese la categoría del premio: ")

    # Confirmar si desea agregar laureados
    # add_laureates = input("¿Desea agregar laureados a este premio? (sí/no): ").strip().lower()

    # laureates = []
    # if add_laureates == "sí" or "si" or "SI" or "s" or "S":
    #     while True:
    #         print("\nIngrese los datos del laureado:")
    #         firstname = input("Nombre: ")
    #         surname = input("Apellido: ")
    #         motivation = input("Motivación: ")
    #         share = input("Share: ")

    #         try:
    #             share = int(share)
    #         except ValueError:
    #             print("El 'share' debe ser un número entero.")
    #             continue

    #         laureates.append({
    #             "firstname": firstname,
    #             "surname": surname,
    #             "motivation": motivation,
    #             "share": share
    #         })

    #         another = input("¿Desea agregar otro laureado? (sí/no): ").strip().lower()
    #         if another != "sí":
    #             break

    # Crear el diccionario con los datos del premio
    prize_data = {
        "year": year,
        "category": category,
        # "laureates": laureates
    }

    # Realizar la solicitud POST al servidor
    url = "http://localhost:8000/prizes"
    response = requests.post(url, json=prize_data)

    # Verificar la respuesta del servidor
    if response.status_code == 200:
        print(f"Premio creado exitosamente: {response.json()['message']}")
    else:
        print(f"Error al crear el premio: {response.json()['detail']}")

# Funciones para procesar las opciones
def create(a):
    # url = "https://api.nobelprize.org/v1/prize.json"
    # print(a)
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         #escribir ok aca
    #         print("200")


    #         print("el año que quiere")
    #         direccion = input()
    #     else:
    #         print("Error al hacer la solicitud a la opción 3:", response.status_code)
    # except requests.exceptions.RequestException as e:
    #     print(f"Error de conexión: {e}")
    while True:
        print("1. Crear Galardonado")
        print("2. Crear Premio")
        print("3. Volver atras")

        seleccion = int(input("Elige una opcion: "))

        if seleccion == 1:
            create_laureate()
        elif seleccion == 2:
            create_prize()
        elif seleccion == 3:
            mostrar_menu()

def read(a):
    # url = "https://api.nobelprize.org/v1/prize.json"

    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         #escribir ok aca el json es == response.json()
    #         print(response.json()["prizes"][0])
    #         print("200")  # Mostrar respuesta
    #     else:
    #         print("Error al hacer la solicitud a la opción 2:", response.status_code)
    # except requests.exceptions.RequestException as e:
    #     print(f"Error de conexión: {e}")
    # while True:
        print("1. Consultar todos los Galardonado")
        print("2. Consultar un Galardonado por ID")
        print("3. Consultar un Galardonado por Nombre")
        print("4. Consultar Premio por Año")
        print("5. Consultar Premio por Categoria")
        # print("3. Volver atras")

        seleccion = int(input("Elige una opcion: "))

        if seleccion == 1:
            get_all_laureates(ip_address)
        elif seleccion == 2:
            id = int(input("Ingrese el ID del laureado: "))
            get_laureate_by_id(id)
        elif seleccion == 3:
            firstname = input("Ingrese el nombre: ")
            surname = input("Ingrese el apellido: ")
            search_laureates_by_name(firstname, surname)
        elif seleccion == 4:
            year = int(input("Ingrese el anio: "))
            get_prizes_by_year(year)
        elif seleccion == 5:
            print("Categorias:")
            print("1.chemistry")
            print("2.economics")
            print("3.literature")
            print("4.peace")
            print("5.physics")
            print("6.medicine")
            categoria = int(input("Inserte categoria: "))

            if categoria == 1:
                categoria = "chemistry"
            elif categoria == 2:
                categoria = "economics"
            elif categoria == 3:
                categoria = "literature"
            elif categoria == 4:
                categoria = "peace"
            elif categoria == 5:
                categoria = "physics"
            elif categoria == 6:
                categoria = "medicine"
            get_prizes_by_category(categoria)

def delete_prize():
    # Obtener la lista de premios disponibles
    url = f"{ip_address}/prizes"
    # Solicitar el ID del premio a eliminar
    prize_id = input("Ingrese el ID del premio que desea eliminar: ").strip()

    # Validar si el ID existe en el servidor
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error al obtener los premios: {response.json().get('detail', 'Error desconocido')}")
        return

    prizes = response.json()
    # print(prizes)

    # for prize_key in prizes:
    #     print(prize_key)

    # Verificar si el ID ingresado está en los premios
    if prize_id not in prizes:
        print("Error: el ID ingresado no corresponde a un premio existente.")
        return

    # Mostrar información del premio para confirmación
    prize = prizes[prize_id]
    print(f"Detalles del premio a eliminar:")
    print(f"  ID: {prize_id}")
    print(f"  Año: {prize['year']}")
    print(f"  Categoría: {prize['category']}")
    if "laureates" in prize and isinstance(prize["laureates"], list):
        print("  Laureados:")
        for laureate in prize["laureates"]:
            print(f"    - {laureate['firstname']} {laureate.get('surname', '')} (ID: {laureate['id']})")
    else:
        print("  Sin laureados asociados.")

    # Confirmación del usuario
    confirmation = input("¿Está seguro que desea eliminar este premio? (sí/no): ").strip().lower()
    if confirmation not in ["sí", "si"]:
        print("Eliminación cancelada.")
        return

    # Enviar solicitud DELETE
    delete_url = f"{url}/{prize_id}"
    delete_response = requests.delete(delete_url)

    # Manejo de la respuesta
    if delete_response.status_code == 200:
        print(f'{delete_response.json().get('message', 'Eliminado')}')
    elif delete_response.status_code == 404:
        print(f"Error: {delete_response.json().get('detail', 'Premio no encontrado')}")
    else:
        print(f"Error inesperado: {delete_response.json().get('detail', 'Error desconocido')}")

import requests

def update_laureate():
    try:
        laureate_id = input("Ingrese el ID del laureado que desea actualizar: ")
        print("Ingrese los nuevos datos del laureado (deje vacío para no modificar):")
        firstname = input("Nuevo nombre (firstname): ") or None
        surname = input("Nuevo apellido (surname): ") or None
        motivation = input("Nueva motivación (motivation): ") or None
        share = input("Nuevo share (share): ") or None

        data = Laureate(
            id = laureate_id,
            firstname = firstname,
            surname = surname,
            motivation = motivation,
            share = share
        )
        # if firstname:
        #     data["firstname"] = firstname
        # if surname:
        #     data["surname"] = surname
        # if motivation:
        #     data["motivation"] = motivation
        # if share:
        #     data["share"] = share

        if not data:
            print("No se ingresaron datos para actualizar. Operación cancelada.")
            return

        url = f"{ip_address}/laureates/{laureate_id}"
        datos_item = data.dict()
        response = requests.put(url, json=datos_item)
        print(f'URL: {url}')
        print(f'Data: {datos_item}')

        if response.status_code == 200:
            print("Actualización exitosa:", response.json())
        elif response.status_code == 404:
            print(f"Laureado con ID {laureate_id} no encontrado.")
        else:
            print(f"Error {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"Error al actualizar el laureado: {e}")

def update_prize():
    item_id = input("Ingresa el ID del ítem: ")
    year = input("Ingresa el año del ítem: ")
    category = input("Ingresa la categoría del ítem: ")
    year = str(year)
    category = str(category)


    # Crear un objeto Item con los nuevos datos
    nuevo_item = Prize(year=year, category=category)


    # URL de la API con el ID proporcionado
    url = f"http://127.0.0.1:8000/prizes/{item_id}"
    datos_item = nuevo_item.dict()


    # Hacer una solicitud PUT a la API
    response = requests.put(url, json=datos_item)


    # Comprobar la respuesta
    if response.status_code == 200:
        print("Ítem actualizado con éxito:")
        print(response.json())  # Muestra la respuesta de la API (el ítem actualizado)
    else:
        print(f"Error al actualizar el ítem. Código de estado: {response.status_code}")
        print(response.json())  # Muestra el mensaje de error


def update(a):
    print("1. Editar Laureado")
    print("2. Editar Premio")
    print("5. Exit")

    seleccion = int(input("Elige una opción: "))

    if seleccion == 1:
        update_laureate()
    elif seleccion == 2:
        update_prize()
    else:
        print("Opción no válida. Intenta de nuevo.")

def menu_borrar():
    print("1. Eliminar Premio")
    print("2. Eliminar Laureado")

    seleccion = int(input("Elige una opcion: "))

    if seleccion == 1:
        delete_prize()
    # elif seleccion == 2:
    #     delete_laureate()

# Función para mostrar el menú y manejar la selección
def mostrar_menu(dir):
    # while True:
        print("\nOscar Prizes API:")
        print("1. Create")
        print("2. Read")
        print("3. Update")
        print("4. Delete")
        print("5. Exit")

        seleccion = input("Elige una opción: ")

        if seleccion == "1":
            create(dir)
        elif seleccion == "2":
            read(dir)
        elif seleccion == "3":
            update(dir)
        elif seleccion == "4":
            menu_borrar()
            # break  # Salir del bucle y terminar el programa
        else:
            print("Opción no válida. Intenta de nuevo.")




# arranca?
def checkip():
    print("ingrese la ip del equipo servidor")
    ip_address = input()
    ip_address = "http://" + str(ip_address)+ ":8000"
    try:
        # response = requests.get(ip_address)
        response = requests.get(f"{ip_address}/testconeccion")
        if response.status_code == 200:
            print("coneccion establecida exitosamente")
            mostrar_menu(ip_address)

        else:
                print("Error la ip ingresada no esta respondiendo")
                checkip()
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        checkip()


# Iniciar el menú
if __name__ == "__main__":
    checkip()