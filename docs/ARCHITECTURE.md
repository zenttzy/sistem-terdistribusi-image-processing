# Arsitektur Sistem

## Tujuan

Sistem membagi pemrosesan sekumpulan gambar menjadi task independen. Setiap
gambar dapat diproses worker berbeda, sedangkan master mengirim pekerjaan,
menunggu hasil, dan membuat laporan performa.

## Diagram

```text
                   +----------------------+
                   | Master CLI           |
                   | app/cli.py           |
                   +----------+-----------+
                              |
                              | task message
                              v
                   +----------------------+
                   | Redis                |
                   | broker + result      |
                   +----------+-----------+
                              |
                +-------------+-------------+
                |                           |
                v                           v
       +------------------+        +------------------+
       | Celery Worker 1  |  ...   | Celery Worker N  |
       | OpenCV pipeline  |        | OpenCV pipeline  |
       +--------+---------+        +--------+---------+
                |                           |
                +-------------+-------------+
                              |
                              v
                 output/ dan reports/
```

## Komponen

### Master

`app/cli.py` melakukan penemuan gambar, membuat direktori eksperimen,
mengirim task, mengumpulkan hasil, serta menghitung waktu total dan throughput.

### Redis

Redis berfungsi sebagai message broker dan result backend. Broker menyimpan
antrean task, sedangkan result backend menyimpan hasil sementara agar dapat
diambil master.

### Worker

Worker Celery mengambil task dari Redis dan menjalankan fungsi di
`app/tasks.py`. Setiap task mencatat hostname worker dan task ID.

### Pipeline Citra

`app/image_processor.py` menjalankan tahapan berikut:

1. Membaca gambar.
2. Membatasi lebar maksimal menjadi 1920 piksel.
3. Mengubah gambar menjadi grayscale.
4. Mengurangi noise menggunakan Gaussian blur kernel 11x11.
5. Menjalankan Canny edge detection.
6. Menyimpan hasil sebagai PNG.
7. Mengembalikan ukuran dan durasi pemrosesan.

## Aliran Data

1. Master membaca gambar dari `dataset/`.
2. Master membuat satu task untuk setiap gambar.
3. Redis menyimpan task hingga diambil worker.
4. Worker memproses gambar dan menyimpan hasil ke `output/<experiment-id>/`.
5. Worker mengirim metadata hasil ke Redis.
6. Master mengambil seluruh hasil.
7. Master membuat `summary.json` dan `task-results.csv`.

## Fault Tolerance

- Task menggunakan late acknowledgement agar pesan diakui setelah selesai.
- Prefetch dibatasi satu task agar distribusi lebih merata.
- Kesalahan I/O dapat diulang maksimal tiga kali dengan exponential backoff.
- File gambar tidak valid ditandai gagal tanpa menghentikan keseluruhan batch.
- Jika worker berhenti sebelum acknowledgement, task dapat dikirim kembali oleh
  broker kepada worker yang tersedia.

## Single Node dan Multi Node

Pada single node, master, Redis, dan worker berjalan sebagai proses terpisah
tetapi berbagi mesin yang sama. Konfigurasi ini cukup untuk menunjukkan antrean,
pembagian task, konkurensi, dan kegagalan worker.

Pada multi node, Redis dapat berjalan pada master dan worker menggunakan
`REDIS_URL=redis://IP_MASTER:6379/0`. Dataset dan output harus tersedia melalui
NFS, shared storage, atau mekanisme transfer file.

