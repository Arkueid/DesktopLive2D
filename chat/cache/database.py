import datetime

import peewee as pw
import atexit

db = pw.SqliteDatabase("messages.db")
db.connect()


class Message(pw.Model):
    src = pw.TextField(null=False)
    dst = pw.TextField(null=False)
    text = pw.TextField(null=False, default='')
    sound = pw.TextField(null=True)  # 假设存储音频文件路径，可以根据需要调整类型
    asr = pw.TextField(null=True)
    ct = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


db.create_tables([Message], safe=True)

atexit.register(db.close)
