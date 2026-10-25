import yt_dlp
from pydub import AudioSegment
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', name)

def download_youtube_audio(url: str) -> str:
    """Download audio from YouTube and normalize to 16kHz mono WAV."""
    client_candidates = [
        ["mweb", "android", "web_embedded"],
        ["android", "ios"],
        ["web_embedded", "tv"],
    ]
    last_err = None
    video_id = None
    raw_wav = None

    # Check for cookies file or environment variable
    cookie_file = None
    if os.path.exists("cookies.txt"):
        cookie_file = "cookies.txt"
    elif os.getenv("YOUTUBE_COOKIES"):
        try:
            with open("cookies.txt", "w", encoding="utf-8") as f:
                f.write(os.getenv("YOUTUBE_COOKIES").strip())
            cookie_file = "cookies.txt"
        except Exception:
            pass

    for client_list in client_candidates:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "quiet": True,
            "windowsfilenames": True,
            "noplaylist": True,
            "extractor_args": {
                "youtube": {
                    "player_client": client_list
                }
            },
        }
        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info.get("id", "audio")
                raw_wav = os.path.join(DOWNLOAD_DIR, f"{video_id}.wav")
                if os.path.exists(raw_wav):
                    break
        except Exception as e:
            last_err = e
            continue

    if not raw_wav or not os.path.exists(raw_wav):
        if last_err:
            raise last_err
        raise RuntimeError("Failed to extract YouTube audio.")

    # Standardize to 16kHz mono WAV for Whisper & Sarvam
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}_16k.wav")
    try:
        audio = AudioSegment.from_file(raw_wav)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(output_path, format="wav")
        if os.path.exists(raw_wav) and raw_wav != output_path:
            try:
                os.remove(raw_wav)
            except Exception:
                pass
        return output_path
    except Exception:
        if os.path.exists(raw_wav):
            return raw_wav
        raise

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to 16kHz mono WAV format using pydub."""
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    safe_name = sanitize_filename(base_name)
    output_path = os.path.join(DOWNLOAD_DIR, f"{safe_name}_converted.wav")
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path

def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_file(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    if len(audio) == 0:
        return []

    # If audio is shorter than or equal to chunk_minutes, use the file directly
    if len(audio) <= chunk_ms:
        return [wav_path]

    base_name = os.path.splitext(wav_path)[0]
    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        if len(chunk) < 500:  # Skip slivers under 0.5s
            continue
        chunk_path = f"{base_name}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks if chunks else [wav_path]

def process_input(source: str) -> list:
    source = source.strip().strip("'\"")
    if not source:
        raise ValueError("Source cannot be empty.")

    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(
                f"File not found: '{source}'. If you intended to process an online video, ensure the URL starts with http:// or https://"
            )
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks
