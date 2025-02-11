# Tech News Briefing

| Initial View | With Summary |
|:---:|:---:|
| ![Tech News Initial View](assets/app_screenshot1.png) | ![Tech News with Summary](assets/app_screenshot2.PNG) |

A FastAPI application that fetches tech news articles, creates a summary using OpenAI's GPT-3.5, and converts it to speech using Google Cloud Text-to-Speech.

## Features
- Fetches latest tech news articles
- Generates concise summaries using GPT-3.5
- Converts summaries to natural-sounding speech
- Interactive audio player with progress tracking
- Configurable summary lengths (5, 10, or 15 articles)

# Personalized Tech News Briefing App

This project is a **Python-based Tech News Summarization App** that delivers personalized tech news briefings. It integrates tech news aggregation, AI-powered text summarization, and text-to-speech (TTS) features to provide users with brief, conversational summaries of recent tech news articles.

---

## **Features**

1. **Tech News Aggregation**

   - Fetches recent tech news articles from a public news API (e.g., NewsAPI).

2. **AI-Powered Summarization**

   - Uses an LLM (e.g., OpenAI GPT) to generate short, conversational summaries of the tech news articles. The user should be able to choose between short, medium, and long summaries (5min, 10, 15, respectively).

3. **Text-to-Speech Integration**

   - Converts the tech news summaries into audio using a TTS API, allowing users to listen to the tech news briefing.

---

## **Tech Stack**

### **Backend**

- **Python** (FastAPI)

### **APIs**

- **News API**: To fetch recent tech news articles.
- **LLM API**: OpenAI GPT for article summarization.
- **TTS API**: Google Text-to-Speech, AWS Polly, or ElevenLabs.

### **Frontend** (optional for MVP)

- Basic web interface using HTML/CSS/JavaScript (or React).

---

## **Setup Instructions**

1. Clone the repository
2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables in `.env`:
```env
NEWS_API_KEY=your_news_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

4. Run the application:
```bash
poetry run uvicorn main:app --reload
```

Visit `http://localhost:8000` to use the application.

---

## **API Endpoints**

### **1. Get Tech News Briefing**

Endpoint: `/get-tech-news-briefing/`

#### **Query Parameters:**

| Parameter      | Type | Description                         |
| -------------- | ---- | ----------------------------------- |
| `max_articles` | int  | Maximum number of articles to fetch |

#### **Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/get-tech-news-briefing/?max_articles=5"
```

#### **Response Format:**

```json
{
    "briefing": [
        {
            "title": "AI Startups Raise Record Funding",
            "summary": "Here's the latest on technology: AI startups raised a record amount of funding this quarter...",
            "audio_url": "https://your-audio-link.com/ai-news-summary.mp3"
        },
        {
            "title": "New Tech Gadget Released",
            "summary": "A major tech company has just unveiled its latest gadget...",
            "audio_url": "https://your-audio-link.com/gadget-news-summary.mp3"
        }
    ]
}
```

---

## **Project Directory Structure**

```
tech-news-briefing-app/
    ├── main.py                # Main FastAPI application entry point
    ├── app/
    │   ├── __init__.py        # Initializes the app module
    │   ├── routes.py          # Defines API routes and endpoints
    │   ├── services.py        # Contains business logic for fetching news, summarization, and TTS conversion
    │   ├── models.py          # Defines data models (e.g., request and response schemas)
    │   └── utils.py           # Helper functions (e.g., API request handling)
    ├── requirements.txt       # Python dependencies
    ├── .env                   # Environment variables (API keys, etc.)
    ├── README.md              # Project documentation (this file)
    └── tests/
        ├── test_routes.py     # Tests for API endpoints
        └── test_services.py   # Tests for core services
```

### **Explanation of Key Files**

- **main.py**: Initializes and runs the FastAPI application.
- **app/routes.py**: Defines API routes for fetching tech news, summarizing articles, and generating TTS audio.
- **app/services.py**: Implements the core logic for integrating with News, LLM, and TTS APIs.
- **app/models.py**: Contains data models and schemas for request and response handling.
- **app/utils.py**: Helper functions to streamline API requests, error handling, and data processing.
- **requirements.txt**: Lists the Python packages required for the app.
- **.env**: Stores sensitive information like API keys.
- **tests/**: Contains unit tests for API endpoints and core services.

---

## **How It Works**

1. **Tech News Fetching**: The app retrieves tech articles from the News API.
2. **Summarization**: The article content is sent to the LLM API with a prompt to generate a conversational summary.
3. **Text-to-Speech**: The app uses a TTS API to convert each summary into an audio file.
4. **Output**: The app returns both text summaries and audio URLs for the tech news articles.

---

## **Future Enhancements**

1. **User Authentication**: Allow users to save preferences.
2. **Daily Notifications**: Send daily personalized tech news briefings via email or push notifications.
3. **Mobile App Support**: Create a mobile-friendly version.
4. **Improved UI**: Add a full-featured frontend with dynamic controls.

---

## **Dependencies**

- Python 3.9+
- FastAPI
- Requests
- Python-dotenv
- OpenAI Python Client
- TTS API client library

---

## **Contributing**

Feel free to submit issues or pull requests for new features, bug fixes, or improvements.

---

## **License**

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

