import game
import db_admin
"""
Třída sloužící k ukládání her do seznamu
byla vytvořena pro snadné přidávání a správu seznamu her
"""
class GameList:
    """
    Inicializace třídy
    """
    def __init__(self):
        self.games = []
        
    """
    Funkce pro přidání hry do seznamu
    """
    def add_game(self, game):
        self.games.append(game)

    """
    Funkce pro získání pole her
    return: pole her
    """
    def get_games(self):
        return self.games
    
    """
    Funkce pro získání pole názvů her
    return: pole názvů her
    """
    def get_games_names(self):
        names = []
        for g in self.games:
            names.append(g.get_name())
        return names
    
    """
    Funkce pro spuštění hry podle názvu
    return: "Hra nebyla nalezena, chyba při spuštění" pokud hra není nalezena
    """
    def play_game(self, name):
        for g in self.games:
            if g.get_name() == name:
                g.play()
                return
        print("Hra nebyla nalezena, chyba při spuštění")

    """
    Funkce pro získání názvu hry podle indexu
    return: název hry (string)
    """
    def get_game_name(self, index):
        return self.games[index].get_name()
    
    """
    Funkce pro získání umístění hry podle indexu
    return: absolutní cesta k zdrojovému kódu hry (string)
    """
    def get_game_location(self, index):
        return self.games[index].get_location()
    
    """
    Funkce pro získání umístění obrázku podle indexu
    return: absolutní cesta k obrázku (string)
    """
    def get_game_img_location(self, index):
        return self.games[index].get_img_location()
    
    """
    Funkce pro spuštění hry podle indexu
    """
    def play_game_by_index(self, index, player):
        score = int(self.games[index].play())
        if score != None:
            print("Výsledek hry: " + str(score))
            game_name = self.get_game_name(index)
            print("Hra: " + game_name)
            db_admin.update_score(game_name, player, score)
            print("Zpracováno.")
    
    """
    Funkce pro získání délky seznamu her
    return: délka seznamu her (int)
    """
    def list_length(self):
        return len(self.games)
    
"""
Funce pro inicializaci seznamu her.
Pro přidání nové hry do konzole je nutné zapsat hru do této funkce.
Nová hra se přidává pouze do této funkce, vše ostatní se řídí automaticky.
return: pole her
"""
def initialize_games():
    list = GameList()
    list.add_game(game.Game("Snake", "games/snake/main.py", "pict/0.jpg"))
    list.add_game(game.Game("Pong", "games/pong/main.py", "pict/1.jpg"))
    return list

"""
Funkce pro načtení seznamu her ze souboru.
Soubor musí být ve formátu: název hry, absolutní cesta k zdrojovému kódu hry, absolutní cesta k obrázku
return: GameList naplněný daty ze souboru
"""
def get_games_from_txt():
    list = GameList()
    with open("games.txt", "r") as f:
        next(f)
        for line in f:
            game_name, game_location, game_img_location = line.split(", ")
            game_img_location = game_img_location.replace("\n", "")
            list.add_game(game.Game(game_name, game_location, game_img_location))
            print("Hra: " + game_name + " byla úspěšně přidána.")
    return list

"""
testovací funkce
"""
if __name__ == "__main__":
    #games = initialize_games()
    #print(games.get_games_names())
    games = get_games_from_txt()
    print(games.get_games_names())
