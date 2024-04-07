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

    def draw(self, surface, grid_size):
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

    def __init__(self, position=ZERO_POS, body_color=RED):
        """
        Инициализация нового яблока.
        С параметрами родительского класса GameObject.
        """
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Случайное изменение позиции яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1),
                         randint(0, GRID_HEIGHT - 1))


class Snake(GameObject):
    """Класс для змеи на игровом поле. Наследует от класса GameObject."""

    def __init__(self, position=ZERO_POS, body_color=GREEN):
        """Инициализация новой змеи с параметрами координаты и цвета."""
        super().__init__(position, body_color)
        self.positions = [position]
        self.reset()

    def draw(self, surface, block_size):
        """
        Отрисовка змеи на игровом поле
        С указанием поверхности для отрисовки и размера блока.
        """
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
        if self.direction == UP:
            new_head = (head_x + UP[0], head_y + UP[1])
        elif self.direction == DOWN:
            new_head = (head_x + DOWN[0], head_y + DOWN[1])
        elif self.direction == LEFT:
            new_head = (head_x + LEFT[0], head_y + LEFT[1])
        elif self.direction == RIGHT:
            new_head = (head_x + RIGHT[0], head_y + RIGHT[1])

        self.positions.insert(0, new_head)

        if not grow:
            self.positions.pop()
        # у меня не получилось сделать работающий вариант с %
        # при замене на метод с % змейка съезжает и не может совпасть с яблоком
        # ещё ломается скорость змейки и её растягивает и появляются дыры
        head_x, head_y = self.get_head_position()
        if head_x < 0:
            head_x = GRID_WIDTH - 1
        elif head_x >= GRID_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = GRID_HEIGHT - 1
        elif head_y >= GRID_HEIGHT:
            head_y = 0
        self.positions[0] = (head_x, head_y)

    def reset(self):
        """Сброс позиции змеи и направления движения."""
        self.position = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [self.position]

    def update_direction(self, new_direction):
        """Обновление направления движения змеи."""
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction


def handle_keys(snake):
    """
    Обработка нажатий клавиш для управления змеей.
    Snake: объект для обновления направления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2), GREEN)
    apple = Apple((randint(0, GRID_WIDTH - 2),
                   randint(0, GRID_HEIGHT - 2)), RED)

    while True:
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            # теперь яблоки не могут появиться в змее, костыльно но работает
            while apple.position in snake.positions:
                apple.randomize_position()
            snake.move(grow=True)
        else:
            snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen, GRID_SIZE)
        apple.draw(screen, GRID_SIZE)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
