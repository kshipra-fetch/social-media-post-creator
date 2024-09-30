# PostPerfect - Social Media Post Creation Application

PostPerfect is a web-based application that takes a website URL as input and generates a well-crafted social media post based on the content of that URL.The app makes it easy to create visually appealing and engaging social media content.

## Features

- **Website Scraping**: Extracts the main content from a given website URL.
- **Social Media Caption Generation**: Uses an AI-based model to generate a well-formatted and engaging social media caption.

## Technologies Used

- **Flask**: A lightweight web framework for Python.
- **uAgents**: Decentralized AI agents used for handling the different tasks of website scraping, post generation, and image generation.
- **OpenAI**: Used for generating captions and images via AI models.
- **HTML & CSS**: Frontend for displaying the web interface.

## Installation

To set up this project locally, follow these steps:

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)
- OpenAI API Key (required for generating captions and images)

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/kshipra-fetch/social-media-post-creator.git
    cd social-media-post-creator
    ```

2. **Create a Virtual Environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    Install the required Python packages by running:
    ```bash
    pip install uagents openai bs4 flask
    pip install 'flask[async]'
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory of your project and add your OpenAI API key and agent seeds:
    ```
    OPENAI_API_KEY=your-openai-api-key
    ```
5. Update the SEED phrase in all three agent files

6. **Run the Agents**:
    Keep all the three agents running in separate terminals
    ```
    website-scraping-agent.py
    post-caption-generator.py
    ```

7. **Update Agent Address**
    Copy the agent address after you run the agents from the terminal and paste it in `app.py`

6. **Run the Application**:
    You can now run the Flask app:
    ```bash
    python app.py
    ```

7. **Access the Web App**:
    Open your browser and go to:
    ```
    http://127.0.0.1:5000/
    ```

## Usage

1. Enter a website URL into the provided input field on the homepage.
2. Click on the "Generate Caption" button.
3. The app will display a caption in the center of the screen.



