# planning_agent.py

class PlanningAgent:
    def provide_plan(self, summarized_data, selected_crop, additional_input=None):
        """
        Provides a sustainable growing plan for the selected crop using real-time data.
        """
        user_data = summarized_data.get("user", {})
        location = user_data.get("location", "your area")
        plan = f"Growing Plan for {selected_crop} in {location}:\n"
        plan += "- Use organic fertilizers and integrated pest management strategies.\n"
        plan += "- Optimize irrigation based on local rainfall and water availability.\n"
        plan += "- Practice crop rotation to maintain soil fertility.\n"
        plan += "- Monitor local weather forecasts for optimal planting and harvesting.\n"
        if additional_input:
            plan += f"\nAdditional Recommendations: {additional_input}\n"
        return plan
