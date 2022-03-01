data_location_allowed_transitions = {
    "CREATING": ["CREATE_ERROR", "COMPLETE"],
    "CREATE_ERROR": ["CREATING", "DELETING"],
    "COMPLETE": ["DELETING"],
    "DELETING": ["DELETE_ERROR", "DELETED"],
    "DELETE_ERROR": ["CREATING", "DELETING"],
    "DELETED": ["CREATING"]
}


class StateTable:
    def __init__(self, transitions_set):
        self.transitions_set = transitions_set

    @staticmethod
    def _allowed_transitions_from_dict(transition_dict):
        return {
            (source, target) for source, targets in transition_dict.items()
            for target in targets
        }

    @classmethod
    def from_dict(cls, d):
        return cls(cls._allowed_transitions_from_dict(d))

    @property
    def reverse_transitions_set(self):
        return {t[::-1] for t in self.transitions_set}

    def can_transition(self, source, target):
        return (source, target) in self.transitions_set

    @property
    def states(self):
        return [*{state for transition in self.transitions_set
                  for state in transition}]

    def allowed_targets(self, state):
        return [target for source, target in self.transitions_set
                if source == state]

    def allowed_sources(self, state):
        return [source for source, target in self.transitions_set
                if target == state]


data_location_state_table = StateTable.from_dict(
    data_location_allowed_transitions)

__all__ = ["StateTable", "data_location_state_table"]
