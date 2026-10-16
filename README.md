# Layar — rekomendasi film TMDB

Aplikasi Streamlit untuk menjelajahi film trending TMDB, menyaring berdasarkan genre, dan menemukan film dengan genre serupa.

## Menjalankan di Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Isi `TMDB_API_KEY` pada `.env` sebelum menjalankan aplikasi. Salin `.env.example` menjadi `.env` dan masukkan API key TMDB milik Anda jika belum memiliki file `.env`. Jangan membagikan atau mengunggah `.env`.

Katalog TMDB disimpan di cache selama satu jam. Gunakan tombol rerun Streamlit untuk memuat ulang tampilan.
