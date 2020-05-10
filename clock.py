import pygame
import datetime
import tkinter as tk
import math

pygame.init()

world_time = {
    "GMT": ["Greenwich MT       +00:00", +0],
    "ECT": ["European CT         +01:00", +1.0],
    "EET": ["East Eur Time       +02:00", +2.0],
    "ART": ["Arabic ST              +02:00", +2.0],
    "EAT": ["East African ST    +03:00", +3.0],
    "MET": ["Middle East ST     +03:30", +3.5],
    "NET": ["Near East ST         +04:00", +4.0],
    "PLT": ["Pakistan ST           +05:00", +5.0],
    "IST": ["India ST                +05:30", +5.5],
    "BST": ["Bangladesh ST     +06:00", +6.0],
    "VST": ["Vietnam ST           +07:00", +7.0],
    "CTT": ["China Taiwan ST   +08:00", +8.0],
    "JST": ["Japan ST               +09:00", +9.0],
    "ACT": ["Australia Central +09:30", +9.5],
    "AET": ["Australia Eastern +10:00", +10.0],
    "SST": ["Solomon ST         +11.00", +11.0],
    "NST": ["New Zealand ST     +12.00", +12.0],
    "MIT": ["Midway Islands ST  -11:00", -11.0],
    "HST": ["Hawaii ST                -10:00", -10.0],
    "AST": ["Alaska ST                -09:00", -9.0],
    "PST": ["Pacific ST                 -08:00", -8.0],
    "PNT": ["Phoenix ST               -07:00", -7.0],
    "MST": ["Mountain ST            -07:00", -7.0],
    "CST": ["Central ST               -06:00", -6.0],
    "EST": ["Eastern ST               -05:00", -5.0],
    "IET": ["Indiana Eastern ST  -05:00", -5.0],
    "PRT": ["Puerto Rico ST         -04:00", -4.0],
    "CNT": ["Canada ST               -03:30", -4.0],
    "AGT": ["Argentina ST           -03:00", -3.0],
    "BET": ["Brazil ST                 -03:00", -3.0],
    "CAT": ["Central African        -01:00", -1.0],
}
formated_world_time = {
    "GMT": "Greenwich MT +00:00",
    "ECT": "European CT  +01:00",
    "EET": "East Eur    +02:00",
    "ART": "Arabic ST   +02:00",
    "EAT": "East African+03:00",
    "MET": "Middle East +03:30",
    "NET": "Near East   +04:00",
    "PLT": "Pakistan ST +05:00",
    "IST": "India ST    +05:30",
    "BST": "Bangladesh  +06:00",
    "VST": "Vietnam ST +07:00",
    "CTT": "China ST   +08:00",
    "JST": "Japan ST   +09:00",
    "ACT": "Australia CTR+09:30",
    "AET": "Australia EST+10:00",
    "SST": "Solomon ST   +11.00",
    "NST": "New Zealand +12.00",
    "MIT": "Midway ST   -11:00",
    "HST": "Hawaii ST   -10:00",
    "AST": "Alaska ST   -09:00",
    "PST": "Pacific ST   -08:00",
    "PNT": "Phoenix ST   -07:00",
    "MST": "Mountain ST   -07:00",
    "CST": "Central ST   -06:00",
    "EST": "Eastern ST   -05:00",
    "IET": "Indiana ST   -05:00",
    "PRT": "Puerto Rico ST-04:00",
    "CNT": "Canada ST   -03:30",
    "AGT": "Argentina ST -03:00",
    "BET": "Brazil ST   -03:00",
    "CAT": "African ST   -01:00"
}
location = 'IST'


def get_time():
    time = datetime.datetime.now()
    sys_time = time.hour + time.minute / 60
    gmt_time = sys_time - world_time['IST'][1]
    temp_converted_time = gmt_time + (world_time[location][1])

    if temp_converted_time < 0:
        converted_time = temp_converted_time + 24
    elif temp_converted_time > 24:
        converted_time = temp_converted_time - 24
    else:
        converted_time = temp_converted_time

    convered_time_hrs, convered_time_min, convered_time_sec = int(converted_time), math.floor(
        (converted_time - int(converted_time)) * 60), time.second
    return convered_time_hrs if convered_time_hrs <= 12 else convered_time_hrs - 12, convered_time_min, convered_time_sec, "AM" if convered_time_hrs < 12 else "PM"


def change_zone():
    global root
    root = tk.Tk()

    def change_timezone(timezone):
        global location
        location = timezone
        root.destroy()

    canvas = tk.Canvas(root, height=500, width=200)
    GMT = tk.Button(canvas, text=world_time['GMT'][0], font=('verdana', 10), command=lambda: change_timezone('GMT'))
    ECT = tk.Button(canvas, text=world_time['ECT'][0], font=('verdana', 10), command=lambda: change_timezone('ECT'))
    EET = tk.Button(canvas, text=world_time['EET'][0], font=('verdana', 10), command=lambda: change_timezone('EET'))
    ART = tk.Button(canvas, text=world_time['ART'][0], font=('verdana', 10), command=lambda: change_timezone('ART'))
    EAT = tk.Button(canvas, text=world_time['EAT'][0], font=('verdana', 10), command=lambda: change_timezone('EAT'))
    MET = tk.Button(canvas, text=world_time['MET'][0], font=('verdana', 10), command=lambda: change_timezone('MET'))
    NET = tk.Button(canvas, text=world_time['NET'][0], font=('verdana', 10), command=lambda: change_timezone('NET'))
    PLT = tk.Button(canvas, text=world_time['PLT'][0], font=('verdana', 10), command=lambda: change_timezone('PLT'))
    IST = tk.Button(canvas, text=world_time['IST'][0], font=('verdana', 10), command=lambda: change_timezone('IST'))
    BST = tk.Button(canvas, text=world_time['BST'][0], font=('verdana', 10), command=lambda: change_timezone('BST'))
    VST = tk.Button(canvas, text=world_time['VST'][0], font=('verdana', 10), command=lambda: change_timezone('VST'))
    CTT = tk.Button(canvas, text=world_time['CTT'][0], font=('verdana', 10), command=lambda: change_timezone('CTT'))
    JST = tk.Button(canvas, text=world_time['JST'][0], font=('verdana', 10), command=lambda: change_timezone('JST'))
    ACT = tk.Button(canvas, text=world_time['ACT'][0], font=('verdana', 10), command=lambda: change_timezone('ACT'))
    AET = tk.Button(canvas, text=world_time['AET'][0], font=('verdana', 10), command=lambda: change_timezone('AET'))
    SST = tk.Button(canvas, text=world_time['SST'][0], font=('verdana', 10), command=lambda: change_timezone('SST'))
    NST = tk.Button(canvas, text=world_time['NST'][0], font=('verdana', 10), command=lambda: change_timezone('NST'))
    MIT = tk.Button(canvas, text=world_time['MIT'][0], font=('verdana', 10), command=lambda: change_timezone('MIT'))
    HST = tk.Button(canvas, text=world_time['HST'][0], font=('verdana', 10), command=lambda: change_timezone('HST'))
    AST = tk.Button(canvas, text=world_time['AST'][0], font=('verdana', 10), command=lambda: change_timezone('AST'))
    PST = tk.Button(canvas, text=world_time['PST'][0], font=('verdana', 10), command=lambda: change_timezone('PST'))
    PNT = tk.Button(canvas, text=world_time['PNT'][0], font=('verdana', 10), command=lambda: change_timezone('PNT'))
    MST = tk.Button(canvas, text=world_time['MST'][0], font=('verdana', 10), command=lambda: change_timezone('MST'))
    CST = tk.Button(canvas, text=world_time['CST'][0], font=('verdana', 10), command=lambda: change_timezone('CST'))
    EST = tk.Button(canvas, text=world_time['EST'][0], font=('verdana', 10), command=lambda: change_timezone('EST'))
    IET = tk.Button(canvas, text=world_time['IET'][0], font=('verdana', 10), command=lambda: change_timezone('IET'))
    PRT = tk.Button(canvas, text=world_time['PRT'][0], font=('verdana', 10), command=lambda: change_timezone('PRT'))
    CNT = tk.Button(canvas, text=world_time['CNT'][0], font=('verdana', 10), command=lambda: change_timezone('CNT'))
    AGT = tk.Button(canvas, text=world_time['AGT'][0], font=('verdana', 10), command=lambda: change_timezone('AGT'))
    BET = tk.Button(canvas, text=world_time['BET'][0], font=('verdana', 10), command=lambda: change_timezone('BET'))
    CAT = tk.Button(canvas, text=world_time['CAT'][0], font=('verdana', 10), command=lambda: change_timezone('CAT'))

    canvas.pack()

    GMT.grid(column=0, row=0)
    ECT.grid(column=0, row=1)
    EET.grid(column=0, row=2)
    ART.grid(column=0, row=3)
    EAT.grid(column=0, row=4)
    MET.grid(column=0, row=5)
    NET.grid(column=0, row=6)
    PLT.grid(column=0, row=7)
    IST.grid(column=0, row=8)
    BST.grid(column=0, row=9)
    VST.grid(column=0, row=10)
    CTT.grid(column=0, row=11)
    JST.grid(column=0, row=12)
    ACT.grid(column=0, row=13)
    AET.grid(column=0, row=14)
    SST.grid(column=0, row=15)
    NST.grid(column=1, row=0)
    MIT.grid(column=1, row=1)
    HST.grid(column=1, row=2)
    AST.grid(column=1, row=3)
    PST.grid(column=1, row=4)
    PNT.grid(column=1, row=5)
    MST.grid(column=1, row=6)
    CST.grid(column=1, row=7)
    EST.grid(column=1, row=8)
    IET.grid(column=1, row=9)
    PRT.grid(column=1, row=10)
    CNT.grid(column=1, row=11)
    AGT.grid(column=1, row=12)
    BET.grid(column=1, row=13)
    CAT.grid(column=1, row=14)

    root.mainloop()


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('keraleeyam', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width // 2  - text.get_width() // 2), self.y + 3 + (self.height // 2 - text.get_height() // 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
line = (200, 230, 255)
bg = (40, 40, 40)
width = 600  # Width of the window
height = 800  # Height of the window

window = pygame.display.set_mode((width, height))  # Creating the window

frame = pygame.image.load('images/frame.png')
frame.set_colorkey(bg)

center = pygame.image.load('images/center.png')
center.set_colorkey(bg)

# Importing the second hand niddle image
min = pygame.image.load('images/min.png').convert()
min.set_colorkey(white)

# Importing the minute hand niddel image
hrs = pygame.image.load('images/hr.png').convert()
hrs.set_colorkey(white)

sec = pygame.image.load('images/sec.png').convert()
sec.set_colorkey(white)

button = button((200, 200, 200), (width // 2) - 120, height - 190, 250, 40, ' Change Time Zone ')

zone_font = pygame.font.SysFont('notosanscjktc', 30)
zone_text = zone_font.render('', True, green, bg)
zone_textRect = zone_text.get_rect()
zone_textRect.center = ((width // 2) - 110, height-240)

time_font = pygame.font.SysFont('ubuntu', 50)
time_text = time_font.render('', True, green, bg)
time_textRect = time_text.get_rect()
time_textRect.center = ((width // 2) - 130, height - 300)

def clock():
    pygame.display.set_caption('Clock')  # Title of the window
    pygame.time.delay(10)
    window.fill(bg)

    hrs_val, min_val, sec_val, after = get_time()

    window.blit(frame, (width // 2 - frame.get_width() // 2, 250 - frame.get_height() // 2))

    hrs_cpy = pygame.transform.rotate(hrs, -((hrs_val * 30) + (min_val / 2)))
    window.blit(hrs_cpy, (width // 2 - hrs_cpy.get_width() // 2, 250 - hrs_cpy.get_height() // 2))

    min_cpy = pygame.transform.rotate(min, -min_val * 6)
    window.blit(min_cpy, (width // 2 - min_cpy.get_width() // 2, 250 - min_cpy.get_height() // 2))

    sec_cpy = pygame.transform.rotate(sec, -sec_val * 6)
    window.blit(sec_cpy, (width // 2 - sec_cpy.get_width() // 2, 250 - sec_cpy.get_height() // 2))

    window.blit(center, (width // 2 - center.get_width() // 2, 250 - center.get_height() // 2))

    button.draw(window, bg)

    zone_str = zone_font.render(formated_world_time[location], True, line, bg)
    window.blit(zone_str, zone_textRect)

    time_str = time_font.render("%02d:%02d:%02d %s" % (hrs_val, min_val, sec_val, after), True, line, bg)
    window.blit(time_str, time_textRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.isOver(pos):
                change_zone()

        if event.type == pygame.MOUSEMOTION:
            if button.isOver(pos):
                button.color = (151, 147, 245)
            else:
                button.color = (200, 200, 200)

    pygame.display.update()


while True:
    clock()
