class ProductivityAgent:
    def __init__(self, task_data):
        self.task_data = task_data

    def calculate_tcr(self):
        completed = sum(1 for task in self.task_data if task['status'] == 'completed')
        assigned = len(self.task_data)
        return (completed / assigned) * 100 if assigned > 0 else 0