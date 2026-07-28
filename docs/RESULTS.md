# Hasil Pengujian

Pengujian dilakukan pada Ubuntu 24.04.4 LTS dengan 2 CPU core, RAM 1,9 GiB,
dan swap 1,9 GiB. Dataset berisi 300 gambar berukuran 1920x1080.

| Mode | Worker | Waktu (detik) | Throughput | Speedup | Efficiency |
|---|---:|---:|---:|---:|---:|
| Sequential | 1 | 12,991 | 23,09 gambar/detik | 1,00 | 100,00% |
| Distributed | 2 | 12,299 | 24,39 gambar/detik | 1,06 | 52,82% |
| Distributed | 2 | 10,694 | 28,05 gambar/detik | 1,21 | 60,74% |

Seluruh skenario berhasil memproses 300 dari 300 gambar. Eksperimen
distributed terbaik sekitar 17,68% lebih cepat daripada baseline sequential.

Speedup belum linear karena server hanya memiliki dua CPU core dan terdapat
overhead serialisasi task, komunikasi Redis, penjadwalan Celery, operasi I/O,
serta proses latar belakang.

Regenerasi laporan:

```bash
python scripts/aggregate_reports.py
```
