from dataclasses import dataclass
from typing import Literal

Suit = Literal['♠', '♣', '♥', '♦']
Rank = Literal['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

@dataclass
class Card:
    rank: Rank
    suit: Suit
    face_up: bool = True
    
    def __str__(self):
        if not self.face_up:
            return "🂠"
        return f"{self.rank}{self.suit}"
        
    @property
    def value(self) -> list[int]:
        if self.rank == 'A':
            return [1, 11]
        elif self.rank in ['J', 'Q', 'K']:
            return [10]
        return [int(self.rank)] 