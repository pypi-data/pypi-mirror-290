import os
import json
from memgpt import Admin
from memgpt import create_client
from memgpt.memory import ChatMemory
from memgpt.utils import get_human_text

def ask_to(self, agent_name: str, question: str, address:str) -> str:
    """
    Ask a question to an agent and return the response value.

    :param agent_name: The name of the agent
    :type agent_name: str
    :param question: The question to be sent to the API.
    :type question: str
    :param address: The address hostname:port to be sent to the API.
    :type address: str
    :return: The response from the API as a string.
    :rtype: str
    :raises requests.HTTPError: If the request to the API returns a status code indicating an error.
    :raises requests.RequestException: If there is an error making the request.

    Example usage:
    ask_to("isp_hr_expert", "What is the vacation policy?", "localhost:8898")
    """
    import requests

    api_url = f'http://{address}/api/v1/ask'
    params = {'agent_name': agent_name, 'question': question}

    response = requests.get(api_url, params=params)
    return response.text

def verify(self, agent_name: str, address:str) -> str:
    """
    Verify connection with an agent and return the response value.

    :param agent_name: The name of the agent
    :type agent_name: str
    :param address: The address hostname:port to be sent to the API.
    :type address: str
    :return: The response from the API as a string.
    :rtype: str
    :raises requests.HTTPError: If the request to the API returns a status code indicating an error.
    :raises requests.RequestException: If there is an error making the request.

    Example usage:
    verify("isp_hr_expert", "localhost:8898")
    """
    import requests

    api_url = f'http://{address}/api/v1/verify'

    response = requests.get(api_url)
    return response.text
    

class memGPT():

    def __init__(self,name:str,human:str,persona:str,base_url=os.getenv("MEMGPT_BASEURL", default="http://localhost:8083")) -> None:
        _, k = self._get_memGPT_credential()
        self._client = create_client(base_url=base_url,token=k)

        # chatmemory = ChatMemory(human=human, persona=persona)
        # chatmemory.core_memory_append("human","Name: Emmanuele")
        # chatmemory.core_memory_append("persona","Name: agentBUDDY")

        tools = []
        for tool in [ask_to,verify]:
            tools.append(self._client.create_tool(tool, tags=["extras"]).name)

        self._agent_client = self._client.create_agent(
                # memory = chatmemory,
                metadata = {"human:": human, "persona": persona},
                tools=tools,
            ).id

    def _get_memGPT_credential(self):
        # admin = Admin(base_url=os.getenv("MEMGPT_BASEURL", default="http://localhost:8083"), token="password")
        # response = admin.create_user()
        user_id = None # response.user_id # unique UUID for the user 
        api_key = os.getenv("MEMGPT_KEY", default="sk-") # response.api_key # bearer token for authentication
        return user_id, api_key

    def _handle_message(self,messages):
        response = None
        for message in messages:
            if 'internal_monologue' in message:
                print("Internal Monologue:", message['internal_monologue'])
            elif 'function_call' in message:
                try:
                    function_arguments = json.loads(message['function_call']['arguments'])
                    print(f"Function Call ({message['function_call']['name']}):", function_arguments)
                    if message['function_call']['name'] == 'send_message':
                        response = function_arguments['message']
                except json.JSONDecodeError:
                    print("Function Call:", message['function_call'])
            elif 'function_return' in message:
                print("Function Return:", message['function_return'])
            else:
                print("Message:", message)
                # TODO warning
                return message
        return response

    def _send_message(self, question):
        response = self._client.user_message(agent_id=self._agent_client, message=question)
        return response.messages, response.usage
    
    def notify(self, news):
        # TODO problem, la risposta non arriva sempre nella function call.
        message, usage = self._send_message(news)
        return message

    def ask(self, question):
        # TODO problem, la risposta non arriva sempre nella function call.
        request =f"without more question about it, search in your archival memory and give an accurate response to the question: {question}. give me the response always in the function call with the send_message. respond without any comment or disclaimer."
        message, usage = self._send_message(request)
        response = self._handle_message(message)
        return str(response)
    
    def request(self, agents,request):
        # TODO problem, la risposta non arriva sempre nella function call.
        instructions = f"""You are the coordinator of these agents which you can call with the function ask_to: {str(agents)}. 
        The user has made the following request: {request}. 
        Break down the request into steps and for each part, try to use at least one agent. 
        Then try to response to the quesiton."""
        # Provide in JSON format, without commenting, the following structure: 
        # {{'observation': 'observation', 'questions': [('question', 'agent_name')]}}
        # In the observation field, insert a description of what you have decided."""
        message, usage = self._send_message(instructions)
        response = self._handle_message(message)
        return str(response)
    
    def create_source(self, name):
        source = self._client.create_source(name=name)
        return source.id
    
    def add_file_to_source(self, source_id, filename):
        self._client.load_file_into_source(filename=filename, source_id=source_id)
        self._client.attach_source_to_agent(source_id=source_id, agent_id=self._agent_client)
        