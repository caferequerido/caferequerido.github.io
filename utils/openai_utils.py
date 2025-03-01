import os
import openai


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
