#!/usr/bin/env python3

 
import getpass
username = getpass.getuser()


def display_help():
    help_banner = f"""
    
👋 Hey \033[96m{username}
   \033[92m                                                                                             v1.0
   ___             __         ____    ___   ____   _____         ____    ___   _  _     ___    ___  
  / __\ /\   /\   /__\       |___ \  / _ \ |___ \ |___ /        |___ \  / _ \ | || |   ( _ )  / _ \ 
 / /    \ \ / /  /_\   _____   __) || | | |  __) |  |_ \  _____   __) || (_) || || |_  / _ \ | (_) |
/ /___   \ V /  //__  |_____| / __/ | |_| | / __/  ___) ||_____| / __/  \__, ||__   _|| (_) | \__, |
\____/    \_/   \__/         |_____| \___/ |_____||____/        |_____|   /_/    |_|   \___/    /_/ 
                                                                                                    



\x1b[31;1mCVE-2023-29489 : Bug scanner for WebPentesters and Bugbounty Hunters 

\x1b[31;1m$ \033[92mCVE-2023-29489\033[0m [option]

Usage: \033[92mCVE-2023-29489\033[0m [options]

Options:
  -u, --url     URL to scan                                CVE-2023-29489 -u https://target.com                
  -i, --input   <filename> Read input from txt             CVE-2023-29489 -i target.txt                         
  -o, --output  <filename> Write output in txt file        CVE-2023-29489 -i target.txt -o output.txt     
  -c, --chatid  Creating Telegram Notification             CVE-2023-29489 --chatid yourid    
  -h, --help    Help Menu                       
    """
    print(help_banner)


def banner():
    help_banner = f"""
    \033[94m
👋 Hey \033[96m{username}
   \033[92m                                                                                             v1.0
   ___             __         ____    ___   ____   _____         ____    ___   _  _     ___    ___  
  / __\ /\   /\   /__\       |___ \  / _ \ |___ \ |___ /        |___ \  / _ \ | || |   ( _ )  / _ \ 
 / /    \ \ / /  /_\   _____   __) || | | |  __) |  |_ \  _____   __) || (_) || || |_  / _ \ | (_) |
/ /___   \ V /  //__  |_____| / __/ | |_| | / __/  ___) ||_____| / __/  \__, ||__   _|| (_) | \__, |
\____/    \_/   \__/         |_____| \___/ |_____||____/        |_____|   /_/    |_|   \___/    /_/ 
                                                                                                    




\x1b[31;1mCVE-2023-29489 : Bug scanner for WebPentesters and Bugbounty Hunters 

\033[0m"""
    print(help_banner)
