from google import genai
from google.genai import types
import os
from pydantic import BaseModel
from typing import List

def gemini_chat(prompt):

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response 

# Define the Pydantic model for an address
class FamousPerson(BaseModel):
   name: str
   birth_year: str
   description: str

class FamousPeople(BaseModel):
   people: List[FamousPerson]

def gemini_chat_famous_people(prompt):

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=FamousPeople,
        ),
    )

    return response.text


# prompt = "Name 3 famous athletes born on March 13. For each person get their name, birth year, and a brief two sentence description."
# response = gemini_chat_famous_people(prompt)
# print(response)
