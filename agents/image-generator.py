import os
import openai
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage
from uagents.setup import fund_agent_if_low
from openai import OpenAI

AGENT_SEED = os.getenv("AGENT_SEED", "image-generator-agent1")
openai.api_key = "YOUR-OPENAI-KEY"


class ImageGeneratorRequest(Model):
    website_content:str

class ImageGeneratorResponse(Model):
    image_url: str


PORT = 8002
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

fund_agent_if_low(agent.wallet.address())

async def generate_social_media_post(website_content,tone="casual"):
    try:
        image_prompt = f"Based on the following content: '{website_content}', describe an image that fits the tone {tone}."
        response_image = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an assistant that generates image descriptions for social media posts."},
                {"role": "user", "content": image_prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        image_description = response_image.choices[0].message.content

        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=image_description,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url

    except Exception as e:
        return "Error encountered: " + str(e)


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_query(
    ImageGeneratorRequest, replies={ImageGeneratorResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: ImageGeneratorRequest):
    ctx.logger.info(f"Received website content: {msg.website_content}")
    try:
        image_url = await generate_social_media_post(msg.website_content)
        image_url_str=str(image_url)
        print(image_url_str)
        await ctx.send(sender, ImageGeneratorResponse(image_url=image_url_str))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))




if __name__ == "__main__":
    agent.run()