import pygame
import datetime

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
line = (200, 230, 255)
bg = (40, 40, 40)
width = 600
height = 700
ubuntu_font = 'font/Ubuntu-Regular.ttf'
opensans_font = 'font/OpenSans-SemiBold.ttf'
node = 'font/NotoSansCJK-Medium.ttc'

window = pygame.display.set_mode((width, height))

class button():
    def __init__(self, color, text_color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(opensans_font, 25)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                            self.y + 3 + ((self.height // 2 - text.get_height() // 2)-5)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


clock_button = button(bg, (200, 200, 200), 5, 0, 70, 30, ' Clock ')
alarm_button = button(bg, (200, 200, 200), 93, 0, 70, 30, ' Alarm ')
stopwatch_button = button(bg, (200, 200, 200), 188, 0, 130, 30, ' Stop Watch ')
timer_button = button(bg, (200, 200, 200), 335, 0, 70, 30, ' Timer ')

def stopwatch_window():
    pygame.display.set_caption('Stop Watch')
    run = True
    while run:
        pygame.time.delay(10)
        window.fill(bg)
        stopwatch_button.text_color = (151, 147, 245)
        time = datetime.datetime.now()
        sys_hrs, sys_min, ampm = time.hour if time.hour <= 12 else time.hour - 12, time.minute, 'AM' if time.hour < 12 else 'PM'

        clock_button.draw(window, bg)
        alarm_button.draw(window, bg)
        stopwatch_button.draw(window, bg)
        timer_button.draw(window, bg)

        # alarm1.comparison(sys_hrs, sys_min, ampm)
        # alarm2.comparison(sys_hrs, sys_min, ampm)
        # alarm3.comparison(sys_hrs, sys_min, ampm)
        # alarm4.comparison(sys_hrs, sys_min, ampm)
        # alarm5.comparison(sys_hrs, sys_min, ampm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # if clock_button.isOver(pos):
                #     clock_window()
                # if alarm_button.isOver(pos):
                #     alarm_window()
                # if timer_button.isOver(pos):
                #     timer_window()

            if event.type == pygame.MOUSEMOTION:
                if clock_button.isOver(pos):
                    clock_button.text_color = (151, 147, 245)
                else:
                    clock_button.text_color = (200, 200, 200)

                if alarm_button.isOver(pos):
                    alarm_button.text_color = (151, 147, 245)
                else:
                    alarm_button.text_color = (200, 200, 200)

                if timer_button.isOver(pos):
                    timer_button.text_color = (151, 147, 245)
                else:
                    timer_button.text_color = (200, 200, 200)

        pygame.display.update()

stopwatch_window()