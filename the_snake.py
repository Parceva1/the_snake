from random import randint

import pygame

# Инициализация PyGame:
pygame.init()


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (255, 255, 255)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Задержка между каждым движением змеи (в миллисекундах):
MOVE_INTERVAL = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class Apple:
    def __init__(self):
        self.position = (200, 200)
        self.body_color = APPLE_COLOR

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake:
    def __init__(self):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.move_counter = 0

    def draw(self):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        self.move_counter += 1
        if self.move_counter >= MOVE_INTERVAL:
            # Сохраняем предыдущее положение головы
            prev_segment = self.positions[0]

            # Перемещаем голову змейки в новое место
            x, y = self.direction
            new_head_pos = (self.positions[0][0] + x * GRID_SIZE, self.positions[0][1] + y * GRID_SIZE)
            if new_head_pos[0] >= SCREEN_WIDTH:
                new_head_pos = (0, new_head_pos[1])
            elif new_head_pos[0] < 0:
                new_head_pos = (SCREEN_WIDTH - GRID_SIZE, new_head_pos[1])
            elif new_head_pos[1] >= SCREEN_HEIGHT:
                new_head_pos = (new_head_pos[0], 0)
            elif new_head_pos[1] < 0:
                new_head_pos = (new_head_pos[0], SCREEN_HEIGHT - GRID_SIZE)
            if new_head_pos in self.positions:
                pygame.quit()

            # Проверяем, съедено ли яблоко
            if new_head_pos == apple.position:
                # Создаем новую позицию для нового последнего сегмента
                new_tail_pos = (prev_segment[0] - x * GRID_SIZE, prev_segment[1] - y * GRID_SIZE)
                self.positions.append(new_tail_pos)
                apple.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

            # Перемещаем остальные сегменты
            self.positions[0] = new_head_pos
            for i in range(1, len(self.positions)):
                temp = self.positions[i]
                self.positions[i] = prev_segment
                prev_segment = temp

            self.move_counter = 0


def main():
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT

        snake.move(apple)
        snake.update_direction()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
