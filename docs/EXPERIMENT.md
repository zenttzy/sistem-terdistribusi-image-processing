# Panduan Eksperimen

## Tujuan

Eksperimen membandingkan waktu, throughput, speedup, dan efficiency antara
pemrosesan sequential dan distributed.

## Dataset

Gunakan dataset yang sama untuk semua skenario. Contoh dataset sintetis:

```bash
python scripts/generate_dataset.py --count 100 --width 1920 --height 1080
```

Untuk hasil yang lebih representatif, lakukan pengujian pada 100, 500, dan
1.000 gambar. Perhatikan kapasitas disk server sebelum membuat dataset besar.

## Skenario

1. Sequential dengan satu proses.
2. Distributed dengan satu worker.
3. Distributed dengan dua worker.
4. Distributed dengan tiga worker jika resource mencukupi.
5. Fault test dengan menghentikan salah satu worker ketika task berjalan.

Setiap skenario sebaiknya diulang minimal tiga kali. Gunakan nilai rata-rata
untuk mengurangi pengaruh proses latar belakang dan cache sistem.

## Perintah

Baseline:

```bash
python -m app.cli --mode sequential --workers 1
```

Distributed:

```bash
python -m app.cli --mode distributed --workers 2
```

## Metrik

### Waktu Eksekusi

Waktu dari sebelum pekerjaan dimulai sampai seluruh hasil diterima master.

### Throughput

```text
throughput = jumlah gambar berhasil / waktu eksekusi
```

### Speedup

```text
speedup = waktu sequential / waktu parallel
```

### Efficiency

```text
efficiency = speedup / jumlah worker x 100%
```

## Tabel Hasil

| Dataset | Mode | Worker | Waktu (s) | Throughput | Speedup | Efficiency |
|---:|---|---:|---:|---:|---:|---:|
| 100 | Sequential | 1 | isi hasil | isi hasil | 1,00 | 100% |
| 100 | Distributed | 1 | isi hasil | isi hasil | hitung | hitung |
| 100 | Distributed | 2 | isi hasil | isi hasil | hitung | hitung |

## Interpretasi

Mode distributed dapat lebih lambat untuk dataset kecil karena serialisasi,
komunikasi Redis, penjadwalan task, dan pengambilan hasil. Speedup biasanya baru
terlihat ketika beban komputasi lebih besar daripada overhead distribusi.

Pada single node, jumlah worker yang melebihi jumlah CPU dapat menurunkan
efisiensi akibat context switching dan perebutan resource. Temuan tersebut
merupakan hasil eksperimen yang valid dan perlu dijelaskan dalam laporan.

