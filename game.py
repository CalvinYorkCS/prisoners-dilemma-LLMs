from agents import Agent

class Game:
    def __init__(self, args):
        self.args = args
        self.alice = Agent(args, 'Alice')
        self.bob = Agent(args, 'Bob')

    def play(self):
        for round in range(self.args.max_negotiation_round):
            if self.args.who_first == 'Alice':
                alice_message = self.alice.negotiate()
                if alice_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_messages.append('Alice said in round {}: '.format(round+1)+alice_message)
                self.bob.previous_messages.append('Alice said in round {}: '.format(round+1)+alice_message)
                bob_message = self.bob.negotiate()
                if bob_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_messages.append('Bob replied in round {}: '.format(round+1)+bob_message)
                self.bob.previous_messages.append('Bob replied in round {}: '.format(round+1)+bob_message)
            else:
                bob_message = self.bob.negotiate()
                if bob_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_messages.append('Bob said in round {}: '.format(round+1)+bob_message)
                self.bob.previous_messages.append('Bob said in round {}: '.format(round+1)+bob_message)
                alice_message = self.alice.negotiate()
                if alice_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_messages.append('Alice replied in round {}: '.format(round+1)+alice_message)
                self.bob.previous_messages.append('Alice replied in round {}: '.format(round+1)+alice_message)
        alice_action = self.alice.make_action()
        bob_action = self.bob.make_action()
        return alice_action, bob_action