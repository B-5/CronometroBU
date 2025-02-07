import tkinter as tk
from tkinter import ttk
import time
import pygame
from tkinter import font
from tkinter import messagebox
from ttkthemes import ThemedStyle

class SimpleStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronômetro")

        self.is_timing = False
        self.start_time = 0
        self.sound_file = "horn.wav"
        self.sound = None

        # Set the default font size for the entire application
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=25)

        # Create a frame to center the widgets
        center_frame = ttk.Frame(root)
        center_frame.pack(expand=True, fill='both')

        self.add_static_image(center_frame)

        # Create a ThemedStyle instance
        style = ThemedStyle(root)
        style.set_theme("plastik")

        self.sound_button = ttk.Button(center_frame, text="Tocar buzina e iniciar cronômetro", command=self.play_sound_and_start_stopwatch)
        self.sound_button.pack(expand=True)

        self.stopwatch_label = ttk.Label(center_frame, text="00:00:00", font=("Helvetica", 120))
        self.stopwatch_label.pack(expand=True)

        self.stop_button = ttk.Button(center_frame, text="Parar cronômetro", command=self.stop_stopwatch, state="disabled")
        self.stop_button.pack(expand=True)

        # Create a frame for the history
        history_frame = ttk.Frame(center_frame)
        history_frame.pack(expand=True, fill='both', pady=10)

        # Add a label for the history
        history_label = ttk.Label(history_frame, text="Histórico")
        history_label.pack()

        # Create a frame for history list and clear button
        history_list_frame = ttk.Frame(history_frame)
        history_list_frame.pack(expand=True, fill='both')

        self.history_listbox = tk.Listbox(history_list_frame, font=("Arial", 20), selectmode=tk.SINGLE)
        self.history_listbox.pack(expand=True, fill='both')

        self.clear_history_button = ttk.Button(history_list_frame, text="Limpar Histórico", command=self.clear_history)
        self.clear_history_button.pack(side=tk.RIGHT)

        # Register keyboard shortcuts
        root.bind("i", lambda event: self.play_sound_and_start_stopwatch())
        root.bind("p", lambda event: self.stop_stopwatch())

    def play_sound_and_start_stopwatch(self):
        if not self.is_timing:
            pygame.mixer.init()
            self.sound = pygame.mixer.Sound(self.sound_file)
            self.sound.play()

            # Wait for the sound to finish playing
            while pygame.mixer.get_busy():
                pass

            self.start_time = time.time()
            self.is_timing = True
            self.sound_button["state"] = "disabled"
            self.stop_button["state"] = "normal"
            self.update_time()

    def update_time(self):
        if self.is_timing:
            elapsed_time = time.time() - self.start_time
            self.update_stopwatch_display(elapsed_time)
            self.root.after(10, self.update_time)

    def update_stopwatch_display(self, elapsed_time):
        if hasattr(self, 'stopwatch_label'):
            minutes, seconds = divmod(int(elapsed_time), 60)
            fractions = int((elapsed_time - int(elapsed_time)) * 100)
            self.stopwatch_label.config(text=f"{minutes:02}:{seconds:02}:{fractions:02}")

    def stop_stopwatch(self):
        if self.is_timing:
            elapsed_time = time.time() - self.start_time
            self.is_timing = False
            if self.sound:
                self.sound.stop()
            self.sound_button["state"] = "normal"
            self.stop_button["state"] = "disabled"
            self.history_listbox.insert(tk.END, self.stopwatch_label.cget("text"))

    def clear_history(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar o histórico?"):
            self.history_listbox.delete(0, tk.END)
            self.show_message("Histórico limpo com sucesso.")

    def show_message(self, message):
        messagebox.showinfo("Aviso", message)

    def add_static_image(self, frame):
        static_image = tk.PhotoImage(file="image.png")  # Replace with your image file
        static_image = static_image.subsample(2)  # Adjust the value to control the size
        static_image_label = ttk.Label(frame, image=static_image)
        static_image_label.image = static_image
        static_image_label.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleStopwatchApp(root)

    style = ThemedStyle(root)
    style.set_theme("arc")

    root.state('zoomed')  # Maximize the window
    root.mainloop()
