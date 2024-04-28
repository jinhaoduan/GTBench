from gamingbench.games.crazy_eights import llm_output_to_action_code_mapping
from gamingbench.games.crazy_eights import suits
from gamingbench.games.crazy_eights import ranks

def _construct_head_prompt():
           
    prompt = "\nCrazy Eights is a shedding-type card game with a standard 52-card deck. The object of the game is to be the first player to discard all of their cards. There are two players in this game.\n" 
    prompt += "Seven cards are dealt to each player. The remaining cards of the deck are placed face down at the center of the table as the stock pile. The top card is then turned face up to start the game as the first card in the discard pile.\n" 
    prompt += "In each player's turn, it needs to play a card that either match the suit or the rank of the card on the top of the discard pile. And then place this card on the discard pile top for the next player to match. \n" 
    prompt += "A player can play an 8 as a wild card, however, at anytime. If it does, it needs to nominate a card suit needs to be nominated for the next player to match.\n" 
    prompt += "A player can also decide to draw cards from the stock pile. Notice that it is the only action available if it does not have a available card to play at its turn. But it doesn't prevent the player to draw cards even if it has playable.\n" 
    prompt += "If a player plays a card, it cannot draw at the current turn anymore. A player may draw up to five cards consecutively before ending its turn.\n" 
    prompt += "If there are no remaining cards in the stock pile, all cards in the discard pile are shuffled and add those cards are added to the stock pile.\n"
    prompt += "The game ends once a player exhausted all cards in its hand.\n"

    prompt += "You are playing CrazyEights with the opponent. The actions are denoted by <Draw> for drawing a card from the stockpile, <Play {CARD}> for putting on the discard pile the specific card, and <Nominate {SUIT}> for nominating a new suit to change."

    return prompt


'''
Observation Prompt to Create: 

Your current hand contains <CARDS>. 
You must match the top card <TOP CARD> with the next card you play or must draw from the stockpile. 
The moves in the past from you and your opponent are <MOVES>.
'''

def find_first_occurrence_index(string_list, substring):
    for index, string in enumerate(string_list):
        if substring in string:
            return index
    return -1  # Return -1 if the substring is not found in any string


# TO-DO: 
def construct_observation_prompt(observations):

    # print("construct_observation_prompt, observations parameter", observations)

    prompt = ""

    CARDS = observations.get('cards', []) 
    TOP_CARD = observations.get('top_card', "")
    SUIT_TO_MATCH = observations.get('suit_to_match', "") # NEED TO DEAL WITH THIS SPECIFICALLY FOR WILDCARD 8 CASE 
    MOVES = ""
    OPPONENT_CARD_COUNT = observations.get('opponent_card_count', "")
    player_idx = observations.get('player_idx', "")
    legal_moves = observations.get('legal_moves', [])

    # reversed_dict = {value: key for key, value in llm_output_to_action_code_mapping.items()}

    # print("legal_moves", legal_moves)
    # print("legal_moves[0]", legal_moves[0])
    # print("type(legal_moves[0])", type(legal_moves[0]))
    # print("reversed_dict", reversed_dict)
    # print("reversed_dict[legal_moves[0]]", reversed_dict[legal_moves[0]])


    # LEGAL = [reversed_dict[move]for move in legal_moves if move in list(reversed_dict.keys())]


    card_prompt = f"Your current hand contains {CARDS}. "

    if TOP_CARD.split(" ")[2] != SUIT_TO_MATCH: 
        top_prompt = f"You must match the suit {SUIT_TO_MATCH} with the next card you play or must draw from stockpile."
    else: 
        top_prompt = f"You must match the top card {TOP_CARD} with the next card you play or must draw from the stockpile."



    opponent_cards_prompt = f"You opponent's hand contains {OPPONENT_CARD_COUNT} cards."

    state_list = str(observations.get("state")).split("\n")

    start_of_gameplay = find_first_occurrence_index(state_list, "draws")
    end_of_gameplay = find_first_occurrence_index(state_list, "Last")

    for index, event in enumerate(state_list[start_of_gameplay:end_of_gameplay]): 
        
        event = event.split(" ")

        TRANSITION_WORD = "Next"

        if event[1] == str(player_idx): 
            ROLE = "you"

            if event[2] == "plays": 
                ACTION = "played"
                CARD_TO_REPORT = f"{ranks[event[3][1]]} of {suits[event[3][0]]}" 
            elif event[2] == "draws": 
                ACTION = "drew"
                CARD_TO_REPORT = f"{ranks[event[3][1]]} of {suits[event[3][0]]}" 
            elif event[2] == "nominates": 
                ACTION = "nominated"
                CARD_TO_REPORT = f"{suits[event[4]]} as new suit" 


        else: 
            ROLE = "your opponent"

            if event[2] == "plays": 
                ACTION = "played"
                CARD_TO_REPORT = f"{ranks[event[3][1]]} of {suits[event[3][0]]}" 
            elif event[2] == "draws": 
                ACTION = "drew"
                CARD_TO_REPORT = "a card" 
            elif event[2] == "nominates": 
                ACTION = "nominates"
                CARD_TO_REPORT = f"{suits[event[4]]} as new suit" 
        
    
        round_event_string = f"{TRANSITION_WORD}, {ROLE} {ACTION} {CARD_TO_REPORT}. "
        MOVES += round_event_string

    moves_prompt = "The following is the sequence of play between you and your opponent: First, both you and your opponent were dealt seven cards. " + MOVES + "\n"
    # print("moves_prompt", moves_prompt)

    legal_moves_prompt = "\n Your legal moves are: " + ", ".join(["<" + el[1:-1] + ">" for el in legal_moves]) + "."

    prompt += _construct_head_prompt() + "\n\n" + card_prompt + "\n" + top_prompt + "\n" + opponent_cards_prompt + "\n" + moves_prompt
    prompt += legal_moves_prompt 

    return prompt