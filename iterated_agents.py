from openai import OpenAI
from payoffs import payoff_matrix
import time
from prompts import Prompts
from collections import defaultdict
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

class Iterated_Agent:
    def __init__(self, args, name):
        self.args = args
        self.name = name
        self.other_agent = 'Bob' if name == 'Alice' else 'Alice'
        self.previous_messages = []
        self.actions = list(payoff_matrix[self.args.payoff][self.name].keys())
        self.system_prompt, self.game_setting, self.action_prompt, self.negotiation_prompt = self.get_prompts()
        self.memory_len = self.args.memory_len
        self.actions_only_memory = self.args.actions_only_memory
        self.memory_dict = defaultdict(lambda: ([], []))

    def get_prompts(self):
        prompts = Prompts(self.args, self.name)
        if self.args.game_setting_choice == 'iterated_game':
            return prompts.iterated_game_setting()
        elif self.args.game_setting_choice == 'business_partnership':
            return prompts.business_partnership_setting()
        elif self.args.game_setting_choice == 'security_negotiation':
            return prompts.security_negotiation_setting()
        else:
            raise ValueError(f"Invalid game setting choice: {self.args.game_setting_choice}")
        
    def get_memory(self, current_iter):
        # Create memory message from the last memory_len iteration's messages and/or actions
        current_memory = []
        min_iter = max(0, current_iter - self.memory_len)
        for i in range(min_iter, current_iter + 1):
            iter_messages, iter_actions = self.memory_dict[f"iteration_{i+1}"]
            current_memory.append(f"Iteration {i+1} messages:")
            if not self.actions_only_memory and iter_messages:
                current_memory.append('\n'.join(iter_messages))
            if iter_actions:
                current_memory.append('\n'.join(iter_actions))
        return '\n\n'.join(current_memory) + '\n\n'

    def make_action(self, iter):
        action_prompt = self.action_prompt
        if self.memory_dict:
            current_memory = "\n### Memory\n\nIt is now iteration {}. \
                Your memory of previous messages and iterations is presented below:\n".format(iter+1) + self.get_memory(iter)
            action_prompt = current_memory + '\n' + action_prompt

        action_prompt = self.game_setting + '\n' + action_prompt
        while True:
            try:
                action_message = call_api(self.args.model, action_prompt, self.system_prompt)
                action = parse_action(action_message, self.actions)
                return action 
            except:
                time.sleep(0.1)
    
    def negotiate(self, iter):
        negotiate_prompt = self.negotiation_prompt
        if self.memory_dict:
            current_memory = "\n\nThe existing iterations, rounds of negotiation, and actions are presented below:\n" + self.get_memory(iter)
            negotiate_prompt += current_memory
        negotiate_prompt = self.game_setting + negotiate_prompt
        while True:
            try:
                message = call_api(self.args.model, negotiate_prompt, self.system_prompt)
                message = parse(message)
                return message
            except:
                time.sleep(0.1)