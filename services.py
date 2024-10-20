import json
import os
from abc import ABC, abstractmethod

import openai
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


def get_prompt(policy, webpage_content):
    return """You are an expert Compliance Analyst specializing in regulatory adherence and policy enforcement.
    Your task is to meticulously examine the provided content against a specific compliance policy and identify any potential violations.

    Given the following compliance policy:
    ----- START POLICY -----
    %s
    ----- END POLICY -----

    And the following webpage content to be checked:
    ----- START CONTENT -----
    %s
    ----- END CONTENT -----

    Please follow these steps:

    1. Preprocessing:
       a. Carefully read and process both the policy and the content.
       b. If necessary, restructure the text for improved readability, ensuring no information is lost.

    2. Analysis:
       a. Systematically compare the content against each point in the compliance policy.
       b. Identify any instances where the content may violate or contradict the policy.
       c. Consider both explicit violations and potential implicit non-compliance.

    3. Reporting:
       Compile your findings into a JSON object with the following structure and just return the structure
       {
         "results": [
           {
             "violation": "Concise description of the potential violation (10 words or less)",
             "policy_reference": "Specific section or point in the policy that is potentially violated",
             "content_excerpt": "Brief quote from the content illustrating the potential violation",
             "explanation": "Detailed explanation (50-100 words) of why this might be a violation, including any nuances or contextual factors"
           },
           // Additional violations follow the same structure
         ],
         "confidence_assessment": "A brief overall assessment of your confidence in the findings, highlighting any areas where the policy or content was ambiguous and might require human review."
       }

       If no violations are found, return:
       {
         "results": [],
         "confidence_assessment": "Explanation of why no violations were found and any pertinent observations."
       }

    Remember:
    - Be thorough and consider all aspects of the policy.
    - Maintain objectivity and avoid over-interpretation.
    - If a potential violation is borderline or context-dependent, include it with an explanation of the ambiguity.
    - Ensure your response is a valid JSON object that can be parsed programmatically.

    Important:
    - Your entire response must be a valid JSON object.
    - Do not include any text before or after the JSON object.

    Your analysis should be precise, well-reasoned, and actionable for compliance officers or content creators.
    """ % (policy, webpage_content)


class AIModel(ABC):
    @abstractmethod
    def search(self, query):
        pass


class OpenAIModel(AIModel):
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.Client()

    def search(self, query):
        response = self.client.chat.completions.create(

            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compliance checker assistant."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content


class GeminiAIModel(AIModel):
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')

    def search(self, query):
        response = self.model.generate_content(query)
        return response.text


def check_non_compliance_issues(policy_content, webpage_content) -> dict:
    prompt = get_prompt(policy_content, webpage_content)
    ai_model = GeminiAIModel()
    results = ai_model.search(prompt)
    print(results)
    results = results.replace('`', '')
    return json.loads(results)
