<div align="center">

# 🎬 LAYAR
### Temukan film berikutnya. Nikmati cerita yang berbeda.

Ruang kecil untuk menjelajahi film trending, menyaring genre, dan menemukan
rekomendasi yang terasa dekat dengan seleramu — semua dalam satu aplikasi Streamlit.

[English](README.md) · **Bahasa Indonesia** &nbsp;•&nbsp; **TMDB Trending** &nbsp;•&nbsp; **Rekomendasi berbasis genre**

</div>

---

> Dibangun dengan **Vibe Coding**: proses pengembangan berbantuan AI yang diarahkan, ditinjau, dan disempurnakan oleh manusia.

## ✨ Tentang Layar

Layar mengambil katalog film yang sedang trending dari **The Movie Database (TMDB)**,
kemudian membantu kamu:

- Menjelajahi pilihan film mingguan lengkap dengan poster, sinopsis, dan rating.
- Menyaring film berdasarkan genre dan mengurutkan berdasarkan popularitas, rating, atau tanggal rilis.
- Mendapatkan rekomendasi film serupa menggunakan kemiripan genre **TF-IDF** dan **cosine similarity**.
- Melihat perbandingan popularitas lewat grafik interaktif.
- Mengganti bahasa aplikasi sekaligus bahasa katalog TMDB ke **English** atau **Indonesia**.

> Data film dan gambar disediakan oleh [TMDB](https://www.themoviedb.org/).
> Layar adalah proyek independen dan tidak berafiliasi dengan TMDB.

## 🎨 Tampilan aplikasi

Antarmuka menggunakan tema gelap dengan aksen ungu dan mint, kartu poster, filter di sidebar,
serta grafik popularitas yang interaktif.

## 🚀 Mulai dalam beberapa menit

### 1. Siapkan prasyarat

- Windows 10/11
- Python **3.10 atau lebih baru**
- API key TMDB yang aktif

Buat atau kelola API key melalui [pengaturan akun TMDB](https://www.themoviedb.org/settings/api).

### 2. Siapkan project

Jika project sudah tersedia di komputer, buka PowerShell pada folder project. Untuk clone
repository, gunakan URL yang disediakan tim:

```powershell
git clone <URL-REPOSITORY>
cd <NAMA-FOLDER>
```

### 3. Buat dan aktifkan virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Pastikan prompt PowerShell menunjukkan `(.venv)`. Jika Windows memblokir eksekusi script,
izinkan aktivasi untuk sesi PowerShell saat ini:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Kamu juga bisa menjalankan perintah tanpa mengaktifkan environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### 4. Pasang dependency

Dengan `.venv` aktif:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Atur API key

Buat file `.env` lokal dari template, kemudian masukkan API key milikmu:

```powershell
Copy-Item .env.example .env
notepad .env
```

Isi file `.env`:

```dotenv
TMDB_API_KEY=masukkan_api_key_tmdb_di_sini
```

**Jangan commit atau membagikan `.env`**. File ini dikecualikan oleh `.gitignore`. Jika API key
pernah terungkap secara publik, cabut key tersebut dan buat yang baru melalui TMDB.

### 6. Jalankan aplikasi

```powershell
python -m streamlit run app.py
```

Buka alamat lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`. Bahasa default
aplikasi adalah **English**; gunakan pilihan bahasa di sidebar untuk beralih ke **Indonesia**.

## 🧭 Struktur project

```text
.
├── app.py                         # Antarmuka Streamlit, bahasa, filter, dan grafik
├── src/
│   ├── __init__.py
│   └── catalog.py                 # Akses TMDB dan rekomendasi genre
├── .streamlit/
│   └── config.toml                # Tema dan konfigurasi Streamlit
├── .env.example                   # Template konfigurasi lokal (tanpa API key aktif)
├── .gitignore                     # Mengecualikan .env, .venv, dan cache
├── requirements.txt               # Dependency aplikasi
├── README.md                      # Panduan developer berbahasa Inggris (default)
├── README.id.md                   # Panduan developer berbahasa Indonesia
└── LXS-Simple-System-Recomendations-TMDB.ipynb
                                  # Notebook eksplorasi awal
```

Jangan menambahkan `.venv/`, `.env`, `__pycache__/`, atau secret lokal ke repository.

## ⚙️ Cara kerja

1. Aplikasi membaca `TMDB_API_KEY` dari environment atau `.env`.
2. `src/catalog.py` mengambil genre dan daftar film trending mingguan dari TMDB.
3. Respons dinormalisasi, lalu di-cache Streamlit selama satu jam.
4. Daftar genre diubah menjadi fitur TF-IDF dan dibandingkan menggunakan cosine similarity.
5. `app.py` menampilkan katalog, rekomendasi, filter, dan grafik sesuai bahasa pilihan.

Pilihan bahasa juga mengatur bahasa respons TMDB: `en-US` untuk English dan `id-ID` untuk
Indonesia. Cache katalog dipisahkan berdasarkan API key dan bahasa. Gunakan **Rerun** di Streamlit
untuk memperbarui data sebelum cache kedaluwarsa.

## 👩‍💻 Berkontribusi

### Lokasi perubahan

| Ingin mengubah... | Mulai dari |
| --- | --- |
| Tampilan halaman, bahasa, filter, atau grafik | `app.py` |
| Endpoint TMDB, data film, atau cache katalog | `src/catalog.py` |
| Skor rekomendasi | `get_recommendations()` di `src/catalog.py` |
| Warna tema global | `.streamlit/config.toml` dan CSS di `app.py` |
| Dependency project | `requirements.txt` |

### Menambahkan dependency

Tambahkan library baru dengan batasan versi yang sesuai ke `requirements.txt`, lalu pasang di
environment aktif:

```powershell
python -m pip install -r requirements.txt
```

Jangan mengandalkan paket yang hanya terpasang di komputer sendiri. Developer lain harus bisa
membuat ulang environment dari manifest.

### Validasi perubahan

Jalankan pemeriksaan sintaks dan dependency:

```powershell
python -m compileall app.py src
python -m pip check
```

Jalankan aplikasi dan pastikan:

1. Halaman terbuka tanpa exception.
2. English dan Indonesia berfungsi, termasuk teks header utama.
3. Filter genre dan setiap opsi pengurutan bekerja sesuai harapan.
4. Film yang dipilih tidak muncul sebagai rekomendasi.
5. Data kosong dan error API dijelaskan dengan jelas.

Sebelum membuka pull request, jelaskan perubahan dan cara mengujinya, perbarui manifest dependency
jika diperlukan, serta pastikan `.env` dan secret lain tidak ikut di-stage.

## ♻️ Membuat ulang environment

Jika virtual environment rusak atau perlu instalasi ulang, buat kembali `.venv` dan pulihkan
dependency dari manifest:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Perintah `Remove-Item` di atas hanya menargetkan folder `.venv` milik project ini. File project dan
`.env` lokal tidak ikut dihapus.

## 🩺 Pemecahan masalah

| Masalah | Yang perlu diperiksa |
| --- | --- |
| API key tidak ditemukan | Pastikan `.env` berada di root project dan berisi `TMDB_API_KEY=...`. |
| TMDB menolak permintaan | Periksa API key, koneksi internet, dan akun TMDB. |
| Poster tidak tampil | Sebagian film tidak memiliki poster; periksa juga koneksi internet. |
| Paket tidak dapat di-import | Aktifkan `.venv` yang benar, lalu jalankan `python -m pip install -r requirements.txt`. |
| Streamlit tidak ditemukan | Pasang dependency, lalu jalankan `python -m streamlit run app.py`. |
| Katalog atau genre tampak tidak berubah | Cache berlangsung hingga satu jam; gunakan **Rerun** atau mulai ulang aplikasi. |

## 📄 Lisensi dan atribusi

Periksa ketentuan dan persyaratan lisensi TMDB sebelum mendistribusikan aplikasi ini. Poster,
metadata, dan detail film disediakan oleh TMDB; project ini tidak menyimpan atau mengklaim
kepemilikan atas konten tersebut.

---

<div align="center">

Dibuat untuk malam film yang lebih seru. 🍿

</div>
