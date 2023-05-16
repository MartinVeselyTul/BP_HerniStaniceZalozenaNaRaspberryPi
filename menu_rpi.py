import tkinter as tk
from PIL import ImageTk, Image
from pygame import mixer
import random
from db_admin import load_score
import alsaaudio #ovládání hlasitosti rpi
import games_list, grove_controls
import keyboard_tk as kt

"""
Funkce, která vytvoří nové okno s nastavením
"""
def open_settings():
    button_sound()
    new_window = tk.Toplevel(root)
    new_window.title("Settings")
    new_window.geometry("1024x600")
    new_window.attributes('-fullscreen',True)
    new_window.config(cursor="none")
    global selected, volume_setting, brightness_setting
    selected = 0
    volume_setting = False
    brightness_setting = False

    font_header = ("Courier", 40)
    font_text = ("Courier", 36)
    text_width = 12

    settings_label = tk.Label(new_window, text = "SETTINGS", font = font_header, width = text_width)
    settings_label.place(relx=0.5, rely=0.15, anchor="center")

    volume_label = tk.Label(new_window, text = "volume", bg = "dark grey", font = font_text, width = text_width)
    volume_label.place(relx=0.5, rely=0.3, anchor="center")
    volume_scale = tk.Scale(new_window, from_=0, to=100, orient="horizontal", label="Volume", length=300)
    volume_scale.set(m.getvolume()[0])
    volume_scale.place_forget()
    
    brightness_label = tk.Label(new_window, text = "brightness", bg = "light grey", font = font_text, width = text_width)
    brightness_label.place(relx=0.5, rely=0.42, anchor="center")
    brightness_scale = tk.Scale(new_window, from_=0, to=100, orient="horizontal", label="Brightness", length=300) #nastavení šířky lenght - dle displeje nastavit
    brightness_scale.set(50)
    brightness_scale.place_forget()
    
    reset_label = tk.Label(new_window, text = "reset", bg = "light grey", font = font_text, width = text_width)
    reset_label.place(relx=0.5, rely=0.54, anchor="center")
   
    turnoff_label = tk.Label(new_window, text = "turnoff", bg = "light grey", font = font_text, width = text_width)
    turnoff_label.place(relx=0.5, rely=0.66, anchor="center")
    
    new_window.bind("<Down>", lambda event: move_y("down"))
    new_window.bind("<Up>", lambda event: move_y("up"))
    new_window.bind("p", lambda event: action())
    new_window.bind("q", lambda event: new_window.destroy())

    new_window.bind("<Left>", lambda event: move_x("left"))
    new_window.bind("<Right>", lambda event: move_x("right"))

    def move_x(direction):
        global volume_setting, brightness_setting
        if volume_setting:
            new_volume = volume_scale.get() - 1 if direction == "left" else volume_scale.get() + 1
            volume_scale.set(new_volume)
            m.setvolume(volume_scale.get())
        elif brightness_setting:
            new_brightness = brightness_scale.get() - 1 if direction == "left" else brightness_scale.get() + 1
            brightness_scale.set(new_brightness)

    def move_y(direction):
        global selected, volume_setting, brightness_setting
        if volume_setting == False and brightness_setting == False:
            new_selected = selected + 1 if direction == "down" else selected - 1
            selected = new_selected % 4
            update()
            button_sound()

    def update():
        volume_label.config(bg = "light grey" if selected != 0 else "dark grey")
        brightness_label.config(bg = "light grey" if selected != 1 else "dark grey")
        reset_label.config(bg = "light grey" if selected != 2 else "dark grey")
        turnoff_label.config(bg = "light grey" if selected != 3 else "dark grey")

    def action():
        global selected, volume_setting, brightness_setting
        if selected == 0:
            if not volume_setting:
                volume_scale.place(relx=0.5, rely=0.3, anchor="center")
                volume_label.place_forget()
            else:
                volume_scale.place_forget()
                volume_label.place(relx=0.5, rely=0.3, anchor="center")
                change_volume()
            volume_setting = not volume_setting
        elif selected == 1:
            if not brightness_setting:
                brightness_scale.place(relx=0.5, rely=0.42, anchor="center")
                brightness_label.place_forget()
            else:
                brightness_scale.place_forget()
                brightness_label.place(relx=0.5, rely=0.42, anchor="center")
                change_brightness()
            brightness_setting = not brightness_setting
        elif selected == 2:
            reset_settings()
        elif selected == 3:
            turnoff()

    def change_volume():
        print("Volume changed")

    def reset_settings():
        volume_scale.set(100)
        m.setvolume(100)
        print("Settings reset")

    def change_brightness():
        print("Brightness changed")

    def turnoff():
        root.destroy() #později přidat vypnutí RPI

"""
Funkce pro přehrání zvuku tlačítka
načte náhodný zvuk z adresáře sounds/button a přehraje jej
"""
def button_sound():
    random_number = random.randint(1, 7)
    mixer.init()
    mixer.music.load("./sounds/button/button"+str(random_number)+".mp3")
    mixer.music.play()

"""
Funkce pro zobrazení nového okna s hrou
je zde zobrazena zvolená hra, její skóre a tlačítko pro spuštění hry
"""
def start_game():
    global current_game
    size = 400
    game_window = tk.Toplevel(root)
    game_window.geometry("1024x600")
    game_window.attributes("-fullscreen", True)
    game_window.config(cursor="none")

    font_game = ("Courier", 36)
    font_text = ("Courier", 20)

    frame_sg2 = tk.Frame(game_window)
    frame_sg2.pack(pady=20, padx=20)
    frame_sg2.place(relx=0.5, rely=0.5, anchor="center")

    img = ImageTk.PhotoImage(Image.open(games.get_game_img_location(current_game)).resize((size, size)))
    game_label = tk.Label(frame_sg2, image=img, text=games.get_game_name(current_game)+"\n", font= font_game, compound="bottom")
    game_label.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    game_label.image = img
    
    """
    play_game_lab = tk.Label(frame_sg2, text = "play game", bg = "dark grey", font = font_text, width = 14)
    play_game_lab.place(relx=0.5, rely=0.55, anchor="center")
    """
    
    score_lab = tk.Label(frame_sg2, text = "score leaderboard", bg = "light grey", font = font_text, width = 20)
    score_lab.place(relx=0.5, rely=0.71, anchor="center")
    
    score = load_score(games.get_game_name(current_game))
    score_text_lab = tk.Label(frame_sg2, text = score, bg = "white", font = font_text, width = 20)
    score_text_lab.place(relx=0.5, rely=0.84, anchor="center")

    game_window.bind("q", lambda event: game_window.destroy())
    game_window.bind("p", lambda event: user_choice())

    """
    Funkce pro zobrazení virtuální klávesnice
    slouží pro zadání jména hráče před spuštěním hry
    """
    def display_keyboard(root):
        k_window = tk.Toplevel(root)
        k_window.resizable(0, 0)
        k_window.config(cursor="none")
        k_window.title("Enter your name")
        k_window.geometry("650x230")
        screen_width = k_window.winfo_screenwidth()
        screen_height = k_window.winfo_screenheight()
        x = int((screen_width / 2) - (650 / 2))
        y = int((screen_height / 2) - (230 / 2))
        k_window.geometry("650x230+{}+{}".format(x, y))

        keyboard = kt.Keyboard(k_window)
        k_window.wait_window(keyboard.master)
        player_name = keyboard.player_name
        k_window.destroy()
        return player_name

    """
    Funkce pro spuštění zvolené hry
    """
    def user_choice():
        game_to_play = current_game % int(games_count)
        player_name = display_keyboard(game_window)
        games.play_game_by_index(game_to_play, player_name)
        game_window.destroy()
        start_game()

"""
Funkce pro přepínání mezi hrami v hlavním menu
Mění se proměnná current_game, která určuje index hry v poli games
"""
def game_change(move_right):
    size = 300
    global current_game
    current_game = (current_game + 1) % int(games_count) if move_right else (current_game - 1) % int(games_count)
    img = ImageTk.PhotoImage(Image.open("./pict/"+ str(current_game) +".jpg").resize((size, size)))
    game_label.config(image=img,text=games.get_game_name(current_game)+"\n")
    game_label.image = img
    button_sound()

"""
Inicializace OS konzole v knihovně Tkinter
"""
root = tk.Tk()
m = alsaaudio.Mixer()
root.config(cursor="none")
root.title("Retro Menu")
root.geometry("1024x600")
root.attributes('-fullscreen',True)
root.resizable(False, False)

games = games_list.get_games_from_txt()
games_count = games.list_length()
current_game = 0

frame = tk.Frame(root)
frame.pack(side="left", fill="both", expand=True)

game_frame = tk.Frame(frame)
game_frame.pack(pady=20, padx=20)
game_frame.place(relx=0.5, rely=0.5, anchor="center")

size = 300
font_text = ("Courier", 36)

img = ImageTk.PhotoImage(Image.open(games.get_game_img_location(current_game)).resize((size, size)))

#popisek, název hry
game_label = tk.Label(game_frame, image=img, text=games.get_game_name(current_game)+"\n", font=font_text, compound="bottom")
game_label.pack(side="top", fill="both", expand=True, padx=5, pady=5)

#přidání tlačítek, pouze pro vzhled, nevolají žádné funkce
left_button = tk.Button(frame, text="<")
left_button.pack(side="left", pady=10)
left_button.place(relx=0.1, rely=0.5, anchor="center")

right_button = tk.Button(frame, text=">")
right_button.pack(side="right", pady=10)
right_button.place(relx=0.9, rely=0.5, anchor="center")

settings_button = tk.Button(frame, text="Settings")
settings_button.pack(side="top")
settings_button.place(relx=0.9, rely=0.05, anchor="center")

#inicilizace joysticku
joystick = grove_controls.Joystick_controller(0)
joystick.joystick_handle(root)

#inicializace PIR senzoru pro detekci pohybu
pir = grove_controls.PIRMotionSensor(22)
pir.get_motion(root)

#inicializace tlačítek
blueButton = grove_controls.Button_controller(5, 'p')
whiteButton = grove_controls.Button_controller(6, 'q')
#redButton = grove_controls.Button_controller(5, 'left')
#greenButton = grove_controls.Button_controller(6, 'right')

#naslouchání stisku kláves (ve skutečnosti stisku tlačítek)
root.bind("<Left>", lambda event: game_change(False))
root.bind("<Right>", lambda event: game_change(True))
root.bind("p", lambda event: open_settings())
root.bind("g", lambda event: start_game())

#hlavní smyčka tkinter programu
root.mainloop()
