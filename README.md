# LINE Reminder Bot v2

## 功能

✔ LINE Bot

✔ Render部署

✔ GitHub自動部署

✔ Cron-job

✔ 台灣工作日判斷

✔ 自動記錄好友

✔ 自動記錄群組

✔ 臨時事故

✔ 單日事故

✔ 多日事故

✔ 管理員

✔ /help

✔ /list

✔ /members

✔ /status

✔ /reset

✔ /clear

✔ /version

✔ #測試

---

## Render

Environment

LINE_CHANNEL_ACCESS_TOKEN

LINE_CHANNEL_SECRET

ADMIN_USERS

---

## Cron-job

Wake

```
https://你的網址.onrender.com/wake
```

每10分鐘

Trigger

```
https://你的網址.onrender.com/trigger
```

每天14:55

---

## 指令

```
/help

/h

/list

/status

/reset

/clear

/members

/version

#測試

/測試
```

---

## 事故

### 臨時

```
宗旂：休
```

今天14:55發送

立即清除

---

### 單日

```
宗旂：7/1休假
```

6/30回報

---

### 多日

```
宗旂：7/1-7/3休假
```

6/30開始回報

7/2最後一次回報

7/3清除
