import json

class DialogueManager:
    def __init__(self):
        with open("dialogue_states.json") as f:
            self.states = json.load(f)

    def get_response(self, intent, entities):
        state = self.states[intent]
        response = state["response"]
        for entity in entities:
            response = response.replace(entity[0], entity[1])
        return response