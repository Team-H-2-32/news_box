# import os
# from celery import Celery
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
#
# app = Celery('news')
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Automatically discover tasks from all registered Django apps
# app.autodiscover_tasks()
#
#
# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
#
