#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ZXX-TOOL Pentesting Suite v2.0
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

# ==================== Halaman Awal Baru ====================
def initial_screen():
    """Tampilan awal sebelum cek user"""
    show_welcome()
    
    termux_id = subprocess.getoutput("whoami")
    
    print(f"\n{BR}{Y}Welcome User{RS}")
    print(f"{G}{'='*45}{RS}")
    print(f"{C}ID-Termux: {termux_id}{RS}")
    print(f"{C}User: {termux_id}{RS}")
    print(f"{G}{'='*45}{RS}")
    
    # CEK APAKAH INI ADMIN
    print(f"\n{BR}{G}[1]{RS} Admin Panel (Login untuk admin)")
    print(f"{BR}{R}[2]{RS} Exit")
    
    choice = input(f"\n{Y}[?] Pilih opsi (1-2): {RS}")
    
    if choice == '1':
        admin_login()
    elif choice == '2':
        print(f"\n{Y}Terima kasih!{RS}")
        time.sleep(1)
        sys.exit(0)
    else:
        print(f"{R}Pilihan tidak valid!{RS}")
        time.sleep(1)
        initial_screen()

def admin_login():
    """Login admin di halaman awal"""
    os.system('clear' if os.name == 'posix' else 'cls')
    show_admin_panel()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'ADMIN LOGIN':^50}║{RS}")
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
        initial_screen()

def admin_menu():
    """Menu admin setelah login sukses"""
    db = UserDB()
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_admin_panel()
        
        print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
        print(f"{BR}{C}║{'ADMIN DASHBOARD':^50}║{RS}")
        print(f"{BR}{C}╚{'═'*50}╚{RS}")
        
        termux_id = subprocess.getoutput("whoami")
        print(f"\n{BR}{Y}Logged in as: {ADMIN_USERNAME}{RS}")
        print(f"{Y}Your ID-Termux: {termux_id}{RS}")
        print(f"{C}{'='*50}{RS}")
        
        print(f"\n{BR}{G}[1]{RS} Tambah User Baru")
        print(f"{BR}{G}[2]{RS} Hapus User")
        print(f"{BR}{G}[3]{RS} Lihat Semua User")
        print(f"{BR}{G}[4]{RS} Masuk ke Tools (User Mode)")
        print(f"{BR}{R}[5]{RS} Logout Admin")
        
        choice = input(f"\n{Y}[?] Pilih opsi (1-5): {RS}")
        
        if choice == '1':
            add_user_menu(db)
        elif choice == '2':
            remove_user_menu(db)
        elif choice == '3':
            view_users_menu(db)
        elif choice == '4':
            # Admin bisa masuk ke tools juga
            db = UserDB()
            termux_id = subprocess.getoutput("whoami")
            if db.check_user(termux_id):
                print(f"\n{BR}{G}[✓] Masuk ke tools...{RS}")
                time.sleep(1)
                user_tools_menu()
            else:
                # Auto add admin sebagai user
                db.add_user(termux_id, ADMIN_USERNAME)
                print(f"\n{BR}{G}[✓] Admin ditambahkan sebagai user!{RS}")
                time.sleep(1)
                user_tools_menu()
        elif choice == '5':
            print(f"\n{BR}{Y}[*] Logging out...{RS}")
            time.sleep(1)
            break

def add_user_menu(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'TAMBAH USER BARU':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    print(f"\n{Y}[*] Cara mendapatkan ID Termux user:{RS}")
    print(f"{C}   Minta user jalankan: {BR}whoami{RS}")
    print(f"{C}   Contoh output: {BR}u0_a123{RS}")
    
    print(f"\n{G}{'='*50}{RS}")
    user_id = input(f"\n{Y}[?] Masukkan ID Termux user: {RS}")
    
    if not user_id:
        print(f"\n{R}[!] ID tidak boleh kosong!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    if db.check_user(user_id):
        print(f"\n{R}[!] User dengan ID {user_id} sudah terdaftar!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    username = input(f"{Y}[?] Masukkan nama user: {RS}")
    
    if db.add_user(user_id, username):
        print(f"\n{BR}{G}[✓] User berhasil ditambahkan!{RS}")
        print(f"{G}ID Termux: {user_id}{RS}")
        print(f"{G}Username: {username}{RS}")
        print(f"\n{Y}[!] Informasi untuk user:{RS}")
        print(f"{C}1. User harus install dependencies{RS}")
        print(f"{C}2. Jalankan tools dengan: python zxx-tool.py{RS}")
        print(f"{C}3. Tools akan otomatis mendeteksi ID Termux{RS}")
    else:
        print(f"\n{R}[!] Gagal menambahkan user!{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def remove_user_menu(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'HAPUS USER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    users = db.list_users()
    if not users:
        print(f"\n{R}[!] Tidak ada user terdaftar!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    print(f"\n{BR}{G}{'No.':<5} {'ID Termux':<20} {'Username':<20}{RS}")
    print(f"{G}{'='*50}{RS}")
    user_list = list(users.keys())
    for i, user_id in enumerate(user_list, 1):
        print(f"{W}{i:<5} {user_id:<20} {users[user_id].get('username', 'N/A'):<20}{RS}")
    
    print(f"\n{BR}{G}[0]{RS} Kembali")
    choice = input(f"\n{Y}[?] Pilih nomor user yang akan dihapus: {RS}")
    
    if choice == '0':
        return
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(user_list):
            user_id = user_list[idx]
            confirm = input(f"{R}[?] Yakin hapus user {user_id}? (y/n): {RS}")
            if confirm.lower() == 'y':
                if db.remove_user(user_id):
                    print(f"\n{BR}{G}[✓] User {user_id} berhasil dihapus!{RS}")
                else:
                    print(f"\n{R}[!] Gagal menghapus user!{RS}")
        else:
            print(f"{R}[!] Pilihan tidak valid!{RS}")
    except:
        print(f"{R}[!] Input tidak valid!{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def view_users_menu(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'DAFTAR SEMUA USER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    users = db.list_users()
    if users:
        print(f"\n{BR}{G}{'No.':<5} {'ID Termux':<20} {'Username':<20} {'Tanggal Daftar':<20}{RS}")
        print(f"{G}{'='*70}{RS}")
        for i, (user_id, data) in enumerate(users.items(), 1):
            print(f"{W}{i:<5} {user_id:<20} {data.get('username', 'N/A'):<20} {data.get('created_at', 'N/A'):<20}{RS}")
        
        print(f"\n{BR}{G}Total User: {len(users)} orang{RS}")
    else:
        print(f"\n{R}[!] Tidak ada user terdaftar!{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# ==================== User Tools ====================
def user_tools_menu():
    """Menu tools untuk user terdaftar"""
    db = UserDB()
    termux_id = subprocess.getoutput("whoami")
    
    if not db.check_user(termux_id):
        print(f"\n{R}[!] User tidak terdaftar!{RS}")
        print(f"{Y}Silakan hubungi admin: @Zxxtirwd{RS}")
        time.sleep(2)
        initial_screen()
        return
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_main_tools()
        
        user_data = db.users[termux_id]
        username = user_data.get('username', termux_id)
        
        print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
        print(f"{BR}{C}║{'ZXX-TOOL PENTESTING SUITE':^50}║{RS}")
        print(f"{BR}{C}║{'User: ' + username:^50}║{RS}")
        print(f"{BR}{C}╚{'═'*50}╚{RS}")
        
        print(f"\n{BR}{G}[1]{RS} Vulnerability Scanner")
        print(f"{BR}{G}[2]{RS} Port Scanner")
        print(f"{BR}{G}[3]{RS} Database Dumper (sqlmap)")
        print(f"{BR}{Y}[4]{RS} Admin Panel (Butuh Login)")
        print(f"{BR}{R}[0]{RS} Logout")
        
        choice = input(f"\n{Y}[?] Pilih opsi (0-4): {RS}")
        
        if choice == '1':
            vuln_scanner()
        elif choice == '2':
            port_scanner()
        elif choice == '3':
            database_dumper()
        elif choice == '4':
            # User coba akses admin panel
            print(f"\n{Y}[*] Mengakses admin panel...{RS}")
            time.sleep(1)
            user_admin_access()
        elif choice == '0':
            print(f"\n{BR}{Y}[*] Logging out...{RS}")
            time.sleep(1)
            initial_screen()
            break

def user_admin_access():
    """User mencoba akses admin panel"""
    os.system('clear' if os.name == 'posix' else 'cls')
    show_admin_panel()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'ADMIN PANEL - AKSES DITOLAK':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    print(f"\n{R}[!] HANYA ADMIN YANG BISA AKSES!{RS}")
    print(f"{Y}Jika Anda admin, login di halaman awal{RS}")
    print(f"{C}Username: {ADMIN_USERNAME}{RS}")
    print(f"{C}Password: ********{RS}")
    
    print(f"\n{Y}[!] Fitur admin:{RS}")
    print(f"{C}• Tambah/hapus user{RS}")
    print(f"{C}• Lihat semua user terdaftar{RS}")
    print(f"{C}• Manage akses tools{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# ==================== Tools Functions ====================
def vuln_scanner():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_vuln_scan()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'VULNERABILITY SCANNER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    target = input(f"\n{Y}[?] Masukkan URL target (contoh: https://example.com): {RS}")
    
    if not target.startswith('http'):
        target = 'http://' + target
    
    print(f"\n{BR}{Y}[*] Memulai scan...{RS}")
    loading_animation("Scanning target", 3)
    
    try:
        response = requests.get(target, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        print(f"\n{BR}{G}[✓] Target aktif!{RS}")
        print(f"\n{BR}{C}════════ HASIL SCAN ════════{RS}")
        print(f"{Y}URL:{RS} {target}")
        print(f"{Y}Status Code:{RS} {response.status_code}")
        print(f"{Y}Server:{RS} {response.headers.get('Server', 'Tidak diketahui')}")
        
        # Security checks
        vulns = []
        
        # Check headers
        security_headers = {
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'X-XSS-Protection': 'XSS protection',
            'Content-Security-Policy': 'Content Security Policy'
        }
        
        for header, desc in security_headers.items():
            if header not in response.headers:
                vulns.append(f"Missing: {desc}")
        
        # Check for PHP info
        if 'php' in response.headers.get('X-Powered-By', '').lower():
            vulns.append("PHP version exposed")
        
        # Display results
        if vulns:
            print(f"\n{R}[!] VULNERABILITIES FOUND:{RS}")
            for vuln in vulns:
                print(f"{R}  ⚠ {vuln}{RS}")
        else:
            print(f"\n{G}[✓] Tidak ditemukan vulnerability{RS}")
            
    except requests.exceptions.Timeout:
        print(f"\n{R}[!] Timeout: Target tidak merespons{RS}")
    except requests.exceptions.ConnectionError:
        print(f"\n{R}[!] Connection Error: Tidak bisa terhubung{RS}")
    except Exception as e:
        print(f"\n{R}[!] Error: {str(e)}{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def port_scanner():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_portscan()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'PORT SCANNER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    target = input(f"\n{Y}[?] Masukkan target IP/Domain: {RS}")
    
    # Resolve domain to IP
    try:
        if not target.replace('.', '').isdigit():
            ip = socket.gethostbyname(target)
            print(f"{C}[*] Resolved {target} → {ip}{RS}")
            target = ip
    except:
        print(f"{R}[!] Gagal resolve domain{RS}")
        input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    try:
        start_port = int(input(f"{Y}[?] Port awal (1-65535, default: 1): {RS}") or "1")
        end_port = int(input(f"{Y}[?] Port akhir (1-65535, default: 100): {RS}") or "100")
        
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            print(f"{R}[!] Port harus antara 1-65535{RS}")
            return
        if start_port > end_port:
            print(f"{R}[!] Port awal harus lebih kecil dari port akhir{RS}")
            return
    except:
        print(f"{R}[!] Input port tidak valid{RS}")
        return
    
    print(f"\n{BR}{Y}[*] Memulai scan port {start_port}-{end_port}...{RS}")
    print(f"{Y}Target: {target}{RS}")
    
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    # Scan with progress
    total_ports = end_port - start_port + 1
    for i, port in enumerate(range(start_port, end_port + 1), 1):
        progress = (i / total_ports) * 100
        sys.stdout.write(f"\r{BR}{C}Scanning: {i}/{total_ports} ports [{progress:.1f}%]{RS}")
        sys.stdout.flush()
        
        if scan_port(port):
            open_ports.append(port)
            print(f"\r{G}[✓] Port {port} terbuka{' '*50}{RS}")
        
        if i % 10 == 0:
            time.sleep(0.01)
    
    print(f"\n\n{BR}{C}════════ HASIL SCAN ════════{RS}")
    if open_ports:
        print(f"{G}Port terbuka ditemukan:{RS}")
        for port in open_ports:
            try:
                service = socket.getservbyport(port)
                print(f"  {G}Port {port:5d}:{RS} {service}")
            except:
                print(f"  {G}Port {port:5d}:{RS} Unknown service")
        print(f"\n{Y}Total: {len(open_ports)} port terbuka{RS}")
    else:
        print(f"{R}Tidak ada port terbuka ditemukan{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def database_dumper():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_dump_db()
    
    print(f"\n{BR}{C}╔{'═'*50}╗{RS}")
    print(f"{BR}{C}║{'DATABASE DUMPER':^50}║{RS}")
    print(f"{BR}{C}╚{'═'*50}╚{RS}")
    
    # Check sqlmap
    print(f"\n{Y}[*] Memeriksa sqlmap...{RS}")
    try:
        result = subprocess.run(['which', 'sqlmap'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{G}[✓] sqlmap terdeteksi!{RS}")
        else:
            print(f"{R}[!] sqlmap tidak ditemukan!{RS}")
            print(f"{Y}Install dengan: pkg install sqlmap{RS}")
            input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
            return
    except:
        print(f"{R}[!] Gagal memeriksa sqlmap{RS}")
        input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    target = input(f"\n{Y}[?] Masukkan URL target: {RS}")
    
    if not target:
        print(f"{R}[!] URL tidak boleh kosong{RS}")
        return
    
    print(f"\n{BR}{Y}[*] Memulai dump database...{RS}")
    print(f"{Y}[!] Proses ini mungkin memakan waktu{RS}")
    print(f"{C}Tekan Ctrl+C untuk membatalkan{RS}")
    
    try:
        # Basic sqlmap command
        cmd = [
            'sqlmap', '-u', target,
            '--batch',
            '--level=1',
            '--risk=1',
            '--dbs'
        ]
        
        print(f"\n{BR}{C}════════ MENJALANKAN SQLMAP ════════{RS}")
        print(f"{Y}Command: sqlmap -u {target} --batch --dbs{RS}")
        
        # Run sqlmap
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Read output in real-time
        print(f"\n{Y}Output:{RS}")
        for line in process.stdout:
            if any(keyword in line.lower() for keyword in ['database', 'injection', 'payload', 'available']):
                if 'not vulnerable' not in line.lower():
                    if 'available' in line.lower():
                        print(f"{BR}{G}{line.strip()}{RS}")
                    else:
                        print(f"{Y}{line.strip()}{RS}")
        
        process.wait()
        
        if process.returncode == 0:
            print(f"\n{BR}{G}[✓] Proses selesai!{RS}")
            print(f"{Y}Untuk dump data lengkap, gunakan perintah manual:{RS}")
            print(f"{C}sqlmap -u {target} --dump-all --batch{RS}")
        else:
            print(f"\n{R}[!] Proses gagal atau dibatalkan{RS}")
        
    except KeyboardInterrupt:
        print(f"\n{R}[!] Proses dihentikan oleh user{RS}")
    except Exception as e:
        print(f"\n{R}[!] Error: {str(e)}{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# ==================== Main Function ====================
def main():
    # Check Python version
    if sys.version_info[0] < 3:
        print(f"{R}[!] Python 3 diperlukan!{RS}")
        sys.exit(1)
    
    # First run setup
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'w') as f:
            json.dump({}, f)
        print(f"{G}[✓] Database user dibuat{RS}")
    
    # Check dependencies
    try:
        import requests
        import colorama
    except ImportError:
        print(f"{R}[!] Dependencies tidak ditemukan!{RS}")
        install = input(f"{Y}[?] Install dependencies? (y/n): {RS}")
        if install.lower() == 'y':
            os.system('pip install requests colorama')
            print(f"{G}[✓] Dependencies berhasil diinstall{RS}")
            time.sleep(1)
    
    # Start initial screen
    initial_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Program dihentikan{RS}")
        sys.exit(0)
