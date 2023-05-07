import json
import openai

with open("APIKEYS.json", 'r') as f:
    data = json.load(f)
    api_key = data["GPT_api_key"]
    openai.api_key = api_key


def form_prompt(prompt, sentence_quantity):
    return f'''Привет, можешь, пожалуйста, выделить самое главное в этом тексте''' + f'''и написать это
     в {sentence_quantity} предложениях: {prompt}.'''


def request(prompt, sentence_quantity):
    prompt = form_prompt(prompt, sentence_quantity)
    print(prompt)
    return openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text
