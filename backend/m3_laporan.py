# --- BAGIAN 1: ALGORITMA PENGURUTAN (SORT) ---

def insertion_sort(arr, kunci):
    """
    Mengurutkan array menggunakan Insertion Sort (Stabil, O(n^2)).
    Mengembalikan tuple: (array_terurut, jumlah_perbandingan, jumlah_pemindahan)
    """
    # Salin array agar tidak mengubah data asli secara implisit
    data = [item for item in arr]
    n = len(data)
    perbandingan = 0
    pemindahan = 0

    for i in range(1, n):
        key_item = data[i]
        key_val = key_item[kunci]
        j = i - 1

        while j >= 0:
            perbandingan += 1
            # Menggunakan '>' (bukan '>=') agar pengurutan bersifat stabil
            if data[j][kunci] > key_val:
                data[j + 1] = data[j]
                pemindahan += 1
                j -= 1
            else:
                break
        data[j + 1] = key_item
        pemindahan += 1

    return data, perbandingan, pemindahan


def merge_sort(arr, kunci):
    """
    Mengurutkan array menggunakan Merge Sort (Stabil, O(n log n)).
    Mengembalikan tuple: (array_terurut, jumlah_perbandingan, jumlah_pemindahan)
    """
    data = [item for item in arr]
    perbandingan = [0]  # Menggunakan list mutable untuk penghitung rekursif
    pemindahan = [0]

    def _merge(left, right):
        result = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            perbandingan[0] += 1
            # Pakai '<=' agar stabil: jika nilai kunci sama, elemen kiri didahulukan
            if left[i][kunci] <= right[j][kunci]:
                result.append(left[i])
                pemindahan[0] += 1
                i += 1
            else:
                result.append(right[j])
                pemindahan[0] += 1
                j += 1

        while i < len(left):
            result.append(left[i])
            pemindahan[0] += 1
            i += 1
        while j < len(right):
            result.append(right[j])
            pemindahan[0] += 1
            j += 1

        return result

    def _merge_sort_recursive(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr
        mid = len(sub_arr) // 2
        left = _merge_sort_recursive(sub_arr[:mid])
        right = _merge_sort_recursive(sub_arr[mid:])
        return _merge(left, right)

    data_terurut = _merge_sort_recursive(data)
    return data_terurut, perbandingan[0], pemindahan[0]


# --- BAGIAN 2: ALGORITMA PENCARIAN (SEARCH) ---

def linear_search(arr, target_oid):
    """
    Mencari pesanan berdasarkan OID menggunakan Linear Search (O(n)).
    Data tidak harus terurut.
    Mengembalikan tuple: (indeks_ditemukan, data_item, jumlah_perbandingan)
    """
    perbandingan = 0
    for i in range(len(arr)):
        perbandingan += 1
        if arr[i]['oid'] == target_oid:
            return i, arr[i], perbandingan
    return -1, None, perbandingan


def binary_search(arr_terurut_oid, target_oid):
    """
    Mencari pesanan berdasarkan OID menggunakan Binary Search (O(log n)).
    Syarat wajib: array HARUS sudah terurut berdasarkan 'oid'!
    Mengembalikan tuple: (indeks_ditemukan, data_item, jumlah_perbandingan)
    """
    lo = 0
    hi = len(arr_terurut_oid) - 1
    perbandingan = 0

    while lo <= hi:  # Syarat <= bukan <
        perbandingan += 1
        mid = (lo + hi) // 2
        mid_oid = arr_terurut_oid[mid]['oid']

        if mid_oid == target_oid:
            return mid, arr_terurut_oid[mid], perbandingan
        elif mid_oid < target_oid:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, None, perbandingan