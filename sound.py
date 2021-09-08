import pygame.mixer

pygame.mixer.init()

def play(sound: pygame.mixer.Sound):
    sound.play()