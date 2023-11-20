import json
import os

files=["knowledge.docx","membership.docx","policies.docx","facilities.docx","faq.docx","equipment.docx","refreshments.docx","menu.docx","cancellation.docx","schedule.docx","services.docx"]

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    files_upload=[]
    for file in files:
      file_result = client.files.create(file=open(f"./models/{file}", "rb"),
                               purpose='assistants')
      files_upload.append(file_result.id)

    assistant = client.beta.assistants.create(instructions="""
          You are an AI assistant, Ally from Orchid Gym, that has been programmed to help the users to answer questions about Orchid Gym, like pricing information and schedule a visit. Please be concise and give short answers, always in first person. 
          A series of documents have been provided with information on Orchid Gym prices and general information. Please review each document before submitting an answer.
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              name="Orchid Gym",
                                              file_ids=files_upload)

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      assistant_id = assistant.id
      print(f"Created a new assistant and saved the ID: {assistant_id}")

      assistant_id = assistant.id

  return assistant_id
