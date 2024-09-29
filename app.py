from flask import Flask, render_template, request
from uagents.envelope import Envelope
import requests
import json
from uagents import Model
from uagents.query import query

app = Flask(__name__)

class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str

class PostGeneratorRequest(Model):
    website_content: str

class PostGeneratorResponse(Model):
    post_caption: str

class ImageGeneratorRequest(Model):
    website_content: str

class ImageGeneratorResponse(Model):
    image_url: str


website_scraping_agent_address="agent1qfnfh7axy6lvau9537ce3n0dy86y7w37vshu94gwm6e5gmlxutkmg0el2yz"
post_generator_agent_address="agent1qvjaj9ntt6vh5wq6vyrlr9tuvz7n3f0nwjd88p48m6hlscys0q4wv599hxf"
image_generator_agent_address="agent1qvdrc9usesg8rxdmzvjqc58cfvhvlp5vg83y06nps6nnmefz4c78yjy5rzc"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_caption', methods=['POST'])
async def generate_caption():
    url = request.form['url']

    try:
        response = await query(website_scraping_agent_address,message=WebsiteScraperRequest(url=url),timeout=15.0)        # Parse the webpage content using BeautifulSoup
        if isinstance(response, Envelope):
            data = json.loads(response.decode_payload())
            website_content = data['text']

        response = await query(post_generator_agent_address, message=PostGeneratorRequest(website_content=website_content), timeout=15.0)
        if isinstance(response, Envelope):
            data = json.loads(response.decode_payload())
            post_caption = data['post_caption']

        response = await query(image_generator_agent_address,
                               message=ImageGeneratorRequest(website_content=website_content), timeout=15.0)
        if isinstance(response, Envelope):
            data = json.loads(response.decode_payload())
            print(data)
            if 'image_url' in data:
                image_url = data['image_url']
            else:
                image_url = "Could not generate Image"

        return render_template('index.html', url=url, caption=post_caption,image_url=image_url)

    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"


if __name__ == '__main__':
    app.run(debug=True)
