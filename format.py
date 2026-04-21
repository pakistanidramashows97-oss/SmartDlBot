import yt_dlp
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ----------------------------
# PLATFORM DETECTOR
# ----------------------------
def detect_platform(url: str):
    url = url.lower()

    if "youtube" in url or "youtu.be" in url:
        return "youtube"
    elif "instagram" in url:
        return "instagram"
    elif "facebook" in url:
        return "facebook"
    elif "tiktok" in url:
        return "tiktok"
    elif "pinterest" in url:
        return "pinterest"
    elif "spotify" in url:
        return "spotify"
    else:
        return "unknown"


# ----------------------------
# FETCH INFO (yt-dlp)
# ----------------------------
def fetch_info(url: str):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": "cookies.txt"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


# ----------------------------
# FORMAT EXTRACTOR (REAL ONLY)
# ----------------------------
def extract_formats(info):
    formats = []

    for f in info.get("formats", []):
        # video streams only
        if f.get("vcodec") != "none":
            formats.append({
                "id": f.get("format_id"),
                "res": f.get("height") or 0,
                "ext": f.get("ext"),
                "size": f.get("filesize") or 0
            })

    # remove duplicates
    seen = set()
    clean = []

    for f in sorted(formats, key=lambda x: x["res"], reverse=True):
        key = f["res"]
        if key not in seen:
            seen.add(key)
            clean.append(f)

    return clean


# ----------------------------
# UNIVERSAL BUTTON BUILDER
# ----------------------------
def build_quality_ui(url: str):
    platform = detect_platform(url)

    # SPOTIFY → AUDIO ONLY
    if platform == "spotify":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 Download Audio", callback_data=f"audio|{url}")]
        ])

    try:
        info = fetch_info(url)
        formats = extract_formats(info)
    except:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Download Best Quality", callback_data=f"fast|{url}")]
        ])

    buttons = []

    # ----------------------------
    # YOUTUBE → FULL QUALITY LIST
    # ----------------------------
    if platform == "youtube":
        for f in formats[:10]:
            label = f"📹 {f['res']}p" if f["res"] else "📹 Unknown"
            buttons.append([
                InlineKeyboardButton(
                    label,
                    callback_data=f"vid|{url}|{f['id']}"
                )
            ])

        buttons.append([
            InlineKeyboardButton("🎵 MP3 Audio", callback_data=f"audio|{url}")
        ])

    # ----------------------------
    # ALL OTHER PLATFORMS
    # (Instagram / Facebook / TikTok / Pinterest)
    # ----------------------------
    else:
        if formats:
            for f in formats[:6]:
                label = f"📹 {f['res']}p" if f["res"] else "📥 Best Quality"
                buttons.append([
                    InlineKeyboardButton(
                        label,
                        callback_data=f"vid|{url}|{f['id']}"
                    )
                ])
        else:
            buttons.append([
                InlineKeyboardButton("📥 Download Best Available", callback_data=f"fast|{url}")
            ])

    return InlineKeyboardMarkup(buttons)


# ----------------------------
# SIMPLE HELPER
# ----------------------------
def get_platform(url: str):
    return detect_platform(url)
