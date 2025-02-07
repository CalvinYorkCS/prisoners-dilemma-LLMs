import plotly.graph_objects as go
import plotly.express as px
from payoffs import payoff_matrix

class Iterated_Evaluator:
    def __init__(self, game_histories, game):
        """ game_histories
        [
            [{'Alice_action': choice, 'Bob_action': choice}, {'Alice_action': choice, 'Bob_action': choice}, {iter3}],
            [{'Alice_action': choice, 'Bob_action': choice}, {'Alice_action': choice, 'Bob_action': choice}, {iter3}],
            [{'Alice_action': choice, 'Bob_action': choice}, {'Alice_action': choice, 'Bob_action': choice}, {iter3}],
        ]
        """
        self.samples = len(game_histories)
        self.actions = list(payoff_matrix[game]['Alice'].keys()) 

        self.alice_coop = [0] * len(game_histories[0])
        self.bob_coop = [0] * len(game_histories[0])

        self.total_payoffs = []
        """ total_payoffs
        [
            {'Alice_payoff': int, 'Bob_payoff': int} # sample 1
            {'Alice_payoff': int, 'Bob_payoff': int} # sample 2
            {'Alice_payoff': int, 'Bob_payoff': int} # sample 3
        ]
        """

        for sample, game_history in enumerate(game_histories):
            self.total_payoffs.append({})
            for i, iteration in enumerate(game_history):
                alice = iteration['Alice_action']
                bob = iteration['Bob_action']

                # Add iteration payoff to game's total payoffs
                self.total_payoffs[sample]['Alice_payoff'] = \
                    self.total_payoffs[sample].get('Alice_payoff', 0) + payoff_matrix[game]['Alice'][alice]['Bob_'+bob]
                self.total_payoffs[sample]['Bob_payoff'] = \
                    self.total_payoffs[sample].get('Bob_payoff', 0) + payoff_matrix[game]['Bob'][bob]['Alice_'+alice]

                # count total cooperations per iteration
                if alice == self.actions[0]:
                    self.alice_coop[i] += 1
                if bob == self.actions[0]:
                    self.bob_coop[i] += 1

    def get_coop_rates(self):
        return  {
            'Alice': [count / self.samples for count in self.alice_coop],
            'Bob': [count / self.samples for count in self.bob_coop]
        }

    def plot_cooperation_over_time(self): 
        # Calculate average cooperation per iteration
        coop_rates = self.get_coop_rates()

        fig = px.line(
            coop_rates, 
            labels={'value': 'Cooperation Rate', 'index': 'Iteration'},
            title='Cooperation Rate Over Iterations'
        )
        return fig
    
    def get_metrics(self):
        return {
            "Total Payoffs": self.total_payoffs,
            "Cooperation Rates": self.get_coop_rates()
        }

    def print_metrics(self):
        metrics = self.get_metrics()
        for name, value in metrics.items():
            print(f"{name}: {value}")