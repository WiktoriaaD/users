# Program do zarządzania użytkownikami i walidacji danych

Program umożliwia zarządzanie użytkownikami w systemie, w tym dodawanie, edytowanie, usuwanie użytkowników oraz przechowywanie ich danych (PESEL, NIP, REGON). Dodatkowo, oferuje funkcje generowania silnych haseł oraz sprawdzania ich siły. Program zapisuje dane użytkowników w pliku JSON i zapewnia walidację danych wprowadzanych przez użytkownika.

## Funkcje programu:

- **`validate_pesel(pesel)`**: Waliduje numer PESEL użytkownika, sprawdzając poprawność formatu oraz cyfrę kontrolną.
- **`validate_nip(nip)`**: Sprawdza poprawność numeru NIP, w tym sumę kontrolną.
- **`validate_regon(regon)`**: Weryfikuje numer REGON, sprawdzając jego długość oraz sumę kontrolną w przypadku 9-cyfrowego numeru.
- **`add_user(user_data)`**: Dodaje nowego użytkownika do pliku JSON, po uprzedniej walidacji jego danych (PESEL, NIP, REGON).
- **`edit_user(user_id, updated_data)`**: Umożliwia edytowanie danych użytkownika w pliku JSON.
- **`remove_user(user_id)`**: Usuwa użytkownika z systemu na podstawie jego ID.
- **`load_users()`**: Wyświetla listę wszystkich użytkowników zapisanych w pliku JSON.
- **`generate_password(length=12)`**: Generuje silne hasło o długości co najmniej 12 znaków, zawierające duże i małe litery, cyfry oraz znaki specjalne.
- **`validate_password(password)`**: Sprawdza siłę hasła, upewniając się, że zawiera przynajmniej 12 znaków, małe i duże litery, cyfrę oraz znak specjalny.

## Przykład użycia:

1. **Dodawanie nowego użytkownika**: Program pozwala na dodanie użytkownika do systemu po podaniu jego imienia, nazwiska, numeru PESEL, NIP i REGON.
2. **Generowanie i walidacja hasła**: Użytkownik może wygenerować losowe hasło, które zostanie automatycznie sprawdzone pod kątem siły.
3. **Edycja danych użytkownika**: Możliwość edytowania istniejącego użytkownika, w tym zmiana numeru PESEL, NIP, REGON.
4. **Usuwanie użytkownika**: Usunięcie użytkownika na podstawie jego ID.

## Przechowywanie danych:

Wszystkie dane użytkowników są przechowywane w pliku `users.json` w folderze `data/`. Program automatycznie tworzy folder i plik, jeśli nie istnieją.
