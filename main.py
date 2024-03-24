from game import Game


if __name__ == '__main__':
    instance = Game()
    
    while True:
        _, gameover, score = instance.play_step()
        
        if gameover:
            break

    