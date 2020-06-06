import pygame
import datetime
import time

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

class stopwatch:
    def __init__(self, x, y):
        self.font0 = pygame.font.Font(ubuntu_font, 75)
        self.font1 = pygame.font.Font(ubuntu_font, 85)

        self.hrs_text = self.font0.render('', True, line, bg)
        self.hrs_textRect = self.hrs_text.get_rect()
        self.hrs_textRect.center = x + self.hrs_text.get_width() // 2, y + self.hrs_text.get_height() // 2

        self.min_text = self.font0.render('', True, line, bg)
        self.min_textRect = self.min_text.get_rect()
        self.min_textRect.center = 150 + x + self.min_text.get_width() // 2, y + self.min_text.get_height() // 2

        self.sec_text = self.font0.render('', True, line, bg)
        self.sec_textRect = self.sec_text.get_rect()
        self.sec_textRect.center = 300 + x + self.sec_text.get_width(), y + self.sec_text.get_height() // 2

        self.colan_text = self.font1.render(':', True, line, bg)
        self.colan_textRect = self.colan_text.get_rect()
        self.colan_textRect.center = 105 + x + self.colan_text.get_width() // 2, y - 15 + self.colan_text.get_height() // 2

        self.colan_dot = self.font1.render('.', True, line, bg)
        self.colan_dotRect = self.colan_dot.get_rect()
        self.colan_dotRect.center = 255 + x + self.colan_dot.get_width() // 2, y - 15 + self.colan_dot.get_height() // 2

stopwatch_obj = stopwatch(100, 50)

def stopwatch_window():
    pygame.display.set_caption('Stop Watch')
    run = True
    duration = 0
    sec = 0
    min = 0
    while run:
        duration += 1
        time.sleep(0.01)
        window.fill(bg)
        stopwatch_button.text_color = (151, 147, 245)
        sys_time = datetime.datetime.now()
        sys_hrs, sys_min, ampm = sys_time.hour if sys_time.hour <= 12 else sys_time.hour - 12, sys_time.minute, 'AM' if sys_time.hour < 12 else 'PM'

        clock_button.draw(window, bg)
        alarm_button.draw(window, bg)
        stopwatch_button.draw(window, bg)
        timer_button.draw(window, bg)

        # alarm1.comparison(sys_hrs, sys_min, ampm)
        # alarm2.comparison(sys_hrs, sys_min, ampm)
        # alarm3.comparison(sys_hrs, sys_min, ampm)
        # alarm4.comparison(sys_hrs, sys_min, ampm)
        # alarm5.comparison(sys_hrs, sys_min, ampm)

        millis = duration % 100
        sec += 1 if duration % 100 == 0 else 0
        sec %= 60
        min += 1 if duration % 6000 == 0 else 0

        stopwatch_obj.hrs_text = stopwatch_obj.font0.render('%02d' % min, True, line, bg)
        window.blit(stopwatch_obj.hrs_text, stopwatch_obj.hrs_textRect)

        stopwatch_obj.min_text = stopwatch_obj.font0.render('%02d' % sec, True, line, bg)
        window.blit(stopwatch_obj.min_text, stopwatch_obj.min_textRect)

        stopwatch_obj.sec_text = stopwatch_obj.font0.render('%02d' % millis, True, line, bg)
        window.blit(stopwatch_obj.sec_text, stopwatch_obj.sec_textRect)

        window.blit(stopwatch_obj.colan_text, stopwatch_obj.colan_textRect)

        window.blit(stopwatch_obj.colan_dot, stopwatch_obj.colan_dotRect)

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