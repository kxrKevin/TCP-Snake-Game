import socket
import snake
import pygame

cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
cSocket.connect(("localhost", 5555))

# Draws the gridspace 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

def redrawWindow(surface):
    global rows, width, s, snacks
    surface.fill((0, 0, 0))
    for i in snacks:
        i.draw(surface)
    snakes[0].draw(surface, True)
    for i in snakes[1:]:
        i.draw(surface)
    drawGrid(width, 20, surface)
    pygame.display.update() 

# Splits the state sent by the server and reassigned to both the snake and snacks
def parseState(state):
    state = state.split('|')
    snakes = state[0].split('*')
    snacks = state[1].split("**")
    
    for i in range(len(snakes)):
        snakes[i] = snake.cube(eval(snakes[i].strip("()")))
    for i in range(len(snacks)):
        snacks[i] = snake.cube(eval(snacks[i].strip("()")), 1, 0, (0, 255, 0))
    return snakes, snacks

def main():

    # if you ask me, the width and rows variables are kind of dumb
    global width, rows, snakes, snacks
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    clock = pygame.time.Clock()
    
    # i don't know why the tutorial guy used a flag it seems absolutely pointless
    # works fine without it
    while True:
        pygame.time.delay(50)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            # wasd controls for the TA's convenience
            for i in keys:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    action = 'up'
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    action = 'down'
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    action = 'left'
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    action = 'right'
                elif keys[pygame.K_r]:
                    action = 'reset'
                elif keys[pygame.K_ESCAPE]:
                    action = 'quit'
                    pygame.quit()
                    break
                else:
                    action = 'get'

        cSocket.send(action.encode())
        state = cSocket.recv(500).decode()

        snakes, snacks = parseState(state)
        redrawWindow(win)

if __name__ == "__main__":
    main()

