import secrets
import base64

# Генерация безопасного случайного ключа
SECRET_KEY = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
print(f"Ваш SECRET_KEY: {SECRET_KEY}")
