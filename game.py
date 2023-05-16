import os, sys
"""
Třída pro inicializaci jednotlivých her.
"""
class Game:
    """
    inicializace třídy
    """
    def __init__(self, name, location, img_location):
        self.name = name
        self.location = location
        self.img_location = img_location
        
    """
    funkce pro získání názvu hry
    return: název hry (string)
    """
    def get_name(self):
        return self.name

    """
    funkce pro získání umístění hry
    return: absolutní cesta k zdrojovému kódu hry (string)
    return: "Cesta k hře nenalezena." pokud cesta neexistuje
    """
    def get_location(self):
        location = self.location
        if os.path.exists(location):
            return location
        else:
            return "Cesta k hře nenalezena."
    
    """
    funkce pro získání umístění obrázku
    return: absolutní cesta k obrázku (string) pokud cesta existuje
    return: "Cesta k obrázku nenalezena." pokud cesta neexistuje
    """
    def get_img_location(self):
        location = self.img_location
        if os.path.exists(location):
            return location
        else:
            return "Cesta k obrázku nenalezena."
    
    """
    funkce pro spuštění hry
    """
    def play(self):
        score = 0
        original_cwd = os.getcwd()
        loc = str(self.get_location())
        dir_path = os.path.dirname(os.path.abspath(loc))
        try:
            os.chdir(dir_path)
            sys.path.insert(0, '')
            if self.get_name() == "Snake":
                from games.snake.main import main
                score = main()
            elif self.get_name() == "Tetris":
                from games.tetris.main import main
                score = main()
            elif self.get_name() == "Ultrasonic":
                from games.ultrasonic.main import main
                score = main()
            elif self.get_name() == "Pong":
                from games.pong.main import main
                score = main()
            
        except Exception as e:
            print(e)
        os.chdir(original_cwd)
        sys.path.pop(0)
        return score