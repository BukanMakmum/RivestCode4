import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menu
from ttkthemes import ThemedStyle
import webbrowser
from PIL import Image, ImageTk
import os
import re

def swap(S, i, j):
    S[i], S[j] = S[j], S[i]

def initialize_state(key):
    S = list(range(8))
    T = [key[i % len(key)] for i in range(8)]
    return S, T

def permutation(S, T):
    j = 0
    for i in range(8):
        j = (j + S[i] + T[i]) % 8
        S[j], S[i] = S[i], S[j]

def generate_key_stream(S):
    i, j = 0, 0
    key_stream = []
    for iteration in range(4):
        i = (i + 1) % 8
        j = (j + S[i]) % 8
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 8
        k = S[t]
        key_stream.append(k)
    return key_stream

def rc4_simple_encrypt(plaintext, key):
    S, T = initialize_state(key)
    permutation(S, T)
    key_stream = generate_key_stream(S)
    ciphertext = [p ^ k for p, k in zip(plaintext, key_stream)]
    return ciphertext

def rc4_simple_decrypt(ciphertext, key):
    S, T = initialize_state(key)
    permutation(S, T)
    key_stream = generate_key_stream(S)
    plaintext = [c ^ k for c, k in zip(ciphertext, key_stream)]
    return plaintext

def is_valid_input(input_str):
    return re.match("^[0-7]+$", input_str)

def encrypt_text():
    plaintext_str = text_entry.get("1.0", "end-1c").replace(" ", "").strip()
    key_str = key_entry.get("1.0", "end-1c").strip()

    if not is_valid_input(plaintext_str) or not is_valid_input(key_str):
        messagebox.showerror("Error", "Masukkan angka desimal antara 0 - 7 untuk plaintext dan key.")
        return

    if len(plaintext_str) != 4 or len(key_str) != 4:
        messagebox.showerror("Error", "Masukkan 4 angka untuk plaintext dan kunci.")
        return

    plaintext = [int(bit) for bit in plaintext_str]
    key = [int(bit) for bit in key_str]

    ciphertext = rc4_simple_encrypt(plaintext, key)
    ciphertext_str = "".join(map(str, ciphertext))
    result_entry.config(state='normal')
    result_entry.delete("1.0", tk.END)
    result_entry.insert("1.0", ciphertext_str)
    result_entry.config(state='disabled')

def decrypt_text():
    ciphertext_str = text_entry.get("1.0", "end-1c").replace(" ", "").strip()
    key_str = key_entry.get("1.0", "end-1c").strip()

    if not is_valid_input(ciphertext_str) or not is_valid_input(key_str):
        messagebox.showerror("Error", "Masukkan angka desimal antara 0 - 7 untuk ciphertext dan key.")
        return

    if len(ciphertext_str) != 4 or len(key_str) != 4:
        messagebox.showerror("Error", "Masukkan 4 angka untuk ciphertext dan kunci.")
        return

    ciphertext = [int(bit) for bit in ciphertext_str]
    key = [int(bit) for bit in key_str]

    decrypted_text = rc4_simple_decrypt(ciphertext, key)

    decrypted_text_str = "".join(map(str, decrypted_text))
    result_entry.config(state='normal')
    result_entry.delete("1.0", tk.END)
    result_entry.insert("1.0", decrypted_text_str)
    result_entry.config(state='disabled')

def reset_text():
    text_entry.delete("1.0", tk.END)
    key_entry.delete("1.0", tk.END)
    result_entry.config(state='normal')
    result_entry.delete("1.0", tk.END)
    result_entry.config(state='disabled')

def show_about_info():
    root_title = root.title()
    email = "imamsyt22@mhs.usk.ac.id"
    about_info = f"{root_title}\nVersion {app_version}\n\nDeveloped by [Bukan Makmum]\nEmail: {email}"
    result = messagebox.showinfo("About", about_info, icon=messagebox.INFO)
    if result:
        open_github()

def open_github():
    webbrowser.open("https://github.com/BukanMakmum/RivestCode4.git")

def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def exit_app():
    root.quit()

def open_email(event):
    webbrowser.open("mailto:imamsayuti.usk@gmail.com")

def on_enter(event):
    event.widget.config(bg=event.widget.highlight_color, fg='white')

def on_leave(event):
    event.widget.config(bg=event.widget.original_color, fg='black')

root = tk.Tk()
root.title("Rivest Code 4")
app_version = "Education 1.0"

window_width = 335
window_height = 245
root.geometry(f"{window_width}x{window_height}")
root.configure(bg="#87CEFA")

root.resizable(False, False)

current_directory = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'

favicon_path = os.path.join(current_directory, "favicon.ico")
root.iconbitmap(default=favicon_path)

style = ThemedStyle(root)
style.set_theme("adapta")

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Debug Result", command="", state=tk.DISABLED)
file_menu.add_command(label="Exit", command=exit_app)

menubar.add_command(label="About", command=show_about_info)

judul_jendela = root.title()

title_label = ttk.Label(root, text=judul_jendela, font=("Helvetica", 14, "bold"), background=root.cget('bg'))
title_label.grid(row=0, column=1, padx=10, pady=10)

version_label = ttk.Label(root, text=f"Version {app_version}", font=("Helvetica", 10), background=root.cget('bg'))
version_label.grid(row=1, column=1, padx=10, pady=2)

title_label.grid(pady=(20, 0))

text_label = ttk.Label(root, text="Text (4 digits):", foreground="black", background=root.cget('bg'))
text_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

text_entry = tk.Text(root, height=1, width=20)
text_entry.grid(row=2, column=1, padx=5, pady=5)

key_label = ttk.Label(root, text="Key (4 digits):", foreground="black", background=root.cget('bg'))
key_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

key_entry = tk.Text(root, height=1, width=20)
key_entry.grid(row=3, column=1, padx=5, pady=5)

reset_button = tk.Button(root, text="Reset", width=6, command=reset_text)
reset_button.grid(row=4, column=0, padx=(10, 5), pady=10, sticky="")
reset_button.highlight_color = 'red'
reset_button.original_color = 'SystemButtonFace'
reset_button.bind("<Enter>", on_enter)
reset_button.bind("<Leave>", on_leave)

decrypt_button = tk.Button(root, text="Decrypt", width=6, command=decrypt_text)
decrypt_button.grid(row=4, column=1, padx=5, pady=10, sticky="")
decrypt_button.highlight_color = 'green'
decrypt_button.original_color = 'SystemButtonFace'
decrypt_button.bind("<Enter>", on_enter)
decrypt_button.bind("<Leave>", on_leave)

encrypt_button = tk.Button(root, text="Encrypt", width=6, command=encrypt_text)
encrypt_button.grid(row=4, column=2, padx=5, pady=10, sticky="")
encrypt_button.highlight_color = 'blue'
encrypt_button.original_color = 'SystemButtonFace'
encrypt_button.bind("<Enter>", on_enter)
encrypt_button.bind("<Leave>", on_leave)

result_label = ttk.Label(root, text="Result:", foreground="black", background=root.cget('bg'))
result_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

result_entry = tk.Text(root, height=1, width=20, bg="light gray", state='disabled')
result_entry.grid(row=5, column=1, padx=5, pady=5)

# #Dilarang hapus, sesama pengembang/pemrograman/mahasiswa/sarjana harus saling menghargai karya orang lain!
copyright_label = tk.Label(root, text="© 2023 BukanMakmum.", font=("Helvetica", 8, "bold"), foreground="#fbf7f6", cursor="hand2", background=root.cget('bg'))
copyright_label.grid(row=6, column=1, pady=(10, 20), sticky="nsew")
"""
Jika ingin berkontribusi silakan Clone Github berikut https://github.com/BukanMakmum/RivestCode4.git
#User sangat menghargai kontribusi Anda, dengan menampilkan profil di halaman kontribusi. 

# Mengatur teks hak cipta menjadi rata tengah horizontal
#copyright_label.configure(anchor="center", justify="center")
"""
copyright_label.bind("<Button-1>", open_email)

center_window(root)

root.mainloop()
