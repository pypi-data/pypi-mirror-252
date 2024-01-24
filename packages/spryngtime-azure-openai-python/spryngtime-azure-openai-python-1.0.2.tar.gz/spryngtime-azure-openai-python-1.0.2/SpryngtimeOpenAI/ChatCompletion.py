import time
import openai
import os

from spryngtime_analytics_sdk import SpryngtimeAnalyticsSdk


class ChatCompletion():

    def create(*args, **kwargs):
        spryngtime_analytics_sdk = SpryngtimeAnalyticsSdk(api_key=os.getenv('SPRYNGTIME_API_KEY', 'default_api_key'))

        start_time = time.time()
        conversation_id = kwargs.get("conversation_id", "")
        if conversation_id != "":
            kwargs.pop("conversation_id") # OpenAI API doesn't like conversation_id
        result = openai.ChatCompletion.create(*args, **kwargs)

        latency = int((time.time() - start_time) * 1000) # Convert to milliseconds

        user = kwargs.get("user", "default_user")
        messages = kwargs.get("messages", [])
        query = messages[-1]["content"] if len(messages) > 0 else ""
        spryngtime_analytics_sdk.usage_tracking.track_usage(user=user, query=query, conversation_id=conversation_id, open_ai_response=result, latency=latency)
        return result

