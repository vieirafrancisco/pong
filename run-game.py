from pong.game.game import PongGame

if __name__ == '__main__':
    g = PongGame()
    while True:
        g.new()
        g.menu_screen()
        g.execute()