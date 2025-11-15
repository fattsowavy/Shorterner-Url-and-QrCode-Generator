# URL Shortener + QR Code Generator

[![Flask](https://img.shields.io/badge/Flask-3.0.3-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-4A154B?logo=render)](https://render.com)

Sebuah **URL Shortener** modern dengan fitur **QR Code Generator** otomatis, dibangun menggunakan **Flask**, **SQLite**, dan **qrcode**.  
Setiap URL pendek yang dibuat akan otomatis menghasilkan **QR Code** yang bisa di-scan langsung dari halaman hasil.

## Fitur Utama

| Fitur | Deskripsi |
|------|----------|
| **Short URL Unik** | Kode pendek 6 karakter acak (unik, aman, anti-tabrakan) |
| **QR Code Otomatis** | QR Code langsung muncul dalam format Base64 (tanpa file eksternal) |
| **Redireksi Cepat** | `@/kodependek` → langsung ke URL asli |
| **SQLite Database** | Penyimpanan ringan & persistent |
| **Production-Ready** | Deploy otomatis via Render + Gunicorn |
| **HTTPS & Mobile-Friendly** | Siap digunakan di HP/PC |


## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (`shortener.db`)
- **QR Code**: `qrcode` + `Pillow`
- **Server**: Gunicorn
- **Deploy**: [Render.com](https://render.com) (Free tier)


## Struktur Proyek
