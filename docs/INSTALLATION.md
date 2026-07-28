# Instalasi dan Operasional

## Ubuntu

```bash
git clone https://github.com/HansPiterson/Sistem-Terdistribusi--distributed-image-processing.git
cd Sistem-Terdistribusi--distributed-image-processing
chmod +x scripts/*.sh
./scripts/setup-ubuntu.sh
source .venv/bin/activate
redis-cli ping
```

## AlmaLinux

```bash
git clone https://github.com/HansPiterson/Sistem-Terdistribusi--distributed-image-processing.git
cd Sistem-Terdistribusi--distributed-image-processing
chmod +x scripts/*.sh
./scripts/setup-almalinux.sh
source .venv/bin/activate
redis-cli ping
```

## Menjalankan Worker

Setiap worker dijalankan pada terminal berbeda:

```bash
./scripts/start_worker.sh worker1 1
./scripts/start_worker.sh worker2 1
```

Argumen pertama adalah nama worker dan argumen kedua adalah concurrency.
Untuk mesin dua core, gunakan dua worker dengan concurrency satu atau satu
worker dengan concurrency dua.

## Konfigurasi Environment

Nilai bawaan dapat diganti melalui environment variable:

```bash
export REDIS_URL=redis://127.0.0.1:6379/0
export DATASET_DIR=/path/to/dataset
export OUTPUT_DIR=/path/to/output
export REPORTS_DIR=/path/to/reports
```

## Menjalankan Master

```bash
python -m app.cli --mode distributed --workers 2 --timeout 3600
```

## Troubleshooting

### Redis tidak terhubung

```bash
sudo systemctl status redis-server
sudo systemctl restart redis-server
redis-cli ping
```

Pada AlmaLinux nama service biasanya `redis`, bukan `redis-server`.

### Worker tidak menerima task

- Pastikan master dan worker menggunakan `REDIS_URL` yang sama.
- Pastikan worker menampilkan status `ready`.
- Periksa firewall jika Redis berada di mesin berbeda.
- Pastikan modul dijalankan dari root repository.

### Gambar tidak ditemukan

- Pastikan ekstensi termasuk JPG, JPEG, PNG, BMP, TIFF, atau TIF.
- Pastikan path pada `--dataset` dapat dibaca oleh proses master dan worker.

### Proses kehabisan RAM

- Kurangi concurrency worker.
- Gunakan gambar beresolusi lebih kecil.
- Kurangi jumlah batch pengujian.
- Jangan menjalankan terlalu banyak worker pada mesin dengan RAM kecil.

