# 🔒 S-Box Analysis Tools

S-Box Analysis Tools adalah aplikasi berbasis Python yang menggunakan **Streamlit** untuk menganalisis properti keamanan matriks S-Box dalam kriptografi. Alat ini menghitung berbagai metrik yang penting untuk menilai kekuatan dan efektivitas S-Box terhadap serangan kriptografi.

## 📂 Struktur Direktori

```
📦 S-Box Analysis Tools
├── __pycache__/           # Folder cache Python yang dibuat otomatis
├── app.py                 # File utama aplikasi Streamlit
├── hitung.py              # Modul berisi fungsi untuk analisis S-Box
├── sbox.xlsx              # Contoh file Excel berisi matriks S-Box
├── requirements.txt       # Dependensi Project
```

### Penjelasan File
1. **`app.py`**  
   Merupakan file utama untuk menjalankan aplikasi Streamlit. File ini memuat logika untuk memproses file Excel, menghitung metrik, menampilkan hasil analisis, dan memberikan opsi ekspor hasil ke file Excel.

2. **`hitung.py`**  
   Berisi fungsi-fungsi utama untuk menghitung metrik-metrik keamanan, seperti:
   - Nonlinearity (NL)
   - Strict Avalanche Criterion (SAC)
   - Bit Independence Criterion Nonlinearity (BIC-NL) 
   - Bit Independence Criterion Strict Avalanche Criterion (BIC-SAC) 
   - Linear Approximation Probability (LAP)
   - Differential Approximation Probability (DAP)

3. **`sbox.xlsx`**  
   Contoh file Excel berisi matriks S-Box persegi yang dapat digunakan sebagai input untuk aplikasi.

4. **`__pycache__/`**  
   Folder otomatis yang berisi *cache* Python untuk mempercepat eksekusi kode. Tidak perlu dimodifikasi.

## ⚙️ Cara Menggunakan
1. Pastikan Python dan **Streamlit** telah terinstal di sistem Anda.
2. Letakkan file matriks S-Box (format `.xlsx`) di direktori proyek.
3. Jalankan aplikasi dengan perintah berikut:
   ```bash
   streamlit run app.py
   ```
4. Upload file Excel berisi matriks S-Box melalui antarmuka Streamlit.
5. Pilih metrik yang ingin dianalisis pada sidebar dan lihat hasilnya.
6. Ekspor hasil analisis ke file Excel jika diperlukan.

## 🔧 Instalasi
1. Clone repositori ini:
   ```bash
   git clone <repository_url>
   cd sbox-analysis-tools
   ```
2. Install dependensi Python:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi sesuai langkah di atas.

## 🚀 Fitur
- Analisis keamanan S-Box dengan metrik NL, SAC, LAP, DAP, BIC-SAC, atau BIC-NL.
- Antarmuka pengguna interaktif menggunakan **Streamlit**.
- Ekspor hasil analisis ke file Excel.
