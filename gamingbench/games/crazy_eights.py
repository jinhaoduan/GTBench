from gamingbench.games.openspiel_adapter import OpenSpielGame
import re


llm_output_to_action_code_mapping = {
            "<Play 2 of Clubs>": 0,
            "<Play 2 of Diamonds>": 1,
            "<Play 2 of Hearts>": 2,
            "<Play 2 of Spades>": 3,
            "<Play 3 of Clubs>": 4,
            "<Play 3 of Diamonds>": 5,
            "<Play 3 of Hearts>": 6,
            "<Play 3 of Spades>": 7,
            "<Play 4 of Clubs>": 8,
            "<Play 4 of Diamonds>": 9,
            "<Play 4 of Hearts>": 10,
            "<Play 4 of Spades>": 11,
            "<Play 5 of Clubs>": 12,
            "<Play 5 of Diamonds>": 13,
            "<Play 5 of Hearts>": 14,
            "<Play 5 of Spades>": 15,
            "<Play 6 of Clubs>": 16,
            "<Play 6 of Diamonds>": 17,
            "<Play 6 of Hearts>": 18,
            "<Play 6 of Spades>": 19,
            "<Play 7 of Clubs>": 20,
            "<Play 7 of Diamonds>": 21,
            "<Play 7 of Hearts>": 22,
            "<Play 7 of Spades>": 23,
            "<Play 8 of Clubs>": 24,
            "<Play 8 of Diamonds>": 25,
            "<Play 8 of Hearts>": 26,
            "<Play 8 of Spades>": 27,
            "<Play 9 of Clubs>": 28,
            "<Play 9 of Diamonds>": 29,
            "<Play 9 of Hearts>": 30,
            "<Play 9 of Spades>": 31,
            "<Play 10 of Clubs>": 32,
            "<Play 10 of Diamonds>": 33,
            "<Play 10 of Hearts>": 34,
            "<Play 10 of Spades>": 35,
            "<Play Jack of Clubs>": 36,
            "<Play Jack of Diamonds>": 37,
            "<Play Jack of Hearts>": 38,
            "<Play Jack of Spades>": 39,
            "<Play Queen of Clubs>": 40,
            "<Play Queen of Diamonds>": 41,
            "<Play Queen of Hearts>": 42,
            "<Play Queen of Spades>": 43,
            "<Play King of Clubs>": 44,
            "<Play King of Diamonds>": 45,
            "<Play King of Hearts>": 46,
            "<Play King of Spades>": 47,
            "<Play Ace of Clubs>": 48,
            "<Play Ace of Diamonds>": 49,
            "<Play Ace of Hearts>": 50,
            "<Play Ace of Spades>": 51,
            "<Draw>": 52, 
            "<Pass on Draw>": 53, 
            "<Nominate Clubs>": 54, 
            "<Nominate Diamonds>": 55, 
            "<Nominate Hearts>": 56, 
            "<Nominate Spades>": 57
}


suits = {
    "C": "Clubs", 
    "D": "Diamonds", 
    "H": "Hearts", 
    "S": "Spades"
}

ranks = {
    "2": "2", 
    "3": "3", 
    "4": "4", 
    "5": "5", 
    "6": "6",
    "7": "7", 
    "8": "8", 
    "9": "9", 
    "T": "10", 
    "J": "Jack", 
    "Q": "Queen", 
    "K": "King", 
    "A": "Ace"
}
# TO-DO: 
class CrazyEights(OpenSpielGame):


    def __init__(self) -> None:
        super().__init__("crazy_eights")
        self.game_name = 'crazy_eights'
    

    # figure out the current legal actions and return back to llm to append to the prompt
    def openspiel_action_to_agent(self, action):
        print("from openspiel_action_to_agent, action parameter:", action)

        legal_actions = [] 

        for el in action: 

            if el == "Draw": 
                legal_actions.append("<Draw>") 
            elif el == 'Nominate suit C': 
                legal_actions.append("<Nominate Clubs>")
            elif el == 'Nominate suit D': 
                legal_actions.append("<Nominate Diamonds>")
            elif el == "Nominate suit H":
                legal_actions.append("<Nominate Hearts>")
            elif el == "Nominate suit S": 
                legal_actions.append("<Nominate Spades>")
            elif el == "Pass on Draw" or el == "Pass": 
                legal_actions.append("<Pass on Draw>")
            else: 

                # print(el)

                card_to_play = el.split()[1] # figure out the card that is being played 
                suit_of_card = card_to_play[0]
                rank_of_card = card_to_play[1:] 

                # if rank_of_card == "8": 
                legal_actions.append(f"<Play {ranks[rank_of_card]} of {suits[suit_of_card]}>")
                # else: 
                #     legal_actions.append(f"<Play {ranks[rank_of_card]} of {suits[suit_of_card]} and Nominate Clubs>")
                #     legal_actions.append(f"<Play {ranks[rank_of_card]} of {suits[suit_of_card]} and Nominate Diamonds>")
                #     legal_actions.append(f"<Play {ranks[rank_of_card]} of {suits[suit_of_card]} and Nominate Hearts>")
                #     legal_actions.append(f"<Play {ranks[rank_of_card]} of {suits[suit_of_card]} and Nominate Spades>") 

        # print("from openspiel_action_to_agent, legal_actions:", legal_actions)

        return legal_actions
    
    def parse_cards_i_have_per_suit(self, input_string, suit): 

        cards_per_suit_str = []

        input_string = input_string[len("Suit C: "):]

        for char in input_string: 
            if char in list(ranks.keys()): 
                cards_per_suit_str.append(f"{ranks[char]} of {suit}")

        return cards_per_suit_str

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):

        state = self.env

        # print("from openspiel_observation_to_dict, current_player_idx:", current_player_idx)
        # print("from openspiel_observation_to_dict, openspiel_obs:", openspiel_obs)
        # print("from openspiel_observation_to_dict, state:", state)

        new_line_split = openspiel_obs.split("\n")
        # print(new_line_split)

        # cards = [f"{ranks[el]} of Clubs" for el in new_line_split[1].split()[2:]]
        # cards += [f"{ranks[el]} of Diamonds" for el in new_line_split[2].split()[2:]]
        # cards += [f"{ranks[el]} of Hearts" for el in new_line_split[3].split()[2:]]
        # cards += [f"{ranks[el]} of Spades" for el in new_line_split[4].split()[2:]]

        cards = self.parse_cards_i_have_per_suit(new_line_split[1], "Clubs")
        cards += self.parse_cards_i_have_per_suit(new_line_split[2], "Diamonds")
        cards += self.parse_cards_i_have_per_suit(new_line_split[3], "Hearts")
        cards += self.parse_cards_i_have_per_suit(new_line_split[4], "Spades")

        # print("CARDS", cards)

        top_card = new_line_split[5][len("Previous card: "):]
        top_suit = suits[top_card[0]]
        top_rank = ranks[top_card[1]]
        top_card = f"{top_rank} of {top_suit}" 

        previous_suit = suits[new_line_split[6][len("Previous suit: "):]]
        
        
        player_idx = current_player_idx

        # Sample string
        string = new_line_split[7]

        # Define a regular expression pattern to match numbers
        pattern = r'\b\d+\b'

        # Find all matches of the pattern in the string
        numbers = re.findall(pattern, string)

        # Convert the numbers from strings to integers
        numbers = set([int(num) for num in numbers]) 

        if len(numbers) == 1: 
            opponent_card_count = len(cards)
        else: 
            numbers.remove(len(cards))
            opponent_card_count = numbers.pop() 

        res = {
            "cards": cards, 
            "top_card": top_card, 
            "suit_to_match": previous_suit, 
            "opponent_card_count": opponent_card_count, 
            "player_idx": player_idx 
        }
        
        # print("openspiel_observation_to_dict, res: ", res)
        
        return res

    # converts the agent action as denoted by the LLM into the action-id(s) needed by OpenSpiel to apply each game move
    def agent_action_to_openspiel(self, action):

        try: 
            if action == "<Draw>" or action == "<Pass on Draw>": 

                # print("action from openspiel_observation_to_dict", llm_output_to_action_code_mapping["<" + action[0] + ">"])
                return llm_output_to_action_code_mapping[action]

            elif "<" + action[0] + ">" in llm_output_to_action_code_mapping.keys(): 

                # print("action from openspiel_observation_to_dict", llm_output_to_action_code_mapping["<" + action[0] + ">"])
                return llm_output_to_action_code_mapping["<" + action[0] + ">"]

        except: 
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
