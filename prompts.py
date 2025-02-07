from payoffs import payoff_matrix

class Prompts: 
    def __init__(self, args, name):
        self.args = args
        self.name = name
        self.other_agent = 'Bob' if self.name == 'Alice' else 'Alice'
        self.max_negotiation_round = args.max_negotiation_round
        self.game_setting_choice = args.game_setting_choice
        self.num_iterations = self.args.num_iterations
        self.personality = self.args.alice_personality if self.name == 'Alice' else self.args.bob_personality

        self.actions = list(payoff_matrix[self.args.payoff][self.name].keys()) 
        self.action_names = ', '.join(self.actions)

    def create_rule_description(self):
        sentences = []
        for choice_1 in self.actions:
            for choice_2 in self.actions:
                player_1_payoff = payoff_matrix[self.args.payoff][self.name][choice_1][self.other_agent+"_"+choice_2]
                player_2_payoff = payoff_matrix[self.args.payoff][self.other_agent][choice_2][self.name+"_"+choice_1]
                # Game setting
                if self.game_setting_choice == 'game':
                    if choice_1 == choice_2:
                        r = f"- If both you and {self.other_agent} choose {choice_1}, you will receive a reward of {player_1_payoff} and {self.other_agent} will receive a reward of {player_2_payoff}."
                        sentences.append(r)
                    elif choice_1 != choice_2:
                        r = f"- If you choose {choice_1} while {self.other_agent} chooses {choice_2}, you will receive a reward of {player_1_payoff} and {self.other_agent} will receive a reward of {player_2_payoff}."
                        sentences.append(r)
                # Prisoner setting
                elif self.game_setting_choice == 'prisoner':
                    if choice_1 == choice_2:
                        r = f"- If both you and {self.other_agent} choose {choice_1}, you will be sentenced to {player_1_payoff} years of prison and {self.other_agent} will be sentenced to {player_2_payoff} years of prison."
                        sentences.append(r)
                    elif choice_1 != choice_2:
                        r = f"- If you choose {choice_1} while {self.other_agent} chooses {choice_2}, you will receive {player_1_payoff} years of prison and {self.other_agent} will receive {player_2_payoff} years of prison."
                        sentences.append(r)
                # Corporate Transparency setting
                elif self.game_setting_choice == 'corporate_transparency':
                    if choice_1 == choice_2:
                        r = f"- If both you and {self.other_agent} choose {choice_1}, you receive a benefit of {player_1_payoff} while {self.other_agent} receives a benefit of {player_2_payoff}."
                        sentences.append(r)
                    elif choice_1 != choice_2:
                        r = f"- If you choose {choice_1} while {self.other_agent} chooses {choice_2}, the mismatch in transparency will result in a competitive advantage for one side: you get a benefit of {player_1_payoff} while {self.other_agent} gets {player_2_payoff}."
                        sentences.append(r)
                # Iterated Game setting
                elif self.game_setting_choice == 'iterated_game':
                    if choice_1 == choice_2:
                        r = f"- In this repeated interaction, if both you and {self.other_agent} choose {choice_1}, you will accumulate a benefit equivalent to {player_1_payoff} (per round) while {self.other_agent} accumulates {player_2_payoff}."
                        sentences.append(r)
                    elif choice_1 != choice_2:
                        r = f"- In a round where you choose {choice_1} and {self.other_agent} chooses {choice_2}, you will receive {player_1_payoff} while {self.other_agent} will receive {player_2_payoff}."
                        sentences.append(r)
                # Business Partnership setting
                elif self.game_setting_choice == 'business_partnership':
                    if choice_1 == choice_2:
                        r = f"- If both you and {self.other_agent} choose {choice_1}, you companies will earn profits of {player_1_payoff} and {player_2_payoff} respectively."
                        sentences.append(r)
                    elif choice_1 != choice_2:
                        r = f"- If you choose {choice_1} while {self.other_agent} chooses {choice_2}, the asymmetry in strategy yields a profit of {player_1_payoff} for you and {player_2_payoff} for {self.other_agent}."
                        sentences.append(r)
                # Security Negotiation setting
                elif self.game_setting_choice == 'security_negotiation':
                    if choice_1 == choice_2:
                        r = f"- If both you and {self.other_agent} choose {choice_1}, the resulting security outcomes will be {player_1_payoff} and {player_2_payoff} respectively."
                        sentences.append(r)
                    elif choice_1 != choice_2:
                        r = f"- If you choose {choice_1} while {self.other_agent} chooses {choice_2}, you will achieve a security advantage of {player_1_payoff} while {self.other_agent} gets {player_2_payoff}."
                        sentences.append(r)
                else:
                    raise ValueError(f"Invalid game setting choice: {self.game_setting_choice}")
        sentences.append('\n')
        return '\n'.join(sentences)

    def game_setting(self):
        """
        Setting summary: Prisoner's dilemma presented as a game without explicit mention of PD
        """
        system_prompt = f"""
                You are a {self.personality} player engaged in a one-round strategic game. 
                Use your analytical skills to maximize your reward through optimal decision-making and negotiation with {self.other_agent}.
                """
        game_setting = f"""
                ### Setting

                You are playing a one-round game with another player to maximize the reward you can obtain.
                You are playing as {self.name}. You have two choices: {self.action_names}.
                The other player, {self.other_agent}, also has two choices: {self.action_names}.

                ### Rules

                {self.create_rule_description()}
                """
        action_prompt = f"""
                ### Your Action

                Analyse the problem and the negotiation message if there is any.
                Please choose one of the following actions to maximize your reward.
                Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice. For example, '<s>choice_1</s>', '<s>choice_2</s>'.

                Action choices: {self.action_names}
                """
        negotiation_prompt = f"""
                ### Negotiation

                You can discuss with {self.other_agent} to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
                Analyze the situation and decide on what to say to the other player.

                Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
                You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
                """
        return system_prompt, game_setting, action_prompt, negotiation_prompt

    def prisoner_setting(self):
        """
        Setting summary: two criminals are facing prison time. Each criminal can choose to cooperate with the other to both receive a lighter sentence,
        or they can defect to get a significantly lighter sentence while giving the other a significantly stronger sentence.
        If both defect, they both receieve worse sentencing than if they both cooperated.
        """
        system_prompt = f"""
                You are a {self.personality} individual facing a critical decision that affects your prison sentence. 
                Strategize with {self.other_agent} to minimize your time in prison while considering the potential outcomes of cooperation and betrayal.
                """
        game_setting = f"""
                ### Setting

                You and your accomplice committed a crime, and you are both facing prison time.
                You are playing as {self.name}. You have two choices: {self.action_names}.
                Your accomplice, {self.other_agent}, also has two choices: {self.action_names}.

                ### Rules

                {self.create_rule_description()}
                """
        action_prompt = f"""
                ### Your Action

                Analyse the problem and the negotiation message if there is any.
                Please choose one of the following actions.
                Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice. For example, '<s>choice_1</s>', '<s>choice_2</s>'.

                Action choices: {self.action_names}
                """
        negotiation_prompt = f"""
                ### Negotiation

                You can discuss with {self.other_agent} to minimize the years of prison you are sentenced to. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
                Analyze the situation and decide on what to say to {self.other_agent}.

                Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
                You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
                """
        return system_prompt, game_setting, action_prompt, negotiation_prompt
    
    def corporate_transparency_setting(self):
        """
        Setting summary: Two companies decide whether to be transparent about their finances or to hide details during a negotiation.
        Transparency can build trust and lead to a mutually beneficial deal, while deception might yield a short-term advantage for one party.
        """
        system_prompt = f"""
                You are a {self.personality} corporate executive negotiating a deal. Decide whether to disclose financial details to 
                build trust or withhold information for competitive advantage, aiming to optimize your company's benefits.
                """
        game_setting = f"""
                ### Setting

                You are an executive at a company deciding whether to disclose your financial details or keep them confidential in a negotiation with {self.other_agent}'s company.
                Your choices are: {self.action_names}.
                {self.other_agent} is making a similar decision on behalf of their company.

                ### Rules

                {self.create_rule_description()}
                """
        action_prompt = f"""
                ### Your Action

                Analyze the situation and any negotiation messages.
                Please choose one of the following actions to optimize your company’s position.
                Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice. For example, '<s>{self.actions[0]}</s>' or '<s>{self.actions[1]}</s>'.

                Action choices: {self.action_names}
                """
        negotiation_prompt = f"""
                ### Negotiation

                You can discuss with {self.other_agent} to negotiate terms that might benefit both companies.
                You have a maximum of {self.max_negotiation_round} rounds to negotiate.
                Analyze the situation and decide on your message.

                Surround your message with '<s>' and '</s>' to indicate the start and end of your message, e.g., '<s>Let's work together transparently.</s>'.
                You can also choose to halt the negotiation by saying '<s>halt negotiation</s>'.
                """
        return system_prompt, game_setting, action_prompt, negotiation_prompt

    def iterated_game_setting(self):
        """
        Setting summary: An iterated game where you face the same strategic dilemma repeatedly, allowing you to adjust your strategy based on past outcomes.
        """
        system_prompt = f"""
                You are a {self.personality} participant in a repeated strategic game. 
                Decide between two choices each round to maximize your total reward.
                """
        game_setting = f"""
                ### Setting

                You are playing a repeated game with another player to maximize your long-term reward.
                You are playing as {self.name}. In each iteration, you have two choices: {self.action_names}.
                {self.other_agent} will also choose from the same set of actions in every iteration.
                This game will be played for a total of {self.num_iterations} iterations.
                Your decisions in previous iterations can influence future iterations, so think strategically over the long term.

                ### Rules

                {self.create_rule_description()}
                """
        action_prompt = f"""
                ### Your Action

                Analyze the negotiation message (if any) and the outcomes from previous iterations.
                Please choose one of the following actions to maximize your long-term reward.
                Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice. For example, '<s>{self.actions[0]}</s>' or '<s>{self.actions[1]}</s>'.

                Action choices: {self.action_names}
                """
        negotiation_prompt = f"""
                ### Negotiation

                You can discuss strategies with {self.other_agent} between rounds to influence future outcomes.
                You have a maximum of {self.max_negotiation_round} rounds to negotiate.
                Keep in mind that there are {self.num_iterations} iterations in total.
                Analyze the situation and decide on a message to help shape the long-term interaction.

                Surround your message with '<s>' and '</s>' to indicate the start and end of your message, e.g., '<s>Let’s cooperate for mutual long-term benefit.</s>'.
                You can also choose to halt the negotiation by saying '<s>halt negotiation</s>'.
                """
        return system_prompt, game_setting, action_prompt, negotiation_prompt

    def business_partnership_setting(self):
        """
        Setting summary: In an iterated business scenario, you and another company repeatedly decide whether to launch a joint marketing campaign or cut prices aggressively.
        A joint campaign benefits both companies over the long term, while an aggressive price cut can yield a short-term advantage at the risk of damaging future profits.
        Your decisions in each round will cumulatively affect your company’s overall market position and profitability.
        """
        system_prompt = f"""
                You are a {self.personality} business executive in a long-term partnership scenario. Navigate the balance between collaborative 
                campaigns and aggressive tactics over {self.num_iterations} iterations to secure your company's profitability and market position.
                """
        game_setting = f"""
                ### Setting

                You are an executive at a company engaged in an iterated strategic competition with {self.other_agent}'s company.
                In each round, you face a choice: launch a joint marketing campaign or cut prices aggressively.
                Your available actions are: {self.action_names}.
                {self.other_agent} will also choose between these options in every round.
                This competition will occur over {self.num_iterations} iterations.
                The outcomes from each round will influence your long-term profitability and market reputation.

                ### Rules

                {self.create_rule_description()}
                """
        action_prompt = f"""
                ### Your Action

                Analyze the outcomes from previous rounds and any negotiation messages.
                Please choose one of the following actions to maximize your company's total profit at the end of the {self.num_iterations} iterations.
                Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice, for example, '<s>{self.actions[0]}</s>' or '<s>{self.actions[1]}</s>'.

                Action choices: {self.action_names}
                """
        negotiation_prompt = f"""
                ### Negotiation

                You can discuss strategies with {self.other_agent} between rounds to try to form a mutually beneficial long-term strategy.
                You have a maximum of {self.max_negotiation_round} rounds to negotiate before the next business decision.
                Keep in mind that there are {self.num_iterations} iterations in total.
                Analyze the situation and decide on your message to shape future interactions and outcomes.

                Surround your message with '<s>' and '</s>' to indicate the start and end of your message, for example, '<s>Let's aim for a collaborative strategy over the long run.</s>'.
                You can also choose to halt the negotiation by saying '<s>halt negotiation</s>'.
                """
        return system_prompt, game_setting, action_prompt, negotiation_prompt
    
    def security_negotiation_setting(self): 
        """
        Setting summary: In an iterated diplomatic scenario, you represent a nation engaged in repeated negotiations regarding border security with {self.other_agent}.
        In each round, you must decide whether to share or withhold intelligence.
        Consistent cooperation builds long-term trust and cumulative security benefits, whereas persistent defection may yield short-term gains but increase long-term risks.
        """
        system_prompt = f"""
                You are a {self.personality} representative in diplomatic security negotiations. 
                Your decisions on sharing intelligence will affect national security over {self.num_iterations} rounds. 
                Aim to build trust or secure advantages through strategic choices and communication.
                """
        game_setting = f"""
                ### Setting

                You represent a nation engaged in repeated diplomatic negotiations with {self.other_agent} over border security.
                In every round, you face a decision: to share intelligence or withhold it.
                Your available actions are: {self.action_names}.
                {self.other_agent} will make a similar decision in each round.
                This negotiation will take place over {self.num_iterations} iterations.
                The results of each round accumulate, affecting long-term national security and trust between the nations.
                Consider that mutual sharing over time strengthens security and cooperation, while repeated unilateral withholding can undermine trust and lead to increased long-term risks.

                ### Rules

                {self.create_rule_description()}
                """
        action_prompt = f"""
                ### Your Action

                Consider the outcomes from previous rounds and any negotiation messages.
                Please choose one of the following actions to maximize your nation's long-term security.
                Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice, for example, '<s>{self.actions[0]}</s>' or '<s>{self.actions[1]}</s>'.

                Action choices: {self.action_names}
                """
        negotiation_prompt = f"""
                ### Negotiation

                You can discuss strategic approaches with {self.other_agent} between rounds to help build a pattern of trust or secure a tactical advantage.
                You have a maximum of {self.max_negotiation_round} rounds to negotiate before each new decision.
                Remember, the negotiation spans a total of {self.num_iterations} iterations.
                Analyze the situation and decide on your diplomatic message to influence long-term security outcomes.

                Surround your message with '<s>' and '</s>' to indicate the start and end of your message, for example, '<s>Let's work together for our mutual long-term security.</s>'.
                You can also choose to halt the negotiation by saying '<s>halt negotiation</s>'.
                """
        return system_prompt, game_setting, action_prompt, negotiation_prompt