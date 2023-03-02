import openai


# Set the API key
openai.api_key = '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'
# Use the ChatGPT model to generate text
model_engine = 'text-davinci-002'
prompt = "could you help me write the code using the zigzag indicator to identify peaks and valleys of choppiness index?"
completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.7)
message = completion.choices[0].text
print(message)