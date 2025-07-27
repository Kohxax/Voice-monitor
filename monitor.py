import sounddevice as sd
import numpy as np
import requests
import time
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from datetime import datetime

load_dotenv()

DEVICE_KEYWORD = os.getenv("DEVICE_KEYWORD", "USB")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
THRESHOLD_DB = float(os.getenv("THRESHOLD_DB", -30))

# 夜間のみ通知（JST）
def is_night_time():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    return now.hour >= 21 or now.hour < 4  # 21:00〜翌4:00

def rms_to_db(audio):
    rms = np.sqrt(np.mean(audio**2))
    return 20 * np.log10(rms + 1e-6)

def send_discord_alert(db):
    msg = f"@bokukoha 音量がしきい値を超えました！静かにしてください！ ({db:.2f} dB)"
    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
        print("📨 Discord通知送信", flush=True)
    except Exception as e:
        print(f"[!] Discord送信失敗: {e}", flush=True)

def find_device_index(keyword):
    for i, dev in enumerate(sd.query_devices()):
        if keyword.lower() in dev['name'].lower():
            print(f"🎤 使用マイク: {dev['name']} (index: {i})", flush=True)
            return i
    raise RuntimeError("マイクが見つかりません")

if __name__ == "__main__":
    index = find_device_index(DEVICE_KEYWORD)
    with sd.InputStream(device=index, channels=1, samplerate=44100, blocksize=1024) as stream:
        print("🎧 dB監視開始", flush=True)
        while True:
            audio, _ = stream.read(1024)
            db = rms_to_db(audio)
            print(f"🔊 現在の音量: {db:.2f} dB", flush=True)
            if db > THRESHOLD_DB and is_night_time():
                print(f"🔔 閾値超過（{db:.2f} > {THRESHOLD_DB}）", flush=True)
                send_discord_alert(db)
            time.sleep(1)
