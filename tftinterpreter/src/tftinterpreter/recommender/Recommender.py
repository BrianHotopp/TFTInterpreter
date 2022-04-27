from ..predictor.Predictor import Predictor
import json
import heapq
class Recommender:
    def __init__(self, labels_file_path: str, perfects_file_path: str) -> None:
        """
        Initialize a recommender object
        Args:
            self: the current Predictor object
            labels_file_path: path to a labels file
            model_path: path to a model file
        """
        self.full_to_abb = Predictor.get_labels(labels_file_path)
        self.abb_to_full = {v: k for k, v in self.full_to_abb.items()}
        self.perfects = Recommender.load_perfects(perfects_file_path)
    @staticmethod
    def load_perfects(perfects_file_path: str) -> dict:
        """
        Load the perfect synergies from a file.
        Args:
            perfects_file_path: the path to the json file
        Returns:
            dictionary of perfect synergies
            keys are integers 4-9
            values are lists of lists of strings representing units 
        """
        return json.load(open(perfects_file_path))
    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """
        Calculate the jaccard similarity between two sets.
        Args:
            set1: first set
            set2: second set
        Returns:
            float representing the similarity
        """
        return len(set1.intersection(set2)) / len(set1.union(set2)) 

    def get_closest_matches(self, board_state):
        """
        gets the perfect synergies that are closest to the board state
        board state is a list of abbreviated unit names
        """ 
        # map abbreviated unit names to full unit names and convert to set
        board_state = set([self.abb_to_full[unit] for unit in board_state])
        # get the perfects that are closest to the board state by jaccard similarity
        closest_perfects = {}
        for teamsize in self.perfects:
            # remove the score from the comp by map and take the best by jaccard
            # get nlargest using heapq by jaccard similarity
            closest_perfects[teamsize] = heapq.nlargest(3, self.perfects[teamsize], key=lambda x: self.jaccard_similarity(board_state, set(x)))
        return closest_perfects






