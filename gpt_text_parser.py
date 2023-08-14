import re, os
from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot

load_dotenv()

def retrieve_information(disease: str):
    with open(os.path.join(os.path.dirname(__file__), "dictionary_example.txt"), "r") as fh:
        request_string = str(fh.read())

    chatbot = Chatbot(config={"access_token": os.getenv("ACCESS_TOKEN")})

    prompt = (
        f"Is {disease} an existing disease/illness? if it is a disease/illness, "\
        f"provide an overview of the given disease and respond with dictionary "\
        f"same in style as the one provided below. if it is not a disease/illness, "\
        f"return an empty dictionary. do not provide anything other than the dictionary."
        + request_string + disease
    )

    response = ""
    for data in chatbot.ask(prompt):
        response = data["message"]

    try:
        pattern = r"\{.*$"
        matches = re.findall(pattern, response, re.DOTALL)

        pre_json = matches[0]

        pattern = r"^.*\}"
        matches = re.findall(pattern, pre_json, re.DOTALL)

        json = matches[0]
        return json
    
    except:
        return "{\"existing\": 0}"

# print(create_meeting("meeting in pakistan tomorrow at 11am"))
