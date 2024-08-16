import requests
from datetime import datetime
import json
import uuid
import time

class SinopsisAI:
    """
    SinopsisAI SDK for managing conversation sessions and interacting with the Sinopsis AI backend API.
    
    Attributes:
        api_key (str): The API key for authenticating requests.
        backend_url (str): The base URL for the Sinopsis AI API.
        headers (dict): Headers used in API requests, including authorization.
        session (dict): The current session, including user, session ID, conversation ID, and chat history.
    """

    def __init__(self, api_key=None):
        """
        Initializes the SinopsisAI instance.
        
        Args:
            api_key (str): The API key required to authenticate requests.
        
        Raises:
            ValueError: If no API key is provided.
        """
        if not api_key:
            raise ValueError("API key is required to initialize SinopsisAI.")
        
        self.api_key = api_key
        self.backend_url = 'https://sinopsis-ai-api-9739a6f1a007.herokuapp.com'
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session = None  # Session will be initialized in start_session()

    def start_session(self, user=None, session_id=None, conversation_id=None):
        """
        Starts a new session by initializing session attributes.
        
        Args:
            user (str): The unique identifier for the user. Defaults to a random UUID if not provided.
            session_id (str): The unique session identifier. Defaults to a random UUID if not provided.
            conversation_id (str): The unique conversation identifier. Defaults to a random UUID if not provided.
        
        Returns:
            dict: The initialized session dictionary.
        """
        self.session = {
            "chat_history": [],
            "user": user or uuid.uuid4().hex,
            "session_id": session_id or uuid.uuid4().hex,
            "conversation_id": conversation_id or uuid.uuid4().hex
        }
        self._retrieve_existing_chat_history()
        return self.session

    def end_session(self):
        """
        Ends the current session by clearing session attributes.
        
        Returns:
            bool: True if the session was ended successfully, False if there was no active session.
        """
        if self.session:
            self.update_conversation_in_db()  # Ensure conversation is updated before ending session
            self.session = None
            return True
        return False

    def _make_request(self, endpoint, payload, retries=3, delay=2):
        """
        Makes an API request with error handling and retries.
        
        Args:
            endpoint (str): The API endpoint to send the request to.
            payload (dict): The JSON payload to include in the request body.
            retries (int): Number of times to retry the request in case of failure. Defaults to 3.
            delay (int): Delay in seconds between retries. Defaults to 2.
        
        Returns:
            dict or None: The JSON response from the API if successful, None otherwise.
        """
        for attempt in range(retries):
            try:
                response = requests.post(f'{self.backend_url}/{endpoint}', json=payload, headers=self.headers)
                response.raise_for_status()  # Raises an HTTPError if the response status is 4xx, 5xx

                return response.json() if response.status_code == 200 else None

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                if response.status_code in [500, 502, 503, 504]:  # Server-side errors
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    break  # Non-recoverable error, exit loop

            except requests.exceptions.ConnectionError as conn_err:
                print(f"Connection error occurred: {conn_err}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

            except requests.exceptions.Timeout as timeout_err:
                print(f"Timeout error occurred: {timeout_err}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

            except requests.exceptions.RequestException as req_err:
                print(f"An error occurred: {req_err}")
                break  # Non-recoverable error, exit loop

        return None

    def _retrieve_existing_chat_history(self):
        """
        Retrieves the existing chat history for the current conversation from the API.
        
        If the retrieval is successful, the chat history is stored in the session. 
        If not, the chat history is set to an empty list.
        """
        if not self.session:
            raise ValueError("No active session. Please start a session first.")

        payload = {
            'conversation_id': self.session['conversation_id'],
            'api_key': self.api_key
        }

        chat_history = self._make_request('retrieve_chat_history', payload)
        if chat_history:
            self.session['chat_history'] = chat_history
        else:
            self.session['chat_history'] = []

    def update_conversation_in_db(self):
        """
        Updates the current conversation in the database by sending the session data to the API.
        
        Prints an error message if the update fails.
        """
        if not self.session:
            raise ValueError("No active session. Please start a session first.")

        payload = {
            'api_key': self.api_key,
            'session': self.session
        }

        result = self._make_request('update_conversation_in_db', payload)
        if result is None:
            print("Error updating conversation in database.")

    def log_prompt(self, user_input):
        """
        Logs a user prompt in the session's chat history and updates the conversation in the database.
        
        Args:
            user_input (str): The user's input message to log.
        """
        if not self.session:
            raise ValueError("No active session. Please start a session first.")

        timestamp = datetime.utcnow().isoformat()
        self.session['chat_history'].append({
            "role": "User",
            "user": self.session['user'],
            "message": user_input,
            "timestamp": timestamp
        })
        self.update_conversation_in_db()

    def log_response(self, assistant_response, chatbot_name, model_name, model_input):
        """
        Logs an assistant's response in the session's chat history and updates the conversation in the database.
        
        Args:
            assistant_response (str): The response message from the assistant to log.
            chatbot_name (str): The name of the chatbot generating the response.
            model_name (str): The name of the model used to generate the response.
            model_input (dict): The input data used by the model to generate the response.
        """
        if not self.session:
            raise ValueError("No active session. Please start a session first.")

        timestamp = datetime.utcnow().isoformat()
        input_string = json.dumps(model_input)
        self.session['chat_history'].append({
            "role": "Assistant",
            "message": assistant_response,
            "timestamp": timestamp,
            "chatbot_name": chatbot_name,
            "model_name": model_name,
            "model_input": input_string
        })
        self.update_conversation_in_db()