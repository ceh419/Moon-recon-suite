import requests
import socket
import whois
import json
import threading
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def banner():
    print("""
 __  __                       _____                                      
|  \/  |                     |  __ \
| \  / | ___  _ __ ___   ___ | |__) |__ _ __ ___  ___  _ __ ___   __ _  
| |\/| |/ _ \| '_ ` _ \ / _ \|  ___/ _ \ '__/ __|/ _ \| '_ ` _ \ / _` | 
| |  | | (_) | | | | | | (_) | |  |  __/ |  \__ \ (_) | | | | | | (_| | 
|_|  |_|\___/|_| |_| |_|\___/|_|   \___|_|  |___/\___/|_| |_| |_|\__,_| 
                                                                        
          Moon Recon Suite v3.0 by Jan | Full Recon Toolkit
""")

def http_header_analyzer(url):
    print(f"\n[+] Fetching headers for: {url}")
    try:
        r = requests.get(url, timeout=5)
        for key, value in r.headers.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"[!] Error fetching headers: {e}")

def whois_lookup(domain):
    print(f"\n[+] Performing WHOIS lookup for: {domain}")
    try:
        info = whois.whois(domain)
        print(json.dumps(info, indent=2, default=str))
    except Exception as e:
        print(f"[!] Error in WHOIS: {e}")

def subdomain_finder(domain):
    print(f"\n[+] Finding subdomains for: {domain}")
    subdomains = ["www", "mail", "ftp", "cpanel", "webmail", "dev"]
    found = []
    for sub in subdomains:
        try:
            full = f"{sub}.{domain}"
            socket.gethostbyname(full)
            print(f"[+] Found: {full}")
            found.append(full)
        except:
            pass
    if not found:
        print("[-] No subdomains found (from list)")

def port_scanner(host):
    print(f"\n[+] Scanning top ports on: {host}")
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]
    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((host, port))
            print(f"[OPEN] Port {port}")
            s.close()
        except:
            pass

def dir_brute(url):
    print(f"\n[+] Brute-forcing directories on: {url}")
    common_dirs = ["admin", "login", "dashboard", "uploads", "config", ".git"]
    for d in common_dirs:
        full = f"{url}/{d}"
        try:
            r = requests.get(full, timeout=3)
            if r.status_code == 200:
                print(f"[FOUND] {full}")
        except:
            pass

def extract_js_links(url):
    print(f"\n[+] Extracting JavaScript links from: {url}")
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        scripts = soup.find_all('script')
        for s in scripts:
            src = s.get('src')
            if src:
                print(f"[JS] {src}")
    except Exception as e:
        print(f"[!] JS Extraction failed: {e}")

def ip_lookup(domain):
    print(f"\n[+] IP lookup for: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] IP: {ip}")
    except Exception as e:
        print(f"[!] Failed to get IP: {e}")

if __name__ == "__main__":
    banner()
    target_url = input("Enter full URL (https://example.com): ").strip()
    domain = input("Enter domain only (example.com): ").strip()
    ip = input("Enter IP or domain for port scan: ").strip()

    http_header_analyzer(target_url)
    whois_lookup(domain)
    subdomain_finder(domain)
    port_scanner(ip)
    dir_brute(target_url)
    extract_js_links(target_url)
    ip_lookup(domain)
