# best_crop_agent.py

from camel.agents import ChatAgent  # Requires camel-ai package
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig

class BestCropRecommendationAgent:
    def __init__(self):
        # Create a model using Camel AI's ModelFactory with your desired settings.
        self.model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI,
            model_config_dict=ChatGPTConfig().as_dict,
        )
        # Prepare a base system message.
        self.system_msg = BaseMessage.make_assistant_message(
            role_name="Crop Advisor",
            content="You are a world-class agricultural expert. Provide crop recommendations based on environmental and economic factors.",
        )
        # Initialize the chat agent.
        self.chat_agent = ChatAgent(system_message=self.system_msg, model=self.model)

    def recommend_crops(self, summarized_data):
        """
        Constructs a prompt from real-time user and API data and uses Camel AI to generate crop recommendations.
        """
        user_data = summarized_data.get("user", {})
        api_data = summarized_data.get("api", {})

        soil_type = user_data.get("soil_type", "unknown").lower()
        water_availability = user_data.get("water_availability", "unknown").lower()
        try:
            budget = float(user_data.get("budget", "0"))
        except ValueError:
            budget = 0
        temperature = api_data.get("environmental", {}).get("temperature", 25)
        rainfall = api_data.get("environmental", {}).get("rainfall", 0)
        average_income = api_data.get("economic", {}).get("average_income", 0)
        crop_prices = api_data.get("economic", {}).get("crop_prices", {})

        prompt = f"""
Based on the following real-time data:
- Soil Type: {soil_type}
- Water Availability: {water_availability}
- Budget: {budget}
- Average Income: {average_income}
- Temperature: {temperature}°C
- Rainfall: {rainfall} mm
- Crop Prices: {crop_prices}

Please recommend five crops that are both economically viable and environmentally suitable. Return your answer as a comma-separated list.
"""
        response = self.chat_agent.get_response(prompt)
        recommendations = [crop.strip() for crop in response.split(",") if crop.strip()]
        if len(recommendations) < 5:
            # Fallback rule-based recommendation (if needed)
            if soil_type in ["loamy", "silty"] and water_availability in ["high", "medium"]:
                recommendations = ["Rice", "Soybean", "Corn", "Wheat", "Barley"]
            elif soil_type in ["sandy", "clay"] or water_availability == "low":
                recommendations = ["Wheat", "Barley", "Millet", "Sorghum", "Oats"]
            else:
                recommendations = ["Corn", "Rice", "Wheat", "Soybean", "Barley"]
        return recommendations[:5]
