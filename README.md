# Compliance Checker API

## Overview

The Compliance Checker API is a Flask-based web service that analyzes web content against specified compliance policies. It uses AI models (OpenAI's GPT or Google's Gemini) to perform intelligent compliance checks and report potential violations.

## Features

- RESTful API endpoint for compliance checking
- Support for multiple AI models (OpenAI GPT and Google Gemini)
- Configurable through environment variables
- Detailed violation reporting with policy references and explanations
- Confidence assessment for each compliance check

## Prerequisites

- Python 3.7+
- Flask
- requests
- beautifulsoup4
- python-dotenv
- openai (for OpenAI GPT model)
- google.generativeai (for Google Gemini model)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/compliance-checker-api.git
   cd compliance-checker-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   AI_MODEL=OPENAI  # or GEMINI
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Send a POST request to the `/check-compliance` endpoint:
   ```
   curl -X POST http://localhost:5000/check-compliance \
        -H "Content-Type: application/json" \
        -d '{"webpage_url": "https://example.com", "policy_url": "https://policy-example.com"}'
   ```

3. The API will return a JSON response with the compliance check results:
   ```json
   {
     "results": [
       {
         "violation": "Brief description of violation",
         "policy_reference": "Relevant policy section",
         "content_excerpt": "Excerpt from webpage",
         "explanation": "Detailed explanation of the violation"
       }
     ],
     "confidence_assessment": "Overall assessment of the findings"
   }
   ```

## Configuration

- `AI_MODEL`: Set to either `OPENAI` or `GEMINI` to choose the AI model for compliance checking.
- `OPENAI_API_KEY`: Your OpenAI API key (required if using the OpenAI model).
- `GEMINI_API_KEY`: Your Google Gemini API key (required if using the Gemini model).


## Disclaimer

This tool is designed to assist in compliance checking but should not be considered a substitute for professional legal advice. Always consult with a qualified legal professional for compliance matters.
