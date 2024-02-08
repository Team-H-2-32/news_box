import json
import wikipedia as w
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        keyword = data['keyword']
        language = 'en'  # Set the default language for Wikipedia search

        try:
            result = w.summary(keyword, sentences=1, lang=language)
            response = {'message': result}
        except w.DisambiguationError as e:
            # Handle disambiguation errors (multiple results)
            response = {'message': f"Disambiguation: {', '.join(e.options)}"}
        except w.PageError as e:
            # Handle page not found errors
            response = {'message': f"Page not found for '{keyword}'"}

        await self.send(text_data=json.dumps(response))
