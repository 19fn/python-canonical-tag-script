#!/usr/bin/python3
# Autor: @federicocabreraf

import requests, signal, lxml, os, argparse, pathlib, datetime
from os import name, system
from bs4 import BeautifulSoup as bs4
from colorama import Fore, init
init(autoreset=True)

# HEADER
HEADER = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

# Abort Script Function
def ctrl_c(sig, frame):
    print(Fore.RED + "\n[!] Aborting...\n\n")
    exit()
signal.signal(signal.SIGINT,ctrl_c)

# Clear Screen Function
def clearScreen():
    # Windows
    if name == 'nt':
        _ = system('cls')
    # Linux, Mac
    else:
        _ = system('clear')

# Total Of Urls
def CountUrl(file):
    total_urls = 0
    try:
        with open(file) as url_file:
            for url in url_file:
                if url.strip() != "":
                    total_urls += 1
        return total_urls
    except: FileNotFoundError

# Read Url File
def ReadUrlFile(file):
    URLs = []
    try:
        with open(file,"r") as url_file:
            for url in url_file:
                if url.strip() != "":
                    URLs.append(url.rstrip())
        return URLs
    except:
        print(Fore.RED + "\n\nError: 'No se pudo leer los urls del archivo ingresado'\n\n")

# Write Scan Results
def WriteResultFile(match_list):
    try:
        with open("scan_results.txt","a") as scan_file:
            scan_file.write("\n[+] Total of 'URLs' that match: \n")
            for url in match_list:
                scan_file.write("%s\n" % str(url))
    except:
        print(Fore.RED + "\n\nError: 'can not write results file'\n\n")

# Get Canonital Tag Function
def GetCanonicalTag(urls):
    canonical_url = []
    try:
        for url in urls:
            page = requests.get(url, HEADER)
            soup = bs4(page.text, 'lxml')
            for url in soup.select('link[rel*=canonical]'):
                canonical_url.append(url['href'])
        return set(canonical_url)
    except:
        print(Fore.RED + "\n\nError: 'No se pudo obtener etiqueta rel canonical de los urls ingresados'\n\n")

# Match Url Function
def URLmatch(file):
    get_urls = ReadUrlFile(file)
    get_canonical_url = GetCanonicalTag(get_urls)
    match_URLs = []
    not_match_URLs = []
    try:
        for url in get_urls:
            if url not in get_canonical_url:
                not_match_URLs.append(url)
            else:
                match_URLs.append(url)
        not_match_URLs = list(set(not_match_URLs))
        return match_URLs
    except: 
        print(Fore.RED + "\n\nError: 'can not match any url'\n\n")

# Main Function
def main():
    parser = argparse.ArgumentParser(description="Self Referral Rel Canonical Tag Monitor")
    parser.add_argument("-u", "--url-list",
                        help="url list",
                        dest="urls",
                        type=pathlib.Path,
                        action="store", 
                        required=True)
    argument = parser.parse_args()

    clearScreen()    
    url_file = argument.urls

    if os.path.isfile(url_file):
        clearScreen()
        print(Fore.CYAN + "\n[*] Canonical Tag Monitor")
        print("\n[*] 'ctrl + c' para abortar script.")
        date_time = datetime.datetime.now()
        date_time = date_time.strftime(' %H:%M:%S <> %d/%m/%Y')
        print(f"\n[*] Total of 'URLs' : {CountUrl(url_file)}\n\n[*] Scanning: '{url_file}' \n")
        WriteResultFile(URLmatch(url_file))
        print(f"[*] Last scan: {date_time}\n\n")
    else:
        print(Fore.RED + f"\n[!] '{url_file}' not found.\n\n")

if __name__ == "__main__":
    main()