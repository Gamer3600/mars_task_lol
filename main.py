import os
import sys
from consts import *
import pygame
import requests
from tkinter import *
from tkinter import ttk


def get_txt(mod, address):
    if mod in all_map_mods:
        current_mode = mod
        address_lox = address


def settings():
    window = Tk()
    window.title("Новое окно")
    window.geometry('400x250')
    lbl = Label(window, text="Формат карты")
    lbl.grid(column=0, row=0)
    lbl2 = Label(window, text="Шо ищем?")
    lbl2.grid(column=0, row=1)
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)
    txt2 = Entry(window, width=20)
    txt2.grid(column=1, row=1)
    button = Button(window, command=lambda: get_txt(txt.get(), txt2.get()), text='Жмяк')
    button.grid(column=0, row=2)
    window.mainloop()


settings()
geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={address_lox}&format=json"
response = requests.get(geocoder_request)
if response:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    toponym_coodrinates = toponym["Point"]["pos"]
    print(toponym_coodrinates)
    print(toponym_address, "имеет координаты:", toponym_coodrinates)
else:
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
coords_in_map = ','.join(f'{toponym_coodrinates}')

map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_in_map}&spn={scale}&l=mod"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = f"map{count}.png"
current_map_file = map_file
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((w, h))
screen.blit(pygame.image.load(map_file), (0, 0))
running = True
list_to_delete.append(map_file)
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_UP] and (int_scale[0] >= 0 and int_scale[1] >= 0):
        int_scale[0] -= 0.001
        int_scale[1] -= 0.001
        scale = f'{int_scale[0]},{int_scale[1]}'
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_in_map}&spn={scale}&l=map"
        response = requests.get(map_request)
        map_file = f"map{count}.png"
        list_to_delete.append(map_file)
        with open(map_file, "wb") as file:
            file.write(response.content)
        current_map_file = map_file
        screen.blit(pygame.image.load(current_map_file), (0, 0))
    if keys[pygame.K_DOWN] and (int_scale[0] <= 0.1 and int_scale[1] <= 0.1):
        int_scale[0] += 0.001
        int_scale[1] += 0.001
        scale = f'{int_scale[0]},{int_scale[1]}'
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords_in_map}&spn={scale}&l=map"
        response = requests.get(map_request)
        map_file = f"map{count}.png"
        list_to_delete.append(map_file)
        with open(map_file, "wb") as file:
            file.write(response.content)
        current_map_file = map_file
        screen.blit(pygame.image.load(current_map_file), (0, 0))
    if keys[pygame.K_w]:
        pass
    if keys[pygame.K_a]:
        pass
    if keys[pygame.K_s]:
        pass
    if keys[pygame.K_d]:
        pass
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
for i in list_to_delete:
    os.remove(i)
