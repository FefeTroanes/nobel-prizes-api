from fastapi import FastAPI
import requests
import json

ip_address = "http://127.0.0.1:8000"

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
        # return print(response.json()["results"])  # Devuelve la lista de laureados que coinciden
        return print_response(response.json())
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
            create_prize(dir)
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




def opcion_3(a):
    url = "https://api.nobelprize.org/v1/prize.json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            #escribir ok aca


            print("200")
        else:
            print("Error al hacer la solicitud a la opción 3:", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

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
            opcion_3(dir)
        elif seleccion == "4":
            print("Saliendo del programa...")
            # break  # Salir del bucle y terminar el programa
        else:
            print("Opción no válida. Intenta de nuevo.")




# arranca?
def checkip(ip_address: str):
    # print("ingrese la ip del equipo servidor")
    # ip_address = input()
    # ip_address = "http://" + str(ip_address)+ ":8000/testconeccion/"
    # ip_address = "http://127.0.0.1:8000/testconeccion/"
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
    checkip(ip_address)