# Rivest Code 4 12 bit
Implementasi sederhana algoritma Rivest Code4 (RC4) menggunakan Python dan pustaka Tkinter untuk antarmuka pengguna grafis. Rivest Code4 (RC4) versi Education merupakan skrip yang dikembangkan untuk pembelajaran proses enkripsi dan dekripsi menggunakan RC4.


## Daftar Isi

- [Pendahuluan](#pendahuluan)
- [Fitur](#fitur)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Tangkapan Layar](#tangkapan-layar)
- [Lisensi](#lisensi)
- [Kontak](#kontak)

## Pendahuluan

Algoritma RC4 (Rivest Cipher 4) adalah algoritma stream cipher, yang berarti algoritma ini mengenkripsi data bit per bit atau byte per byte secara berurutan. RC4 berbeda dari algoritma block cipher seperti AES, yang mengenkripsi data dalam blok berukuran tetap. RC4 menggunakan kunci simetris, yang sama seperti DES dan AES. Kunci yang digunakan untuk enkripsi data harus sama dengan kunci yang digunakan untuk dekripsi data.
Salah satu keunggulan RC4 adalah fleksibilitas dalam panjang kunci. RC4 dapat digunakan dengan panjang kunci yang dapat bervariasi dari 1 hingga 2.048 byte. Kunci yang lebih panjang cenderung lebih kuat dalam melindungi data. Sebelum mengenkripsi atau mendekripsi data, algoritma RC4 memerlukan inisialisasi dengan sebuah kunci. Selama inisialisasi, kunci tersebut digunakan untuk menghasilkan keystream (deretan byte acak) yang akan digunakan untuk mengenkripsi atau mendekripsi data.
RC4 memiliki proses yang disebut keystream generator. Generator ini menghasilkan byte-byte acak yang digunakan untuk melakukan operasi XOR dengan data yang akan dienkripsi atau didekripsi. Operasi XOR ini menghasilkan ciphertext (data terenkripsi) saat mengenkripsi dan mengembalikan data ke plaintext saat mendekripsi.
Penting untuk dicatat bahwa karena masalah keamanan yang signifikan yang ditemukan dalam RC4, algoritma ini tidak lagi disarankan untuk digunakan dalam aplikasi keamanan modern. Sebagai gantinya, algoritma enkripsi yang lebih kuat seperti AES sekarang lebih disukai dan dianjurkan.

## Fitur

- Enkripsi dan Dekripsi menggunakan RC4 12 bit;
- Input berupa  4 digit Desimal antara 0 - 7 (12 bit);
- Output berupa  4 digit Desimal antara 0 - 7 (12 bit);
- Validasi input key dan plaintext/ciphertext;
- Menampilkan dan simpan hasil Debug Result Enkripsi dan Dekripsi (Khusus v2.0.beta setelahnya)
- Reset input; dan
- Tampilan modern menggunakan tkinter/antarmuka grafis yang ramah pengguna.
  
- Contoh Input dan Output
  ```bash
  Plaintext:   1222
  Key:         1236
  Ciphertext:  4323

  Plaintext:   7654
  Key:         1234
  Ciphertext:  2237
   ```

## Instalasi

1. Clone repositori ini:

   ```bash
   git clone https://github.com/BukanMakmum/RivestCode4.git
   ```

2. Masuk ke direktori proyek:

   ```bash
   cd RivestCode4
   ```

3. Instal pustaka yang diperlukan:

   ```bash
   pip install tk
   pip install ttkthemes

   ```

## Penggunaan

1. Jalankan aplikasinya:

   ```bash
   RC4vx.x.py atau RC4vx.x.exe
   x.x = nomor versi
   ```

2. Masukkan 4 digit Desimal antara 0 - 7 (12 bit) Plaintext/Ciphertext dan kunci.

3. Klik tombol "Enkripsi" atau "Dekripsi" sesuai kebutuhan.

4. Hasil akan ditampilkan di bidang "Hasil/Output".

## Tangkapan Layar

![RC4](https://github.com/BukanMakmum/RivestCode4/assets/32379649/3e906c0d-70c7-41cc-aa4e-2646fd45f029)

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat berkas [LICENSE](LICENSE) untuk detailnya.

## Kontak

Untuk pertanyaan atau umpan balik, silakan hubungi pengembang:
- Nama: [Bukan Makmum]
- Email: [imamsyt22@mhs.usk.ac.id]

© 2023 BukanMakmum.
