import psycopg2
import configparser
from grove_controls import FlashLed
"""
soubor, který slouží pro správu databáze a testování připojení k databázi
PRO BĚH APLIKACE NENÍ TŘEBA
v databázi je tabulka users, která obsahuje jméno a heslo uživatele
a tabulka tasks, která obsahuje jméno uživatele, úkol a boolean, zda je úkol splněn nebo ne
"""

"""
Funkce, která zařizuje připojení k databázi. Data pro připojení jsou uložena v souboru config.ini.
@return conn - připojení k databázi
"""
def connect_db():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        host = config.get('database', 'host')
        port = config.get('database', 'port')
        dbname = config.get('database', 'database')
        user = config.get('database', 'user')
        password = config.get('database', 'password')

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port, sslmode='require')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

"""
Funkce pro výpis top3 skóre z databáze.
@param game - název hry
@return score - top3 skóre (str) ve formátu: 1. hráč: skóre
"""
def load_score(game):
    conn = None
    try:
        conn = connect_db()

        cur = conn.cursor()
        cur.execute("SELECT * FROM score WHERE game = %s ORDER BY score DESC;", (game,))
        raw_score = cur.fetchall()
        if raw_score == []:
            add_game(game)
            cur.execute("SELECT * FROM score WHERE game = %s ORDER BY score DESC;", (game,))
            raw_score = cur.fetchall()
        score = ""
        for i in range(3):
            score += str(i+1) + ". " + raw_score[i][1] + ": " + str(raw_score[i][2])
            if i != 2:
                score += "\n"
        cur.close()
        return score
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed succesfully.')

"""
Funke pro přidání nové hry do databáze. Přidává se 3 záznamy s názvem hry, jménem hráče a skóre 0.
@param game - název hry
"""
def add_game(game):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO score (game, player, score) VALUES (%s, %s, %s)", (game, "no_player1", 3))
        cur.execute("INSERT INTO score (game, player, score) VALUES (%s, %s, %s)", (game, "no_player2", 2))
        cur.execute("INSERT INTO score (game, player, score) VALUES (%s, %s, %s)", (game, "no_player3", 1))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed succesfully.')

def does_game_exist(game):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM score WHERE game = %s", (game,))
        raw_score = cur.fetchall()
        if len(raw_score) == 0:
            return False
        else:
            return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

"""
Funkce pro zjištění, zda je nové skóre v TOP 3.
@param game - název hry
@param score - skóre hráče
@return remove_record - seznam, který obsahuje název hry, jméno hráče a skóre, které se má odstranit
"""
def remove_record(game, score):
    if does_game_exist(game):
        remove_record = ["","",0]
        top3 = load_score(game)
        top3 = top3.split("\n")
        top3 = [i.split(": ") for i in top3]
        top3 = [[i[0], int(i[1])] for i in top3]
        if score > top3[2][1]:
            remove_record[0] = game
            player = str(top3[2][0])
            remove_record[1] = player.split(". ")[1]
            remove_record[2] = str(top3[2][1])
        else:
            print("Score is not in top3.")
            return 0
        return remove_record
    else:
        print("Game does not exist.")
        return 0

"""
Funkce pro odstranění záznamu z databáze.
@param remove_record - seznam, který obsahuje název hry, jméno hráče a skóre, které se má odstranit
"""
def remove_score(remove_record):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM score WHERE game = %s AND player = %s AND score = %s", (remove_record[0], remove_record[1], remove_record[2]))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed succesfully.')
            
"""
Funkce pro zápis nového skóre do databáze.
@param game - název hry
@param player - jméno hráče
@param score - skóre hráče
"""
def write_new_score(game, player, score):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO score (game, player, score) VALUES (%s, %s, %s)", (game, player, score))
        conn.commit()
        cur.close()
        leds = FlashLed(24, 26)
        leds.flash()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

"""
Funke pro aktualizaci skóre v databázi.
@param game - název hry
@param player - jméno hráče
@param score - skóre hráče
@return 1 - pokud se skóre aktualizovalo
@return 0 - pokud zůstanulo skóre stejné
"""
def update_score(game, player, score):
    remove_data = remove_record(game, score)
    if remove_data != 0:
        remove_score(remove_data)
        write_new_score(game, player, score)
        return 1
    else:
        return 0

"""
TESTOVACÍ FUNKCE
Slouží pro tisk všech záznamů dané hry z databáze.
"""
def print_all(game):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM score WHERE game = %s ORDER BY score DESC;", (game,))
        raw_score = cur.fetchall()
        print(raw_score)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

"""
TESTOVACÍ FUNKCE
Slouží pro testování připojení k databázi a případnou správu databáze.
"""
def connect():
    conn = None
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        host = config.get('database', 'host')
        port = config.get('database', 'port')
        dbname = config.get('database', 'dbname')
        user = config.get('database', 'user')
        password = config.get('database', 'password')

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port, sslmode='require')

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        """
        správa databáze
        vytvoření tabulky users - jméno(PK), heslo
        cur.execute("CREATE TABLE users (login VARCHAR(255) PRIMARY KEY, password VARCHAR(255))")
        vytvoření tabulky tasks - jméno(FK), úkol, splněno/nesplněno
        cur.execute("CREATE TABLE tasks (login VARCHAR(255) REFERENCES users(login), task VARCHAR(255), done BOOLEAN DEFAULT FALSE)")
        
        přidání uživatele martin s heslem 1234
        cur.execute("INSERT INTO users (login, password) VALUES ('martin', '1234')")
        
        přidání úkolů pro uživatele martin, boolean není třeba zadávat, jelikož je defaultně nastaven na false
        cur.execute("INSERT INTO tasks (login, task) VALUES ('martin', 'task1')")
        cur.execute("INSERT INTO tasks (login, task) VALUES ('martin', 'task2')")
        cur.execute("INSERT INTO tasks (login, task) VALUES ('martin', 'task3')")
        conn.commit()
        
        cur.execute("INSERT INTO users (login, password) VALUES ('test', 'test')")
        cur.execute("INSERT INTO tasks (login, task) VALUES ('test', 'kup hranolky')")
        cur.execute("INSERT INTO tasks (login, task, done) VALUES ('test', 'došlo pivo', TRUE)")
        conn.commit()
        """

        """
        cur.execute("DROP TABLE score")
        conn.commit()
        """

        """
        cur.execute("CREATE TABLE score (game VARCHAR(255), player VARCHAR(255), score INTEGER)")
        cur.execute("INSERT INTO score (game, player, score) VALUES ('had', 'test1', 100)")
        cur.execute("INSERT INTO score (game, player, score) VALUES ('had', 'test2', 50)")
        cur.execute("INSERT INTO score (game, player, score) VALUES ('had', 'test3', 25)")
        conn.commit()
        """

        cur.execute("SELECT * FROM score")
        print(cur.fetchall())

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def remove_game(game):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM score WHERE game = %s", (game,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 1
    finally:
        if conn is not None:
            conn.close()
            return 0

"""
TESTOVACÍ MAIN FUNKCE
"""
if __name__ == '__main__':
    conn = connect_db()
    print(conn)
    """
    update_score("had", "test4", 90)

    print(load_score("had "))
    """