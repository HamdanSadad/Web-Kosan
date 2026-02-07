# Proyek Kosan - Panduan Troubleshooting & Setup

Panduan ini mendokumentasikan masalah umum yang ditemui selama pengaturan dan cara mengatasinya.

## Masalah Umum & Solusi

### 1. Error Kebijakan Eksekusi (Powershell Execution Policy)

**Masalah:**
Saat mencoba mengaktifkan virtual environment (`.\venv\Scripts\Activate.ps1`), Anda mendapatkan error:
`File ...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`

**Solusi:**
Anda dapat melewati (bypass) kebijakan eksekusi untuk sesi terminal saat ini dengan menjalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```
Setelah menjalankan perintah ini, Anda akan dapat menjalankan `.\venv\Scripts\Activate.ps1`.

---

### 2. ModuleNotFoundError: No module named 'flask'

**Masalah:**
Menjalankan aplikasi (`python run.py`) gagal meskipun `venv` sudah ada, karena dependensi seperti `flask` belum terinstal di dalamnya.

**Solusi:**
Instal paket-paket yang diperlukan menggunakan versi pip di dalam virtual environment Anda:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Cara Menjalankan Aplikasi

Jika Anda tidak ingin mengaktifkan virtual environment, Anda dapat menjalankan aplikasi secara langsung menggunakan executable `venv`:

```powershell
.\venv\Scripts\python.exe run.py
```

Atau, jika venv sudah diaktifkan:
```powershell
python run.py
```

Aplikasi akan dapat diakses di `http://127.0.0.1:5000`.
