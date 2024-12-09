import json
import os
import random
import re


# Funkcja walidacji numeru PESEL (w tym momencie pusta)
def validate_pesel(pesel):
    # Tu zaimplementujesz walidację numeru PESEL
    return True

# Funkcja walidacji numeru NIP (w tym momencie pusta)
def validate_nip(nip):
    # Tu zaimplementujesz walidację numeru NIP
    return True

# Funkcja walidacji numeru REGON (w tym momencie pusta)
def validate_regon(regon):
    # Tu zaimplementujesz walidację numeru REGON
    return True

# Funkcja dodająca użytkownika do pliku
def add_user(user_data):
    folder_path = "data/"
    filename = os.path.join(folder_path, "users.json")
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    pesel = user_data.get('pesel')
    nip = user_data.get('nip')
    regon = user_data.get('regon')

    if not validate_pesel(pesel):
        raise ValueError("Nieprawidłowy numer PESEL.")
    if not validate_nip(nip):
        raise ValueError("Nieprawidłowy numer NIP.")
    if not validate_regon(regon):
        raise ValueError("Nieprawidłowy numer REGON.")

    users = []
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except json.JSONDecodeError:
            print(f"Plik {filename} jest pusty lub ma nieprawidłowy format. Tworzę nowy plik.")
            users = []

    next_id = users[-1]['id'] + 1 if users else 1
    user_data['id'] = next_id


    users.append(user_data)


    with open(filename, "w") as file:
        json.dump(users, file, indent=4)
    print(f"Użytkownik '{user_data['name']}' został dodany pomyślnie.")


def edit_user(user_id, updated_data):
    folder_path = "data/"
    filename = os.path.join(folder_path, "users.json")
    
    # Wczytanie danych z pliku
    if not os.path.exists(filename):
        print("Plik z użytkownikami nie istnieje.")
        return
    
    with open(filename, "r") as file:
        users = json.load(file)


    user = next((user for user in users if user['id'] == user_id), None)
    
    if user is None:
        print(f"Nie znaleziono użytkownika o ID {user_id}.")
        return

    # Aktualizacja danych użytkownika
    user.update(updated_data)


    with open(filename, "w") as file:
        json.dump(users, file, indent=4)
    print(f"Dane użytkownika o ID {user_id} zostały zaktualizowane.")

# Funkcja usuwająca użytkownika na podstawie ID
def remove_user(user_id):
    folder_path = "data/"
    filename = os.path.join(folder_path, "users.json")
    
    # Wczytanie danych z pliku
    if not os.path.exists(filename):
        print("Plik z użytkownikami nie istnieje.")
        return
    
    with open(filename, "r") as file:
        users = json.load(file)

    # Szukamy użytkownika o podanym ID
    user = next((user for user in users if user['id'] == user_id), None)

    if user is None:
        print(f"Nie znaleziono użytkownika o ID {user_id}.")
        return
    
    # Usuwamy użytkownika
    users.remove(user)

   
    with open(filename, "w") as file:
        json.dump(users, file, indent=4)
    print(f"Użytkownik o ID {user_id} został usunięty.")


def load_users():
    folder_path = "data/"
    filename = os.path.join(folder_path, "users.json")

    # Wczytanie danych z pliku
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                users = json.load(file)
            
            if users:
                print("\nLista użytkowników:")
                for user in users:
                    print(f"ID: {user['id']}")
                    print(f"Imię i nazwisko: {user['name']}")
                    print(f"NIP: {user['nip']}")
                    print(f"PESEL: {user['pesel']}")
                    print(f"REGON: {user['regon']}")
                    print("-" * 40)
            else:
                print("Brak użytkowników w pliku.")
        except json.JSONDecodeError:
            print(f"Plik {filename} jest pusty lub ma nieprawidłowy format.")
    else:
        print(f"Plik {filename} nie istnieje.")

if __name__ == "__main__":
    while True:
        print("\n1. Dodaj użytkownika")
        print("2. Edytuj użytkownika")
        print("3. Usuń użytkownika")
        print("4. Wyświetl wszystkich użytkowników")
        print("5. Zakończ")

        option = input("Wybierz opcję: ")
        if option == "1":
            print("\nDodawanie nowego użytkownika:")
            try:
                name = input("Podaj imię i nazwisko: ").strip()
                pesel = input("Podaj PESEL: ").strip()
                nip = input("Podaj NIP: ").strip()
                regon = input("Podaj REGON: ").strip()

                user_data = {
                    "name": name,
                    "pesel": pesel,
                    "nip": nip,
                    "regon": regon
                }

                add_user(user_data)
            except Exception as e:
                print(f"Błąd podczas dodawania użytkownika: {e}")
        elif option == "2":
            try:
                user_id = int(input("Podaj ID użytkownika do edycji: ").strip())
                updated_name = input("Podaj nowe imię i nazwisko: ").strip()
                updated_pesel = input("Podaj nowy PESEL: ").strip()
                updated_nip = input("Podaj nowy NIP: ").strip()
                updated_regon = input("Podaj nowy REGON: ").strip()

                updated_data = {
                    "name": updated_name,
                    "pesel": updated_pesel,
                    "nip": updated_nip,
                    "regon": updated_regon
                }

                edit_user(user_id, updated_data)
            except Exception as e:
                print(f"Błąd podczas edycji użytkownika: {e}")
        elif option == "3":
            try:
                user_id = int(input("Podaj ID użytkownika do usunięcia: ").strip())
                remove_user(user_id)
            except Exception as e:
                print(f"Błąd podczas usuwania użytkownika: {e}")
        elif option == "4":
            load_users()
        elif option == "5":
            print("Zakończenie programu")
            break
