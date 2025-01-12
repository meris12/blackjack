from typing import List
from card import Card

class Player:
    def __init__(self, balance: int = 1000):
        self.balance = balance
        self.bet = 0
        self.hand: List[Card] = []
        
    def clear_hand(self):
        self.hand = []
        
    def add_card(self, card: Card):
        self.hand.append(card)
        
    def get_score(self) -> int:
        scores = [0]
        
        for card in self.hand:
            new_scores = []
            for value in card.value:
                for score in scores:
                    new_scores.append(score + value)
            scores = new_scores
            
        valid_scores = [s for s in scores if s <= 21]
        return max(valid_scores) if valid_scores else min(scores)
        
    def has_blackjack(self) -> bool:
        return len(self.hand) == 2 and self.get_score() == 21

class Dealer(Player):
    def __init__(self):
        super().__init__()
        
    def should_hit(self) -> bool:
        return self.get_score() < 17 