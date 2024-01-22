from django.db import models


class QuickStartChatbotMessage(models.Model):
    content = models.TextField(help_text='유저가 질문할 내용')
    help_text = models.TextField(blank=True, default='')
    is_shown = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'chatbot_quickstartchatbotmessage'