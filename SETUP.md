# TikTok Downloader Bot - Setup Guide

## Prerequisites

1. **Telegram Bot Token**
   - Buka @BotFather di Telegram
   - Ketik `/newbot`
   - Ikuti instruksi, dapat token
   - Simpan token itu

2. **Server/Hosting Gratis** (pilih salah satu)

   ### Opsi A: Railway (recommended)
   - Daftar di https://railway.app
   - Connect GitHub repo
   - Set environment variable: `TELEGRAM_BOT_TOKEN`
   - Deploy

   ### Opsi B: Replit
   - Buat repl Python
   - Copy bot.py & requirements.txt
   - Install deps: `pip install -r requirements.txt`
   - Set secret `TELEGRAM_BOT_TOKEN`
   - Gunakan UptimeRobot untuk ping (足防止 sleep)

   ### Opsi C: Fly.io
   - Install flyctl
   - `fly launch`
   - Set secrets: `fly secrets set TELEGRAM_BOT_TOKEN=xxx`
   - `fly deploy`

## Local Testing (sebelum deploy)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set token
export TELEGRAM_BOT_TOKEN="your_token_here"

# 3. Install ffmpeg
# Windows: download dari https://ffmpeg.org/download.html
# Linux: sudo apt install ffmpeg

# 4. Run bot
python bot.py
```

## Untuk Story TikTok (opsional)

Story butuh cookie dari akun yang sudah login:

1. Login TikTok di browser (Chrome)
2. Install ekstensi "Get cookies.txt LOCALLY"
3. Export cookies ke file `cookies.txt`
4. Upload ke server, set path di `bot.py` line:
   ```python
   app.bot_data["cookies_path"] = "/path/to/cookies.txt"
   ```

## Deploy ke Railway (langkah lengkap)

```bash
# 1. Buat GitHub repo, push semua file

# 2. Daftar Railway, click "New Project"
# 3. "Deploy from GitHub repo"

# 4. Variables:
# TELEGRAM_BOT_TOKEN = (token dari BotFather)

# 5. Railway auto-install requirements.txt
```

## Cara Pakai

1. Buka bot di Telegram
2. Kirim `/start`
3. Kirim link TikTok
4. Bot kirim video/foto

## Troubleshooting

| Error | Solution |
|-------|----------|
| "No module named yt_dlp" | `pip install yt-dlp` |
| "ffmpeg not found" | Install ffmpeg, add to PATH |
| Video terlalu besar | TikTok limit 50MB, coba format lain |
| Story tidak bisa | Perlu cookie valid |

## Alternatif: Auto-redeploy script

```python
# Railway otomatis tidur kalau tidak dipakai
# Gunakan UptimeRobot:
# - Type: HTTP
# - URL: your-railway-app.railway.app/health
# - Interval: 5 menit
```