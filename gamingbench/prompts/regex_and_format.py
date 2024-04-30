

def get_step_env_regex_and_format(env_name):
    if env_name == 'tictactoe':
        regex = 'C[1-3]R[1-3]'
        format = '<CxRy>, e.g., <C1R1>, <C3R3>'
    elif env_name == 'connect4':
        regex = '(<C[1-7]>|Column.{0,3}[1-7]|column.{0,3}[1-7])'
        format = '<Cx>, e.g., <C1>, <C7>'
    elif env_name == "dots_and_boxes":
        regex = '<(([A-C])(\d)[-−—]([A-C])(\d))>'
        format = '<[A-C][1-3]-[A-C][1-3]>, e.g., <A1-B1>, <A1-A2>'
    elif env_name == 'TexasHoldem':
        regex = '<.+>'
        format = '<ALL IN>'
    elif env_name == 'breakthrough':
        regex = '[a-c][1-8]->[a-c][1-8](?:\*)?'
        format = '<[a-c][1-8]->[a-c][1-8]>, e.g., <a7->a6>'
    elif env_name == 'pig':
        regex = '(.+)'
        format = 'e.g., <stop>'
    elif env_name == 'liars_dice':
        regex = '(<[1-2] dices, [1-6] value>|<Liar>|<[1-2] dice, [1-6] value>)'
        format = '<x dice(s), y value> or <Liar>, e.g., <1 dice, 1 value>, <2 dices, 6 value>, <Liar>'
    elif env_name == 'nim':
        regex = '(<pile:1, take:1>|<pile:2, take:[1-3]>|<pile:3, take:[1-5]>|<pile:4, take:[1-7]>)'
        format = '<pile:x, take:y>, e.g., <pile:1, take:1>, <pile:4, take:7>'
    elif env_name == 'negotiation':
        regex = '(?:agree|Agree|AGREE)|\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]'
        format = '<Proposal|Utterance: [a, b, c]> e.g., <Proposal: [1, 2, 3]> <Utterance: [4, 2, 1]> or <agree>'
    elif env_name == 'first_sealed_auction':
        regex = '<(?:[0-9]|10)>'
        format = '<[0-9]|10>, e.g., <0>, <10>'
    elif env_name == 'kuhn_poker':
        regex = '(<Pass>|<Bet>)'
        format = '<Pass|Bet> e.g., <Pass>'
    elif env_name == 'python_iterated_prisoners_dilemma':
        regex = '(<Testify>|<Silent>)'
        format = '<Testify|Silent>, e.g., <Testify>, <Silent>'
    # TO-DO
    elif env_name == 'crazy_eights': 
        # regex = "<(Draw|Pass on Draw|Play (2|3|4|5|6|7|9|10|Jack|Queen|King|Ace) of (Clubs|Diamonds|Hearts|Spades)|Play 8 of (Clubs|Diamonds|Hearts|Spades) and Nominate (Clubs|Diamonds|Hearts|Spades))>"
        # format = "<(Draw|Play (2|3|4|5|6|7|9|10|Jack|Queen|King|Ace) of (Clubs|Diamonds|Hearts|Spades)|Play 8 of (Clubs|Diamonds|Hearts|Spades) and Nominate (Clubs|Diamonds|Hearts|Spades))>"
        # format += ", e.g. <Draw>, <Play 5 of Clubs>, <Play 8 of Diamonds and Nominate Hearts>"

        regex = "<(Draw|Pass on Draw|Play (2|3|4|5|6|7|8|9|10|Jack|Queen|King|Ace) of (Clubs|Diamonds|Hearts|Spades)|Nominate (Clubs|Diamonds|Hearts|Spades))>"
        format = "<(Draw|Pass on Draw|Play (2|3|4|5|6|7|8|9|10|Jack|Queen|King|Ace) of (Clubs|Diamonds|Hearts|Spades)|Nominate (Clubs|Diamonds|Hearts|Spades))>"
        format += ", e.g. <Draw>, <Pass on Draw>,<Play 5 of Clubs>, <Play 8 of Diamonds>, <Nominate Hearts>"
    else:
        raise NotImplementedError
    return regex, format
