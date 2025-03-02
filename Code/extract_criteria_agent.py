import json
from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

criteria_keys = ['Sold Price', 'Type', 'Year built', 'Heating', 'Cooling',
       'Parking', 'Bedrooms', 'Bathrooms',
       'Elementary School Score', 'Elementary School Distance',
        'Middle School Score', 'Middle School Distance',
      'High School Score', 'High School Distance',
       'Appliances included', 'Laundry features', 'Neighborhood']

class ExtractCriteriaAgent:
    def __init__(self, api_key):
        """Initialize the agent with predefined criteria keys and Azure OpenAI settings"""
        self.criteria_keys = criteria_keys
        self.llm = AzureChatOpenAI(
            azure_endpoint="https://096290-oai.openai.azure.com",
            openai_api_key=api_key,
            deployment_name="team6-gpt4o",
            openai_api_version="2023-05-15",
            model="gpt-4o",
        )

    def extract_criteria(self, user_input):
        """Extracts structured details from user input and maps them to predefined keys"""
        messages = [
            SystemMessage(content=(
                    "You are an AI that extracts structured real estate at Los Angeles search criteria from user input."
                    "Return a JSON object with the following keys: " + ", ".join(self.criteria_keys) + ". "
                    "Only include values explicitly mentioned in the input. If a value is missing, set it to 'unknown'."
                    "If a user explicitly mentions Heating, Parking, or Cooling features in their query, record their preference only Yes or No."
                    "If Heating, Parking, or Cooling are not explicitly mentioned in the user's query, automatically assume Yes for these features."
                    "if the user's budget is mentioned with a K or M (indicating thousands, millions respectively), convert it to a full numerical value."                                                                                                                                                                                                                                                      
                    "Strip out any dollar signs ($) from the budget inputs to maintain numerical clarity and prevent formatting errors."
                    "if the query include number in word form then convert it to a numerical form. (e.g three to 3)"
                    "For the Type, use one of these: Apartment, Condo, MultiFamily, SingleFamily, Townhouse"
                    "If the user does not explicitly mention a specific neighborhood but instead refers to a general location as ‘near’ (e.g., ‘near Mid-City’ or ‘near city center’), return the nearest defined neighborhood. If the user refers to being near the city center, return ‘Downtown LA’ as the neighborhood."
           )),
            HumanMessage(content=user_input)
        ]

        response = self.llm.invoke(messages).content

        cleaned_response = clean_json_string(response)
        try:
            parsed_data = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            parsed_data = {}

        return parsed_data


def clean_json_string(response):
    """Cleans and prepares the JSON string."""
    return response.strip("```json").strip("```").strip()