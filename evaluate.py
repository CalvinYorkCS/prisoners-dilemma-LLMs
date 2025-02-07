import plotly.graph_objects as go
from payoffs import payoff_matrix

class Evaluator:
    def __init__(self, decisions_dict, game):
        self.decisions = decisions_dict
        self.total_games = len(decisions_dict)
        self.actions = list(payoff_matrix[game]['Alice'].keys()) 
        
        self.pareto_optimal = 0
        self.nash_equilibrium = 0
        self.mixed = 0
        self.alice_betrayals = 0
        self.bob_betrayals = 0        

        self.matrix_counts = {
            (self.actions[0], self.actions[0]): 0,
            (self.actions[0], self.actions[1]): 0,
            (self.actions[1], self.actions[0]): 0,
            (self.actions[1], self.actions[1]): 0
        }

        for d in self.decisions:
            alice = d['Alice_action']
            bob = d['Bob_action']
            
            # Game Outcomes
            if alice == self.actions[0] and bob == self.actions[0]:
                self.pareto_optimal += 1
            elif alice == self.actions[1] and bob == self.actions[1]:
                self.nash_equilibrium += 1
            else:
                self.mixed += 1
            
            # Individual betrayals
            if alice == self.actions[1]:
                self.alice_betrayals += 1
            if bob == self.actions[1]:
                self.bob_betrayals += 1

        # Count action pairs
        for d in self.decisions:
            pair = (d['Alice_action'], d['Bob_action'])
            self.matrix_counts[pair] += 1

    def get_metrics(self):
        return {
            "Pareto Optimal Rate": self.pareto_optimal / self.total_games,
            "Nash Equilibrium Rate": self.nash_equilibrium / self.total_games,
            "Mixed Rate": self.mixed / self.total_games,
            "Alice Betray Rate": self.alice_betrayals / self.total_games,
            "Bob Betray Rate": self.bob_betrayals / self.total_games
        }

    def print_metrics(self):
        metrics = self.get_metrics()
        for name, value in metrics.items():
            print(f"{name}: {value:.2%}")

    def plot_action_matrix(self):
        action_labels = self.actions
        matrix = [
            [self.matrix_counts[(self.actions[0], self.actions[0])], self.matrix_counts[(self.actions[0], self.actions[1])]],
            [self.matrix_counts[(self.actions[1], self.actions[0])], self.matrix_counts[(self.actions[1], self.actions[1])]]
        ]

        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=action_labels,
            y=action_labels,
            colorscale='Blues',
        ))
        
        fig.update_layout(
            title='Action Pair Distribution',
            xaxis_title="Bob's Action",
            yaxis_title="Alice's Action",
            width=600,
            height=600
        )
        
        # Add annotations with simple threshold
        max_value = max(max(row) for row in matrix)
        for i in range(len(action_labels)):
            for j in range(len(action_labels)):
                font_color = 'white' if matrix[i][j] > max_value * 0.5 else 'black'
                fig.add_annotation(
                    x=action_labels[j],
                    y=action_labels[i],
                    text=f"{matrix[i][j]}<br>({matrix[i][j]/self.total_games:.1%})",
                    showarrow=False,
                    font={"size": 14, "color": font_color}
                )
        
        return fig