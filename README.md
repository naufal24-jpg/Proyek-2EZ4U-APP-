# Proyek "2EZ4U APP"
**Studi Kasus Proyek Akhir — Struktur Data & Analisa Algoritma (EC234303)**  
**Cakupan**: Milestone 1 (M1) – Milestone 3 (M3)

---

## 1. Deskripsi Proyek
Proyek **2EZ4U APP** adalah pengembangan engine backend layanan pengiriman barang/makanan (*food delivery*) berskala besar berbasis Python. Aplikasi ini memproses data transaksi hingga **200.000 baris** (`data/pesanan.csv`) dengan menerapkan struktur data dan algoritma buatan sendiri tanpa memanfaatkan *library* atau fungsi bawaan seperti `dict`, `set`, `sorted()`, `.sort()`, `collections.*`, atau `heapq`.

---

## 2. Ringkasan Dataset (`data/pesanan.csv`)
Berdasarkan analisis langsung pada berkas `pesanan.csv`:
- **Total Baris Data**: 200.000 baris
- **Distribusi Status Pesanan**:
  - `DONE`: 163.993 pesanan (Selesai)
  - `ANTRE`: 19.850 pesanan (Dalam antrean)
  - `CANCEL`: 16.157 pesanan (Dibatalkan)
- **Distribusi Prioritas Layanan**:
  - Prioritas 1 (VIP): 20.119 pesanan
  - Prioritas 2 (Prioritas): 120.000 pesanan
  - Prioritas 3 (Reguler): 59.881 pesanan

---

## 3. Analisis & Laporan Fitur (M1 – M3)

### 🔹 Milestone 1 (M1): Array vs Linked List (`backend/m1_pesanan.py`)
M1 membandingkan performa dua struktur data dasar linier untuk mengelola data pesanan dengan 3 aturan penyisipan bisnis:
1. **REGULER**: Masuk di barisan paling belakang.
2. **PRIORITAS**: Menyerobot ke tengah barisan.
3. **VIP**: Langsung ditempatkan pada urutan pertama (paling depan).

| Operasi / Fitur | Custom Array | Custom Linked List | Keterangan Teknis |
| :--- | :--- | :--- | :--- |
| **Akses Pesanan (`get`)** | $O(1)$ | $O(n)$ | Array langsung menghitung alamat memori indeks ke-i; Linked List harus menelusuri dari `head`. |
| **Tambah REGULER** | $O(1)$ *amortized* | $O(1)$ | Array melipatgandakan kapasitas jika penuh; Linked List menggunakan penunjuk `tail`. |
| **Tambah PRIORITAS** | $O(n)$ | $O(n)$ | Array menggeser elemen; Linked List menelusuri simpul untuk menyambung penunjuk. |
| **Tambah VIP** | $O(n)$ | $O(1)$ | Array menggeser semua elemen ke kanan; Linked List cukup mengubah penunjuk `head`. |
| **Hapus Pesanan** | $O(n)$ | $O(n)$ | Array menggeser sisa elemen ke kiri; Linked List membelokkan pointer simpul. |

---

### 🔹 Milestone 2 (M2): Stack & Queue (`backend/m2_antrean.py`)

#### 1. Mesin Kasir (Postfix Evaluator)
- Mengonversi ekspresi kalkulasi dari format *infix* ke *postfix* menggunakan **Stack Operator**, lalu dihitung nilainya menggunakan **Stack Operand**.
- **Pengujian Struk**: `(3 * 12000) + (2 * 8500) - 5000`
  - Hasil Konversi Postfix: `3 12000 * 2 8500 * + 5000 -`
  - Total Kalkulasi: **Rp 48.000**

#### 2. Antrean (Queue Naif vs Queue Circular)
- **Queue Naif**: Mengambil elemen terdepan dengan menggeser sisa elemen ke kiri ($O(n)$). Saat melayani 19.850 data `ANTRE`, satu kali `dequeue` memicu 19.849 pergeseran elemen memori (~0,08 ms).
- **Queue Circular**: Memanfaatkan variabel modulo `(front + 1) % capacity` ($O(1)$). Memajukan penunjuk `front` tanpa menggeser elemen array sama sekali (~0,01 ms).

#### 3. Sistem Undo & Redo
- Menggunakan dua tumpukan: `undo_stack` dan `redo_stack`.
- Pembatalan `DEQUEUE` mengembalikan data terhapus secara presisi ke **depan** antrean circular.
- Setiap aksi baru (`enqueue` / `dequeue`) akan otomatis mengosongkan `redo_stack`.

---

### 🔹 Milestone 3 (M3): Sort & Search (`backend/m3_laporan.py`)

#### 1. Algoritma Pengurutan (Sorting)
Pengurutan dilakukan pada kunci `harga` dengan sifat **stabil** (mempertahankan urutan asli untuk data bernilai sama):

| Sampel Data ($N$) | Insertion Sort ($O(n^2)$) | Merge Sort ($O(n \log n)$) |
| :--- | :--- | :--- |
| **1.000 Baris** | **122,31 ms** (233.802 perbandingan) | **12,67 ms** (8.650 perbandingan) |
| **2.000 Baris** | **530,77 ms** (962.430 perbandingan) | **26,65 ms** (19.240 perbandingan) |
| **4.000 Baris** | **2.303,77 ms** (3.831.520 perbandingan) | **53,34 ms** (42.355 perbandingan) |

> **Analisis**: Saat $N$ dilipatgandakan, perbandingan dan waktu pada Insertion Sort meningkat $\approx 4\times$ (kuadratik), sedangkan Merge Sort hanya meningkat $\approx 2\times$ ($n \log n$).

#### 2. Algoritma Pencarian (Searching)
Mencari target `oid` = `O-199999` pada total 200.000 data pesanan:
- **Linear Search ($O(n)$)**: **183,64 ms** dengan **199.999 perbandingan**. Bekerja tanpa syarat data terurut.
- **Binary Search ($O(\log n)$)**: **0,05 ms** dengan hanya **17 perbandingan**. Menuntut data diurutkan terlebih dahulu (*merge sort* awal membutuhkan waktu ~3,1 detik).

---

## 4. Struktur Repositori
```text
2ez4u/
├── README.md             <- Laporan Resmi Proyek
├── data/
│   ├── pesanan.csv       <- Dataset 200.000 baris
│   └── peta.csv          <- Data peta/lokasi
├── backend/
│   ├── m1_pesanan.py     <- Custom Array & Linked List
│   ├── m2_antrean.py     <- Postfix Kasir, Circular Queue, Undo/Redo
│   └── m3_laporan.py     <- Insertion/Merge Sort & Linear/Binary Search
└── frontend/
    └── app.py            <- Antarmuka utama berbasis Tkinter