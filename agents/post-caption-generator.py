import os
import openai
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage
from uagents.setup import fund_agent_if_low


AGENT_SEED = os.getenv("AGENT_SEED", "post-generator-agent1")
openai.api_key = os.getenv("OPENAI_API_KEY")


class PostGeneratorRequest(Model):
    website_content: str

class PostGeneratorResponse(Model):
    post_caption: str


PORT = 8001
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

fund_agent_if_low(agent.wallet.address())
# post_proto = Protocol(name="Post-Generator-Protocol", version="0.1.0")


async def generate_social_media_post(website_content,tone="casual"):
    try:
        # post_prompt = f"Based on the following content: '{website_content}', write a {tone} social media post."
        post_prompt = (
            f"Based on the following content: '{website_content}', write a {tone} social media post.\n\n"
            "Ensure that the post is well-formatted, using proper alignment with appropriate new lines and spacing between sentences or sections where necessary.\n"
            "Use tabs or spaces for indentation where relevant and make sure the post flows nicely. Also, ensure any important points or sections are clearly separated."
        )
        # if cta:
        #     post_prompt += f" Include a call-to-action: {cta}."
        # if hashtags:
        #     post_prompt += f" Use the following hashtags: {hashtags}."


        # Call OpenAI to generate the post
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that generates social media posts."},
                {"role": "user", "content": post_prompt}
            ],
            max_tokens=150,
            temperature=0.7  # Adjust the creativity level
        )

        return response.choices[0].message.content

    except Exception as e:
        return "Error encountered: " + str(e)


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_query(
    PostGeneratorRequest, replies={PostGeneratorResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: PostGeneratorRequest):
    ctx.logger.info(f"Received website content: {msg.website_content}")
    try:
        caption = await generate_social_media_post(msg.website_content)
        await ctx.send(sender, PostGeneratorResponse(post_caption=caption))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))


# agent.include(post_proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()