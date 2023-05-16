import tkinter as tk

class Keyboard:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.player_name = 'def_player'

        self.num_of_chars = 0
        self.input_text = tk.StringVar()
        self.text_label = tk.Label(self.frame, textvariable=self.input_text, font=('Arial', 12))
        self.text_label.grid(row=0, column=0, columnspan=10)

        self.keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '_',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', '<--', 'Enter', 'Clear'
        ]

        self.highlighted_key = 24
        self.update_keyboard()

        self.master.bind('<Left>', lambda event: self.move_left())
        self.master.bind('<Right>', lambda event: self.move_right())
        self.master.bind('<Up>', lambda event: self.move_up())
        self.master.bind('<Down>', lambda event: self.move_down())
        self.master.bind('p', lambda event: self.on_enter_key())

    def on_enter_key(self):
        char_index = self.highlighted_key
        if char_index == 37:
            self.backspace()
        elif char_index == 38:
            self.confirm_text()
        elif char_index == 39:
            self.clear_text()
        else:
            char_new = self.keys[char_index]
            self.update_text(char_new)

    def update_text(self, char):
        self.input_text.set(self.input_text.get()[:self.num_of_chars] + char + self.input_text.get()[self.num_of_chars:])
        self.num_of_chars += 1

    def backspace(self):
        if self.num_of_chars > 0:
            self.num_of_chars -= 1
            self.input_text.set(self.input_text.get()[:self.num_of_chars] + self.input_text.get()[self.num_of_chars + 1:])
            
    def clear_text(self):
        self.input_text.set('')
        self.num_of_chars = 0

    def confirm_text(self):
        if self.num_of_chars > 0:
            #print(self.input_text.get())  #tenhle text potřebujeme dostat jako výstup
            self.player_name = self.input_text.get()
            self.master.destroy()
        else:
            self.master.destroy()
            

    def update_keyboard(self):
        for i, key in enumerate(self.keys):
            if i == self.highlighted_key:
                btn = tk.Button(self.frame, text=key, width=3, font=('Arial', 16), bg='#bddff0', fg='orange')
                btn.grid(row=1 + i // 10, column=i % 10)
            else:
                btn = tk.Button(self.frame, text=key, width=3, font=('Arial', 16))
                btn.grid(row=1 + i // 10, column=i % 10)
            

    def move_left(self):
        if self.highlighted_key > 0:
            self.highlighted_key -= 1
            self.update_keyboard()
        
    def move_right(self):
        if self.highlighted_key < 39:
            self.highlighted_key += 1
            self.update_keyboard()
    
    def move_up(self):
        if self.highlighted_key > 9:
            self.highlighted_key -= 10
            self.update_keyboard()
    
    def move_down(self):
        if self.highlighted_key <= 29:
            self.highlighted_key += 10
            self.update_keyboard()

"""
def display_keyboard(root):
    k_window = tk.Toplevel(root)
    k_window.title('Keyboard')
    k_window.resizable(0, 0)
    keyboard = Keyboard(k_window)
    k_window.wait_window(keyboard.master)
    player_name = keyboard.player_name
    print(player_name) 

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Main window')
    root.geometry('300x300')
    root.bind('<Return>', lambda event: display_keyboard(root))
    root.mainloop()
"""

    

