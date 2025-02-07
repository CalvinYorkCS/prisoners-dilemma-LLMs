from openai import OpenAI
from payoffs import payoff_matrix
import time
from prompts import Prompts
import os

def call_api(model, message, system_prompt):
    open_ai_key = os.getenv('OPENAI_API_KEY')

    openai_client = OpenAI(api_key=open_ai_key)
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=1.0,
        max_tokens=2000,
    )
    return response.choices[0].message.content

def parse(message):
    assert '<s>' in message and '</s>' in message 
    start = message.index('<s>') + len('<s>')
    end = message.index('</s>')
    return message[start:end]

def parse_action(message, choices):
    assert '<s>' in message and '</s>' in message 
    start = message.index('<s>') + len('<s>')
    end = message.index('</s>')
    action = message[start:end].strip('\n').strip()
    assert action in choices
    return message[start:end]

class Agent:
    def __init__(self, args, name):
        self.args = args
        self.name = name
        self.other_agent = 'Bob' if name == 'Alice' else 'Alice'
        self.previous_messages = []
        self.actions = list(payoff_matrix[self.args.payoff][self.name].keys())
        self.system_prompt, self.game_setting, self.action_prompt, self.negotiation_prompt = self.get_prompts()

    def get_prompts(self):
        prompts = Prompts(self.args, self.name)
        if self.args.game_setting_choice == 'game':
            return prompts.game_setting()
        elif self.args.game_setting_choice == 'prisoner':
            return prompts.prisoner_setting()
        elif self.args.game_setting_choice == 'corporate_transparency':
            return prompts.corporate_transparency_setting()
        else:
            raise ValueError(f"Invalid game setting choice: {self.args.game_setting_choice}")

    def make_action(self):
        action_prompt = self.action_prompt
        if self.previous_messages:
            previous_messages = "\n### Negotiation Messages\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_messages)
            action_prompt = previous_messages + '\n' + action_prompt

        action_prompt = self.game_setting + '\n' + action_prompt
        while True:
            try:
                action_message = call_api(self.args.model, action_prompt, self.system_prompt)
                action = parse_action(action_message, self.actions)
                return action 
            except:
                time.sleep(0.1)
    
    def negotiate(self):
        negotiate_prompt = self.negotiation_prompt
        if self.previous_messages:
            previous_messages = "\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_messages)
            negotiate_prompt += previous_messages
        negotiate_prompt = self.game_setting + negotiate_prompt
        while True:
            try:
                message = call_api(self.args.model, negotiate_prompt, self.system_prompt)
                message = parse(message)
                return message 
            except:
                time.sleep(0.1)