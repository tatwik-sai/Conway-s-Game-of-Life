import pygame

pygame.init()


class CGL:
    """Implementation of 'Conway's Game of Life'"""
    def __init__(self, shape: tuple = (33, 65), size: int = 20):
        # Variables
        self.running = True
        self.shape = shape
        self.size = size
        self.adding_cell = False
        self.removing_cell = False
        self.simulating = False
        self.blocks = []

        # Sizes
        self.shape = self.shape
        self.block_size = self.size
        self.gap = 1
        self.width = self.shape[1] * self.block_size + (self.shape[1] + 1) * self.gap
        self.height = self.shape[0] * self.block_size + (self.shape[0] + 1) * self.gap

        # Display
        self.screen = pygame.display.set_mode((self.width, self.height))
        # pygame.display.set_icon(pygame.image.load('icon.png'))
        pygame.display.set_caption("Conway's Game of Life" + str(shape))

        # Colors
        self.bg_color = (0, 255, 255)
        self.block_color = [(255, 255, 255), (0, 0, 0)]

        # Adding Blocks
        x, y = self.gap, self.gap
        for i in range(self.shape[0]):
            row_blocks = []
            for j in range(self.shape[1]):
                row_blocks.append([pygame.Rect((x, y), (self.block_size, self.block_size)), 0])
                x += self.block_size + self.gap
            self.blocks.append(row_blocks)
            x = self.gap
            y += self.block_size + self.gap

    def draw(self):
        """
        Draws Everything on to the screen based on the state of the block i.e (dead: 0, alive: 1).
        """
        self.screen.fill(self.bg_color)
        for row in self.blocks:
            for block in row:
                pygame.draw.rect(self.screen, self.block_color[block[1]], block[0], border_radius=5)
        pygame.display.flip()

    def handle_clicks(self, pos: tuple):
        """
        Handles the mouse click and draws and erases blocks from the screen.
        :param pos: The position of the mouse click.
        """
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                if self.blocks[row][col][0].collidepoint(pos):
                    if self.adding_cell and self.blocks[row][col][1] == 0:
                        self.blocks[row][col][1] = 1
                    elif self.removing_cell and self.blocks[row][col][1] == 1:
                        self.blocks[row][col][1] = 0

    def num_neighbours(self, pos: tuple) -> int:
        """
        Returns number of neighbours around the block.
        :param pos: The blocks alive around the block.
        """
        x, y = pos
        neighbours_pos = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1),
                          (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
        num_neighbours = 0
        for pos in neighbours_pos:
            if all([not(pos[0] < 0), not(pos[0] >= self.shape[0]), not(pos[1] < 0), not(pos[1] >= self.shape[1])]):
                if self.blocks[pos[0]][pos[1]][1] == 1:
                    num_neighbours += 1
        return num_neighbours

    def simulate(self):
        """
        Goes through one iteration of all the blocks and reassigns the values of the block
         based on number of neighbors alive.
        """
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                neighbours = self.num_neighbours((row, col))
                new_state = 0
                if self.blocks[row][col][1] == 1:
                    if neighbours in [2, 3]:
                        new_state = 1
                else:
                    if neighbours == 3:
                        new_state = 1
                self.blocks[row][col][1] = new_state

    def main(self):
        """
        The main function that checks for events and runs the game loop.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.adding_cell = True
                    elif event.button == 3:
                        self.removing_cell = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.adding_cell = False
                    elif event.button == 3:
                        self.removing_cell = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.simulating = not self.simulating
                    elif event.key == pygame.K_RETURN:
                        self.simulate()
                    elif event.key == pygame.K_r:
                        self.__init__(self.shape, self.size)
            if any([self.adding_cell, self.removing_cell]):
                self.handle_clicks(pygame.mouse.get_pos())
            elif self.simulating:
                self.simulate()
            self.draw()


if __name__ == '__main__':
    """
    Mouse Clicks:
        left: To Draw Blocks on to the screen.
        right: To erase blocks from the screen.
    Key Presses:
        space: Simulates the conway's game of life. 
        enter: Goes through frame by frame.
        r: Resets the game.
    """
    # cgl = CGL()
    cgl = CGL(shape=(80, 160), size=8)
    cgl.main()
