import random
from card import Card, Suit, Rank

class Deck:
    SUITS: list[Suit] = ['♠', '♣', '♥', '♦']
    RANKS: list[Rank] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self) -> Card:
        return self.cards.pop() 