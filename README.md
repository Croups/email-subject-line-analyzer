# Email Subject Line Analyzer

A simple AI-powered email subject line analyzer using Pydantic-AI with agent structure. This tool analyzes email subject lines considering sender context and provides structured insights about priority, sentiment, and required actions.

## Features
- Context-aware email subject analysis
- Structured response with priority levels
- Sentiment analysis
- Action requirement detection
- Keyword extraction

## Installation
```bash
pip install -r requirements.txt
```

## Example Usage
```bash
email = EmailContext(
    sender_email="sample@gmail.com",
    sender_name="John Doe",
    department="software"
)
        
result = agent3.run_sync(
    user_prompt="Code Review Needed for project #1234 ASAP",
    deps=email
)

print(result.data.model_dump_json(indent=2))
```

## Credits
This project is inspired by [Pydantic-AI-Tutorial](https://github.com/daveebbelaar/pydantic-ai-tutorial) example by Dave Ebbelaar. Special thanks for the concepts and implementation ideas.
