import os
import json
from qdrant_client import QdrantClient

from interacting_agent import InteractingAgent
from extract_criteria_agent import ExtractCriteriaAgent
from exploring_agent import ExploringAgent
from recommendation_agent import RecommendationAgent

def load_env_file(filepath=".env"):
    """
    Load key-value pairs from a .env file into environment variables.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist.")

    with open(filepath, "r") as file:
        for line in file:
            # Ignore empty lines and comments
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value.strip()


# Function to format and print recommendations
def Generate_response(recommendations):
    print("=" * 60)
    print("🏡 Property Recommendations 🏡".center(60))
    print("=" * 60)
    
    for rank, details in recommendations.items():
        print(f"\n🔹 Rank: {rank[-1]} | Score: {details['score']}")
        print("-" * 60)
        print(f"🏠 Description: {details['description']}")
        print(f"📝 Explanation: {details['explanation']}")
        print("=" * 60)

if __name__ == "__main__":
    # Load environment variables and API key
    load_env_file()
    api_key = os.getenv("API_KEY")

    collection_name = "realestate_ai_final"
    qdrant_client = QdrantClient(
        url="https://00408636-7100-4931-aaec-7626a00437cc.eu-central-1-0.aws.cloud.qdrant.io:6333",
        api_key="DU1L3IyEuy5m3_6pFj4UaIMao6kAiVc5CgLYrGRpyZ5ClXLMIPRxFg",
    )

    interacting_agent = InteractingAgent(api_key)
    extract_criteria_agent = ExtractCriteriaAgent(api_key)
    exploring_agent = ExploringAgent(api_key, qdrant_client, collection_name)
    recommendation_agent = RecommendationAgent(api_key)

    user_query = input("What kind of property are you looking for in Los Angeles?\n")

    final_user_input = interacting_agent.chat_with_user(user_query)
    structured_criteria = extract_criteria_agent.extract_criteria(final_user_input)
    estate_dict = exploring_agent.get_estates_list(structured_criteria)
    final_recommendations = recommendation_agent.generate_recommendation(final_user_input, estate_dict)
    Generate_response(final_recommendations)

