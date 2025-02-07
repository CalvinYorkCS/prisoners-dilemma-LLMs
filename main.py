import argparse 
from game import Game
from iterated_game import Iterated_Game
from tqdm import tqdm
from evaluate import Evaluator
from iterated_evaluate import Iterated_Evaluator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--payoff', type=str, default='prisoner_dilemma')
    parser.add_argument('--max_negotiation_round', type=int, default=0)
    parser.add_argument('--who_first', type=str, default='Bob')
    parser.add_argument('--alice_personality', type=str, default="rational")
    parser.add_argument('--bob_personality', type=str, default="rational")
    parser.add_argument('--sample_num', type=int, default=10)
    parser.add_argument('--model', type=str, default='gpt-4o-mini')
    parser.add_argument('--game_setting_choice', type=str, default='game')
    parser.add_argument('--memory_len', type=int, default=2)
    parser.add_argument('--actions_only_memory', type=bool, default=False)
    parser.add_argument('--num_iterations', type=int, default=3)
    args = parser.parse_args()

    RUN_CLASSIC = True
    RUN_ITERATED = False

    if RUN_CLASSIC:
        args.max_negotiation_round = 1
        args.sample_num = 1
        args.model = 'gpt-4o'
        args.game_setting_choice = 'corporate_transparency'
        args.payoff = 'corporate_transparency'
        args.alice_personality = 'cunning, deceitful, and vengeful'
        args.bob_personality = 'altruistic'

        decisions_dict = []
        procedure = []

        for i in tqdm(range(args.sample_num)):
            game = Game(args)
            alice_action, bob_action = game.play()
            print(f'alice_action: {alice_action}')
            print(f'bob_action: {bob_action}')
            procedure.append(game.alice.previous_messages)
            decisions_dict.append({'Alice_action':alice_action, 'Bob_action':bob_action})

        # Evaluate results
        print(decisions_dict)

        evaluator = Evaluator(decisions_dict, args.payoff)
        evaluator.print_metrics()

        matrix_fig = evaluator.plot_action_matrix()
        matrix_fig.show()

        print(procedure[-1])


    if RUN_ITERATED:
        args.max_negotiation_round = 1
        args.sample_num = 1
        args.model = 'gpt-4o'
        args.game_setting_choice = 'business_partnership'
        args.payoff = 'business_partnership_imbalanced'
        args.memory_len = 10
        args.num_iterations = 2
        args.alice_personality = 'cunning'
        args.bob_personality = 'rational'

        game_histories = []
        iterated_procedure = []

        for i in tqdm(range(args.sample_num)):
            iterated_game = Iterated_Game(args)
            game_history = iterated_game.play()
            print(game_history)
            iterated_procedure.append(iterated_game.alice.memory_dict)
            game_histories.append(game_history)

        # Evaluate results
        print(f"ALL GAME HISTORIES::: {game_histories}")
        iterated_evaluator = Iterated_Evaluator(game_histories, args.payoff)
        iterated_evaluator.print_metrics()

        cooperation_fig = iterated_evaluator.plot_cooperation_over_time()
        cooperation_fig.show()

        # print(iterated_procedure[-1])