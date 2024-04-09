from random import choice, randint

import pygame

# Определение констант
ZERO_POS = (0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SPEED = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=ZERO_POS, body_color=RED):
        """
        Инициализация нового объекта.
        Принимающий расположения объекта и цвет.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Отрисовка объекта на игровом поле
        С указанием поверхности для отрисовки и размера блока.
        """
        pygame.draw.rect(surface, self.body_color, pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE))


class Apple(GameObject):
    """Класс для яблока на игровом поле."""

    def __init__(self, body_color=RED, snake_positions=None):
        """
        Инициализация нового яблока.
        Принимает параметры родительского класса GameObject и позиции змейки.
        """
        super().__init__(body_color)
        self.randomize_position(snake_positions)

    def randomize_position(self, occupied_positions):
        """Случайное изменение позиции яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1),
                         randint(0, GRID_HEIGHT - 1))
        while self.position in occupied_positions:
            self.position = (randint(0, GRID_WIDTH - 1),
                             randint(0, GRID_HEIGHT - 1))


class Snake(GameObject):
    """Класс для змеи на игровом поле. Наследует от класса GameObject."""

    def __init__(self):
        """Инициализация новой змеи с параметрами координаты и цвета."""
        self.body_color = GREEN
        self.reset()

    def draw(self, surface):
        """
        Отрисовка змеи на игровом поле
        С указанием поверхности для отрисовки и размера блока.
        """
        block_size = GRID_SIZE
        for pos in self.positions:
            pygame.draw.rect(surface, self.body_color, pygame.Rect(
                pos[0] * block_size, pos[1] * block_size,
                block_size, block_size))

    def get_head_position(self):
        """Получение позиции головы змеи."""
        return self.positions[0]

    def move(self, grow=False):
        """Движение змеи на игровом поле и направление движения."""
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + self.direction[0]) % GRID_WIDTH,
                    (head_y + self.direction[1]) % GRID_HEIGHT)

        self.positions.insert(0, new_head)

        if not grow:
            self.positions.pop()

    def reset(self):
        """Сброс позиции змеи и направления движения."""
        self.position = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [self.position]

    def update_direction(self, new_direction):
        """Обновление направления движения змеи."""
        self.direction = new_direction
        # я заменил, но теперь змейка может ходить в обратную сторону
        # прошлый вариант не позволил ей так делать


def handle_keys(snake):
    """
    Обработка нажатий клавиш для управления змеей.
    Snake: объект для обновления направления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple(RED, snake.positions)

    while True:
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.move(grow=True)
        else:
            snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
