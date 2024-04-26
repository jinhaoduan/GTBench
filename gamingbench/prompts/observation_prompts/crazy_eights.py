
def _construct_head_prompt():
           
    prompt = "Crazy Eights is a shedding-type card game with a standard 52-card deck. The object of the game is to be the first player to discard all of their cards. There are two players in this game.\n" 
    prompt += "Seven cards are dealt to each player. The remaining cards of the deck are placed face down at the center of the table as the stock pile. The top card is then turned face up to start the game as the first card in the discard pile.\n" 
    prompt += "In each player's turn, it needs to play a card that either match the suit or the rank of the card on the top of the discard pile. And then place this card on the discard pile top for the next player to match. \n" 
    prompt += "A player can play an 8 as a wild card, however, at anytime. If it does, it needs to nominate a card suit needs to be nominated for the next player to match." 
    prompt += "A player can also decide to draw cards from the stock pile. Notice that it is the only action available if it does not have a available card to play at its turn. But it doesn't prevent the player to draw cards even if it has playable.\n" 
    prompt += "If a player plays a card, it cannot draw at the current turn anymore. A player cannot skip a turn.\n" 
    prompt += "If there are no remaining cards in the stock pile, all cards in the discard pile are shuffled and add those cards are added to the stock pile.\n"
    prompt += "The game ends once a player exhausted all cards in its hand."

    return prompt 


# TO-DO: 
def construct_observation_prompt(observations):

    prompt = ""

    card_mapping = {
        '1': 'Ace (A)',
        '2': '2 (2)',
        '3': '3 (3)', 
        '4': '4 (4)', 
        '5': '5 (5)', 
        '6': '6 (6)', 
        '7': '7 (7)', 
        '8': '8 (8)', 
        '9': '9 (9)', 
        '10': '10 (10)', 
        '11': 'Jack (J)', 
        '12': 'Queen (Q)', 
        '13': 'King (K)'
    }

    suit_mapping = {
        'C': 'Clubs (C)', 
        'D': 'Diamonds (D)', 
        'H': 'Hearts (H)', 
        'S': 'Spades (S)'
    }

    return prompt


# if __name__ == '__main__':
#     prompt = _construct_head_prompt()
#     obs_prompt = construct_observation_prompt(
#         {'card': 0, 'moves': 'pb', 'player_idx': 0})
#     prompt += '\n' + obs_prompt
#     print(prompt)
