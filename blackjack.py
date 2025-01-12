import os
import pygame
import sys
from typing import Optional
from deck import Deck
from player import Player, Dealer
from card import Card


WINDOW_SIZE = (800, 600)
CARD_SIZE = (71, 96)  
FPS = 60


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVY = (53, 71, 94)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class BlackjackGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Блэкджек")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        
        self.card_images = {}
        self.load_card_images()
        
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.game_state = "betting"
        
    def load_card_images(self):
        
        self.card_back = pygame.image.load(os.path.join('assets', 'cards', 'back.png'))
        self.card_back = pygame.transform.scale(self.card_back, CARD_SIZE)
        
        
        suits = {'♠': 'spades', '♣': 'clubs', '♥': 'hearts', '♦': 'diamonds'}
        ranks = {'A': 'ace', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
                '8': '8', '9': '9', '10': '10', 'J': 'jack', 'Q': 'queen', 'K': 'king'}
        
        for suit, suit_name in suits.items():
            for rank, rank_name in ranks.items():
                
                card_surface = pygame.Surface(CARD_SIZE)
                card_surface.fill(WHITE)
                
                
                image_path = os.path.join('assets', 'cards', f'{rank_name}_of_{suit_name}.png')
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, CARD_SIZE)
                
                
                card_surface.blit(image, (0, 0))
                
                
                pygame.draw.rect(card_surface, BLACK, card_surface.get_rect(), 1)
                
                self.card_images[f"{rank}{suit}"] = card_surface
        
    def draw_card(self, card: Card, pos: tuple[int, int]):
        
        card_rect = pygame.Rect(pos[0], pos[1], CARD_SIZE[0], CARD_SIZE[1])
        pygame.draw.rect(self.screen, WHITE, card_rect)
        pygame.draw.rect(self.screen, BLACK, card_rect, 1)  
        
        if not card.face_up:
            self.screen.blit(self.card_back, pos)
        else:
            card_key = str(card)
            self.screen.blit(self.card_images[card_key], pos)
        
    def draw_text(self, text: str, pos: tuple[int, int], color: tuple[int, int, int] = WHITE, small: bool = False):
        font = self.small_font if small else self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)
        
    def draw_cards(self, cards: list[Card], pos: tuple[int, int], dealer: bool = False):
        for i, card in enumerate(cards):
            card_pos = (pos[0] + i*80, pos[1])
            self.draw_card(card, card_pos)
        
    def draw_button(self, text: str, pos: tuple[int, int], size: tuple[int, int], 
                   color: tuple[int, int, int] = WHITE) -> pygame.Rect:
        button_rect = pygame.Rect(pos[0] - size[0]//2, pos[1] - size[1]//2, size[0], size[1])
        pygame.draw.rect(self.screen, color, button_rect, 2)
        self.draw_text(text, pos)
        return button_rect
        
    def draw_game(self):
        self.screen.fill(NAVY)
        
        buttons = {}
        
        
        balance_text = f"Баланс: {self.player.balance:,}".replace(',', ' ')
        bet_text = f"Ставка: {self.player.bet:,}".replace(',', ' ')
        self.draw_text(balance_text, (100, 30))
        self.draw_text(bet_text, (300, 30))
        
        
        if self.player.balance <= 0 and self.player.bet <= 0:
            
            text_surface = self.font.render("ИГРА ОКОНЧЕНА!", True, WHITE)
            text_rect = text_surface.get_rect(center=(400, 250))
            bg_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, RED, bg_rect, 3)  
            self.draw_text("ИГРА ОКОНЧЕНА!", (400, 250), RED)
            
            
            buttons["reset_game"] = self.draw_button("Начать заново", (400, 350), (200, 50))
            return buttons
        
        
        if self.game_state != "betting": 
            self.draw_text("Карты дилера:", (250, 70))
            self.draw_cards(self.dealer.hand, (100, 100), True)
            
           
            if self.game_state == "game_over":
                self.draw_text(f"Счет дилера: {self.dealer.get_score()}", (100, 220))
            
            if self.game_state == "game_over":
               
                result_text = self.get_result_text()
                
                text_surface = self.font.render(result_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(400, 270))
               
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, BLACK, bg_rect)
                pygame.draw.rect(self.screen, RED, bg_rect, 2) 
                self.draw_text(result_text, (400, 270), WHITE)
            
        
            self.draw_text("Ваши карты:", (250, 350))
            self.draw_cards(self.player.hand, (100, 380))
            
            
            self.draw_text(f"Ваш счет: {self.player.get_score()}", (100, 520))
            
            if self.game_state == "game_over":
               
                buttons["new_game"] = self.draw_button("Новая игра", (100, 560), (150, 40))
        
    
        if self.game_state == "betting":
            buttons["bet_10"] = self.draw_button("+10", (500, 30), (60, 40))
            buttons["bet_50"] = self.draw_button("+50", (580, 30), (60, 40))
            buttons["bet_100"] = self.draw_button("+100", (660, 30), (70, 40))
            buttons["deal"] = self.draw_button("Сдать", (600, 100), (100, 40))
        elif self.game_state == "playing":
            buttons["hit"] = self.draw_button("Взять карту", (650, 400), (150, 40))
            buttons["stand"] = self.draw_button("Вскрыться", (650, 460), (150, 40))
            
        pygame.display.flip()
        return buttons
        
    def get_result_text(self) -> str:
        player_score = self.player.get_score()
        dealer_score = self.dealer.get_score()
        
        if player_score > 21:
            return "Перебор! Вы проиграли"
        elif dealer_score > 21:
            return "Дилер перебрал! Вы выиграли!"
        elif player_score > dealer_score:
            return "Вы выиграли!"
        elif player_score < dealer_score:
            return "Дилер выиграл"
        else:
            return "Ничья!"

    def handle_betting(self, button_clicked: Optional[str]):
        if not button_clicked:
            return
            
        if button_clicked == "bet_10" and self.player.balance >= 10:
            self.player.bet += 10
            self.player.balance -= 10
        elif button_clicked == "bet_50" and self.player.balance >= 50:
            self.player.bet += 50
            self.player.balance -= 50
        elif button_clicked == "bet_100" and self.player.balance >= 100:
            self.player.bet += 100
            self.player.balance -= 100
        elif button_clicked == "deal" and self.player.bet > 0:
            self.start_round()
            
    def start_round(self):
        self.deck = Deck()
        self.player.clear_hand()
        self.dealer.clear_hand()
        
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        dealer_card = self.deck.deal()
        dealer_card.face_up = False
        self.dealer.add_card(dealer_card)
        
        self.game_state = "playing"
        
    def handle_playing(self, button_clicked: Optional[str]):
        if not button_clicked:
            return
            
        if button_clicked == "hit":
            self.player.add_card(self.deck.deal())
            if self.player.get_score() > 21:
                self.end_round()
        elif button_clicked == "stand":
            self.dealer_turn()
            
    def dealer_turn(self):
        self.dealer.hand[1].face_up = True
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
        self.end_round()
        
    def end_round(self):
        player_score = self.player.get_score()
        dealer_score = self.dealer.get_score()
        
        if player_score > 21:
            pass
        elif dealer_score > 21 or player_score > dealer_score:
            if self.player.has_blackjack():
                self.player.balance += int(self.player.bet * 2.5)
            else:
                self.player.balance += self.player.bet * 2
        elif player_score < dealer_score:
            pass
        else:
            self.player.balance += self.player.bet
            
        self.player.bet = 0
        self.game_state = "game_over"
        
        if self.player.balance <= 0:
            self.draw_game()
            pygame.display.flip()

    def run(self):
        running = True
        while running:
            button_clicked = None
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    buttons = self.draw_game()
                    for name, rect in buttons.items():
                        if rect.collidepoint(mouse_pos):
                            button_clicked = name
            
            if button_clicked == "reset_game":
                self.player = Player()
                self.dealer = Dealer()
                self.deck = Deck()
                self.game_state = "betting"
            elif self.game_state == "betting":
                self.handle_betting(button_clicked)
            elif self.game_state == "playing":
                self.handle_playing(button_clicked)
            elif self.game_state == "game_over" and button_clicked == "new_game":
                if self.player.balance > 0:
                    self.player.clear_hand()
                    self.dealer.clear_hand()
                    self.game_state = "betting"
                else:
                    self.draw_game()
            
            if self.player.balance > 0 or button_clicked == "reset_game":
                self.draw_game()
            
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BlackjackGame()
    game.run() 