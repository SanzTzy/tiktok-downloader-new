#!/usr/bin/env python3
"""
TikTok Downloader Bot for Telegram
Handles: Video, Photo, Story
Requires: python-telegram-bot, yt-dlp, ffmpeg
"""

import os
import re
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit for Telegram

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🎵 TikTok Downloader Bot\n\n"
        "Kirim link TikTok untuk download:\n"
        "- Video\n"
        "- Photo/Image\n"
        "- Story\n\n"
        "Contoh: https://vm.tiktok.com/xxx"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "Cara pakai:\n"
        "1. Kirim link TikTok\n"
        "2. Bot akan download & kirim video/foto\n\n"
        "Story butuh cookie (opsional)"
    )


def extract_tiktok_url(text: str) -> str:
    """Extract TikTok URL from text"""
    patterns = [
        r"https?://(?:www\.)?tiktok\.com/[@\w]+/video/\d+",
        r"https?://(?:www\.)?tiktok\.com/[@\w]+",
        r"https?://vm\.tiktok\.com/\w+",
        r"https?://m\.tiktok\.com/v/\d+",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


async def download_tiktok(url: str, cookies_path: str = None) -> dict:
    """Download TikTok content using yt-dlp"""
    import yt_dlp

    ydl_opts = {
        "format": "best[filesize<50M]/best",
        "outtmpl": "/tmp/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    if cookies_path and os.path.exists(cookies_path):
        ydl_opts["cookiefile"] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            return {
                "success": True,
                "title": info.get("title", "TikTok"),
                "filename": filename,
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
            }
    except Exception as e:
        logger.error(f"Download error: {e}")
        return {"success": False, "error": str(e)}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages with TikTok links"""
    text = update.message.text
    url = extract_tiktok_url(text)

    if not url:
        await update.message.reply_text("Link TikTok tidak valid. Coba lagi.")
        return

    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Mendownload...")

    # Download
    cookies_path = context.bot_data.get("cookies_path")
    result = await download_tiktok(url, cookies_path)

    if not result["success"]:
        await processing_msg.edit_text(f"❌ Error: {result['error']}")
        return

    # Send file
    try:
        filename = result["filename"]
        
        if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
            # Photo
            await processing_msg.delete()
            await update.message.reply_photo(photo=open(filename, "rb"))
        else:
            # Video
            await processing_msg.delete()
            await update.message.reply_video(
                video=open(filename, "rb"),
                caption=f"✅ {result['title']}\n👤 {result['uploader']}"
            )
        
        # Cleanup
        os.remove(filename)
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ Gagal kirim file: {str(e)}")
        logger.error(f"Send error: {e}")


def main():
    """Start the bot"""
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        print("Get token from @BotFather on Telegram")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    print("🤖 Bot started! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()