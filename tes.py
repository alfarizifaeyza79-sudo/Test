#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ZXX-TOOL Pentesting Suite
# Author: MrZXX
# Contact: @Zxxtirwd

import os
import sys
import time
import json
import socket
import requests
import subprocess
import threading
from datetime import datetime
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Konfigurasi
ADMIN_USERNAME = "mrzxx"
ADMIN_PASSWORD = "mrzxx"
USER_DB_FILE = "users.json"

# Warna
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
BR = Style.BRIGHT
RS = Style.RESET_ALL

# Animasi loading
def animate_text(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def typing_effect(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation(text="Loading", duration=2):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{BR}{C}{chars[i % len(chars)]} {text}...{RS}", end="")
        time.sleep(0.1)
        i += 1
    print(f"\r{' ' * 50}", end="\r")

# Database user
class UserDB:
    def __init__(self):
        self.db_file = USER_DB_FILE
        self.users = self.load_users()
    
    def load_users(self):
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def add_user(self, user_id, username):
        self.users[user_id] = {
            "username": username,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        self.save_users()
        return True
    
    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            self.save_users()
            return True
        return False
    
    def check_user(self, user_id):
        return user_id in self.users
    
    def list_users(self):
        return self.users

# ASCII Art
def show_welcome():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{BR}{M}")
    print(""":::       ::: :::::::::: :::        :::        ::::::::   ::::::::  ::::    ::::  ::::::::::      
:+:       :+: :+:        :+:        :+:       :+:    :+: :+:    :+: +:+:+: :+:+:+ :+:             
+:+       +:+ +:+        +:+        +:+       +:+        +:+    +:+ +:+ +:+:+ +:+ +:+             
+#+  +:+  +#+ +#++:++#   +#+        +#+       +#+        +#+    +:+ +#+  +:+  +#+ +#++:++#        
+#+ +#+#+ +#+ +#+        +#+        +#+       +#+        +#+    +#+ +#+       +#+ +#+             
 #+#+# #+#+#  #+#        #+#        #+#       #+#    #+# #+#    #+# #+#       #+# #+#             
  ###   ###   ########## ########## ########## ########   ########  ###       ### ##########      """)
    print(RS)

def show_admin_panel():
    print(f"{BR}{Y}")
    print("""    **          **             **                                                    **
   ****        /**            //                 ******                             /**
  **//**       /** **********  ** *******       /**///**  ******   *******   *****  /**
 **  //**   ******//**//**//**/**//**///**      /**  /** //////** //**///** **///** /**
********** **///** /** /** /**/** /**  /**      /******   *******  /**  /**/******* /**
/**//////**/**  /** /** /** /**/** /**  /**      /**///   **////**  /**  /**/**////  /**
/**     /**//****** *** /** /**/** ***  /**      /**     //******** ***  /**//****** ***
//      //  ////// ///  //  // // ///   //       //       //////// ///   //  ////// /// """)
    print(RS)

def show_main_tools():
    print(f"{BR}{C}")
    print("""███████╗██╗  ██╗██╗  ██╗  ████████╗ ██████╗  ██████╗ ██╗     
╚══███╔╝╚██╗██╔╝╚██╗██╔╝  ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
  ███╔╝  ╚███╔╝  ╚███╔╝█████╗██║   ██║   ██║██║   ██║██║     
 ███╔╝   ██╔██╗  ██╔██╗╚════╝██║   ██║   ██║██║   ██║██║     
███████╗██╔╝ ██╗██╔╝ ██╗     ██║   ╚██████╔╝╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝""")
    print(RS)

def show_vuln_scan():
    print(f"{BR}{R}")
    print("""███████╗ ██████╗ █████╗ ███╗   ██╗██╗   ██╗██╗   ██╗██╗     ███╗   ██╗
██╔════╝██╔════╝██╔══██╗████╗  ██║██║   ██║██║   ██║██║     ████╗  ██║
███████╗██║     ███████║██╔██╗ ██║██║   ██║██║   ██║██║     ██╔██╗ ██║
╚════██║██║     ██╔══██║██║╚██╗██║╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║
███████║╚██████╗██║  ██║██║ ╚████║ ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝""")
    print(RS)

def show_portscan():
    print(f"{BR}{G}")
    print("""██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗    
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║    
██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║    
██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║    
██║     ╚██████╔╝██║  ██╗   ██║   ███████║╚██████╗██║  ██║██║ ╚████║    
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝""")
    print(RS)

def show_dump_db():
    print(f"{BR}{M}")
    print("""██████╗ ██╗   ██╗███╗   ███╗██████╗ ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗
██╔══██╗██║   ██║████╗ ████║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
██║  ██║██║   ██║██╔████╔██║██████╔╝██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗  
██║  ██║██║   ██║██║╚██╔╝██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝  
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ⚻═╝╚══════╝╚══════╝""")
    print(RS)

# Login System
def login():
    db = UserDB()
    termux_id = subprocess.getoutput("whoami")
    
    show_welcome()
    print(f"\n{BR}{Y}Welcome User{RS}")
    print(f"{G}{'='*45}{RS}")
    print(f"{C}ID-Termux: {termux_id}{RS}")
    print(f"{C}User: {termux_id}{RS}")
    print(f"{G}{'='*45}{RS}")
    
    if db.check_user(termux_id):
        print(f"\n{BR}{G}[✓] Login berhasil!{RS}")
        time.sleep(1)
        return True
    else:
        print(f"\n{R}[!] User tidak terdaftar!{RS}")
        print(f"{Y}Untuk mendaftar, chat admin di Telegram: @Zxxtirwd{RS}")
        print(f"\n{Y}Tekan Enter untuk keluar...{RS}")
        input()
        sys.exit(0)

# Admin Panel
def admin_panel():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_admin_panel()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'ADMIN PANEL - MASUKKAN KREDENSIAL':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    username = input(f"\n{Y}[?] Username: {RS}")
    password = input(f"{Y}[?] Password: {RS}")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print(f"\n{BR}{G}[✓] Login admin berhasil!{RS}")
        time.sleep(1)
        admin_menu()
    else:
        print(f"\n{R}[!] Kredensial salah!{RS}")
        time.sleep(2)
        main()

def admin_menu():
    db = UserDB()
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_admin_panel()
        
        print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
        print(f"{BR}{C}║{'MENU ADMIN':^50}║{RS}")
        print(f"{BR}{C}╚{'═'*50}╚{RS}")
        
        print(f"\n{BR}{G}[1]{RS} Tambah User")
        print(f"{BR}{G}[2]{RS} Hapus User")
        print(f"{BR}{G}[3]{RS} Lihat Semua User")
        print(f"{BR}{G}[4]{RS} Kembali ke Menu Utama")
        
        choice = input(f"\n{Y}[?] Pilih opsi (1-4): {RS}")
        
        if choice == '1':
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
            print(f"{BR}{C}║{'TAMBAH USER BARU':^50}║{RS}")
            print(f"{BR}{C}╚{'═'*50}╚{RS}")
            
            user_id = input(f"\n{Y}[?] Masukkan ID Termux user: {RS}")
            username = input(f"{Y}[?] Masukkan nama user: {RS}")
            
            if db.add_user(user_id, username):
                print(f"\n{BR}{G}[✓] User berhasil ditambahkan!{RS}")
            else:
                print(f"\n{R}[!] Gagal menambahkan user!{RS}")
            
            input(f"\n{Y}Tekan Enter untuk melanjutkan...{RS}")
        
        elif choice == '2':
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
            print(f"{BR}{C}║{'HAPUS USER':^50}║{RS}")
            print(f"{BR}{C}╚{'═'*50}╚{RS}")
            
            user_id = input(f"\n{Y}[?] Masukkan ID Termux user yang akan dihapus: {RS}")
            
            if db.remove_user(user_id):
                print(f"\n{BR}{G}[✓] User berhasil dihapus!{RS}")
            else:
                print(f"\n{R}[!] User tidak ditemukan!{RS}")
            
            input(f"\n{Y}Tekan Enter untuk melanjutkan...{RS}")
        
        elif choice == '3':
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
            print(f"{BR}{C}║{'DAFTAR SEMUA USER':^50}║{RS}")
            print(f"{BR}{C}╚{'═'*50}╚{RS}")
            
            users = db.list_users()
            if users:
                print(f"\n{BR}{G}{'No.':<5} {'ID Termux':<20} {'Username':<20} {'Status':<10}{RS}")
                print(f"{G}{'='*60}{RS}")
                for i, (user_id, data) in enumerate(users.items(), 1):
                    print(f"{W}{i:<5} {user_id:<20} {data.get('username', 'N/A'):<20} {data.get('status', 'N/A'):<10}{RS}")
            else:
                print(f"\n{R}[!] Tidak ada user terdaftar!{RS}")
            
            input(f"\n{Y}Tekan Enter untuk melanjutkan...{RS}")
        
        elif choice == '4':
            break

# Vuln Scanner
def vuln_scanner():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_vuln_scan()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'VULNERABILITY SCANNER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    target = input(f"\n{Y}[?] Masukkan URL target (contoh: https://example.com): {RS}")
    
    print(f"\n{BR}{Y}[*] Memulai scan...{RS}")
    loading_animation("Scanning target", 3)
    
    try:
        # Check HTTP headers
        response = requests.get(target, timeout=10)
        headers = response.headers
        
        print(f"\n{BR}{G}[✓] Target aktif!{RS}")
        print(f"\n{BR}{C}════════ HASIL SCAN ════════{RS}")
        print(f"{Y}Status Code:{RS} {response.status_code}")
        print(f"{Y}Server:{RS} {headers.get('Server', 'Tidak diketahui')}")
        print(f"{Y}X-Powered-By:{RS} {headers.get('X-Powered-By', 'Tidak diketahui')}")
        
        # Vulnerability checks
        vulnerabilities = []
        
        # Check for security headers
        security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 
                          'X-XSS-Protection', 'Content-Security-Policy']
        
        for header in security_headers:
            if header not in headers:
                vulnerabilities.append(f"Header {header} tidak ditemukan")
        
        # Check for sensitive information
        sensitive_info = ['password', 'key', 'token', 'secret']
        if any(info in response.text.lower() for info in sensitive_info):
            vulnerabilities.append("Informasi sensitif ditemukan")
        
        # Display vulnerabilities
        if vulnerabilities:
            print(f"\n{R}[!] VULNERABILITIES FOUND:{RS}")
            for vuln in vulnerabilities:
                print(f"{R}  ⚠ {vuln}{RS}")
        else:
            print(f"\n{G}[✓] Tidak ditemukan vulnerability yang jelas{RS}")
            
    except Exception as e:
        print(f"\n{R}[!] Error: {str(e)}{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# Port Scanner
def port_scanner():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_portscan()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'PORT SCANNER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    target = input(f"\n{Y}[?] Masukkan target IP/Domain: {RS}")
    start_port = int(input(f"{Y}[?] Port awal (default: 1): {RS}") or "1")
    end_port = int(input(f"{Y}[?] Port akhir (default: 100): {RS}") or "100")
    
    print(f"\n{BR}{Y}[*] Memulai scan port {start_port}-{end_port}...{RS}")
    
    open_ports = []
    
    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    
    # Animated scanning
    for port in range(start_port, end_port + 1):
        sys.stdout.write(f"\r{BR}{C}Scanning port {port}/{end_port}...{RS}")
        sys.stdout.flush()
        
        if scan_port(port):
            open_ports.append(port)
            print(f"\r{G}[✓] Port {port} terbuka{RS}")
        time.sleep(0.05)
    
    print(f"\n{BR}{C}════════ HASIL SCAN ════════{RS}")
    if open_ports:
        print(f"{G}Port terbuka:{RS}")
        for port in open_ports:
            try:
                service = socket.getservbyport(port)
                print(f"  {G}Port {port}:{RS} {service}")
            except:
                print(f"  {G}Port {port}:{RS} Unknown service")
    else:
        print(f"{R}Tidak ada port terbuka ditemukan{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# Database Dumper
def database_dumper():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_dump_db()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'DATABASE DUMPER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    print(f"\n{Y}[!] Fitur ini memerlukan sqlmap terinstall!{RS}")
    print(f"{Y}[*] Memeriksa sqlmap...{RS}")
    
    # Check if sqlmap is installed
    try:
        result = subprocess.run(['sqlmap', '--version'], 
                              capture_output=True, text=True)
        if 'sqlmap' in result.stdout:
            print(f"{G}[✓] sqlmap terdeteksi!{RS}")
        else:
            print(f"{R}[!] sqlmap tidak ditemukan!{RS}")
            print(f"{Y}Install sqlmap dengan: pkg install sqlmap{RS}")
            input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
            return
    except:
        print(f"{R}[!] sqlmap tidak terinstall!{RS}")
        print(f"{Y}Install sqlmap dengan: pkg install sqlmap{RS}")
        input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    target = input(f"\n{Y}[?] Masukkan URL target (contoh: http://testphp.vulnweb.com): {RS}")
    
    print(f"\n{BR}{Y}[*] Memulai dump database...{RS}")
    print(f"{Y}[!] Proses ini mungkin memakan waktu beberapa menit{RS}")
    
    # Run sqlmap with basic parameters
    try:
        cmd = [
            'sqlmap', '-u', target,
            '--batch',
            '--forms',
            '--crawl=2',
            '--dump-all',
            '--threads=10'
        ]
        
        print(f"\n{BR}{C}════════ MENJALANKAN SQLMAP ════════{RS}")
        print(f"{Y}Command: {' '.join(cmd)}{RS}")
        print(f"\n{Y}Loading...{RS}")
        
        # Run sqlmap in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Display output in real-time
        for line in process.stdout:
            if 'injection' in line.lower() or 'database' in line.lower():
                if 'not vulnerable' not in line.lower():
                    print(f"{BR}{G}{line.strip()}{RS}")
                else:
                    print(f"{R}{line.strip()}{RS}")
            elif 'payload' in line.lower():
                print(f"{Y}{line.strip()}{RS}")
        
        process.wait()
        
        print(f"\n{BR}{C}════════ HASIL DUMP ════════{RS}")
        print(f"{G}Proses selesai!{RS}")
        print(f"{Y}Hasil disimpan di folder output sqlmap{RS}")
        
    except KeyboardInterrupt:
        print(f"\n{R}[!] Proses dihentikan oleh user{RS}")
    except Exception as e:
        print(f"\n{R}[!] Error: {str(e)}{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# Main Menu
def main():
    if not login():
        return
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_main_tools()
        
        termux_id = subprocess.getoutput("whoami")
        
        print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
        print(f"{BR}{C}║{'ZXX-TOOL PENTESTING SUITE':^50}║{RS}")
        print(f"{BR}{C}║{'User: ' + termux_id:^50}║{RS}")
        print(f"{BR}{C}╚{'═'*50}╚{RS}")
        
        print(f"\n{BR}{G}[1]{RS} Vulnerability Scanner")
        print(f"{BR}{G}[2]{RS} Port Scanner")
        print(f"{BR}{G}[3]{RS} Database Dumper (sqlmap)")
        print(f"{BR}{G}[4]{RS} Admin Panel")
        print(f"{BR}{R}[0]{RS} Exit")
        
        choice = input(f"\n{Y}[?] Pilih opsi (0-4): {RS}")
        
        if choice == '1':
            vuln_scanner()
        elif choice == '2':
            port_scanner()
        elif choice == '3':
            database_dumper()
        elif choice == '4':
            admin_panel()
        elif choice == '0':
            print(f"\n{BR}{Y}Terima kasih telah menggunakan ZXX-TOOL!{RS}")
            print(f"{Y}Made with ❤️ by MrZXX{RS}")
            time.sleep(2)
            sys.exit(0)

# Install dependencies
def install_dependencies():
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'INSTALLING DEPENDENCIES':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    dependencies = [
        'requests',
        'colorama'
    ]
    
    for dep in dependencies:
        print(f"\n{Y}[*] Menginstall {dep}...{RS}")
        subprocess.run(['pip', 'install', dep], capture_output=True)
        print(f"{G}[✓] {dep} berhasil diinstall{RS}")
    
    print(f"\n{BR}{G}[✓] Semua dependencies berhasil diinstall!{RS}")
    print(f"{Y}Jalankan tools dengan: python zxx-tool.py{RS}")
    time.sleep(2)

# Entry point
if __name__ == "__main__":
    # Check Python version
    if sys.version_info[0] < 3:
        print(f"{R}[!] Python 3 diperlukan!{RS}")
        sys.exit(1)
    
    # First run setup
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'w') as f:
            json.dump({}, f)
    
    # Check dependencies
    try:
        import requests
        import colorama
    except ImportError:
        print(f"{R}[!] Dependencies tidak ditemukan!{RS}")
        install = input(f"{Y}[?] Install dependencies? (y/n): {RS}")
        if install.lower() == 'y':
            install_dependencies()
    
    # Welcome animation
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{BR}{M}")
    animate_text("""
:::       ::: :::::::::: :::        :::        ::::::::   ::::::::  ::::    ::::  ::::::::::      
:+:       :+: :+:        :+:        :+:       :+:    :+: :+:    :+: +:+:+: :+:+:+ :+:             
+:+       +:+ +:+        +:+        +:+       +:+        +:+    +:+ +:+ +:+:+ +:+ +:+             
+#+  +:+  +#+ +#++:++#   +#+        +#+       +#+        +#+    +:+ +#+  +:+  +#+ +#++:++#        
+#+ +#+#+ +#+ +#+        +#+        +#+       +#+        +#    +#+ +#+       +#+ +#+             
 #+#+# #+#+#  #+#        #+#        #+#       #+#    #+# #+#    #+# #+#       #+# #+#             
  ###   ###   ########## ########## ########## ########   ########  ###       ### ##########      
    """, 0.001)
    print(RS)
    
    typing_effect(f"{BR}{G}ZXX-TOOL Pentesting Suite v1.0{RS}")
    typing_effect(f"{Y}Created by: MrZXX{RS}")
    typing_effect(f"{C}Contact: @Zxxtirwd on Telegram{RS}")
    print(f"\n{BR}{Y}Initializing...{RS}")
    loading_animation("Starting tools", 2)
    
    # Start main program
    main()
