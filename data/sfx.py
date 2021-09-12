import os
from pygame.mixer import Sound

__sfxFolder = os.path.join("resources", "sfx")

HIT = Sound(os.path.join(__sfxFolder, "hit.wav"))