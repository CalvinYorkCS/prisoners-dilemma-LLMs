from iterated_agents import Iterated_Agent

class Iterated_Game:
    def __init__(self, args):
        self.args = args
        self.alice = Iterated_Agent(args, 'Alice')
        self.bob = Iterated_Agent(args, 'Bob')

    def play(self):
        game_history = []
        for iter in range(self.args.num_iterations):
            game_history.append({})
            for round in range(self.args.max_negotiation_round):
                if self.args.who_first == 'Alice':
                    alice_message = self.alice.negotiate(iter)
                    if alice_message == '<s>halt negotiation</s>':
                        print(f"HALTED NEGOTIATION::: {alice_message}")
                        break
                    self.alice.memory_dict[f"iteration_{iter+1}"][0].append('Alice said in round {}: '.format(round+1)+alice_message)
                    self.bob.memory_dict[f"iteration_{iter+1}"][0].append('Alice said in round {}: '.format(round+1)+alice_message)
                    bob_message = self.bob.negotiate(iter)
                    if bob_message == '<s>halt negotiation</s>':
                        print(f"HALTED NEGOTIATION::: {bob_message}")
                        break
                    self.alice.memory_dict[f"iteration_{iter+1}"][0].append('Bob replied in round {}: '.format(round+1)+bob_message)
                    self.bob.memory_dict[f"iteration_{iter+1}"][0].append('Bob replied in round {}: '.format(round+1)+bob_message)
                else:
                    bob_message = self.bob.negotiate(iter)
                    if bob_message == '<s>halt negotiation</s>':
                        break
                    self.alice.memory_dict[f"iteration_{iter+1}"][0].append('Bob said in round {}: '.format(round+1)+bob_message)
                    self.bob.memory_dict[f"iteration_{iter+1}"][0].append('Bob said in round {}: '.format(round+1)+bob_message)
                    alice_message = self.alice.negotiate(iter)
                    if alice_message == '<s>halt negotiation</s>':
                        break
                    self.alice.memory_dict[f"iteration_{iter+1}"][0].append('Alice replied in round {}: '.format(round+1)+alice_message)
                    self.bob.memory_dict[f"iteration_{iter+1}"][0].append('Alice replied in round {}: '.format(round+1)+alice_message)
            alice_action = self.alice.make_action(iter)
            bob_action = self.bob.make_action(iter)

            # Add actions to agent memory_dicts and game_history
            self.alice.memory_dict[f"iteration_{iter+1}"][1].append('Alice chose in iteration {}: '.format(iter+1)+alice_action)
            self.alice.memory_dict[f"iteration_{iter+1}"][1].append('Bob chose in iteration {}: '.format(iter+1)+bob_action)
            self.bob.memory_dict[f"iteration_{iter+1}"][1].append('Alice chose in iteration {}: '.format(iter+1)+alice_action)
            self.bob.memory_dict[f"iteration_{iter+1}"][1].append('Bob chose in iteration {}: '.format(iter+1)+bob_action)
            
            game_history[iter]['Alice_action'] = alice_action
            game_history[iter]['Bob_action'] = bob_action
            print(f"GAME HISTORY::: {game_history}")
        return game_history