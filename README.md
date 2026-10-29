# Room Reservation API

Backend sederhana untuk reservasi ruang belajar / ruang rapat.
Dibuat dengan **Python + FastAPI**, penyimpanan **in-memory**.

## Aturan Bisnis
- Waktu selesai harus setelah waktu mulai
- Durasi reservasi maksimal 3 jam
- Jadwal pada ruangan yang sama tidak boleh bentrok (jadwal "menempel" diperbolehkan)
- Reservasi yang dibatalkan tidak memblokir jadwal

## Struktur
```
app/
├── main.py            # entry point + exception handler
├── dependencies.py    # composition root (dependency injection)
├── exceptions.py      # exception domain
├── models/            # entitas domain (dataclass)
├── schemas/           # request/response (Pydantic)
├── repositories/      # interface (base.py) + implementasi in-memory
├── services/          # logika bisnis + rules/
└── routers/           # endpoint FastAPI
tests/                 # unit test & API test (pytest)
```

## Menjalankan
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Dokumentasi interaktif: http://127.0.0.1:8000/docs

## Menjalankan Test
```bash
pytest -v
```

## Endpoint
| Method | Path | Keterangan |
|---|---|---|
| POST | /rooms | Buat ruangan |
| GET | /rooms | Daftar ruangan |
| GET | /rooms/{id} | Detail ruangan |
| POST | /reservations | Buat reservasi |
| GET | /reservations?room_id= | Daftar reservasi (filter opsional) |
| GET | /reservations/{id} | Detail reservasi |
| PATCH | /reservations/{id}/cancel | Batalkan reservasi |

## Penerapan SOLID
- **S**: tiap class satu tugas (Router = HTTP, Service = orkestrasi, Rule = satu validasi, Repository = penyimpanan)
- **O**: aturan baru = class baru turunan `ReservationRule`, tanpa mengubah `ReservationService`
- **L**: semua `ReservationRule` / repository bisa saling menggantikan
- **I**: interface `RoomRepository` dan `ReservationRepository` dipisah, kecil dan spesifik
- **D**: service bergantung pada abstraksi (`base.py`), implementasi konkret dirakit di `dependencies.py`
