import pygame
import minecraft_launcher_lib
import subprocess
import time

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'minecraft_launcher')

versions = []

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1920, 1200))
pygame.display.set_caption('Minecraft Launcher')
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/bg.png').convert_alpha()

big_font = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 150)
play_label = big_font.render('PLAY', False, 'Brown')
play_label_rect = play_label.get_rect(topleft=(780, 870))

smile_font = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 50)
enter_username_label = smile_font.render('Enter username', False, (19, 255, 239))
enter_version_label = smile_font.render('Enter version', False, (19, 255, 239))
installing_version_label = smile_font.render('Installing...', False, 'Yellow')
starting_label = smile_font.render('Starting...', False, 'Yellow')

is_typing = False
enter_username = False
enter_version = False
username_text = ''
version_text = ''

while True:

    screen.blit(bg, (0, 0))
    screen.blit(play_label, (780, 870))

    field_username = pygame.draw.rect(screen, 'Black', (670, 650, 600, 80), border_radius=10)
    field_version = pygame.draw.rect(screen, 'Black', (670, 780, 600, 80), border_radius=10)

    mouse = pygame.mouse.get_pos()

    if play_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        pygame.draw.rect(screen, 'Blue', (670, 900, 600, 110), border_radius=10)
        screen.blit(installing_version_label, (690, 930))
        pygame.display.update()

        try:
            minecraft_launcher_lib.install.install_minecraft_version(versionid=version_text, minecraft_directory=minecraft_directory)

            pygame.draw.rect(screen, 'Blue', (670, 900, 600, 110), border_radius=10)
            screen.blit(starting_label, (690, 930))

            time.sleep(1)

            pygame.quit()

            options = {
                'username': username_text if username_text else 'Player',
                'uuid': '',
                'token': ''
            }

            subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=version_text, minecraft_directory=minecraft_directory, options=options))
            break
        except Exception as ex:
            pygame.draw.rect(screen, 'Blue', (670, 900, 600, 110), border_radius=10)
            screen.blit(smile_font.render(f'Error: {ex}', False, 'Red'), (690, 930))
            pygame.display.update()
            time.sleep(3)
    if is_typing:
        if pygame.mouse.get_pressed()[0]:
            if not field_username.collidepoint(mouse) and not field_version.collidepoint(mouse):
                is_typing = False
                enter_username = False
                enter_version = False

        if enter_username:
            screen.blit(smile_font.render(username_text, False, 'White'), (690, 660))

            if field_version.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                enter_username = False
                enter_version = True

            pygame.draw.rect(screen, 'Orange', (670, 650, 600, 80), border_radius=10, width=10)

            if len(version_text) > 0:
                screen.blit(smile_font.render(version_text, False, 'White'), (690, 790))
            else:
                screen.blit(enter_version_label, (690, 790))
        elif enter_version:
            screen.blit(smile_font.render(version_text, False, 'White'), (690, 790))

            if field_username.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                enter_version = False
                enter_username = True

            pygame.draw.rect(screen, 'Orange', (670, 780, 600, 80), border_radius=10, width=10)

            if len(username_text) > 0:
                screen.blit(smile_font.render(username_text, False, 'White'), (690, 660))
            else:
                screen.blit(enter_username_label, (690, 660))
    else:
        if pygame.mouse.get_pressed()[0]:
            if field_username.collidepoint(mouse) or enter_username_label.get_rect().collidepoint(mouse):
                is_typing = True
                enter_username = True
            elif field_version.collidepoint(mouse) or enter_version_label.get_rect().collidepoint(mouse):
                is_typing = True
                enter_version = True

        if len(username_text) > 0:
            screen.blit(smile_font.render(username_text, False, 'White'), (690, 660))
        else:
            screen.blit(enter_username_label, (690, 660))

        if len(version_text) > 0:
            screen.blit(smile_font.render(version_text, False, 'White'), (690, 790))
        else:
            screen.blit(enter_version_label, (690, 790))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if is_typing:
            if event.type == pygame.KEYDOWN:
                if enter_username:
                    if event.key != pygame.K_BACKSPACE:
                        username_text += event.unicode

                    else:
                        username_text = username_text[: -1]
                elif enter_version:
                    if event.key != pygame.K_BACKSPACE:
                        version_text += event.unicode
                    else:
                        version_text = version_text[: -1]

                if event.key == pygame.K_RETURN:
                    if enter_username:
                        enter_version = True
                        enter_username = False
                    else:
                        is_typing = False
                        enter_version = False

    clock.tick(15)