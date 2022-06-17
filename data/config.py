import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

QIWI_TOKEN = os.getenv("qiwi")
WALLET_QIWI = os.getenv("wallet")
QIWI_PUBKEY = os.getenv("qiwi_p_pub")
channel_id = os.getenv("channel")

admins = [
    422999166
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
