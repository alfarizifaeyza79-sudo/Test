#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ZXX-TOOL Pentesting Suite v2.2
# Author: MrZXX
# Contact: @Zxxtirwd

import os
import sys
import time
import json
import socket
import requests
import subprocess
from datetime import datetime
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Konfigurasi
ADMIN_USERNAME = "mrzxx"
ADMIN_PASSWORD = "mrzxx"
ADMIN_ID = "u0_a123"  # ID Termux admin khusus
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
        # Pastikan user_id adalah string
        user_id = str(user_id)
        self.users[user_id] = {
            "username": username,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        self.save_users()
        return True
    
    def remove_user(self, user_id):
        user_id = str(user_id)
        if user_id in self.users:
            del self.users[user_id]
            self.save_users()
            return True
        return False
    
    def check_user(self, user_id):
        user_id = str(user_id)
        # Admin selalu bisa akses tanpa perlu didaftarkan
        if user_id == ADMIN_ID:
            return True
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
+#+ +#+#+ +#+ +#+        +#+        +#+       +#+        +#    +#+ +#+       +#+ +#+             
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
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝""")
    print(RS)

# ==================== Halaman Awal ====================
def initial_screen():
    """Tampilan awal sebelum cek user"""
    show_welcome()
    
    termux_id = get_termux_id()
    
    print(f"\n{BR}{Y}Welcome User{RS}")
    print(f"{G}{'='*45}{RS}")
    print(f"{C}ID-Termux: {termux_id}{RS}")
    print(f"{C}User: {termux_id}{RS}")
    print(f"{G}{'='*45}{RS}")
    
    # Cek apakah ini admin khusus
    if termux_id == ADMIN_ID:
        print(f"\n{BR}{G}[!] ADMIN DETECTED!{RS}")
        time.sleep(1)
        admin_or_tools_choice()
    else:
        # User biasa
        db = UserDB()
        if db.check_user(termux_id):
            print(f"\n{BR}{G}[+] User terdaftar!{RS}")
            time.sleep(1)
            user_tools_menu()
        else:
            print(f"\n{R}[!] User tidak terdaftar!{RS}")
            print(f"{Y}Untuk mendaftar, chat admin di Telegram: @Zxxtirwd{RS}")
            print(f"{Y}Kirim ID Termux Anda: {BR}{termux_id}{RS}")
            print(f"\n{Y}Tekan Enter untuk keluar...{RS}")
            input()
            sys.exit(0)

def get_termux_id():
    """Mendapatkan ID Termux dengan handling error"""
    try:
        termux_id = subprocess.getoutput("whoami").strip()
        if not termux_id:
            termux_id = "unknown"
        return termux_id
    except:
        return "unknown"

def admin_or_tools_choice():
    """Admin memilih mau ke admin panel atau tools"""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_welcome()
        
        termux_id = get_termux_id()
        
        print(f"\n{BR}{G}{'='*50}{RS}")
        print(f"{BR}{G}ADMIN ACCESS DETECTED{RS}")
        print(f"{BR}{G}ID: {termux_id}{RS}")
        print(f"{BR}{G}{'='*50}{RS}")
        
        print(f"\n{BR}{C}[1] Admin Panel (Manage Users){RS}")
        print(f"{BR}{C}[2] Pentesting Tools{RS}")
        print(f"{BR}{C}[3] Auto Register Admin as User{RS}")
        print(f"{BR}{R}[0] Exit{RS}")
        
        choice = input(f"\n{Y}[?] Pilih opsi (0-3): {RS}")
        
        if choice == '1':
            admin_login()
        elif choice == '2':
            # Pastikan admin ada di database
            db = UserDB()
            if not db.check_user(termux_id):
                db.add_user(termux_id, "Admin_MrZXX")
                print(f"\n{BR}{G}[+] Admin ditambahkan ke database!{RS}")
                time.sleep(1)
            user_tools_menu()
        elif choice == '3':
            # Auto add admin ke database user
            db = UserDB()
            if not db.check_user(termux_id):
                db.add_user(termux_id, "Admin_MrZXX")
                print(f"\n{BR}{G}[+] Admin berhasil diregistrasi sebagai user!{RS}")
                time.sleep(1)
            else:
                print(f"\n{BR}{Y}[!] Admin sudah terdaftar sebagai user{RS}")
                time.sleep(1)
            admin_login()
        elif choice == '0':
            print(f"\n{Y}Terima kasih!{RS}")
            time.sleep(1)
            sys.exit(0)

def admin_login():
    """Login admin"""
    os.system('clear' if os.name == 'posix' else 'cls')
    show_admin_panel()
    
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}ADMIN LOGIN{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    print(f"\n{Y}[*] ID Admin: {ADMIN_ID}{RS}")
    print(f"{C}{'-'*50}{RS}")
    
    username = input(f"\n{Y}[?] Username: {RS}")
    password = input(f"{Y}[?] Password: {RS}")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print(f"\n{BR}{G}[+] Login admin berhasil!{RS}")
        time.sleep(1)
        admin_menu()
    else:
        print(f"\n{R}[!] Kredensial salah!{RS}")
        time.sleep(2)
        admin_or_tools_choice()

# ==================== Admin Menu ====================
def admin_menu():
    """Menu admin setelah login sukses"""
    db = UserDB()
    termux_id = get_termux_id()
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_admin_panel()
        
        print(f"\n{BR}{C}{'='*50}{RS}")
        print(f"{BR}{C}ADMIN DASHBOARD{RS}")
        print(f"{BR}{C}{'='*50}{RS}")
        
        print(f"\n{BR}{G}Admin ID: {termux_id}{RS}")
        print(f"{G}Username: {ADMIN_USERNAME}{RS}")
        print(f"{C}{'-'*50}{RS}")
        
        print(f"\n{BR}{M}[1] Tambah User Baru{RS}")
        print(f"{BR}{M}[2] Hapus User{RS}")
        print(f"{BR}{M}[3] Lihat Semua User{RS}")
        print(f"{BR}{M}[4] Masuk ke Tools{RS}")
        print(f"{BR}{M}[5] Check User Status{RS}")
        print(f"{BR}{R}[0] Logout Admin{RS}")
        
        choice = input(f"\n{Y}[?] Pilih opsi (0-5): {RS}")
        
        if choice == '1':
            add_user_menu(db)
        elif choice == '2':
            remove_user_menu(db)
        elif choice == '3':
            view_users_menu(db)
        elif choice == '4':
            print(f"\n{BR}{G}[+] Masuk ke tools...{RS}")
            time.sleep(1)
            user_tools_menu()
        elif choice == '5':
            check_user_status(db)
        elif choice == '0':
            print(f"\n{BR}{Y}[*] Logging out...{RS}")
            time.sleep(1)
            admin_or_tools_choice()
            break

def add_user_menu(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}TAMBAH USER BARU{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    print(f"\n{Y}[*] Cara mendapatkan ID Termux user:{RS}")
    print(f"{C}   Minta user jalankan: {BR}whoami{RS}")
    print(f"{C}   Contoh output: {BR}u0_a124, u0_a125, dst{RS}")
    
    print(f"\n{G}{'-'*50}{RS}")
    user_id = input(f"\n{Y}[?] Masukkan ID Termux user: {RS}").strip()
    
    if not user_id:
        print(f"\n{R}[!] ID tidak boleh kosong!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    if user_id == ADMIN_ID:
        print(f"\n{R}[!] Ini adalah ID Admin!{RS}")
        print(f"{Y}Admin sudah memiliki akses penuh{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    # Perbaikan: Gunakan check_user yang sudah benar
    if db.check_user(user_id):
        print(f"\n{R}[!] User dengan ID {user_id} sudah terdaftar!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    username = input(f"{Y}[?] Masukkan nama user: {RS}").strip()
    
    if not username:
        username = user_id
    
    if db.add_user(user_id, username):
        print(f"\n{BR}{G}[+] User berhasil ditambahkan!{RS}")
        print(f"{G}ID Termux: {BR}{user_id}{RS}")
        print(f"{G}Username: {BR}{username}{RS}")
        print(f"\n{Y}Informasi untuk user:{RS}")
        print(f"{C}1. Install dependencies: pip install requests colorama{RS}")
        print(f"{C}2. Jalankan tools: python zxx-tool.py{RS}")
        print(f"{C}3. Tools akan otomatis mendeteksi ID{RS}")
        
        # Simpan log
        with open("admin_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] Admin added user: {user_id} - {username}\n")
    else:
        print(f"\n{R}[!] Gagal menambahkan user!{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def remove_user_menu(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}HAPUS USER{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    users = db.list_users()
    if not users:
        print(f"\n{R}[!] Tidak ada user terdaftar!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    print(f"\n{BR}{G}DAFTAR USER TERDAFTAR:{RS}")
    print(f"{G}{'-'*50}{RS}")
    
    user_list = []
    print(f"{BR}{G}{'No.':<5} {'ID Termux':<20} {'Username':<20}{RS}")
    print(f"{G}{'-'*50}{RS}")
    
    for i, (user_id, data) in enumerate(users.items(), 1):
        if user_id != ADMIN_ID:  # Skip admin dari list
            user_list.append(user_id)
            print(f"{W}{i:<5} {user_id:<20} {data.get('username', 'N/A'):<20}{RS}")
    
    if not user_list:
        print(f"{Y}Tidak ada user selain admin{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    print(f"\n{BR}{G}[0] Kembali{RS}")
    choice = input(f"\n{Y}[?] Pilih nomor user yang akan dihapus: {RS}")
    
    if choice == '0':
        return
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(user_list):
            user_id = user_list[idx]
            username = users[user_id].get('username', 'N/A')
            
            print(f"\n{R}[!] Anda akan menghapus user:{RS}")
            print(f"{R}ID: {user_id}{RS}")
            print(f"{R}Username: {username}{RS}")
            
            confirm = input(f"\n{R}[?] Yakin hapus user ini? (y/n): {RS}")
            if confirm.lower() == 'y':
                if db.remove_user(user_id):
                    print(f"\n{BR}{G}[+] User {user_id} berhasil dihapus!{RS}")
                    
                    # Simpan log
                    with open("admin_log.txt", "a") as f:
                        f.write(f"[{datetime.now()}] Admin removed user: {user_id} - {username}\n")
                else:
                    print(f"\n{R}[!] Gagal menghapus user!{RS}")
        else:
            print(f"{R}[!] Pilihan tidak valid!{RS}")
    except:
        print(f"{R}[!] Input tidak valid!{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def view_users_menu(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}DAFTAR SEMUA USER{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    users = db.list_users()
    if users:
        print(f"\n{BR}{G}{'No.':<5} {'ID Termux':<20} {'Username':<20} {'Status':<10}{RS}")
        print(f"{G}{'='*60}{RS}")
        
        # Tampilkan admin pertama
        admin_count = 0
        user_count = 0
        
        for i, (user_id, data) in enumerate(users.items(), 1):
            if user_id == ADMIN_ID:
                admin_count += 1
                print(f"{BR}{C}{i:<5} {user_id:<20} {'[ADMIN]':<20} {'SPECIAL':<10}{RS}")
            else:
                user_count += 1
                print(f"{W}{i:<5} {user_id:<20} {data.get('username', 'N/A'):<20} {data.get('status', 'active'):<10}{RS}")
        
        print(f"\n{BR}{G}{'='*60}{RS}")
        print(f"{BR}{G}Total: {len(users)} user ({user_count} user biasa + {admin_count} admin){RS}")
    else:
        print(f"\n{R}[!] Tidak ada user terdaftar!{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def check_user_status(db):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}CHECK USER STATUS{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    user_id = input(f"\n{Y}[?] Masukkan ID Termux user: {RS}").strip()
    
    if not user_id:
        print(f"\n{R}[!] ID tidak boleh kosong!{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    if user_id == ADMIN_ID:
        print(f"\n{BR}{G}[+] Ini adalah ADMIN ID{RS}")
        print(f"{G}Status: SPECIAL ADMIN ACCESS{RS}")
        print(f"{G}Tidak perlu registrasi{RS}")
    elif db.check_user(user_id):
        user_data = db.users.get(user_id, {})
        print(f"\n{BR}{G}[+] User DITEMUKAN{RS}")
        print(f"{G}ID Termux: {user_id}{RS}")
        print(f"{G}Username: {user_data.get('username', 'N/A')}{RS}")
        print(f"{G}Tanggal Daftar: {user_data.get('created_at', 'N/A')}{RS}")
        print(f"{G}Status: {user_data.get('status', 'active')}{RS}")
    else:
        print(f"\n{R}[!] User TIDAK DITEMUKAN{RS}")
        print(f"{Y}User dengan ID {user_id} belum terdaftar{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# ==================== User Tools Menu ====================
def user_tools_menu():
    """Menu tools untuk user terdaftar (termasuk admin)"""
    db = UserDB()
    termux_id = get_termux_id()
    
    # Debug: Cek status user
    print(f"\n{BR}{Y}[*] Checking user status...{RS}")
    print(f"{C}Your ID: {termux_id}{RS}")
    print(f"{C}Admin ID: {ADMIN_ID}{RS}")
    
    # Cek apakah user terdaftar
    is_registered = db.check_user(termux_id)
    is_admin = (termux_id == ADMIN_ID)
    
    print(f"{C}Is Admin: {is_admin}{RS}")
    print(f"{C}Is Registered: {is_registered}{RS}")
    
    # Jika bukan admin dan tidak terdaftar
    if not is_admin and not is_registered:
        print(f"\n{R}[!] User tidak terdaftar!{RS}")
        print(f"{Y}Silakan hubungi admin: @Zxxtirwd{RS}")
        print(f"{Y}Kirim ID Termux Anda: {BR}{termux_id}{RS}")
        time.sleep(3)
        sys.exit(0)
    
    # Jika admin tapi belum ada di database, tambahkan otomatis
    if is_admin and not is_registered:
        print(f"\n{BR}{Y}[*] Auto registering admin...{RS}")
        db.add_user(termux_id, "Admin_MrZXX")
        print(f"{G}[+] Admin berhasil diregistrasi!{RS}")
        time.sleep(1)
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_main_tools()
        
        # Ambil data user
        if termux_id == ADMIN_ID:
            username = "Admin_MrZXX"
            user_type = f"{BR}{G}[ADMIN]{RS}"
        else:
            user_data = db.users.get(termux_id, {})
            username = user_data.get('username', termux_id)
            user_type = f"{BR}{C}[USER]{RS}"
        
        print(f"\n{BR}{C}{'='*50}{RS}")
        print(f"{BR}{C}ZXX-TOOL PENTESTING SUITE{RS}")
        print(f"{BR}{C}{user_type} {username}{RS}")
        print(f"{BR}{C}ID: {termux_id}{RS}")
        print(f"{BR}{C}{'='*50}{RS}")
        
        # Menu berbeda untuk admin dan user
        if termux_id == ADMIN_ID:
            print(f"\n{BR}{M}[1] Vulnerability Scanner{RS}")
            print(f"{BR}{M}[2] Port Scanner{RS}")
            print(f"{BR}{M}[3] Database Dumper{RS}")
            print(f"{BR}{G}[4] Admin Panel{RS}")
            print(f"{BR}{G}[5] View All Users{RS}")
            print(f"{BR}{Y}[6] Check My Status{RS}")
            print(f"{BR}{R}[0] Exit{RS}")
        else:
            print(f"\n{BR}{M}[1] Vulnerability Scanner{RS}")
            print(f"{BR}{M}[2] Port Scanner{RS}")
            print(f"{BR}{M}[3] Database Dumper{RS}")
            print(f"{BR}{Y}[9] Contact Admin{RS}")
            print(f"{BR}{R}[0] Logout{RS}")
        
        choice = input(f"\n{Y}[?] Pilih opsi: {RS}")
        
        if choice == '1':
            vuln_scanner()
        elif choice == '2':
            port_scanner()
        elif choice == '3':
            database_dumper()
        elif choice == '4' and termux_id == ADMIN_ID:
            print(f"\n{BR}{G}[*] Mengakses admin panel...{RS}")
            time.sleep(1)
            admin_login()
        elif choice == '5' and termux_id == ADMIN_ID:
            view_users_menu(db)
        elif choice == '6' and termux_id == ADMIN_ID:
            check_user_status(db)
        elif choice == '9' and termux_id != ADMIN_ID:
            contact_admin_menu(termux_id)
        elif choice == '0':
            if termux_id == ADMIN_ID:
                print(f"\n{BR}{Y}[*] Kembali ke menu awal...{RS}")
                time.sleep(1)
                admin_or_tools_choice()
                break
            else:
                print(f"\n{BR}{Y}[*] Logging out...{RS}")
                time.sleep(1)
                sys.exit(0)

def contact_admin_menu(termux_id):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}CONTACT ADMIN{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    print(f"\n{Y}Telegram: @Zxxtirwd{RS}")
    print(f"{C}Kirim pesan dengan format:{RS}")
    print(f"{BR}================================{RS}")
    print(f"{G}Hi Admin, saya ingin mendaftar{RS}")
    print(f"{G}ID Termux saya: {termux_id}{RS}")
    print(f"{G}Nama: [isi nama Anda]{RS}")
    print(f"{BR}================================{RS}")
    
    print(f"\n{Y}Atau gunakan template ini:{RS}")
    print(f"{C}Hi Admin @Zxxtirwd, saya ingin mendaftar ZXX-TOOL.{RS}")
    print(f"{C}ID Termux: {termux_id}{RS}")
    print(f"{C}Nama: [Your Name]{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# ==================== Tools Functions ====================
def vuln_scanner():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_vuln_scan()
    
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}VULNERABILITY SCANNER{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    target = input(f"\n{Y}[?] Masukkan URL target: {RS}").strip()
    
    if not target:
        print(f"{R}[!] URL tidak boleh kosong{RS}")
        input(f"{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    print(f"\n{BR}{Y}[*] Memulai scan...{RS}")
    loading_animation("Scanning target", 2)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        response = requests.get(target, timeout=10, headers=headers, verify=False)
        
        print(f"\n{BR}{G}[+] Target aktif!{RS}")
        print(f"\n{BR}{C}{'='*50}{RS}")
        print(f"{BR}{C}SCAN RESULTS{RS}")
        print(f"{BR}{C}{'='*50}{RS}")
        print(f"{Y}URL: {target}{RS}")
        print(f"{Y}Status: {response.status_code} {response.reason}{RS}")
        print(f"{Y}Server: {response.headers.get('Server', 'Not found')}{RS}")
        print(f"{Y}Powered By: {response.headers.get('X-Powered-By', 'Not found')}{RS}")
        
        # Security checks
        vulns = []
        warnings = []
        
        # Check security headers
        security_headers = {
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'X-XSS-Protection': 'XSS protection',
            'Content-Security-Policy': 'Content Security Policy',
            'Strict-Transport-Security': 'HSTS'
        }
        
        for header, desc in security_headers.items():
            if header not in response.headers:
                warnings.append(f"Missing: {desc} ({header})")
        
        # Check for exposed info
        if 'server' in response.headers:
            warnings.append(f"Server exposed: {response.headers['server']}")
        
        if 'x-powered-by' in response.headers:
            warnings.append(f"Technology exposed: {response.headers['x-powered-by']}")
        
        # Check for common vulnerabilities
        if 'php' in response.headers.get('x-powered-by', '').lower():
            warnings.append("PHP version might be exposed")
        
        # Display results
        if vulns:
            print(f"\n{R}VULNERABILITIES FOUND:{RS}")
            for vuln in vulns:
                print(f"{R}  [-] {vuln}{RS}")
        
        if warnings:
            print(f"\n{Y}WARNINGS:{RS}")
            for warn in warnings:
                print(f"{Y}  [!] {warn}{RS}")
        
        if not vulns and not warnings:
            print(f"\n{G}No vulnerabilities or warnings found{RS}")
            
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
    
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}PORT SCANNER{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    target = input(f"\n{Y}[?] Masukkan target (IP/Domain): {RS}").strip()
    
    if not target:
        print(f"{R}[!] Target tidak boleh kosong{RS}")
        input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    # Resolve domain
    try:
        if not target.replace('.', '').isdigit():
            ip = socket.gethostbyname(target)
            print(f"{C}[*] {target} -> {ip}{RS}")
            target = ip
    except:
        print(f"{R}[!] Gagal resolve domain{RS}")
        input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    try:
        start_port = int(input(f"{Y}[?] Port awal (default: 1): {RS}") or "1")
        end_port = int(input(f"{Y}[?] Port akhir (default: 1000): {RS}") or "1000")
        
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            print(f"{R}[!] Port harus 1-65535{RS}")
            return
        if start_port > end_port:
            print(f"{R}[!] Port awal harus <= port akhir{RS}")
            return
        if (end_port - start_port) > 10000:
            print(f"{Y}[!] Warning: Scanning {end_port-start_port+1} ports{RS}")
            confirm = input(f"{Y}Lanjutkan? (y/n): {RS}")
            if confirm.lower() != 'y':
                return
    except:
        print(f"{R}[!] Input tidak valid{RS}")
        return
    
    print(f"\n{BR}{Y}[*] Scanning {target}:{start_port}-{end_port}...{RS}")
    
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
    
    # Scan with animation
    total = end_port - start_port + 1
    for i, port in enumerate(range(start_port, end_port + 1), 1):
        progress = (i / total) * 100
        sys.stdout.write(f"\r{BR}{C}Scanning: {i}/{total} [{progress:.1f}%]{RS}")
        sys.stdout.flush()
        
        if scan_port(port):
            open_ports.append(port)
            sys.stdout.write(f"\r{G}[+] Port {port} OPEN{' '*30}{RS}\n")
        
        if i % 50 == 0:
            time.sleep(0.01)
    
    print(f"\n\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}SCAN RESULTS{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    print(f"{Y}Target: {target}{RS}")
    print(f"{Y}Port Range: {start_port}-{end_port}{RS}")
    
    if open_ports:
        print(f"\n{G}OPEN PORTS:{RS}")
        common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP Proxy",
            8443: "HTTPS Alt"
        }
        
        for port in sorted(open_ports):
            service = common_ports.get(port, "Unknown")
            print(f"  {G}Port {port:5d}: {service}{RS}")
        
        print(f"\n{Y}Total: {len(open_ports)} open ports{RS}")
    else:
        print(f"\n{R}No open ports found{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

def database_dumper():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_dump_db()
    
    print(f"\n{BR}{C}{'='*50}{RS}")
    print(f"{BR}{C}DATABASE DUMPER{RS}")
    print(f"{BR}{C}{'='*50}{RS}")
    
    # Check sqlmap
    print(f"\n{Y}[*] Checking sqlmap...{RS}")
    try:
        result = subprocess.run(['which', 'sqlmap'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"{G}[+] sqlmap detected!{RS}")
        else:
            print(f"{R}[!] sqlmap not found!{RS}")
            print(f"{Y}Install with: pkg install sqlmap{RS}")
            input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
            return
    except:
        print(f"{R}[!] Failed to check sqlmap{RS}")
        input(f"\n{Y}Tekan Enter untuk kembali...{RS}")
        return
    
    target = input(f"\n{Y}[?] Masukkan URL target (with parameters): {RS}").strip()
    
    if not target:
        print(f"{R}[!] URL tidak boleh kosong{RS}")
        return
    
    print(f"\n{BR}{Y}[*] Scan options:{RS}")
    print(f"{C}[1] Quick Scan (Check vulnerability){RS}")
    print(f"{C}[2] Deep Scan (Full scan){RS}")
    print(f"{C}[3] Dump Databases{RS}")
    print(f"{C}[4] Custom Command{RS}")
    
    scan_type = input(f"\n{Y}[?] Pilih tipe scan (1-4): {RS}")
    
    if scan_type == '1':
        cmd = ['sqlmap', '-u', target, '--batch', '--level=1', '--risk=1']
    elif scan_type == '2':
        cmd = ['sqlmap', '-u', target, '--batch', '--level=3', '--risk=2', '--crawl=10']
    elif scan_type == '3':
        cmd = ['sqlmap', '-u', target, '--batch', '--dbs']
    elif scan_type == '4':
        custom_cmd = input(f"{Y}[?] Masukkan command sqlmap custom: {RS}")
        cmd = custom_cmd.split()
        if 'sqlmap' not in cmd[0]:
            cmd.insert(0, 'sqlmap')
    else:
        print(f"{R}[!] Pilihan tidak valid{RS}")
        return
    
    print(f"\n{BR}{Y}[*] Starting sqlmap...{RS}")
    print(f"{C}Command: {' '.join(cmd)}{RS}")
    print(f"{Y}Press Ctrl+C to cancel{RS}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        print(f"\n{Y}Output:{RS}")
        for line in process.stdout:
            line = line.strip()
            if line:
                if 'sqlmap identified' in line.lower():
                    print(f"{BR}{G}{line}{RS}")
                elif 'available databases' in line.lower():
                    print(f"{BR}{C}{line}{RS}")
                elif 'vulnerable' in line.lower():
                    if 'not vulnerable' not in line.lower():
                        print(f"{BR}{R}{line}{RS}")
                    else:
                        print(f"{G}{line}{RS}")
                elif any(word in line.lower() for word in ['database', 'table', 'payload']):
                    print(f"{Y}{line}{RS}")
        
        process.wait()
        
        print(f"\n{BR}{C}{'='*50}{RS}")
        if process.returncode == 0:
            print(f"{G}Scan completed!{RS}")
            print(f"{Y}Check full results in sqlmap output folder{RS}")
        else:
            print(f"{Y}Process stopped or error{RS}")
        
    except KeyboardInterrupt:
        print(f"\n{R}[!] Scan cancelled{RS}")
    except Exception as e:
        print(f"\n{R}[!] Error: {str(e)}{RS}")
    
    input(f"\n{Y}Tekan Enter untuk kembali...{RS}")

# ==================== Main Function ====================
def main():
    # Check Python version
    if sys.version_info[0] < 3:
        print(f"{R}[!] Python 3 required!{RS}")
        sys.exit(1)
    
    # First run setup
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'w') as f:
            json.dump({}, f)
        print(f"{G}[+] User database created{RS}")
    
    # Check dependencies
    try:
        import requests
        import colorama
    except ImportError:
        print(f"{R}[!] Dependencies not found!{RS}")
        install = input(f"{Y}[?] Install dependencies? (y/n): {RS}")
        if install.lower() == 'y':
            try:
                os.system('pip install requests colorama')
                print(f"{G}[+] Dependencies installed successfully{RS}")
                time.sleep(1)
            except:
                print(f"{R}[!] Failed to install dependencies{RS}")
                print(f"{Y}Try: pip install requests colorama{RS}")
                time.sleep(2)
    
    # Get termux ID
    termux_id = get_termux_id()
    
    # Startup animation
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
    
    typing_effect(f"{BR}{G}ZXX-TOOL Pentesting Suite v2.2{RS}")
    typing_effect(f"{Y}Created by: MrZXX{RS}")
    typing_effect(f"{C}Admin ID: {ADMIN_ID}{RS}")
    typing_effect(f"{M}Contact: @Zxxtirwd on Telegram{RS}")
    
    print(f"\n{BR}{Y}Initializing...{RS}")
    loading_animation("Starting system", 1)
    
    print(f"\n{C}Your ID-Termux: {BR}{termux_id}{RS}")
    
    if termux_id == ADMIN_ID:
        print(f"{BR}{G}[!] ADMIN PRIVILEGES DETECTED!{RS}")
        time.sleep(1)
    
    time.sleep(1)
    
    # Start initial screen
    initial_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Program stopped{RS}")
        sys.exit(0)
