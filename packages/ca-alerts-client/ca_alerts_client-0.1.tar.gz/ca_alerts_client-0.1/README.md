# Клиент для коммуникации с сервисом ca-alerts

## Example (sync)



```
class TelegramAlertChannel(TelegramChannel):
    SHOW_FILENAME = True
    HEADER = "️🆘️ Header text"

alert_channel = TelegramAlertChannel(
    bot_token="bot:token",
    chat_id=12345
)
alert_channel.send_message("Message")
```

## Example (async)



```
class AsyncTelegramAlertChannel(AsyncTelegramChannel):
    SHOW_FILENAME = True
    HEADER = "️🆘️ Header text"

async alert_channel = AsyncTelegramAlertChannel(
    bot_token="bot:token",
    chat_id=12345
)
await alert_channel.send_message("Message")
```

