import json

from groq import Groq

from app.config import settings
from app.prompts.prompts import Prompts


class AIService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def _generate(
        self,
        prompt: str,
        json_output: bool = True,
        temperature: float = 0.2,
    ):
        """
        Sends a prompt to Groq.

        If json_output=True:
            Returns a Python dictionary.

        If json_output=False:
            Returns plain text.
        """

        payload = {
            "model": settings.MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": temperature,
        }

        if json_output:
            payload["response_format"] = {
                "type": "json_object"
            }

        response = self.client.chat.completions.create(
            **payload
        )

        content = response.choices[0].message.content

        if json_output:
            return json.loads(content)

        return content.strip()

    ####################################################
    # Ticket Classification
    ####################################################

    def classify(self, ticket: str):

        return self._generate(
            Prompts.classify(ticket)
        )

    ####################################################
    # Information Extraction
    ####################################################

    def extract(self, ticket: str):

        return self._generate(
            Prompts.extract(ticket)
        )

    ####################################################
    # Draft Reply
    ####################################################


    def draft(
        self,
        ticket: str,
        tool_results=None,
        context="",
    ):
        return self._generate(
            Prompts.draft(
                ticket=ticket,
                tool_results=tool_results,
                context=context,
            )
        )

    ####################################################
    # RAG Answer
    ####################################################

    def rag(
        self,
        question: str,
        context: str,
    ):

        return self._generate(
            Prompts.rag(
                question=question,
                context=context,
            ),
            json_output=False,
            temperature=0.1,
        )
    
    def plan(self, ticket):
        return self._generate(
            Prompts.planner(ticket)
        )
    def chat(self, message, history=None):
        if history is None:
            history = []

        conversation = ""
        for item in history:
            conversation += f"""
{item['role']}:
{item['content']}
"""

        prompt = f"""
You are SupportOps AI.

This is the conversation history:

{conversation}

Current User Message:
{message}

Reply naturally and professionally.
"""

        return self._generate(
            prompt,
            json_output=False,
            temperature=0.3
        )