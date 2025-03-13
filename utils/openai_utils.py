import os
import openai
from pydantic import BaseModel
from typing import List


def openai_chat(prompt):

    my_api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=my_api_key)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            store=True,
            messages=[
                {"role": "user", "content": f"{prompt}"}
            ]
        )
        content = completion.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        name = "Unknown"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        name = "Unknown"
    print(content)

    return content



# Define the Pydantic model for an address
class FamousPerson(BaseModel):
   name: str
   birth_year: str
   description: str

class FamousPeople(BaseModel):
   people: List[FamousPerson]

PROMPT_TEMPLATE = """ {prompt}. For each person get their name, birth year, and a brief two sentence description."""
def openai_chat_famous_people(prompt):
    SYSTEM_PROMPT = "You are a personal assistant."

    my_api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=my_api_key)
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            store=True,
            messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
            {"role": "user", "content": PROMPT_TEMPLATE.format(prompt=prompt)},
            ],
            response_format=FamousPeople
        )
        content = completion.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        name = "Unknown"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        name = "Unknown"
    #print(content)

    return content
