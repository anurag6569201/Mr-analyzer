import os
from openai import AzureOpenAI
import json

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint="https://anura-m5hrl91e-swedencentral.openai.azure.com/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)


def get_images(llm_response):
    words_and_prompts = llm_response.split("\n")
    print(words_and_prompts)

    # List to store image URLs
    image_urls = []

    for item in words_and_prompts:
        if ":" in item:
            word, image_prompt = item.split(":", 1)
            word = word.strip()
            image_prompt = image_prompt.strip()
            print(word)

            # Generate image based on the prompt
            result = client.images.generate(
                model="dall-e-3",  # DALL·E 3 model
                prompt=image_prompt,
                n=1
            )

            image_url = json.loads(result.model_dump_json())['data'][0]['url']
            image_urls.append((word, image_url))


    return image_urls