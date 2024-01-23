# ====== Color =======
red = "\033[1;31m"
green = "\033[1;32m"
# ===================

import platform
import os
from sami_ai import sami_ai 

while True:
    cmd = input(f"{red}[+] Enter your message : ")
    if cmd == "clear":
        if platform.system() == "Linux":
            os.system('clear')
        else:
            os.system('cls')
    else:
        response = sami_ai(cmd)  
        print(green + response['response'])
