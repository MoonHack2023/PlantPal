import openai
import time

openai.api_key = "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"
# insert your api key

model_engine = "text-davinci-003"
prompt = "Give me the optimum temperature, humidity, water, light and carbon dioxide conditions for growing a  "

prompt = "Give me the optimum temperature, humidity, carbon dioxide, tvoc and wavlength of light conditions for growing a   "
plant_name = input("Enter plant name: ")
prompt = prompt + plant_name + "as a comma separated string"
completion = openai.Completion.create(
    engine = model_engine,
    prompt = prompt,
    max_tokens = 1024,
    n=1,
    stop = None,
    temperature=0.5,)


response = completion.choices[0].text
print(response)