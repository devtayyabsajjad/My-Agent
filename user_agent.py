# user_agent.py

class UserConversationAgent:
    def __init__(self):
        self.user_data = {}

    def collect_user_input(self, form_data):
        """
        Collects user input (budget, resources, location, soil type, water availability,
        and equipment) and returns it as a dictionary.
        """
        self.user_data = form_data
        return self.user_data
