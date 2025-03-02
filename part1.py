import pygame
pygame.init()
import time


window_size = (800, 600) #Задаем окно
screen = pygame.display.set_mode(window_size) #Создаем окно

pygame.display.set_caption("Part 1") #Название окна

image = pygame.image.load("123123.png") #Загружаем картинку
image_rect = image.get_rect() #Получаем прямоугольник картинки

image2 = pygame.image.load("123321.png") #Загружаем картинку
image_rect2 = image.get_rect() #Получаем прямоугольник картинки

speed = 5

run = True #Переменная для цикла

while run: #Цикл игры
    for event in pygame.event.get(): #Обработка событий
        if event.type == pygame.QUIT: #Выход из игры
            run = False #Завершение цикла
        if event.type == pygame.MOUSEMOTION: #Если нажата кнопка мыши
                mouseX, mouseY = pygame.mouse.get_pos() #Получаем координаты мыши
                image_rect.x = mouseX - 40  #Перемещаем картинку в координаты мыши
                image_rect.y = mouseY - 40


    if image_rect.colliderect(image_rect2):
        print("Произошло столкновение")
        time.sleep(1)

    # keys = pygame.key.get_pressed() #Получаем нажатые клавиши
    # if keys[pygame.K_LEFT]: #Если нажата клавиша влево
    #     image_rect.x -= speed #Перемещаем картинку влево
    # if keys[pygame.K_RIGHT]: #Если нажата клавиша вправо
    #     image_rect.x += speed #Перемещаем картинку вправо
    # if keys[pygame.K_UP]: #Если нажата клавиша вверх
    #     image_rect.y -= speed #Перемещаем картинку вверх
    # if keys[pygame.K_DOWN]: #Если нажата клавиша вниз
    #     image_rect.y += speed #Перемещаем картинку вниз


    screen.fill((12, 85, 155)) #Цвет фона
    screen.blit(image, image_rect) #Рисуем картинку
    screen.blit(image2, image_rect2) #Рисуем картинку
    pygame.display.flip() #Обновление экрана

pygame.quit() #Выход Основной базовый код готов.


