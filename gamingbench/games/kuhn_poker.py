from gamingbench.games.openspiel_adapter import OpenSpielGame


class KuhnPoker(OpenSpielGame):

    def __init__(self) -> None:
        super().__init__("kuhn_poker")
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):

        state = str(self.env).split(' ')
        print(state)
        observations = {
            'card': state[current_player_idx],
            'moves': state[-1] if (state[-1] != '0' and state[-1] != '1' and state[-1] != '2') else None,
            'player_idx': current_player_idx
        }
        return observations

    def openspiel_action_to_agent(self, action):
        return [f'<{a}>' for a in action]

    def agent_action_to_openspiel(self, action):
        if action == '<Pass>':
            return 0
        elif action == '<Bet>':
            return 1
        else:
            # TODO: illegal action
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
