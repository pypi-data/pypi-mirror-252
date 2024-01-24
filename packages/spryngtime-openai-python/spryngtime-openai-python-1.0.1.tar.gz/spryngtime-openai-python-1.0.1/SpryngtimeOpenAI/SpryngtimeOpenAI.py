import time
from openai import OpenAI
import os

from spryngtime_analytics_sdk import SpryngtimeAnalyticsSdk


class SpryngtimeOpenAI(OpenAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Read API key from environment variable
        api_key = os.getenv('SPRYNGTIME_API_KEY', 'default_api_key')  # Replace 'default_api_key' with a suitable default or error handling

        # Initialize SpryngtimeAnalyticsSDK
        self.spryngtime_analytics_sdk = SpryngtimeAnalyticsSdk(api_key=api_key)

        original_create = self.chat.completions.create

        def create_with_latency(*args, **kwargs):
            start_time = time.time()
            conversation_id = kwargs.get("conversation_id", "")
            kwargs.pop("conversation_id") # OpenAI API doesn't like conversation_id
            result = original_create(*args, **kwargs)

            latency = int((time.time() - start_time) * 1000) # Convert to milliseconds

            user = kwargs.get("user", "default_user")
            messages = kwargs.get("messages", [])
            query = messages[-1]["content"] if len(messages) > 0 else ""
            self.spryngtime_analytics_sdk.usage_tracking.track_usage(user=user, query=query, conversation_id=conversation_id, open_ai_response=result, latency=latency)
            return result

        self.chat.completions.create = create_with_latency


# Usage
# client = SpryngtimeOpenAI()
# completion = client.chat.completions.create(prompt="Your prompt here")
