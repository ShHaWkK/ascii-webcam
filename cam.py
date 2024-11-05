import cv2 as cv
import numpy as np
import os
import sys
import platform
import subprocess
from pynput.keyboard import Listener, Key

###################### Paramètres pour l'affichage ASCII ######################
cols = 120  
rows = 35   
CHAR_LIST = ' .:-=+*#%@'  
##############################################################################

def on_press(key):
    if key == Key.esc:
        finish()

listener = Listener(on_press=on_press)

def finish():
    """Arrête le listener et quitte le programme proprement."""
    listener.stop()
    sys.exit(0)

def main():
    if '--run' not in sys.argv:
        if platform.system() == "Windows":
            subprocess.Popen(['start', 'cmd', '/k', 'python', __file__, '--run'], shell=True)
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            subprocess.Popen(['gnome-terminal', '--', 'python3', __file__, '--run'])
        sys.exit()

    # Capture de la caméra
    vc = cv.VideoCapture(0, cv.CAP_DSHOW if platform.system() == "Windows" else 0)
    if not vc.isOpened():
        print("Impossible d'ouvrir la caméra.")
        sys.exit(1)

    listener.start()
    while True:
        rval, frame = vc.read()
        if not rval:
            print("Erreur de lecture de la caméra.")
            break
        
        ascii_frame = toASCII(frame, cols, rows)
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        print(ascii_frame)

    vc.release()
    sys.exit()

def toASCII(frame, cols=120, rows=35):
    """Convertit un frame en une image ASCII."""
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = frame.shape
    cell_width = width / cols
    cell_height = height / rows
    if cols > width or rows > height:
        raise ValueError("Trop de colonnes ou de lignes.")
    result = ""
    for i in range(rows):
        for j in range(cols):
            gray = np.mean(
                frame[int(i * cell_height):min(int((i + 1) * cell_height), height),
                      int(j * cell_width):min(int((j + 1) * cell_width), width)]
            )
            result += grayToChar(gray)
        result += '\n'
    return result

def grayToChar(gray):
    """Convertit une valeur de gris en caractère ASCII."""
    num_chars = len(CHAR_LIST)
    return CHAR_LIST[min(int(gray * num_chars / 255), num_chars - 1)]

if __name__ == '__main__':
    main()
