import pytest
from db_admin import *

def test_connect_db():
    # testuje úspěšné připojení k databázi
    conn = connect_db()
    assert conn is not None

def test_add_game():
    # testuje, jestli funkce správně přidá novou hru
    add_game("game_test")
    assert load_score("game_test") == "1. no_player1: 3\n2. no_player2: 2\n3. no_player3: 1"

def test_load_score():
    # testuje, jestli funkce vrací očekávaný výstup pro existující hru
    assert load_score("game_test") == "1. no_player1: 3\n2. no_player2: 2\n3. no_player3: 1"

    # testuje, jestli funkce vrací None pro neexistující hru
    assert load_score("not_existing_game") is None

def test_write_new_score():
    # testuje, jestli funkce správně přidá nový záznam
    write_new_score("game_test", "player4", 20)
    assert load_score("game_test") == "1. player4: 20\n2. no_player1: 3\n3. no_player2: 2"

def test_remove_record():
    # testuje, jestli funkce správně určí, který záznam má být odstraněn
    assert remove_record("game_test", 20) == ["game_test", "no_player2", "2"]

    # testuje, jestli funkce vrátí 0 pro skóre, které není v TOP 3
    assert remove_record("game_test", 1) == 0

    # testuje, jestli funkce vrátí 0 pro neexistující hru
    assert remove_record("not_existing_game", 10) == 0

def test_update_score():
    # testuje, jestli se správně aktualizuje tabulka, pokud je nové skóre v TOP 3, nejnižší skóre se odstraní, nové se přidá
    update_score("game_test", "player5", 25)
    assert load_score("game_test") == "1. player5: 25\n2. player4: 20\n3. no_player1: 3"

    # testuje, jestli skóre zůstane stejné, pokud je nové skóre shodné s nejnižším skóre v TOP 3
    update_score("game_test", "player6", 3)
    assert load_score("game_test") == "1. player5: 25\n2. player4: 20\n3. no_player1: 3"

    # testuje, jestli skóre zůstane stejné, pokud je nové skóre vyšší než nejnižší skóre v TOP 3
    update_score("game_test", "player7", 2)
    assert load_score("game_test") == "1. player5: 25\n2. player4: 20\n3. no_player1: 3"


def test_remove_game():
    # testuje, jestli funkce správně odstraní hru
    remove_game("game_test")
    assert does_game_exist("game_test") == False