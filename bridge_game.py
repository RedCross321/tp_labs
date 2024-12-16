import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 6
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
DOT_RADIUS = 8
LINE_WIDTH = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class BridgeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Bridge Game')
        self.size = GRID_SIZE
        self.lines = []  # Store lines as [(x1,y1,x2,y2,color)]
        self.current_player = 'Blue'
        self.selected_point = None
        self.game_over = False
        self.winner = None
        
    def draw_board(self):
        self.screen.fill(WHITE)
        
        # Draw grid points
        for i in range(self.size):
            for j in range(self.size):
                x = j * CELL_SIZE + CELL_SIZE // 2
                y = i * CELL_SIZE + CELL_SIZE // 2
                
                # Highlight selected point
                if self.selected_point and (j, i) == self.selected_point:
                    pygame.draw.circle(self.screen, GRAY, (x, y), DOT_RADIUS + 2)
                
                pygame.draw.circle(self.screen, BLACK, (x, y), DOT_RADIUS)
        
        # Draw lines
        for x1, y1, x2, y2, color in self.lines:
            start_pos = (x1 * CELL_SIZE + CELL_SIZE // 2, y1 * CELL_SIZE + CELL_SIZE // 2)
            end_pos = (x2 * CELL_SIZE + CELL_SIZE // 2, y2 * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(self.screen, BLUE if color == 'Blue' else RED, start_pos, end_pos, LINE_WIDTH)
        
        pygame.display.flip()
    
    def get_clicked_point(self, pos):
        x, y = pos
        # Convert screen coordinates to grid coordinates
        grid_x = round((x - CELL_SIZE // 2) / CELL_SIZE)
        grid_y = round((y - CELL_SIZE // 2) / CELL_SIZE)
        
        # Check if click is close enough to a grid point
        if 0 <= grid_x < self.size and 0 <= grid_y < self.size:
            point_x = grid_x * CELL_SIZE + CELL_SIZE // 2
            point_y = grid_y * CELL_SIZE + CELL_SIZE // 2
            if ((x - point_x) ** 2 + (y - point_y) ** 2) ** 0.5 < DOT_RADIUS * 2:
                return (grid_x, grid_y)
        return None
    
    def is_valid_move(self, x1, y1, x2, y2):
        # Check if points are adjacent
        if not ((abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)):
            return False
        
        # Check if points are within bounds
        if not all(0 <= x < self.size for x in [x1, x2, y1, y2]):
            return False
        
        # Create new line
        new_line = (x1, y1, x2, y2, self.current_player)
        
        # Check for intersections with ANY existing lines
        for line in self.lines:
            if self.lines_intersect(new_line, line):
                return False
            # Also check if line already exists
            if (x1, y1, x2, y2) == line[:4] or (x2, y2, x1, y1) == line[:4]:
                return False
        
        return True
    
    def lines_intersect(self, line1, line2):
        x1, y1, x2, y2 = line1[:4]
        x3, y3, x4, y4 = line2[:4]
        
        # Check if lines share an endpoint
        if (x1, y1) in [(x3, y3), (x4, y4)] or (x2, y2) in [(x3, y3), (x4, y4)]:
            return False
            
        # If both lines are horizontal
        if y1 == y2 and y3 == y4:
            if y1 == y3:  # Same height
                return not (max(x1, x2) < min(x3, x4) or min(x1, x2) > max(x3, x4))
            return False
            
        # If both lines are vertical
        if x1 == x2 and x3 == x4:
            if x1 == x3:  # Same vertical
                return not (max(y1, y2) < min(y3, y4) or min(y1, y2) > max(y3, y4))
            return False
            
        # If one is horizontal and one is vertical
        if x1 == x2:  # First line is vertical
            if min(y1, y2) <= y3 <= max(y1, y2) and min(x3, x4) <= x1 <= max(x3, x4):
                return True
        elif x3 == x4:  # Second line is vertical
            if min(y3, y4) <= y1 <= max(y3, y4) and min(x1, x2) <= x3 <= max(x1, x2):
                return True
            
        return False
    
    def make_move(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2):
            self.lines.append((x1, y1, x2, y2, self.current_player))
            return True
        return False
    
    def get_connected_points(self, x, y, color):
        connected = set()
        to_visit = [(x, y)]
        
        while to_visit:
            curr_x, curr_y = to_visit.pop()
            if (curr_x, curr_y) in connected:
                continue
                
            connected.add((curr_x, curr_y))
            
            # Check all lines of the same color
            for line in self.lines:
                x1, y1, x2, y2, line_color = line
                if line_color != color:
                    continue
                    
                # If current point is at either end of the line
                if (x1, y1) == (curr_x, curr_y) and (x2, y2) not in connected:
                    to_visit.append((x2, y2))
                elif (x2, y2) == (curr_x, curr_y) and (x1, y1) not in connected:
                    to_visit.append((x1, y1))
                    
        return connected
    
    def check_winner(self):
        # Check Blue's win (top to bottom)
        blue_points = set()
        for line in self.lines:
            if line[4] == 'Blue':
                x1, y1, x2, y2, _ = line
                if y1 == 0:
                    blue_points.update(self.get_connected_points(x1, y1, 'Blue'))
                if y2 == 0:
                    blue_points.update(self.get_connected_points(x2, y2, 'Blue'))
        
        if any(y == self.size - 1 for _, y in blue_points):
            return 'Blue'
        
        # Check Red's win (left to right)
        red_points = set()
        for line in self.lines:
            if line[4] == 'Red':
                x1, y1, x2, y2, _ = line
                if x1 == 0:
                    red_points.update(self.get_connected_points(x1, y1, 'Red'))
                if x2 == 0:
                    red_points.update(self.get_connected_points(x2, y2, 'Red'))
        
        if any(x == self.size - 1 for x, _ in red_points):
            return 'Red'
        
        return None
    
    def ai_move(self):
        valid_moves = []
        # First try to find moves that could lead to victory
        for x1 in range(self.size):
            for y1 in range(self.size):
                # Check horizontal moves
                if x1 < self.size - 1 and self.is_valid_move(x1, y1, x1 + 1, y1):
                    valid_moves.append((x1, y1, x1 + 1, y1))
                # Check vertical moves
                if y1 < self.size - 1 and self.is_valid_move(x1, y1, x1, y1 + 1):
                    valid_moves.append((x1, y1, x1, y1 + 1))
        
        if valid_moves:
            # Prioritize moves that are closer to completing a path
            best_moves = []
            best_score = -1
            
            for move in valid_moves:
                x1, y1, x2, y2 = move
                # Prefer moves that are closer to the right side
                score = max(x1, x2)
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
            
            if best_moves:
                move = random.choice(best_moves)
                self.make_move(*move)
                return True
        
        return False
    
    def draw_play_again_screen(self):
        self.screen.fill(WHITE)
        
        # Draw "Play Again?" text
        font = pygame.font.Font(None, 74)
        text = font.render('Play Again?', True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 - 50))
        self.screen.blit(text, text_rect)
        
        # Draw Yes/No buttons
        yes_font = pygame.font.Font(None, 50)
        no_font = pygame.font.Font(None, 50)
        
        yes_text = yes_font.render('Yes', True, BLUE)
        no_text = no_font.render('No', True, RED)
        
        yes_rect = yes_text.get_rect(center=(WINDOW_SIZE/3, WINDOW_SIZE/2 + 50))
        no_rect = no_text.get_rect(center=(2*WINDOW_SIZE/3, WINDOW_SIZE/2 + 50))
        
        self.screen.blit(yes_text, yes_rect)
        self.screen.blit(no_text, no_rect)
        
        pygame.display.flip()
        
        # Wait for user click
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if yes_rect.collidepoint(mouse_pos):
                        return True
                    if no_rect.collidepoint(mouse_pos):
                        return False
    
    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.current_player == 'Blue':
                    clicked_point = self.get_clicked_point(event.pos)
                    if clicked_point:
                        if self.selected_point is None:
                            self.selected_point = clicked_point
                        else:
                            x1, y1 = self.selected_point
                            x2, y2 = clicked_point
                            if self.make_move(x1, y1, x2, y2):
                                self.current_player = 'Red'
                            self.selected_point = None
            
            # AI move
            if self.current_player == 'Red' and not self.game_over:
                if self.ai_move():
                    self.current_player = 'Blue'
                else:
                    # If AI can't make a move, it loses
                    self.game_over = True
                    self.winner = 'Blue'
                    print("AI has no valid moves! Blue wins!")
            
            # Check for winner
            winner = self.check_winner()
            if winner:
                self.game_over = True
                self.winner = winner
                print(f"{winner} wins!")
            
            self.draw_board()
            
            # Draw game over message
            if self.game_over:
                font = pygame.font.Font(None, 74)
                text = font.render(f'{self.winner} Wins!', True, BLUE if self.winner == 'Blue' else RED)
                text_rect = text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait 2 seconds before showing play again screen
                return self.draw_play_again_screen()

def main():
    while True:
        game = BridgeGame()
        if not game.run():  # If player chooses not to play again
            break
    
    pygame.quit()
    sys.exit()

main()
