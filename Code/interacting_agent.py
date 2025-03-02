from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class InteractingAgent:
    def __init__(self, api_key):
        self.llm = AzureChatOpenAI(
            azure_endpoint="https://096290-oai.openai.azure.com",
            openai_api_key=api_key,
            deployment_name="team6-gpt4o",
            openai_api_version="2023-05-15",
            model="gpt-4o",
        )
        self.required_fields = ["budget", "bedrooms", "bathrooms"]

    def chat_with_user(self, user_query):
        """Handles conversation to get all necessary real estate details"""
        conversation_history = [HumanMessage(content=user_query)]

        while True:
            # Ask the LLM if all key details are present
            messages = [
                           SystemMessage(content=(
                               "You are an AI assistant helping users find real estate in Los Angeles." # 
                               "If the user's input lacks necessary features: budget, number of bedrooms, number of bathrooms. ask a follow-up question to get the missing details. "
                               "Write the input without any extras, just keep it simple"
                               "Continue asking until you have all the necessary information. If the user does not have preferences for any other feature that are not necessary features do not ask"
                           ))
                       ] + conversation_history  # Include previous messages for context

            response = self.llm.invoke(messages).content
            print(f"AI: {response}")  # Simulate chatbot response

            # Ask the user for a response if details are still missing
            if "?" in response:
                user_input = input("You: ")  # Get the next user input
                conversation_history.append(HumanMessage(content=user_input))
            else:
                return response  # Final user input with complete details