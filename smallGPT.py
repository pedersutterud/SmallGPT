
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
      
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01"
)

#Dictionary list for our messages
messages_array = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]

#Initialize variables for the promt and completion tokens
prompt_token_count = int()
completion_token_count = int()

while True:
    user_input = input("Enter a question (type 'exit' to exit): ")
    if user_input.lower() == "exit":
        break
      
    messages_array.append({"role": "user", "content": user_input})
    
    completion = client.chat.completions.create(
        model=deployment,
        max_tokens=500,
        temperature=0.5,
        messages=messages_array
    )

    prompt_token_count += completion.usage.prompt_tokens
    completion_token_count += completion.usage.completion_tokens

    completion_message = completion.choices[0].message.content
    messages_array.append({"role": "assistant", "content": completion_message})

    print("> " + completion_message + "\n")
      
print("Have a great day. Nice chatting with you!")
print("Prompt tokens " + str(prompt_token_count) + ", complettion tokens " + str(completion_token_count))

print("Your chat history was: \n")
for msg_entry in messages_array:
    print(msg_entry)