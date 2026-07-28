# Kerangka Laporan UAS

## Judul

Implementasi Sistem Pemrosesan Citra Digital Paralel dan Terdistribusi
Menggunakan Python, OpenCV, Celery, dan Redis pada Ubuntu Server

## Abstrak

Tuliskan latar belakang singkat, tujuan, metode master-worker, teknologi,
jumlah dataset, skenario pengujian, hasil utama, dan kesimpulan. Isi angka hanya
setelah eksperimen final dilakukan.

## BAB I Pendahuluan

### Latar Belakang

Jelaskan pertumbuhan data citra, kebutuhan pemrosesan batch, keterbatasan
pemrosesan sequential, dan pemanfaatan sistem terdistribusi.

### Rumusan Masalah

1. Bagaimana membagi pekerjaan citra kepada beberapa worker?
2. Bagaimana pengaruh jumlah worker terhadap waktu dan throughput?
3. Bagaimana sistem menangani kegagalan worker atau gambar rusak?

### Tujuan

1. Mengimplementasikan pemrosesan citra secara sequential dan distributed.
2. Mengukur waktu, throughput, speedup, dan efficiency.
3. Menguji mekanisme pembagian task dan fault tolerance.

### Batasan

- Pipeline menggunakan resize, grayscale, Gaussian blur, dan Canny.
- Redis digunakan sebagai broker dan result backend.
- Pengujian awal menggunakan satu node Ubuntu dengan beberapa proses worker.
- GPU dan deep learning tidak dibahas.

## BAB II Landasan Teori

Bahas sistem terdistribusi, parallel processing, arsitektur master-worker,
message broker, Celery, Redis, citra digital, OpenCV, Canny edge detection,
speedup, efficiency, throughput, dan fault tolerance.

## BAB III Perancangan

Sertakan diagram dari `docs/ARCHITECTURE.md`, spesifikasi server, alur task,
struktur direktori, rancangan input-output, format laporan, dan skenario uji.

## BAB IV Implementasi dan Pengujian

Jelaskan instalasi, konfigurasi Redis, cara menjalankan worker, implementasi
pipeline, dataset, prosedur eksperimen, tabel hasil, grafik, dan analisis.

Spesifikasi server pengembangan awal:

```text
OS       : Ubuntu 24.04.4 LTS
CPU      : 2 core
RAM      : 1,9 GiB
Swap     : 1,9 GiB
Storage  : sesuaikan dengan kondisi saat pengujian final
```

Jelaskan bahwa beberapa worker pada server yang sama merupakan simulasi
arsitektur terdistribusi multi-process pada satu node fisik.

## BAB V Penutup

### Kesimpulan

Jawab setiap rumusan masalah menggunakan angka hasil eksperimen final.

### Saran

- Pengujian pada beberapa node fisik.
- Shared storage atau object storage.
- Dashboard monitoring.
- Pembagian satu citra besar menjadi beberapa tile.
- Pengujian GPU atau algoritma yang lebih berat.

## Lampiran

- Tautan repository.
- Perintah instalasi.
- Contoh `summary.json` dan `task-results.csv`.
- Screenshot terminal master, Redis, dan worker.
- Screenshot input dan output citra.
- Log eksperimen final.

