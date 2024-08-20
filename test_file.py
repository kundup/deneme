import pygame
import time



a = time.time()
print(a)
while True:
    b = time.time()
    if b-a > 5:
        print(b)
        break