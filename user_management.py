import json
import os
import random
import re

def validate_pesel(pesel):
    """
    Sprawdza poprawność numeru PESEL na podstawie miesiąca, dnia i cyfry kontrolnej.
    Uwzględnia fakt, że osoby urodzone w latach 1900-2099 mają numery miesięcy od 01 do 32.
    """
    if len(pesel) != 11 or not pesel.isdigit():
        print("PESEL musi mieć 11 cyfr. Spróbuj ponownie.")
        return False

    digits = [int(digit) for digit in pesel]  # Rozdzielamy pesel na cyfry

    # Miesiące w numerze PESEL dla osób urodzonych w latach 1900-2099 mogą wynosić od 01 do 32
    month = digits[2] * 10 + digits[3]
    if not (1 <= month <= 32):  # Miesiące mogą mieć wartości od 01 do 32
        print("Niepoprawny miesiąc w numerze PESEL. Spróbuj ponownie.")
        return False

    # Sprawdzenie poprawności dnia (01-31)
    day = digits[4] * 10 + digits[5]
    if not (1 <= day <= 31):  # Sprawdzamy, czy dzień jest w zakresie 01-31
        print("Niepoprawny dzień w numerze PESEL. Spróbuj ponownie.")
        return False

    # Suma kontrolna PESEL
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = sum(d * w for d, w in zip(digits[:10], weights))
    control_digit = (10 - (checksum % 10)) % 10

    # Sprawdzamy, czy cyfra kontrolna jest poprawna
    if control_digit != digits[10]:
        print("Niepoprawna cyfra kontrolna w numerze PESEL. Spróbuj ponownie.")
        return False

    return True



# Funkcja walidacji numeru NIP
def validate_nip(nip):
    if len(nip) != 10 or not nip.isdigit():
        return False  # NIP musi mieć 10 cyfr
    
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    checksum = sum(int(nip[i]) * weights[i] for i in range(9))
    control_digit = checksum % 11
    
    # Sprawdzenie sumy kontrolnej
    if control_digit == 10:
        return False  # Jeśli suma kontrolna wynosi 10, NIP jest niepoprawny
    return int(nip[-1]) == control_digit

def validate_regon(regon):
    if len(regon) == 9 and regon.isdigit():
        # Wagi dla REGON 9-cyfrowego
        weights = [8, 9, 2, 3, 4, 5, 6, 7]
        checksum = sum(int(regon[i]) * weights[i] for i in range(8)) % 11
        return checksum == int(regon[-1])

    # Walidacja 14-cyfrowego REGON (firmowego) – bez sumy kontrolnej
    elif len(regon) == 14 and regon.isdigit():
        return True  # REGON 14-cyfrowy jest poprawny, jeśli składa się z cyfr

    return False

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

def generate_password(length=12):
    """
    Funkcja generująca silne hasło o minimalnej długości 12 znaków, zawierające:
    - Duże litery,
    - Małe litery,
    - Cyfry,
    - Znaki specjalne.
    """

    # Definicje grup znaków
    lowercase = list(string.ascii_lowercase)  # Małe litery
    uppercase = list(string.ascii_uppercase)  # Duże litery
    digits = list(string.digits)  # Cyfry
    special_chars = list(string.punctuation)  # Znaki specjalne

    # Zapewnienie, że hasło zawiera przynajmniej jeden znak z każdej grupy
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    # Dodanie losowych znaków do reszty hasła, aby długość wynosiła co najmniej `length`
    all_chars = lowercase + uppercase + digits + special_chars
    while len(password) < length:
        password.append(random.choice(all_chars))

    # Mieszanie znaków, by hasło nie miało stałego wzorca
    random.shuffle(password)

    # Zwracamy hasło jako połączoną listę znaków
    return ''.join(password)
    
def validate_password(password):
    """
    Funkcja walidująca siłę hasła. Hasło musi:
    - Mieć co najmniej 12 znaków.
    - Zawierać co najmniej jedną dużą literę, małą literę, cyfrę i znak specjalny.
    - Nie zawierać popularnych wzorców.
    """
    # Minimalna długość hasła
    if len(password) < 12:
        print("Hasło musi mieć co najmniej 12 znaków.")
        return False

    # Sprawdzanie, czy hasło zawiera co najmniej jedną dużą literę, małą literę, cyfrę i znak specjalny
    if not re.search(r"[a-z]", password):  # Małe litery
        print("Hasło musi zawierać co najmniej jedną małą literę.")
        return False
    if not re.search(r"[A-Z]", password):  # Duże litery
        print("Hasło musi zawierać co najmniej jedną dużą literę.")
        return False
    if not re.search(r"\d", password):  # Cyfry
        print("Hasło musi zawierać co najmniej jedną cyfrę.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Znaki specjalne
        print("Hasło musi zawierać co najmniej jeden znak specjalny.")
        return False

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
