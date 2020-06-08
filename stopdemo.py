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


class button:
    def __init__(self, color, text_color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.font_size = 25

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(opensans_font, self.font_size)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2),
                            self.y + 3 + ((self.height // 2 - text.get_height() // 2) - 5)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


capture_button = button((200, 200, 200), (0, 0, 0), 30, 635, 150, 55, 'Capture ')
capture_button.font_size = 35

reset_button = button((200, 200, 200), (0, 0, 0), 230, 635, 150, 55, ' Reset ')
reset_button.font_size = 35

start_button = button((200, 200, 200), (0, 0, 0), 430, 635, 150, 55, ' Start ')
start_button.font_size = 35

state_button = button(bg, (200, 200, 200), 335, 0, 70, 30, ' ')


class stopwatch:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.font0 = pygame.font.Font(ubuntu_font, 75)
        self.font1 = pygame.font.Font(ubuntu_font, 85)

        self.hrs_text = self.font0.render('', True, line, bg)
        self.hrs_textRect = self.hrs_text.get_rect()

        self.min_text = self.font0.render('', True, line, bg)
        self.min_textRect = self.min_text.get_rect()

        self.sec_text = self.font0.render('', True, line, bg)
        self.sec_textRect = self.sec_text.get_rect()

        self.milli_text = self.font0.render('', True, line, bg)
        self.milli_textRect = self.milli_text.get_rect()

        self.colan_text = self.font1.render(':', True, line, bg)
        self.colan_textRect = self.colan_text.get_rect()
        self.colan_textRect.center = 105 + self.x + self.colan_text.get_width() // 2, self.y - 15 + self.colan_text.get_height() // 2

        self.colan_dot = self.font1.render('.', True, line, bg)
        self.colan_dotRect = self.colan_dot.get_rect()
        self.colan_dotRect.center = 255 + self.x + self.colan_dot.get_width() // 2, self.y - 15 + self.colan_dot.get_height() // 2


stopwatch_obj = stopwatch(100, 50)


class capture:
    def __init__(self, sn, x, y, hrs, min, sec, milli):
        self.sn, self.x, self.y, self.hrs, self.min, self.sec, self.milli = sn, x, y, hrs, min, sec, milli

        self.font0 = pygame.font.Font(ubuntu_font, 40)
        self.font1 = pygame.font.Font(ubuntu_font, 50)
        self.font3 = pygame.font.Font(opensans_font, 30)

        self.sn_text = self.font3.render("%02d)" % self.sn, True, line, bg)
        self.hrs_text = self.font0.render("%02d" % self.hrs, True, line, bg)
        self.min_text = self.font0.render("%02d" % self.min, True, line, bg)
        self.sec_text = self.font0.render("%02d" % self.sec, True, line, bg)
        self.milli_text = self.font0.render("%02d" % self.milli, True, line, bg)
        self.colan1 = self.font1.render(":", True, line, bg)
        self.colan2 = self.font1.render(":", True, line, bg)
        self.dot = self.font1.render(".", True, line, bg)

        self.sn_textRct = self.sn_text.get_rect()
        self.hrs_textRect = self.hrs_text.get_rect()
        self.min_textRect = self.min_text.get_rect()
        self.sec_textRect = self.sec_text.get_rect()
        self.milli_textRect = self.milli_text.get_rect()
        self.colan1Rect = self.colan1.get_rect()
        self.colan2Rect = self.colan2.get_rect()
        self.dotRct = self.dot.get_rect()

        self.sn_textRct.center = self.x - 80, self.y
        self.hrs_textRect.center = self.x, self.y
        self.colan1Rect.center = self.x + 40, self.y - 5
        self.min_textRect.center = self.x + 80, self.y
        self.colan2Rect.center = self.x + 120, self.y - 5
        self.sec_textRect.center = self.x + 160, self.y
        self.dotRct.center = self.x + 200, self.y - 5
        self.milli_textRect.center = self.x + 240, self.y

    def build(self):
        window.blit(self.sn_text, self.sn_textRct)
        window.blit(self.hrs_text, self.hrs_textRect)
        window.blit(self.colan1, self.colan1Rect)
        window.blit(self.min_text, self.min_textRect)
        window.blit(self.colan2, self.colan2Rect)
        window.blit(self.sec_text, self.sec_textRect)
        window.blit(self.dot, self.dotRct)
        window.blit(self.milli_text, self.milli_textRect)

    def recenter(self, y):
        self.sn_textRct.center = self.x - 80, y
        self.hrs_textRect.center = self.x, y
        self.colan1Rect.center = self.x + 40, y - 5
        self.min_textRect.center = self.x + 80, y
        self.colan2Rect.center = self.x + 120, y - 5
        self.sec_textRect.center = self.x + 160, y
        self.dotRct.center = self.x + 200, y - 5
        self.milli_textRect.center = self.x + 240, y


cap1 = capture(1,   200, 0, 0, 0, 0, 0)
cap2 = capture(2,   200, 0, 0, 0, 0, 0)
cap3 = capture(3,   200, 0, 0, 0, 0, 0)
cap4 = capture(4,   200, 0, 0, 0, 0, 0)
cap5 = capture(5,   200, 0, 0, 0, 0, 0)
cap6 = capture(6,   200, 0, 0, 0, 0, 0)
cap7 = capture(7,   200, 0, 0, 0, 0, 0)
cap8 = capture(8,   200, 0, 0, 0, 0, 0)
cap9 = capture(9,   200, 0, 0, 0, 0, 0)
cap10 = capture(10, 200, 0, 0, 0, 0, 0)
cap11 = capture(11, 200, 0, 0, 0, 0, 0)
cap12 = capture(12, 200, 0, 0, 0, 0, 0)
cap13 = capture(13, 200, 0, 0, 0, 0, 0)
cap14 = capture(14, 200, 0, 0, 0, 0, 0)
cap15 = capture(15, 200, 0, 0, 0, 0, 0)
cap16 = capture(16, 200, 0, 0, 0, 0, 0)
cap17 = capture(17, 200, 0, 0, 0, 0, 0)
cap18 = capture(18, 200, 0, 0, 0, 0, 0)
cap19 = capture(19, 200, 0, 0, 0, 0, 0)
cap20 = capture(20, 200, 0, 0, 0, 0, 0)
cap21 = capture(21, 200, 0, 0, 0, 0, 0)
cap22 = capture(22, 200, 0, 0, 0, 0, 0)
cap23 = capture(23, 200, 0, 0, 0, 0, 0)
cap24 = capture(24, 200, 0, 0, 0, 0, 0)
cap25 = capture(25, 200, 0, 0, 0, 0, 0)
cap26 = capture(26, 200, 0, 0, 0, 0, 0)
cap27 = capture(27, 200, 0, 0, 0, 0, 0)
cap28 = capture(28, 200, 0, 0, 0, 0, 0)
cap29 = capture(29, 200, 0, 0, 0, 0, 0)
cap30 = capture(30, 200, 0, 0, 0, 0, 0)

up = pygame.image.load('images/arrup.png')
up.set_colorkey(white)
down = pygame.image.load('images/arrdw.png')
down.set_colorkey(white)
up_x = 250
up_y = 140
down_x = 250
down_y = 550


def isOverStopwatch(pos):
    if up_x < pos[0] < up_x + up.get_width():
        if up_y < pos[1] < up_y + up.get_height():
            return "add"

    if down_x < pos[0] < down_x + down.get_width():
        if down_y < pos[1] < down_y + down.get_height():
            return 'sub'


def stopwatch_window():
    pygame.display.set_caption('Stop Watch')
    run = True
    duration, millis, sec, min, hrs = 0, 0, 0, 0, 0
    stopwatch_run = False
    active_status = False
    state = False
    counter = 0
    ch = [cap1, cap2, cap3, cap4, cap5, cap6, cap7, cap8, cap9, cap10, cap11, cap12, cap13, cap14, cap15, cap16, cap17,
          cap18, cap19, cap20, cap21, cap22, cap23, cap24, cap25, cap26, cap27, cap28, cap29, cap30]
    position = [220, 270, 320, 370, 420, 470, 520]
    spl_lap = True
    while run:
        duration += 100
        time.sleep(0.01)
        pos_counter = 0
        window.fill(bg)
        if stopwatch_run:
            millis = duration % 100
            sec += 1 if duration % 100 == 0 else 0
            sec %= 60
            min += 1 if duration % 6000 == 0 else 0
            if min == 60:
                state = True
            min %= 60
            hrs += 1 if duration % 360000 == 0 else 0
            start_button.text = ' Pause '
        elif not active_status:
            start_button.text = ' Start '
        else:
            start_button.text = ' Resume '

        if not state:
            minx = stopwatch_obj.x - 8
            secx = stopwatch_obj.x + 142
            millix = stopwatch_obj.x + 292
            stopwatch_obj.min_textRect.center = minx, stopwatch_obj.y + stopwatch_obj.min_text.get_height() // 2
            stopwatch_obj.sec_textRect.center = secx, stopwatch_obj.y + stopwatch_obj.sec_text.get_height() // 2
            stopwatch_obj.milli_textRect.center = millix, stopwatch_obj.y + stopwatch_obj.milli_text.get_height() // 2

            stopwatch_obj.min_text = stopwatch_obj.font0.render('%02d' % min, True, line, bg)
            window.blit(stopwatch_obj.min_text, stopwatch_obj.min_textRect)

            stopwatch_obj.sec_text = stopwatch_obj.font0.render('%02d' % sec, True, line, bg)
            window.blit(stopwatch_obj.sec_text, stopwatch_obj.sec_textRect)

            stopwatch_obj.milli_text = stopwatch_obj.font0.render('%02d' % millis, True, line, bg)
            window.blit(stopwatch_obj.milli_text, stopwatch_obj.milli_textRect)

            stopwatch_obj.colan_dot = stopwatch_obj.font1.render('.', True, line, bg)
        else:
            hrsx = stopwatch_obj.x - 8
            minx = stopwatch_obj.x + 142
            secx = stopwatch_obj.x + 292
            stopwatch_obj.hrs_textRect.center = hrsx, stopwatch_obj.y + stopwatch_obj.hrs_text.get_height() // 2
            stopwatch_obj.min_textRect.center = minx, stopwatch_obj.y + stopwatch_obj.min_text.get_height() // 2
            stopwatch_obj.sec_textRect.center = secx, stopwatch_obj.y + stopwatch_obj.sec_text.get_height() // 2

            stopwatch_obj.hrs_text = stopwatch_obj.font0.render('%02d' % hrs, True, line, bg)
            window.blit(stopwatch_obj.hrs_text, stopwatch_obj.hrs_textRect)

            stopwatch_obj.min_text = stopwatch_obj.font0.render('%02d' % min, True, line, bg)
            window.blit(stopwatch_obj.min_text, stopwatch_obj.min_textRect)

            stopwatch_obj.sec_text = stopwatch_obj.font0.render('%02d' % sec, True, line, bg)
            window.blit(stopwatch_obj.sec_text, stopwatch_obj.sec_textRect)

            stopwatch_obj.colan_dot = stopwatch_obj.font1.render(':', True, line, bg)

        for i in range(counter, counter + 7):
            ch[i].recenter(position[pos_counter])
            ch[i].build()
            pos_counter += 1

        if spl_lap:
            state_button.text = ' SPLIT '
        else:
            state_button.text = ' LAP '

        window.blit(stopwatch_obj.colan_text, stopwatch_obj.colan_textRect)

        window.blit(stopwatch_obj.colan_dot, stopwatch_obj.colan_dotRect)

        start_button.draw(window, bg)
        reset_button.draw(window, bg)
        capture_button.draw(window, bg)
        state_button.draw(window, bg)
        window.blit(up, (up_x, up_y))
        window.blit(down, (down_x, down_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(pos):
                    stopwatch_run = not stopwatch_run
                    active_status = True

                if reset_button.isOver(pos):
                    duration, sec, min, millis, hrs = 0, 0, 0, 0, 0
                    stopwatch_run = False
                    active_status = False
                    state = False

                if capture_button.isOver(pos):
                    print("%02d:%02d:%02d.%02d" % (hrs, min, sec, millis))

                if state_button.isOver(pos):
                    spl_lap = not spl_lap

                if isOverStopwatch(pos) == 'add' and counter > 0:
                    counter -= 1
                if isOverStopwatch(pos) == 'sub' and counter < 23:
                    counter += 1

            if event.type == pygame.MOUSEMOTION:
                if start_button.isOver(pos):
                    start_button.color = (151, 147, 245)
                else:
                    start_button.color = (200, 200, 200)

                if reset_button.isOver(pos):
                    reset_button.color = (151, 147, 245)
                else:
                    reset_button.color = (200, 200, 200)

                if capture_button.isOver(pos):
                    capture_button.color = (151, 147, 245)
                else:
                    capture_button.color = (200, 200, 200)

                if state_button.isOver(pos):
                    state_button.text_color = (151, 147, 245)
                else:
                    state_button.text_color = (200, 200, 200)

        pygame.display.update()


stopwatch_window()
