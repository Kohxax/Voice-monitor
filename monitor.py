import sounddevice as sd
import numpy as np
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

DEVICE_KEYWORD = os.getenv("DEVICE_KEYWORD", "USB")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
THRESHOLD_DB = float(os.getenv("THRESHOLD_DB", 60))

def rms_to_db(audio):
    rms = np.sqrt(np.mean(audio**2))
    return 20 * np.log10(rms + 1e-6)

def send_discord_alert(db):
    msg = f"音量がしきい値を超えました！ ({db:.2f} dB)"
    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
        print("Discord通知送信")
    except Exception as e:
        print(f"[!] Discord送信失敗: {e}")

def find_device_index(keyword):
    for i, dev in enumerate(sd.query_devices()):
        if keyword.lower() in dev['name'].lower():
            print(f"使用マイク: {dev['name']} (index: {i})")
            return i
    raise RuntimeError("マイクが見つかりません")

if __name__ == "__main__":
    index = find_device_index(DEVICE_KEYWORD)
    with sd.InputStream(device=index, channels=1, samplerate=44100, blocksize=1024) as stream:
        print("dB監視開始")
        while True:
            audio, _ = stream.read(1024)
            db = rms_to_db(audio)
            print(f"現在の音量: {db:.2f} dB")
            if db > THRESHOLD_DB:
                send_discord_alert(db)
            time.sleep(1)
