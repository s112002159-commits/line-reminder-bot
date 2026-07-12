import os

# ============================
# LINE
# ============================

LINE_CHANNEL_ACCESS_TOKEN = os.getenv(
    "LINE_CHANNEL_ACCESS_TOKEN"
)

LINE_CHANNEL_SECRET = os.getenv(
    "LINE_CHANNEL_SECRET"
)

# ============================
# 管理員
# Render可設定多位
#
# ADMIN_USERS=
# Uxxxxxxxx,Uyyyyyyyy
# ============================

ADMIN_USERS = os.getenv(
    "ADMIN_USERS",
    ""
).split(",")

# ============================
# DATA FILE
# ============================

DATA_FILE = "data.json"

# ============================
# 成員名單
# ============================

DEFAULT_MEMBERS = [

    "造賓",

    "佳真",

    "宗旂",

    "培昇",

    "季家",

    "佳峻",

    "彥呈",

    "欣雯"

]

# ============================
# BOT VERSION
# ============================

VERSION = "v2.0.0"

BUILD = "2026.07"
