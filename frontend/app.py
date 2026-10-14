import sys
import os
import csv
import time
import tkinter as tk
from tkinter import ttk, messagebox

# Tambahkan direktori utama ke sys.path agar modul backend bisa di-import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.m1_pesanan import CustomArray, CustomLinkedList
from backend.m2_antrean import ke_postfix, hitung_postfix, QueueNaif, QueueCircular, UndoRedoManager
from backend.m3_laporan import insertion_sort, merge_sort, linear_search, binary_search

class App2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U Food Delivery - Progress M1-M3")
        self.root.geometry("900x600")

        # Inisialisasi Struktur Data
        self.arr_pesanan = CustomArray()
        self.ll_pesanan = CustomLinkedList()
        self.q_naif = QueueNaif()
        self.q_circ = QueueCircular()
        self.undo_redo = UndoRedoManager(self.q_naif, self.q_circ)
        self.raw_data = []

        self._setup_ui()
        self.load_csv()

    def load_csv(self):
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pesanan.csv'))
        if not os.path.exists(csv_path):
            messagebox.showwarning("Peringatan", f"File {csv_path} tidak ditemukan!")
            return

        self.raw_data = []
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['harga'] = int(row['harga'])
                self.raw_data.append(row)
                self.arr_pesanan.tambah_reguler(row)
                self.ll_pesanan.tambah_reguler(row)
                if row['status'] == 'ANTRE' or row['status'] == '':
                    self.q_naif.enqueue(row)
                    self.q_circ.enqueue(row)

        self.log(f"Berhasil memuat {len(self.raw_data)} data dari CSV.")

    def _setup_ui(self):
        # Frame Kontrol (Kiri)
        frame_btn = ttk.Frame(self.root, padding=10)
        frame_btn.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(frame_btn, text="MENU AKSI", font=('Helvetica', 10, 'bold')).pack(pady=5)

        ttk.Button(frame_btn, text="M1: Lihat Total Array", command=self.test_m1).pack(fill=tk.X, pady=2)
        ttk.Button(frame_btn, text="M2: Hitung Kasir (Postfix)", command=self.test_m2_kasir).pack(fill=tk.X, pady=2)
        ttk.Button(frame_btn, text="M2: Test Dequeue Naif vs Circular", command=self.test_m2_queue).pack(fill=tk.X, pady=2)
        ttk.Button(frame_btn, text="M2: Undo Aksi", command=self.test_undo).pack(fill=tk.X, pady=2)
        ttk.Button(frame_btn, text="M2: Redo Aksi", command=self.test_redo).pack(fill=tk.X, pady=2)
        ttk.Button(frame_btn, text="M3: Demo Insertion vs Merge Sort", command=self.test_m3_sort).pack(fill=tk.X, pady=2)
        ttk.Button(frame_btn, text="M3: Demo Linear vs Binary Search", command=self.test_m3_search).pack(fill=tk.X, pady=2)

        # Frame Output/Log (Kanan)
        frame_out = ttk.Frame(self.root, padding=10)
        frame_out.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(frame_out, text="OUTPUT & LOG SYSTEM", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        self.txt_log = tk.Text(frame_out, wrap=tk.WORD)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def log(self, text):
        self.txt_log.insert(tk.END, text + "\n")
        self.txt_log.see(tk.END)

    def test_m1(self):
        self.log(f"\n--- [M1] DATA PESANAN ---")
        self.log(f"Total di Array: {self.arr_pesanan.size}")
        self.log(f"Total di Linked List: {self.ll_pesanan.size}")
        if self.arr_pesanan.size > 0:
            self.log(f"Elemen Pertama: {self.arr_pesanan.get(0)['oid']} - {self.arr_pesanan.get(0)['pelanggan']}")

    def test_m2_kasir(self):
        struk = "(3 * 12000) + (2 * 8500) - 5000"
        postfix = ke_postfix(struk)
        total = hitung_postfix(postfix)
        self.log(f"\n--- [M2] MESIN KASIR ---")
        self.log(f"Infix   : {struk}")
        self.log(f"Postfix : {' '.join(str(x) for x in postfix)}")
        self.log(f"Total   : Rp {total:,}")

    def test_m2_queue(self):
        self.log(f"\n--- [M2] PERBANDINGAN QUEUE ---")
        t0 = time.perf_counter()
        d_naif = self.q_naif.dequeue(1)
        t1 = time.perf_counter()

        t2 = time.perf_counter()
        d_circ = self.q_circ.dequeue(1)
        t3 = time.perf_counter()

        self.log(f"Dequeue Naif     : {(t1 - t0)*1000:.4f} ms (Total pergeseran: {self.q_naif.total_geseran})")
        self.log(f"Dequeue Circular : {(t3 - t2)*1000:.4f} ms (Geseran: 0)")
        if d_naif:
            self.undo_redo.catat_aksi('DEQUEUE', d_naif)

    def test_undo(self):
        aksi, msg = self.undo_redo.undo_last()
        self.log(f"\n--- [M2] UNDO ---")
        self.log(msg)

    def test_redo(self):
        aksi, msg = self.undo_redo.redo_last()
        self.log(f"\n--- [M2] REDO ---")
        self.log(msg)

    def test_m3_sort(self):
        self.log(f"\n--- [M3] PERBANDINGAN SORT (Kunci: harga) ---")
        data_sort = self.raw_data[:100]  # Ambil sampel 100 data

        # Insertion Sort
        t0 = time.perf_counter()
        res_ins, cmp_ins, mv_ins = insertion_sort(data_sort, 'harga')
        t1 = time.perf_counter()

        # Merge Sort
        t2 = time.perf_counter()
        res_mrg, cmp_mrg, mv_mrg = merge_sort(data_sort, 'harga')
        t3 = time.perf_counter()

        self.log(f"Insertion Sort : {(t1 - t0)*1000:.4f} ms | Perbandingan: {cmp_ins} | Pemindahan: {mv_ins}")
        self.log(f"Merge Sort     : {(t3 - t2)*1000:.4f} ms | Perbandingan: {cmp_mrg} | Pemindahan: {mv_mrg}")

    def test_m3_search(self):
        self.log(f"\n--- [M3] PERBANDINGAN SEARCH ---")
        target = "O-000004"

        # Linear Search
        t0 = time.perf_counter()
        idx_lin, item_lin, cmp_lin = linear_search(self.raw_data, target)
        t1 = time.perf_counter()

        # Binary Search (Siapkan data terurut OID dulu)
        data_terurut, _, _ = merge_sort(self.raw_data, 'oid')
        t2 = time.perf_counter()
        idx_bin, item_bin, cmp_bin = binary_search(data_terurut, target)
        t3 = time.perf_counter()

        self.log(f"Linear Search : {(t1 - t0)*1000:.4f} ms | Perbandingan: {cmp_lin}")
        self.log(f"Binary Search : {(t3 - t2)*1000:.4f} ms | Perbandingan: {cmp_bin}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App2EZ4U(root)
    root.mainloop()