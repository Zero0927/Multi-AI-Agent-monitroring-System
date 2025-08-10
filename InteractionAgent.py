class InteractionAgent:
    def __init__(self, chat_data):
        self.chat_data = chat_data

    def calculate_ci(self):
        replies = sum(1 for msg in self.chat_data if msg['replied'])
        total_msgs = len(self.chat_data)
        return replies / total_msgs if total_msgs > 0 else 0