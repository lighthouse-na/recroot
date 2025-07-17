from config.env import env

# SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]

# RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_V2_PUBLIC_KEY")
# RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_V2_PRIVATE_KEY")
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_V3_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_V3_PRIVATE_KEY")

# RECAPTCHA_PROXY = {"http": "http://127.0.0.1:8000", "https": "https://127.0.0.1:8000"}
# RECAPTCHA_DOMAIN = "www.recaptcha.net"
