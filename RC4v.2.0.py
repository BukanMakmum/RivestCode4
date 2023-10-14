import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menu  # Tambahkan ini untuk mengimpor modul menu
from ttkthemes import ThemedStyle
from tkinter import scrolledtext  # Import the scrolledtext module
from tkinter import filedialog
import webbrowser # Fungsi untuk mengarahkan ke alamat email saat teks hak cipta diklik
from PIL import Image, ImageTk
import os
import re

# Initialize the debug_results list
debug_results = []

# Fungsi untuk menukar elemen dalam list
def swap(S, i, j):
    S[i], S[j] = S[j], S[i]

# Fungsi untuk menginisialisasi state
def initialize_state(key):
    S = list(range(8))
    T = [key[i % len(key)] for i in range(8)]

    # Debug: Menampilkan nilai S dan T setelah inisialisasi
    debug_results.append("\nInitialize State:")
    debug_results.append(f"S : {' '.join(map(str, S))}")
    debug_results.append(f"T : {' '.join(map(str, T))}")

    return S, T

def permutation(S, T):
    global debug_results  # Tambahkan variabel global
    j = 0

    debug_text = []  # Inisialisasi list untuk menyimpan hasil debug

    for i in range(8):  # Ubah range menjadi range(1, 9) jika ingin dimulai dari 1 hingga 8
        debug_text.append(f"Iterasi Permutasi ke-{i + 1} :")
        debug_text.append(f"S : {' '.join(map(str, S))}")
        debug_text.append(f"T : {' '.join(map(str, T))}")
        debug_text.append(f"j = {j}")
        debug_text.append(f"i = {i}")
        debug_text.append(f"j = (j + S[i] + T[i]) mod 8 = ({j} + {S[i]} + {T[i]}) mod 8 = {(j + S[i] + T[i]) % 8}")
        j = (j + S[i] + T[i]) % 8  # Perbarui nilai j terlebih dahulu
        S[j], S[i] = S[i], S[j]  # Swap yang benar
        debug_text.append(f"Swap (S[i], S[j]) = Swap (S[{i}], S[{j}])")
        debug_text.append(f"S : {' '.join(map(str, S))}\n")

    # Debug: Menggabungkan hasil debug menjadi satu string
    debug_output = "\n".join(debug_text)
    debug_results.append("\nPermutation State:")
    debug_results.append(debug_output)  # Menambahkan hasil debug ke dalam debug_results


# Fungsi untuk menghasilkan stream kunci
def generate_key_stream(S, data, is_encryption=True):
    i, j = 0, 0
    key_stream = []  # Inisialisasi list untuk stream kunci

    for iteration in range(4):  # Empat iterasi
       
        # Debug: Menambahkan hasil debug stream kunci sebelum swap
        debug_results.append("\n"+ f"Iterasi Key Stream ke-{iteration + 1}:")
        debug_results.append(f"S = {' '.join(map(str, S))}")
        debug_results.append(f"i = (i + 1) mod 8 = ({i} + 1) mod 8 = {(i + 1) % 8}")
        i = (i + 1) % 8
        debug_results.append(f"j = (j + S[i]) mod 8 = ({j} + S[{i}]) mod 8 =({j} + {S[i]}) mod 8 = {(j + S[i]) % 8}")
        j = (j + S[i]) % 8

        # Langsung menukar elemen S tanpa menggunakan fungsi swap
        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) % 8
        k = S[t]
        key_stream.append(k)

        # Debug: Menambahkan hasil debug stream kunci setelah swap
        debug_results.append(f"Swap (S[i], S[j]) = Swap(S[{i}], S[{j}])")
        debug_results.append(f"S = {' '.join(map(str, S))}")
        debug_results.append(f"t = (S[i] + S[j]) mod 8 = (S[{i}] + S[{j}])  mod 8 = ({S[i]} + {S[j]}) mod 8 = {(S[i] + S[j]) % 8}")
        debug_results.append(f"k = (S[t]) = S[{t}] = {k}\n")
        
        if is_encryption:
            debug_results.append(f"P = {' '.join(map(str, data))}")
            debug_results.append(f"3-bit ke-{iteration} ciphertext:")
            k_bin = f"{k:03b}"  # Format biner menjadi 3 digit
            data_bin = f"{data[iteration]:03b}"
            result_bin = f"{k ^ data[iteration]:03b}"
            debug_results.append(f"C[{iteration}] = K[{iteration}] XOR P[{iteration}] = {k_bin} XOR {data_bin} = {k} XOR {data[iteration]} = {result_bin} = {k ^ data[iteration]}\n")
        else:
            debug_results.append(f"P = {' '.join(map(str, data))}")
            debug_results.append(f"3-bit ke-{iteration} plaintext:")
            k_bin = f"{k:03b}"  # Format biner menjadi 3 digit
            data_bin = f"{data[iteration]:03b}"
            result_bin = f"{k ^ data[iteration]:03b}"
            debug_results.append(f"C[{iteration + 1}] = K[{iteration}] XOR P[{iteration}] = {k_bin} XOR {data_bin} = {k} XOR {data[iteration]} = {result_bin} = {k ^ data[iteration]}\n")

    return key_stream

# Fungsi untuk enkripsi plaintext
def rc4_simple_encrypt(plaintext, key):
    S, T = initialize_state(key)
    
    permutation(S, T)
    
    key_stream = generate_key_stream(S, plaintext, is_encryption=True)
    
    # Menghitung ciphertext sebagai XOR antara plaintext dan key_stream
    ciphertext = [p ^ k for p, k in zip(plaintext, key_stream)]
    
    # Debug: Menambahkan hasil debug enkripsi dalam format desimal dan 4 kelompok biner 3 bit
    debug_results.append("\nEncryption:")
    
    debug_results.append("Plaintext (Decimal):")
    debug_results.append(" ".join(map(str, plaintext)))
    
    debug_results.append("Plaintext (Binary):")
    plaintext_binary_grouped = [format(bit, '03b') for bit in plaintext]
    debug_results.append(" ".join(plaintext_binary_grouped))
    
    debug_results.append("\nKey (Decimal):")
    debug_results.append(" ".join(map(str, key)))
    
    debug_results.append("Key (Binary):")
    key_binary_grouped = [format(bit, '03b') for bit in key]
    debug_results.append(" ".join(key_binary_grouped))
    
    debug_results.append("\nCiphertext Text (Decimal):")
    debug_results.append(" ".join(map(str, ciphertext)))
    
    debug_results.append("Ciphertext Text (Binary):")
    ciphertext_binary_grouped = [format(bit, '03b') for bit in ciphertext]
    debug_results.append(" ".join(ciphertext_binary_grouped))
    
    return ciphertext

# Fungsi untuk dekripsi ciphertext
def rc4_simple_decrypt(ciphertext, key):
    S, T = initialize_state(key)
    
    permutation(S, T)
    
    key_stream = generate_key_stream(S, ciphertext, is_encryption=False) 
    
    # Menghitung plaintext sebagai XOR antara ciphertext dan key_stream
    plaintext = [c ^ k for c, k in zip(ciphertext, key_stream)]
    
    # Debug: Menambahkan hasil debug dekripsi dalam format desimal dan 4 kelompok biner 3 bit
    debug_results.append("\nDecryption:")
    
    debug_results.append("Ciphertext (Decimal):")
    debug_results.append(" ".join(map(str, ciphertext)))
    
    debug_results.append("Ciphertext (Binary):")
    ciphertext_binary_grouped = [format(bit, '03b') for bit in ciphertext]
    debug_results.append(" ".join(ciphertext_binary_grouped))
    
    debug_results.append("\nKey (Decimal):")
    debug_results.append(" ".join(map(str, key)))
    
    debug_results.append("Key (Binary):")
    key_binary_grouped = [format(bit, '03b') for bit in key]
    debug_results.append(" ".join(key_binary_grouped))
    
    debug_results.append("\nPlaintext Text (Decimal):")
    debug_results.append(" ".join(map(str, plaintext)))
    
    debug_results.append("Plaintext Text (Binary):")
    plaintext_binary_grouped = [format(bit, '03b') for bit in plaintext]
    debug_results.append(" ".join(plaintext_binary_grouped))
    
    return plaintext


def is_valid_input(input_str):
    # Memeriksa apakah input hanya mengandung angka 0-7
    return re.match("^[0-7]+$", input_str)

def encrypt_text():
    # Hapus hasil debug yang sudah ada sebelumnya
    debug_results.clear()
    
    plaintext_str = text_entry.get("1.0", "end-1c").replace(" ", "").strip()
    key_str = key_entry.get("1.0", "end-1c").strip()

    if not is_valid_input(plaintext_str) or not is_valid_input(key_str):
        messagebox.showerror("Error", "Masukkan angka dari 0 hingga 7 untuk plaintext dan kunci.")
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
    # Hapus hasil debug yang sudah ada sebelumnya
    debug_results.clear()
    
    ciphertext_str = text_entry.get("1.0", "end-1c").replace(" ", "").strip()
    key_str = key_entry.get("1.0", "end-1c").strip()

    if not is_valid_input(ciphertext_str) or not is_valid_input(key_str):
        messagebox.showerror("Error", "Masukkan angka dari 0 hingga 7 untuk ciphertext dan kunci.")
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

# Fungsi untuk reset teks
def reset_text():
    text_entry.delete("1.0", tk.END)
    key_entry.delete("1.0", tk.END)
    result_entry.config(state='normal')
    result_entry.delete("1.0", tk.END)
    result_entry.config(state='disabled')

# Initialize the debug_text_widget variable
debug_text_widget = None

# Variabel global untuk melacak apakah enkripsi atau dekripsi telah dilakukan
encryption_done = False

# Inisialisasi global variable
debug_option_enabled = False
    
def show_about_info():
    # Gunakan teks judul jendela dan versi aplikasi untuk mengatur teks keterangan
    root_title = root.title()
    email = "imamsyt22@mhs.usk.ac.id"  # Ganti dengan alamat email Anda
    about_info = f"{root_title}\nVersi {app_version}\n\nDikembangkan oleh [Bukan Makmum]\nEmail: {email}"
    result = messagebox.showinfo("About", about_info, icon=messagebox.INFO)
    if result:
        open_github()

def open_github(): 
    webbrowser.open("https://github.com/BukanMakmum/RivestCode4.git")  # Ganti dengan URL repositori GitHub Anda
    
# Fungsi untuk menempatkan jendela di tengah
def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

# Fungsi untuk keluar dari aplikasi
def exit_app():
    root.quit()

def open_email(event):
    webbrowser.open("mailto:imamsayuti.usk@gmail.com")

# Fungsi saat cursor masuk ke tombol
def on_enter(event):
    event.widget.config(bg=event.widget.highlight_color, fg='white')

# Fungsi saat cursor meninggalkan tombol
def on_leave(event):
    event.widget.config(bg=event.widget.original_color, fg='black')
    
# Fungsi untuk mengaktifkan atau menonaktifkan opsi "Debug Result"
def toggle_debug_option():
    global debug_option_enabled
    debug_option_enabled = not debug_option_enabled
    if debug_option_enabled:
        file_menu.entryconfig("Debug Result", state=tk.NORMAL)
    else:
        file_menu.entryconfig("Debug Result", state=tk.DISABLED)

# Function to open the debug window
def open_debug_result(debug_text):
    global debug_window, debug_text_widget  # Menetapkan variabel global
    debug_window = None  # Inisialisasi variabel debug_window

    if debug_window is not None:
        # Jika jendela debug sudah ada, tutup terlebih dahulu
        debug_window.destroy()

    debug_window = tk.Toplevel(root)
    debug_window.title("Debug Result")  # 

    # Atur ukuran jendela debug (misalnya, 1000x600 piksel)
    debug_window.geometry("600x300")

    # Mendapatkan ukuran layar
    screen_width = debug_window.winfo_screenwidth()
    screen_height = debug_window.winfo_screenheight()

    # Menghitung posisi x dan y untuk memusatkan jendela
    x = (screen_width - 600) // 2
    y = (screen_height - 300) // 2

    # Menetapkan posisi jendela di tengah
    debug_window.geometry(f"600x300+{x}+{y}")

    # Create a scrolled text widget in the debug window
    debug_text_widget = scrolledtext.ScrolledText(debug_window, wrap=tk.WORD)
    debug_text_widget.pack(fill=tk.BOTH, expand=True)  # Mengisi dan memperluas widget ke seluruh jendela

    # Show the debug text in the scrolled text widget
    debug_text_widget.insert(tk.END, debug_text)

    # Create a menu bar for the debug window
    menubar = Menu(debug_window)
    debug_window.config(menu=menubar)

    # Create a "File" menu in the debug window
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    # Add a "Save" option to the "File" menu
    file_menu.add_command(label="Save", command=save_debug_text)

    # Add an "Exit" option to the "File" menu that closes the debug window
    file_menu.add_command(label="Exit", command=debug_window.destroy)

# Function to close the debug window
def close_debug_window():
    global debug_text_widget
    if debug_text_widget is not None:
        debug_text_widget.destroy()

# Function to save debug text to a file
def save_debug_text():
    global debug_text_widget
    if debug_text_widget is not None:
        debug_text = debug_text_widget.get("1.0", tk.END)

        # Replace ⊕ with ^ or + or other suitable symbol
        debug_text = debug_text.replace("⊕", "^")  # You can replace with a different symbol if needed

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if file_path:
            with open(file_path, "w") as file:
                file.write(debug_text)

# Fungsi untuk menggabungkan hasil debug dari berbagai bagian fungsi enkripsi
def handle_debug_result():
    global debug_results  # Tambahkan variabel global

    key = key_entry.get("1.0", "end-1c")  # Mengambil kunci dari input teks
    if not key:
        messagebox.showerror("Error", "Jalankan Enkripsi atau Dekripsi sebelum mengklik Debug Result.")
        return  # Keluar dari fungsi jika kunci kosong

    # Membuat teks hasil debug
    debug_result = []
    debug_result.append("Hasil Debug:")

    # Tambahkan hasil debug dari berbagai bagian fungsi enkripsi ke dalam daftar debug_result
    for debug_text in debug_results:
        debug_result.append(str(debug_text))  # Ubah hasil debug menjadi string dan tambahkan ke hasil debug

    # Menggabungkan hasil debug menjadi satu string
    debug_text = "\n".join(debug_result)

    # Menampilkan hasil debug di jendela debug
    open_debug_result(debug_text)


# Membuat GUI
root = tk.Tk()
root.title("Rivest Code 4")
app_version = "Education 2.0"

# Tentukan ukuran jendela
window_width = 335
window_height = 245
root.geometry(f"{window_width}x{window_height}")
root.configure(bg="#87CEFA")  # Mengatur warna latar belakang jendela utama

# Mencegah pengguna untuk mengubah ukuran jendela
root.resizable(False, False)

# Dapatkan direktori tempat script ini berada
current_directory = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'

# Gabungkan direktori saat ini dengan nama file ikon favicon
favicon_path = os.path.join(current_directory, "favicon.ico")

# Atur favicon
root.iconbitmap(default=favicon_path)

style = ThemedStyle(root)
style.set_theme("adapta")

# Membuat objek menu utama
menubar = tk.Menu(root)
root.config(menu=menubar)

# Membuat menu "File" tanpa garis putus-putus
file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)

# Menambahkan opsi "Debug Result" di menu "File" dan menonaktifkannya saat pertama kali dibuat
file_menu.add_command(label="Debug Result", command=handle_debug_result, state=tk.DISABLED)

# Menambahkan opsi "Exit" di menu "File" tanpa garis pemisah
file_menu.add_command(label="Exit", command=exit_app)

# Menambahkan opsi "About" di menu utama
menubar.add_command(label="About", command=show_about_info)

judul_jendela = root.title()

# Label judul dengan font yang lebih besar
title_label = ttk.Label(root, text=judul_jendela, font=("Helvetica", 14, "bold"), background=root.cget('bg'))
title_label.grid(row=0, column=1, padx=10, pady=10)

# Label versi dengan font yang lebih kecil
version_label = ttk.Label(root, text=f"Versi {app_version}", font=("Helvetica", 10), background=root.cget('bg'))
version_label.grid(row=1, column=1, padx=10, pady=2)

# Agar label versi berada di bawah label judul
title_label.grid(pady=(20, 0))

# Label untuk input teks
text_label = ttk.Label(root, text="Text (4 digits):", foreground="black", background=root.cget('bg'))
text_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

# Text widget untuk input teks
text_entry = tk.Text(root, height=1, width=20)
text_entry.grid(row=2, column=1, padx=5, pady=5)

# Label untuk input kunci
key_label = ttk.Label(root, text="Key (4 digits):", foreground="black", background=root.cget('bg'))
key_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

# Text widget untuk input kunci
key_entry = tk.Text(root, height=1, width=20)
key_entry.grid(row=3, column=1, padx=5, pady=5)

reset_button = tk.Button(root, text="Reset", width=6, command=reset_text)
reset_button.grid(row=4, column=0, padx=(10, 5), pady=10, sticky="")
# Menetapkan warna latar belakang saat disorot dan warna latar belakang asli
reset_button.highlight_color = 'red'  # Warna latar belakang saat disorot
reset_button.original_color = 'SystemButtonFace'  # Warna latar belakang asli
reset_button.bind("<Enter>", on_enter)
reset_button.bind("<Leave>", on_leave)

decrypt_button = tk.Button(root, text="Decrypt", width=6, command=decrypt_text)
decrypt_button.grid(row=4, column=1, padx=5, pady=10, sticky="")
# Menetapkan warna latar belakang saat disorot dan warna latar belakang asli
decrypt_button.highlight_color = 'green'  # Warna latar belakang saat disorot
decrypt_button.original_color = 'SystemButtonFace'  # Warna latar belakang asli
decrypt_button.bind("<Enter>", on_enter)
decrypt_button.bind("<Leave>", on_leave)

encrypt_button = tk.Button(root, text="Encrypt", width=6, command=encrypt_text)
encrypt_button.grid(row=4, column=2, padx=5, pady=10, sticky="")
# Menetapkan warna latar belakang saat disorot dan warna latar belakang asli
encrypt_button.highlight_color = 'blue'  # Warna latar belakang saat disorot
encrypt_button.original_color = 'SystemButtonFace'  # Warna latar belakang asli
encrypt_button.bind("<Enter>", on_enter)
encrypt_button.bind("<Leave>", on_leave)

# Hasil/Output
result_label = ttk.Label(root, text="Result:", foreground="black", background=root.cget('bg'))
result_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

# Text widget untuk hasil
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
# Menghubungkan fungsi dengan klik pada teks hak cipta
copyright_label.bind("<Button-1>", open_email)

# Setelah enkripsi selesai, aktifkan opsi "Debug Result"
toggle_debug_option()

# Panggil fungsi untuk menempatkan jendela di tengah
center_window(root)

root.mainloop()
