import json
from langchain.chat_models import AzureChatOpenAI
from extract_criteria_agent import clean_json_string


class RecommendationAgent:
    def __init__(self, api_key):
        self.llm = AzureChatOpenAI(
            azure_endpoint="https://096290-oai.openai.azure.com",
            openai_api_key=api_key,
            deployment_name="team6-gpt4o",
            openai_api_version="2023-05-15",
            model="gpt-4o",
        )

    def score_estates(self, user_input, estates):
        """
        Scores each estate based on how well it matches user input.
        Uses LLM to compare the descriptions with user preferences.
        """
        prompt = f"""
        You are a real estate recommendation system.
        The user is looking for properties with the following preferences:

        {json.dumps(user_input, indent=2)}

        Below are property descriptions retrieved by the Exploring Agent.
        Score each property from 1-10 based on how well it matches the user's needs.

        {json.dumps(estates, indent=2)}

        Return a JSON object where keys are estate IDs, and values are scores from 1-10.
        The response must be in valid JSON format, without anything else.
        """

        response = self.llm.invoke(prompt).content
        response = clean_json_string(response)
        try:
            scores = json.loads(response)  # Parse JSON response
        except json.JSONDecodeError:
            print("Error: LLM did not return valid JSON.")
            scores = {}

        return scores

    def rank_estates(self, estates, scores):
        """
        Sorts estates based on scores in descending order.
        """
        ranked_estates = sorted(estates.items(), key=lambda x: scores.get(x[0], 0), reverse=True)
        return {f"rank_{i + 1}": {"estate_id": estate[0], "description": estate[1], "score": scores.get(estate[0], 0)}
                for i, estate in enumerate(ranked_estates)}

    def generate_recommendation(self, user_input, estates):
        """
        Returns a final, ranked list of properties with explanations.
        """
        scores = self.score_estates(user_input, estates)
        ranked_estates = self.rank_estates(estates, scores)

        # Generate explanations for the ranking
        prompt = f"""
        The following properties have been ranked based on the user's preferences.
        Generate a brief explanation for why each property was ranked in its position.

        {json.dumps(ranked_estates, indent=2)}

        Return a JSON object where each key is the rank (e.g., "rank_1") and the value contains:
        - The estate description (description)
        - The score (score)
        - A short explanation for why it is ranked in this position. (explanation)

        The response must be in valid JSON format, without anything else.
        """

        response = self.llm.invoke(prompt).content
        response = clean_json_string(response)
        try:
            final_recommendations = json.loads(response)  # Parse JSON response
        except json.JSONDecodeError:
            print("Error: LLM did not return valid JSON.")
            final_recommendations = ranked_estates  # Fallback to ranked list without explanations

        return final_recommendations