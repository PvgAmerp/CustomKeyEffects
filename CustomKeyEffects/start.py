import os
import keyboard
import webbrowser
import pygame
import requests
from io import BytesIO
from time import sleep

script_dir = os.path.dirname(os.path.realpath(__file__))

def check_effects_folder():
    effects_folder = os.path.join(script_dir, 'Effects')
    if not os.path.exists(effects_folder):
        print("Effects folder not found.")
        sleep(2)
        os.makedirs(effects_folder)
        print("Effects folder created. Please create some effects using 'Interface.pyw' or create them manually. Then, re-run the script.")
        input()

check_effects_folder()

def read_value_file(folder_path):
    value_file_path = os.path.join(folder_path, "value.txt")
    if not os.path.exists(value_file_path):
        return None, None
    
    key = None
    path = None
    
    with open(value_file_path, "r") as file:
        lines = file.readlines()
        if len(lines) >= 3:
            key = lines[2].strip().split("=")[1]
        if len(lines) >= 2:
            path = lines[1].strip().split("=")[1]
        
    return key, path

def play_sound(path):
    if path.startswith("http://") or path.startswith("https://"):
        # If the path is a URL
        print("Opening URL in web browser:", path)
        try:
            webbrowser.open(path)
        except Exception as e:
            print("Error opening URL:", e)
    else:
        # If the path is a local file
        if not os.path.exists(path):
            print("Local sound file not found:", path)
            return
        print("Playing sound:", path)
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(path)
        sound.play()

        print("Esc to exit.")

def main():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    effects_folder = os.path.join(script_directory, "Effects")

    if not os.path.exists(effects_folder):
        print("Effects folder not found.")
        return

    pygame.init()
    pygame.mixer.init()

    for root, dirs, files in os.walk(effects_folder):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            key, path = read_value_file(folder_path)
            if key and path:
                print("Setting up keyboard listener for key:", key)
                keyboard.on_press_key(key, (lambda path: lambda _: play_sound(path))(path))

    keyboard.wait("esc")

if __name__ == "__main__":
    main()