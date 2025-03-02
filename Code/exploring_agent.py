import json

from create_embeddings import get_azure_embeddings
from extract_criteria_agent import clean_json_string
from langchain_openai import AzureChatOpenAI

class ExploringAgent:
    def __init__(self, api_key, qdrant_client, collection_name):
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name
        self.api_key = api_key
        self.llm = AzureChatOpenAI(
            azure_endpoint="https://096290-oai.openai.azure.com",
            openai_api_key=api_key,
            deployment_name="team6-gpt4o",
            openai_api_version="2023-05-15",
            model="gpt-4o",
        )

    def format_query(self, criteria: dict):
        filtered_values=[]
        for key, value in criteria.items():
            if str(value).lower() in ["unknown", "none", "nan"]:
                value = ''
            filtered_values.append( f"{key}: {value}")
        return ", ".join(filtered_values)

    def search_estates(self, response, top_k=5):
        query_text = self.format_query(response)
        query_embedding = get_azure_embeddings(query_text, self.api_key)

        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        return [hit.payload for hit in results]



    def generate_descriptions(self, estates):
        """
        Uses LLM to generate a natural language description of the retrieved estates.
        Returns descriptions as a JSON dictionary.
        """
        # Clean estate data (remove missing or NaN values)
        filtered_estates = []
        for estate in estates:
            cleaned_estate = {k: v for k, v in estate.items() if v and str(v).lower() != "nan"}  # Remove empty attributes
            filtered_estates.append(cleaned_estate)

        # Create a structured prompt for the LLM
        prompt = f"""
        Convert the following real estate listings into a structured JSON dictionary, 
        where each property is given a unique key like 'estate1', 'estate2', etc., 
        and the value is a readable description of the property, make sure to put the value just the description:

        {json.dumps(filtered_estates, indent=2)}

        The response must be in valid JSON format.
        """

        response = self.llm.invoke(prompt).content
        response = clean_json_string(response)

        try:
            descriptions = json.loads(response)
        except json.JSONDecodeError:
            print("Error: LLM did not return valid JSON.")
            descriptions = {}

        return descriptions

    def get_estates_list(self, response, top_k=5):
        retrieved_estates = self.search_estates(response, top_k)
        return self.generate_descriptions(retrieved_estates)