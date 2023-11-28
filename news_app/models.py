from django.db import models
from main.models import BaseModel, Category
from user.models import User
from datetime import datetime, timedelta


class News(BaseModel):
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    photo = models.TextField(null=True)
    source = models.CharField(max_length=300, null=True)
    url = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class History(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(days=10)

        super(History, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} read {self.news.title[:15]} "


class SavedNews(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} saved {self.news.title}"


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} commented {self.news.title}"



