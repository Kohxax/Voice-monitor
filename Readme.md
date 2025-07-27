## 室内騒音監視システム
自分用

.envに

```
DEVICE_KEYWORD=デバイス名が含まれるキーワード
WEBHOOK_URL=DiscordのWebhook URL
THRESHOLD_DB=通知の閾値（相対デシベル）
```

を記入して、
```
docker compose up -d --build
```
でOK

夜間（21時～翌4時）のみの通知送信