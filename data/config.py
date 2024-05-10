from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

BOT_NICKNAME = "ProSkill_Planet_bot"

CHANNELS = [
    ["ProSkill Planet", "-1002079175587", "https://t.me/ProSkill_Planet"],
]

not_sub_message = "Kanallarga a'zo bo'lmasangiz davom ettira olmaysiz !"
