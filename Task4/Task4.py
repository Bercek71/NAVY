import pygame
import random
import numpy as np
import time

pygame.init()

WIDTH, HEIGHT = 1000, 800
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
BUTTON_HEIGHT = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)  # barva pro stěny

# načtení obrázků
assetFolder = "assets/"

mouse_img = pygame.image.load(assetFolder + "mouse.png")
mouse_img = pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE))
cheese_img = pygame.image.load(assetFolder + "cheese.png")
cheese_img = pygame.transform.scale(cheese_img, (CELL_SIZE, CELL_SIZE))
trap_img = pygame.image.load(assetFolder + "trap.png")
trap_img = pygame.transform.scale(trap_img, (CELL_SIZE, CELL_SIZE))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find the Cheese - Q-Learning")

#parametry Q-learningu
alpha = 0.1
gamma = 0.9
epsilon = 0.2
q_table = np.zeros((GRID_SIZE, GRID_SIZE, 4))  # 4 akce (nahoru, dolů, doleva, doprava)


original_mouse_pos = (0, 0)
mouse_pos = (0, 0)
cheese_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
traps = []
walls = []
placing_mode = None
game_started = False
is_training = False

class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action
        self.active = False

    def draw(self):
        pygame.draw.rect(screen, self.color if not self.active else DARK_GRAY, self.rect)
        font = pygame.font.Font(None, 30)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# tlačítka
def start_game():
    global game_started, mouse_pos, cheese_pos, traps, walls, is_training
    game_started = True
    is_training = True

    print("Game Started!")

def train_q_learning():
    global q_table
    print("Training agent with Q-learning...")
    for episode in range(10000):
        state = mouse_pos
        done = False
        while not done:
            action = q_learning_step(state)
            next_state = take_action(state, action)
            reward = get_reward(next_state)
            update_q_table(state, action, reward, next_state)
            state = next_state
            if state == cheese_pos:  # hra skončila
                done = True
    print("Training finished!")

def q_learning_step(state):
    if random.uniform(0, 1) < epsilon:
        action = random.choice([0, 1, 2, 3])  # náhodná akce 1 - nahoru, 2 - dolů, 3 - doleva, 4 - doprava
    else:
        action = np.argmax(q_table[state[0], state[1]])  # nejlepší akce
    return action

def take_action(state, action):
    x, y = state
    if action == 0:  # Up
        new_state = (max(0, x - 1), y)
    elif action == 1:  # Down
        new_state = (min(GRID_SIZE - 1, x + 1), y)
    elif action == 2:  # Left
        new_state = (x, max(0, y - 1))
    elif action == 3:  # Right
        new_state = (x, min(GRID_SIZE - 1, y + 1))
    if valid_move(new_state):
        return new_state
    return state  # pokud je tah neplatný, zůstaňte na stejném místě

def get_reward(state):
    if state == cheese_pos:
        return 10  # odměna za nalezení sýra
    elif state in traps:
        return -10  # trest za nalezení pasti
    else:
        return -1  # malá ztráta za každý krok

def update_q_table(state, action, reward, next_state):
    max_future_q = np.max(q_table[next_state[0], next_state[1]])
    current_q = q_table[state[0], state[1], action]
    new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)
    q_table[state[0], state[1], action] = new_q

def reset_game():
    global mouse_pos, original_mouse_pos,  traps, cheese_pos, walls, is_training, game_started
    is_training = False
    game_started = False
    mouse_pos = original_mouse_pos
    print("Game reset!")

def set_mouse():
    global placing_mode
    placing_mode = "mouse"
    print("Placing mouse...")

def set_cheese():
    global placing_mode
    placing_mode = "cheese"
    print("Placing cheese...")

def set_trap():
    global placing_mode
    placing_mode = "trap"
    print("Placing traps...")

def set_wall():
    global placing_mode
    placing_mode = "wall"
    print("Placing walls...")


buttons = [
    Button("Start", 50, HEIGHT - BUTTON_HEIGHT, 100, 40, BLUE, start_game),
    Button("Train", 200, HEIGHT - BUTTON_HEIGHT, 100, 40, GREEN, train_q_learning),
    Button("Reset", 350, HEIGHT - BUTTON_HEIGHT, 100, 40, RED, reset_game),
    Button("Mouse", 500, HEIGHT - BUTTON_HEIGHT, 100, 40, BLUE, set_mouse),
    Button("Cheese", 620, HEIGHT - BUTTON_HEIGHT, 100, 40, GREEN, set_cheese),
    Button("Trap", 740, HEIGHT - BUTTON_HEIGHT, 100, 40, RED, set_trap),
    Button("Wall", 860, HEIGHT - BUTTON_HEIGHT, 100, 40, BROWN, set_wall)
]

# kontrola platnosti tahu
def valid_move(position):
    x, y = position
    if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
        return False
    if (x, y) in walls or (x, y) in traps:  # nemůžete jít skrz stěny nebo pasti
        return False
    return True


running = True

def main_loop():
    global mouse_pos, cheese_pos, traps, walls, is_training, original_mouse_pos
    while running:
        screen.fill(WHITE)

        # vykreslení gridu
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT - BUTTON_HEIGHT))
        for y in range(0, HEIGHT - BUTTON_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # kreslení objektů
        screen.blit(mouse_img, (mouse_pos[1] * CELL_SIZE, mouse_pos[0] * CELL_SIZE))
        screen.blit(cheese_img, (cheese_pos[1] * CELL_SIZE, cheese_pos[0] * CELL_SIZE))
        for trap in traps:
            screen.blit(trap_img, (trap[1] * CELL_SIZE, trap[0] * CELL_SIZE))
        for wall in walls:
            pygame.draw.rect(screen, BROWN, (wall[1] * CELL_SIZE, wall[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


        # kreslení tlačítek
        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] < HEIGHT - BUTTON_HEIGHT:
                    grid_x, grid_y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                    if placing_mode == "mouse":
                        mouse_pos = (grid_x, grid_y)
                        original_mouse_pos = mouse_pos
                    elif placing_mode == "cheese":
                        cheese_pos = (grid_x, grid_y)
                    elif placing_mode == "trap":
                        if (grid_x, grid_y) != mouse_pos and (grid_x, grid_y) != cheese_pos:
                            traps.append((grid_x, grid_y))
                    elif placing_mode == "wall":
                        if (grid_x, grid_y) != mouse_pos and (grid_x, grid_y) != cheese_pos:
                            walls.append((grid_x, grid_y))
                else:  
                    for button in buttons:
                        button.click(pos)
                        button.active = button.text.lower() == placing_mode



        if is_training:
            action = q_learning_step(mouse_pos)
            mouse_pos = take_action(mouse_pos, action)
            pygame.time.delay(100)
            if mouse_pos == cheese_pos:
                print("Mouse found the cheese!")
                reset_game()


        pygame.display.flip()

if __name__ == "__main__":
    main_loop()