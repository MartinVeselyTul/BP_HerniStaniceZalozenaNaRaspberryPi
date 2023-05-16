# Herní konzole založená na Raspberry Pi
## Repozitář pro uložení souborů k bakalářské práci

Tento repozitář obsahuje zdorjové kódy a soubory pro bakalářskou práci Herní konzole založená na Raspberry Pi.

Jedná se kopie souborů, které tvořily herní prostředí a hry na vlastní vytvořené herní konzoli.
V tomto adresáři se nevyskytuje soubor s přihlašovacími údaji k databázi.

- práce využívá jazyk python ver 3.9 a novější a knihovny
  - tkinter
  - pygame
  - grove
  - gpiozero
  - PIL
  - alsaaudio
  - configparser
  - psycopg2
  - pyautogui
  - subprocess

Soubor menu_rpi.py je main soubor, jež je na konzoli spouštěn, a ze kterého jsou ostatní soubory volány.

Stručný popis souborů a jakou mají v práci funkci
- db_admin.py - soubor pro připojení a editaci databáze
- game.py - soubor se třídou Game pro inicializaci instance jedné hry
- games.txt - textový soubor obsahující pojménování her a cestu k jejich souborům
- games_list.py - soubor se třídou GameList pro inicializaci knihovny her (pole instancí třídy Game)
- grove_controls.py - soubor se třídami pro inicializaci a ovládání vstupů systému Grove (tlačítka, joystick, senzory...)
- grove_ultrasonic.py - soubor pro inicializaci samostatného senzoru na měření vzdálenosti
- keyboard_tk.py - soubor pro vytvoření klávesnice na obrazovce pro zadání uživatelského jména
- menu_rpi.py - hlavní soubor pro spuštění herního prostředí
- test_db_admin.py - soubor obsahující pytesty pro testování připojení k databázi (testování souboru db_admin.py)
