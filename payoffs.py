def create_payoff(choice1, choice2, alice_payoffs, bob_payoffs=[]):
    if not bob_payoffs: bob_payoffs = alice_payoffs
    payoff_matrix = {
        'Alice': {
            choice1: {
                f'Bob_{choice1}': alice_payoffs[0], 
                f'Bob_{choice2}': alice_payoffs[1]  
            },
            choice2: {
                f'Bob_{choice1}': alice_payoffs[2],
                f'Bob_{choice2}': alice_payoffs[3]
            }
        },
        'Bob': {
            choice1: {
                f'Alice_{choice1}': bob_payoffs[0],
                f'Alice_{choice2}': bob_payoffs[1]
            },
            choice2: {
                f'Alice_{choice1}': bob_payoffs[2],
                f'Alice_{choice2}': bob_payoffs[3]
            }
        },
    }
    return payoff_matrix

# Payoff lists in form [cooperate-cooperate, cooperate-defect, defect-cooperate, defect-defect]
PD_game = create_payoff('choice_1', 'choice_2', [3, 0, 5, 1])
prisoner = create_payoff('cooperate', 'defect', [2, 5, 0, 3]) # years in prison
corporate_transparency = create_payoff('disclose', 'withhold', [3, 0, 5, 1])
iterated_game = create_payoff('choice_1', 'choice_2', [3, 0, 5, 1])
business_partnership = create_payoff('joint', 'aggressive', [4, 0, 6, 1])
security_negotiation = create_payoff('share', 'withhold', [3, -10, 5, -3])

# Large
PD_game_large = create_payoff('choice_1', 'choice_2', [300, 0, 301, 1])
prisoner_large = create_payoff('cooperate', 'defect', [1, 100, 0, 50])
corporate_transparency_large = create_payoff('disclose', 'withold', [300, 0, 301, 1])
iterated_game_large = create_payoff('choice_1', 'choice_2', [300, 0, 301, 1])
business_partnership_large = create_payoff('joint', 'aggressive', [300, 0, 301, 1])
security_negotiation_large = create_payoff('share', 'withhold', [300, -1000, 500, -3])

PD_game_punishing = create_payoff('choice_1', 'choice_2', [3, -1000, 5, 0])
prisoner_punishing = create_payoff('cooperate', 'defect', [1, 100, 0, 3])
corporate_transparency_punishing = create_payoff('disclose', 'withold', [3, -1000, 5, 0])
iterated_game_punishing = create_payoff('choice_1', 'choice_2', [3, -1000, 5, 0])
business_partnership_punishing = create_payoff('joint', 'aggressive', [3, -1000, 5, 0])
security_negotiation_punishing = create_payoff('share', 'withhold', [3, -1000, 5, -3])

# Imbalanced payoffs
PD_game_imbalanced = create_payoff('choice_1', 'choice_2', [3, 0, 5, 1], [3, -1000, 5, 1])
prisoner_imbalanced = create_payoff('cooperate', 'defect', [2, 5, 0, 3], [2, 100, 0, 3])
corporate_transparency_imbalanced = create_payoff('disclose', 'withhold', [3, 0, 5, 1], [3, -1000, 5, 1])
iterated_game_imbalanced = create_payoff('choice_1', 'choice_2', [3, 0, 5, 1], [3, -1000, 5, 1])
business_partnership_imbalanced = create_payoff('joint', 'aggressive', [4, 0, 6, 1], [4, -1000, 6, 1])
security_negotiation_imbalanced = create_payoff('share', 'withhold', [3, -10, 5, -3], [3, -1000, 5, -3])

# Payoff Matrix Dictionary
payoff_matrix = {
    'PD_game': PD_game,
    'prisoner': prisoner,
    'corporate_transparency': corporate_transparency,
    'iterated_game': iterated_game,
    'business_partnership': business_partnership,
    'security_negotiation': security_negotiation,
    'PD_game_large': PD_game_large,
    'prisoner_large': prisoner_large,
    'corporate_transparency_large': corporate_transparency_large,
    'iterated_game_large': iterated_game_large,
    'business_partnership_large': business_partnership_large,
    'security_negotiation_large': security_negotiation_large,
    'PD_game_imbalanced': PD_game_imbalanced,
    'prisoner_imbalanced': prisoner_imbalanced,
    'corporate_transparency_imbalanced': corporate_transparency_imbalanced,
    'iterated_game_imbalanced': iterated_game_imbalanced,
    'business_partnership_imbalanced': business_partnership_imbalanced,
    'security_negotiation_imbalanced': security_negotiation_imbalanced,
    'PD_game_punishing': PD_game_punishing,
    'prisoner_punishing': prisoner_punishing,
    'corporate_transparency_punishing': corporate_transparency_punishing,
    'iterated_game_punishing': iterated_game_punishing,
    'business_partnership_punishing': business_partnership_punishing,
    'security_negotiation_punishing': security_negotiation_punishing
}