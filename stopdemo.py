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

state_button = button(bg, (200, 200, 200), 50, 595, 110, 35, ' ')
state_button.font_size = 30



class stopwatch:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.font0 = pygame.font.Font(ubuntu_font, 95)
        self.font1 = pygame.font.Font(ubuntu_font, 105)

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
        self.colan_textRect.center = 100 + self.x + self.colan_text.get_width() // 2, self.y - 15 + self.colan_text.get_height() // 2

        self.colan_dot = self.font1.render('.', True, line, bg)
        self.colan_dotRect = self.colan_dot.get_rect()
        self.colan_dotRect.center = 255 + self.x + self.colan_dot.get_width() // 2, self.y - 15 + self.colan_dot.get_height() // 2


stopwatch_obj = stopwatch(100, 60)


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


cap1 = capture(1,   210, 0, 0, 0, 0, 0)
cap2 = capture(2,   210, 0, 0, 0, 0, 0)
cap3 = capture(3,   210, 0, 0, 0, 0, 0)
cap4 = capture(4,   210, 0, 0, 0, 0, 0)
cap5 = capture(5,   210, 0, 0, 0, 0, 0)
cap6 = capture(6,   210, 0, 0, 0, 0, 0)
cap7 = capture(7,   210, 0, 0, 0, 0, 0)
cap8 = capture(8,   210, 0, 0, 0, 0, 0)
cap9 = capture(9,   210, 0, 0, 0, 0, 0)
cap10 = capture(10, 210, 0, 0, 0, 0, 0)
cap11 = capture(11, 210, 0, 0, 0, 0, 0)
cap12 = capture(12, 210, 0, 0, 0, 0, 0)
cap13 = capture(13, 210, 0, 0, 0, 0, 0)
cap14 = capture(14, 210, 0, 0, 0, 0, 0)
cap15 = capture(15, 210, 0, 0, 0, 0, 0)
cap16 = capture(16, 210, 0, 0, 0, 0, 0)
cap17 = capture(17, 210, 0, 0, 0, 0, 0)
cap18 = capture(18, 210, 0, 0, 0, 0, 0)
cap19 = capture(19, 210, 0, 0, 0, 0, 0)
cap20 = capture(20, 210, 0, 0, 0, 0, 0)
cap21 = capture(21, 210, 0, 0, 0, 0, 0)
cap22 = capture(22, 210, 0, 0, 0, 0, 0)
cap23 = capture(23, 210, 0, 0, 0, 0, 0)
cap24 = capture(24, 210, 0, 0, 0, 0, 0)
cap25 = capture(25, 210, 0, 0, 0, 0, 0)
cap26 = capture(26, 210, 0, 0, 0, 0, 0)
cap27 = capture(27, 210, 0, 0, 0, 0, 0)
cap28 = capture(28, 210, 0, 0, 0, 0, 0)
cap29 = capture(29, 210, 0, 0, 0, 0, 0)
cap30 = capture(30, 210, 0, 0, 0, 0, 0)

up = pygame.image.load('images/arrup.png')
up.set_colorkey(white)
up_cord = (270, 170)
down = pygame.image.load('images/arrdw.png')
down.set_colorkey(white)
down_cord = (270, 570)


def isOverStopwatch(pos):
    if up_cord[0] < pos[0] < up_cord[0] + up.get_width():
        if up_cord[1] < pos[1] < up_cord[1] + up.get_height():
            return "up"

    if down_cord[0] < pos[0] < down_cord[0] + down.get_width():
        if down_cord[1] < pos[1] < down_cord[1] + down.get_height():
            return 'down'


s_run = True
s_duration, s_milli, s_sec, s_min, s_hrs = 0, 0, 0, 0, 0
s_stopwatch_run = False
s_active_status = False
s_state = False
s_counter = 0
s_caplsit = [cap1, cap2, cap3, cap4, cap5, cap6, cap7, cap8, cap9, cap10, cap11, cap12, cap13, cap14, cap15, cap16,
             cap17, cap18, cap19, cap20, cap21, cap22, cap23, cap24, cap25, cap26, cap27, cap28, cap29, cap30]
s_position = [240, 290, 340, 390, 440, 490, 540]
s_spl_lap = True
s_cap_count = 0


def stopwatch_window():
    pygame.display.set_caption('Stop Watch')
    global s_hrs, s_min, s_milli, s_sec, s_duration, s_stopwatch_run, s_active_status, s_state, s_spl_lap, s_counter

    def capture():
        global s_cap_count, s_hrs, s_min, s_milli, s_sec, s_duration, s_counter
        if s_stopwatch_run and s_cap_count < 30:
            s_caplsit[s_cap_count].sn_text = s_caplsit[s_cap_count].font3.render("%02d)" % s_caplsit[s_cap_count].sn,
                                                                                 True, line, bg)
            s_caplsit[s_cap_count].hrs_text = s_caplsit[s_cap_count].font0.render("%02d" % s_hrs, True, line, bg)
            s_caplsit[s_cap_count].min_text = s_caplsit[s_cap_count].font0.render("%02d" % s_min, True, line, bg)
            s_caplsit[s_cap_count].sec_text = s_caplsit[s_cap_count].font0.render("%02d" % s_sec, True, line, bg)
            s_caplsit[s_cap_count].milli_text = s_caplsit[s_cap_count].font0.render("%02d" % s_milli, True, line, bg)
            s_cap_count += 1
            if s_cap_count > 7:
                s_counter = s_cap_count-7
            else:
                s_counter = 0
            if not s_spl_lap:
                s_duration, s_sec, s_min, s_milli, s_hrs = 0, 0, 0, 0, 0


    def s_reset():
        global s_hrs, s_min, s_milli, s_sec, s_duration, s_stopwatch_run, s_active_status, s_state, s_cap_count, s_counter
        s_duration, s_sec, s_min, s_milli, s_hrs = 0, 0, 0, 0, 0
        s_stopwatch_run = False
        s_active_status = False
        s_state = False
        s_cap_count = 0
        s_counter = 0
        for i in s_caplsit:
            i.sn_text = i.font3.render("%02d)" % i.sn, True, line, bg)
            i.hrs_text = i.font0.render("%02d" % s_hrs, True, line, bg)
            i.min_text = i.font0.render("%02d" % s_min, True, line, bg)
            i.sec_text = i.font0.render("%02d" % s_sec, True, line, bg)
            i.milli_text = i.font0.render("%02d" % s_milli, True, line, bg)

    while s_run:
        global s_cap_count
        s_duration += 1
        time.sleep(0.01)
        pos_counter = 0
        window.fill(bg)
        if s_stopwatch_run:
            s_milli = s_duration % 100
            s_sec += 1 if s_duration % 100 == 0 else 0
            s_sec %= 60
            s_min += 1 if s_duration % 6000 == 0 else 0
            if s_min == 60:
                s_state = True
            s_min %= 60
            s_hrs += 1 if s_duration % 360000 == 0 else 0
            start_button.text = ' Pause '
        elif not s_active_status:
            start_button.text = ' Start '
        else:
            start_button.text = ' Resume '

        if not s_state:
            minx = stopwatch_obj.x - 20
            secx = stopwatch_obj.x + 140
            millix = stopwatch_obj.x + 290
            stopwatch_obj.min_textRect.center = minx, stopwatch_obj.y + stopwatch_obj.min_text.get_height() // 2
            stopwatch_obj.sec_textRect.center = secx, stopwatch_obj.y + stopwatch_obj.sec_text.get_height() // 2
            stopwatch_obj.milli_textRect.center = millix, stopwatch_obj.y + stopwatch_obj.milli_text.get_height() // 2

            stopwatch_obj.min_text = stopwatch_obj.font0.render('%02d' % s_min, True, line, bg)
            window.blit(stopwatch_obj.min_text, stopwatch_obj.min_textRect)

            stopwatch_obj.sec_text = stopwatch_obj.font0.render('%02d' % s_sec, True, line, bg)
            window.blit(stopwatch_obj.sec_text, stopwatch_obj.sec_textRect)

            stopwatch_obj.milli_text = stopwatch_obj.font0.render('%02d' % s_milli, True, line, bg)
            window.blit(stopwatch_obj.milli_text, stopwatch_obj.milli_textRect)

            stopwatch_obj.colan_dot = stopwatch_obj.font1.render('.', True, line, bg)
        else:
            hrsx = stopwatch_obj.x - 20
            minx = stopwatch_obj.x + 140
            secx = stopwatch_obj.x + 290
            stopwatch_obj.hrs_textRect.center = hrsx, stopwatch_obj.y + stopwatch_obj.hrs_text.get_height() // 2
            stopwatch_obj.min_textRect.center = minx, stopwatch_obj.y + stopwatch_obj.min_text.get_height() // 2
            stopwatch_obj.sec_textRect.center = secx, stopwatch_obj.y + stopwatch_obj.sec_text.get_height() // 2

            stopwatch_obj.hrs_text = stopwatch_obj.font0.render('%02d' % s_hrs, True, line, bg)
            window.blit(stopwatch_obj.hrs_text, stopwatch_obj.hrs_textRect)

            stopwatch_obj.min_text = stopwatch_obj.font0.render('%02d' % s_min, True, line, bg)
            window.blit(stopwatch_obj.min_text, stopwatch_obj.min_textRect)

            stopwatch_obj.sec_text = stopwatch_obj.font0.render('%02d' % s_sec, True, line, bg)
            window.blit(stopwatch_obj.sec_text, stopwatch_obj.sec_textRect)

            stopwatch_obj.colan_dot = stopwatch_obj.font1.render(':', True, line, bg)

        if s_cap_count > 7:
            window.blit(up, up_cord)
            window.blit(down, down_cord)
            for i in range(s_counter, s_counter + 7):
                s_caplsit[i].recenter(s_position[pos_counter])
                s_caplsit[i].build()
                pos_counter += 1
        else:
            for i in range(s_cap_count):
                s_caplsit[i].recenter(s_position[i])
                s_caplsit[i].build()

        if s_spl_lap:
            state_button.text = ' SPLIT '
        else:
            state_button.text = ' LAP '

        window.blit(stopwatch_obj.colan_text, stopwatch_obj.colan_textRect)

        window.blit(stopwatch_obj.colan_dot, stopwatch_obj.colan_dotRect)

        start_button.draw(window, bg)
        reset_button.draw(window, bg)
        capture_button.draw(window, bg)
        state_button.draw(window, bg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(pos):
                    s_stopwatch_run = not s_stopwatch_run
                    s_active_status = True

                if reset_button.isOver(pos):
                    s_reset()

                if capture_button.isOver(pos):
                    capture()

                if state_button.isOver(pos) and not s_active_status:
                    s_spl_lap = not s_spl_lap

                if s_cap_count > 7:
                    if isOverStopwatch(pos) == 'up' and s_counter > 0:
                        s_counter -= 1
                    if isOverStopwatch(pos) == 'down' and s_counter < 23:
                        s_counter += 1

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
