# Distributed Image Processing

Implementasi pemrosesan citra digital paralel dan terdistribusi untuk proyek
UAS mata kuliah Sistem Terdistribusi. Sistem membandingkan pemrosesan
sequential dengan pembagian pekerjaan ke satu atau beberapa Celery worker.

## Fitur

- Pemrosesan batch gambar dengan OpenCV.
- Mode sequential sebagai baseline eksperimen.
- Mode distributed menggunakan Celery dan Redis.
- Satu gambar menjadi satu task yang dapat dibagikan ke worker berbeda.
- Retry otomatis untuk kegagalan penyimpanan atau I/O.
- Laporan eksperimen dalam format JSON dan CSV.
- Generator dataset sintetis yang dapat direproduksi.
- Skrip instalasi untuk Ubuntu dan AlmaLinux.

## Arsitektur

```text
Master CLI -> Redis Broker -> Celery Worker 1..N -> OpenCV -> Output + Report
```

Satu gambar menjadi satu task. Worker melakukan resize, grayscale, Gaussian
blur, dan Canny edge detection. Hasil eksperimen disimpan sebagai JSON dan CSV.

Penjelasan arsitektur lebih lengkap tersedia di `docs/ARCHITECTURE.md`.

## Persyaratan

- Ubuntu 22.04/24.04 atau distribusi Linux yang kompatibel.
- Python 3.10 atau lebih baru.
- Redis Server.
- Minimal 2 GB RAM untuk eksperimen kecil.
- Ruang penyimpanan sesuai ukuran dataset dan output.

## Instalasi Ubuntu

```bash
chmod +x scripts/*.sh
./scripts/setup-ubuntu.sh
source .venv/bin/activate
```

Periksa Redis:

```bash
redis-cli ping
```

Keluaran yang diharapkan adalah `PONG`.

## Membuat Dataset Uji

```bash
python scripts/generate_dataset.py --count 20
```

Dataset asli juga dapat diletakkan di direktori `dataset/`. Format yang
didukung adalah JPG, JPEG, PNG, BMP, TIFF, dan TIF.

## Eksperimen Sequential

```bash
python -m app.cli --mode sequential --workers 1
```

## Eksperimen Distributed

Buka dua terminal worker:

```bash
source .venv/bin/activate
./scripts/start_worker.sh worker1 1
```

```bash
source .venv/bin/activate
./scripts/start_worker.sh worker2 1
```

Kemudian kirim pekerjaan dari terminal lain:

```bash
source .venv/bin/activate
python -m app.cli --mode distributed --workers 2
```

Nilai `--workers` adalah metadata eksperimen. Jumlah worker yang benar-benar
aktif ditentukan oleh banyaknya proses `start_worker.sh` yang dijalankan.

Laporan setiap eksperimen tersedia pada `reports/<experiment-id>/summary.json`
dan `reports/<experiment-id>/task-results.csv`.

## Pengujian

```bash
pytest
```

## Struktur Proyek

```text
app/                     kode aplikasi
  celery_app.py          konfigurasi Celery dan Redis
  cli.py                 master/job submitter
  config.py              konfigurasi direktori dan broker
  image_processor.py     pipeline OpenCV
  reporting.py           laporan JSON dan CSV
  tasks.py               definisi distributed task
dataset/                 gambar input, tidak disimpan di Git
output/                  gambar hasil, tidak disimpan di Git
reports/                 hasil pengukuran, tidak disimpan di Git
scripts/                 instalasi, worker, dan generator dataset
tests/                   unit test
docs/                    dokumentasi teknis dan laporan UAS
```

## Parameter CLI

```text
--mode       sequential atau distributed, wajib
--dataset    direktori gambar input
--output     direktori gambar hasil
--reports    direktori laporan eksperimen
--workers    jumlah worker untuk metadata laporan
--timeout    batas tunggu hasil distributed dalam detik
```

Contoh menggunakan lokasi khusus:

```bash
python -m app.cli \
  --mode sequential \
  --dataset /path/to/images \
  --output /path/to/output \
  --reports /path/to/reports
```

## Dokumentasi

- `docs/ARCHITECTURE.md`: komponen, aliran data, dan fault tolerance.
- `docs/INSTALLATION.md`: instalasi dan troubleshooting.
- `docs/EXPERIMENT.md`: prosedur benchmark dan rumus evaluasi.
- `docs/LAPORAN-UAS.md`: kerangka laporan yang dapat dikembangkan.

## Menggabungkan Hasil Eksperimen

Setelah beberapa eksperimen selesai, buat satu tabel perbandingan dan grafik:

```bash
python scripts/aggregate_reports.py
```

Hasil tersedia di `reports/aggregate/comparison.csv`,
`reports/aggregate/execution-time.png`, dan `reports/aggregate/throughput.png`.

## Catatan Lingkungan

Pengembangan awal berjalan pada Ubuntu. Skrip `scripts/setup-almalinux.sh`
disediakan agar aplikasi yang sama dapat dipasang pada AlmaLinux. Jika seluruh
worker dijalankan pada satu server, eksperimen disebut simulasi sistem
terdistribusi multi-process pada satu node fisik.

## Batasan

- Worker pada satu server berbagi CPU, RAM, dan penyimpanan yang sama.
- Dataset kecil dapat membuat mode distributed lebih lambat karena overhead.
- Proyek belum menyediakan dashboard web dan database permanen.
- Pengujian multi-node membutuhkan direktori bersama atau mekanisme transfer
  file agar semua worker dapat mengakses input dan output.

## Lisensi dan Penggunaan

Proyek ini dibuat untuk kebutuhan pembelajaran dan penelitian akademik.
