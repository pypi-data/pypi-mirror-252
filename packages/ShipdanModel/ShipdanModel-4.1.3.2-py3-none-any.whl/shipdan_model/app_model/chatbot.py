from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatLog(models.Model):
    user = models.ForeignKey(User, related_name='chat_logs', on_delete=models.CASCADE)
    summary = models.CharField(max_length=255, null=True, blank=True, default=None)

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'chatbot_chatlog'


class ChatLogMessage(models.Model):
    UNDEFINED = 'undefined'
    SYSTEM = 'system'
    AI = 'ai'
    USER = 'user'

    CHAT_LOG_ROLE = (
        (UNDEFINED, '미정'),
        (SYSTEM, '시스템'),
        (AI, 'ai'),
        (USER, 'user'),
    )

    log = models.ForeignKey(ChatLog, related_name='messages', on_delete=models.CASCADE)
    prev = models.ForeignKey('self', related_name='nexts', on_delete=models.CASCADE)
    content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'chatbot_chatlogmessage'