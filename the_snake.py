from random import choice, randint

import pygame


# Определение класса GameObject
class GameObject:
    """
    Базовый класс для игровых объектов.
    """
    def __init__(self, position, body_color):
        """
        Инициализация нового объекта.
        Принимающий расположения объекта и цвет.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface, block_size):
        """
        Отрисовка объекта на игровом поле
        С указанием поверхности для отрисовки и размера блока.
        """
        pygame.draw.rect(surface, self.body_color, pygame.Rect(
            self.position[0] * block_size,
            self.position[1] * block_size,
            block_size, block_size))


class Apple(GameObject):
    """
    Класс для яблока на игровом поле.
    """
    def __init__(self, position, body_color):
        """
        Инициализация нового яблока.
        С параметрами родительского класса GameObject.
        """
        super().__init__(position, body_color)

    def randomize_position(self, grid_width, grid_height):
        """
        Случайное изменение позиции яблока на игровом поле.
        """
        self.position = (randint(0, grid_width - 1),
                         randint(0, grid_height - 1))


class Snake(GameObject):
    """
    Класс для змеи на игровом поле.

    Наследует от класса GameObject.
    """
    def __init__(self, position, body_color):
        """
        Инициализация новой змеи
        С параметрами координаты и цвета.
        """
        super().__init__(position, body_color)
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

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
        """
        Получение позиции головы змеи.
        """
        return self.positions[0]

    def move(self, direction, grow=False):
        """
        Движение змеи на игровом поле и направление движения.
        """
        x, y = self.get_head_position()
        if direction == UP:
            self.positions.insert(0, (x, y - 1))
        elif direction == DOWN:
            self.positions.insert(0, (x, y + 1))
        elif direction == LEFT:
            self.positions.insert(0, (x - 1, y))
        elif direction == RIGHT:
            self.positions.insert(0, (x + 1, y))

        if not grow:
            self.positions.pop()

    def reset(self, position):
        """
        Сброс позиции змеи и направления движения.
        """
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def update_direction(self, new_direction):
        """
        Обновление направления движения змеи.
        """
        new_1 = new_direction[1]
        slf = self.direction
        if new_direction[0] * -1 != slf[0] or new_1 * -1 != slf[1]:
            self.direction = new_direction


# Определение констант
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


def handle_keys(snake):
    """
    Обработка нажатий клавиш для управления змеей.
    snake: объект для обновления направления.
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
    """
    Основная функция игры.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2), (0, 255, 0))
    apple = Apple((randint(0, GRID_WIDTH - 2),
                   randint(0, GRID_HEIGHT - 2)), (255, 0, 0))

    while True:
        handle_keys(snake)

        snake.move(snake.direction)
        if snake.get_head_position() == apple.position:
            apple.randomize_position(GRID_WIDTH, GRID_HEIGHT)
            snake.move(snake.direction, grow=True)

        # Обработка столкновения с краями экрана
        head_x, head_y = snake.get_head_position()
        if head_x < 0:
            head_x = GRID_WIDTH - 1
        elif head_x >= GRID_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = GRID_HEIGHT - 1
        elif head_y >= GRID_HEIGHT:
            head_y = 0
        snake.positions[0] = (head_x, head_y)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset((GRID_WIDTH // 2, GRID_HEIGHT // 2))

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen, GRID_SIZE)
        apple.draw(screen, GRID_SIZE)
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
