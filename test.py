import pygame
import datetime
import tkinter as tk
import pickle

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
verdana_font = 'font/verdana.ttf'
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

clock_button = button(bg, (200, 200, 200), 5, 0, 70, 30, ' Clock ')
alarm_button = button(bg, (200, 200, 200), 93, 0, 70, 30, ' Alarm ')
stopwatch_button = button(bg, (200, 200, 200), 188, 0, 130, 30, ' Stop Watch ')
timer_button = button(bg, (200, 200, 200), 335, 0, 70, 30, ' Timer ')







class alarm:
    def __init__(self, hours, minutes, ampm, isActive, y):
        self.hours = hours
        self.minutes = minutes
        self.ampm = ampm
        self.isActive = isActive
        self.on_sw_image = pygame.image.load('images/swon.png')
        self.on_sw_image.set_colorkey(white)
        self.off_sw_image = pygame.image.load('images/swoff.png')
        self.off_sw_image.set_colorkey(white)
        self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image
        self.sw_x = 80 - self.sw_image.get_width() // 2
        self.sw_y = y - self.sw_image.get_height() // 2
        self.rst_image = pygame.image.load('images/bin.png')
        self.rst_image.set_colorkey(white)
        self.rst_x = width - 70 - self.rst_image.get_width() // 2
        self.rst_y = y - self.rst_image.get_height() // 2
        self.alarm_font = pygame.font.Font(ubuntu_font, 50)
        self.alarm_text = self.alarm_font.render('', True, green, bg)
        self.alarm_textRect = self.alarm_text.get_rect()
        self.alarm_textRect.center = 200 - self.alarm_text.get_width() // 2, y + 25 - self.alarm_text.get_height() // 2

    def ring_alarm(self, tone):
        def snooz(snooz_time):
            snooz_hrs = snooz_time // 60
            snooz_min = snooz_time % 60
            if snooz_min + self.minutes > 60:
                self.minutes += snooz_min - 60
                self.hours += 1

            if snooz_hrs + self.hours > 12:
                self.hours += snooz_hrs - 12
                if self.ampm == 'AM':
                    self.ampm = 'PM'
                else:
                    self.ampm = 'AM'

            self.isActive = True
            self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image
            root.destroy()

        def quit():
            root.destroy()

        root = tk.Tk()
        root.geometry("300x250+700+100")

        pygame.mixer.Sound.play(tone)
        pickle_in = open("data/alarm_prop.pickle", "rb")
        alarm_prop = pickle.load(pickle_in)
        pickle_in.close()
        snooz_time = alarm_prop['snooz_time']
        canvas = tk.Canvas(root, height=250, width=300, bg='#282828')
        alarm_label = tk.Label(canvas, text="ALARM", font=('ubuntu', 60), bg='#282828', fg='#C8E6FF')
        time_label = tk.Label(canvas, text="%02d:%02d %s" % (self.hours, self.minutes, self.ampm), font=('ubuntu', 40),
                              bg='#282828', fg='#C8E6FF')
        snooz_button = tk.Button(canvas, text="Snooz %d min" % (snooz_time), font=('verdana', 15),
                                 activebackground="#666699",
                                 bg='#9793F5', command=lambda: snooz(snooz_time))
        close_button = tk.Button(canvas, text="Close", font=('verdana', 15), activebackground="#666699", bg='#9793F5',
                                 command=lambda: quit())
        canvas.pack()
        alarm_label.place(y=1, x=15)
        time_label.place(y=100, x=35)
        snooz_button.place(y=190, x=10)
        close_button.place(y=190, x=200)
        root.mainloop()
        pygame.mixer.Sound.stop(tone)

        alarm_data = {
            "alarm1": [alarm1.hours, alarm1.minutes, alarm1.ampm, alarm1.isActive],
            "alarm2": [alarm2.hours, alarm2.minutes, alarm2.ampm, alarm2.isActive],
            "alarm3": [alarm3.hours, alarm3.minutes, alarm3.ampm, alarm3.isActive],
            "alarm4": [alarm4.hours, alarm4.minutes, alarm4.ampm, alarm4.isActive],
            "alarm5": [alarm5.hours, alarm5.minutes, alarm5.ampm, alarm5.isActive],
        }

        pickle_out = open("data/alarm_data.pickle", "wb")
        pickle.dump(alarm_data, pickle_out)
        pickle_out.close()

    def comparison(self, sys_hrs, sys_min, sys_ampn):
        if self.hours == sys_hrs and self.minutes == sys_min and self.ampm == sys_ampn and self.isActive:
            self.isActive = False
            self.ring_alarm(current_tone)
            self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image

    def isOverSW(self, pos):
        if self.sw_x < pos[0] < self.sw_x + self.sw_image.get_width():
            if pos[1] > self.sw_y and pos[1] < self.sw_y + self.sw_image.get_height():
                return True
        return False

    def sw_clicked(self):
        self.isActive = not self.isActive
        self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image

        alarm_data = {
            "alarm1": [alarm1.hours, alarm1.minutes, alarm1.ampm, alarm1.isActive],
            "alarm2": [alarm2.hours, alarm2.minutes, alarm2.ampm, alarm2.isActive],
            "alarm3": [alarm3.hours, alarm3.minutes, alarm3.ampm, alarm3.isActive],
            "alarm4": [alarm4.hours, alarm4.minutes, alarm4.ampm, alarm4.isActive],
            "alarm5": [alarm5.hours, alarm5.minutes, alarm5.ampm, alarm5.isActive],
        }

        pickle_out = open("data/alarm_data.pickle", "wb")
        pickle.dump(alarm_data, pickle_out)
        pickle_out.close()

    def isOverRST(self, pos):
        if self.rst_x < pos[0] < self.rst_x + self.rst_image.get_width():
            if self.rst_y < pos[1] < self.rst_y + self.rst_image.get_height():
                return True
        return False

pickle_in = open("data/alarm_data.pickle", "rb")
alarm_data = pickle.load(pickle_in)
pickle_in.close()

alarm1 = alarm(alarm_data['alarm1'][0], alarm_data['alarm1'][1], alarm_data['alarm1'][2], alarm_data['alarm1'][3], 290)
alarm2 = alarm(alarm_data['alarm2'][0], alarm_data['alarm2'][1], alarm_data['alarm2'][2], alarm_data['alarm2'][3], 380)
alarm3 = alarm(alarm_data['alarm3'][0], alarm_data['alarm3'][1], alarm_data['alarm3'][2], alarm_data['alarm3'][3], 470)
alarm4 = alarm(alarm_data['alarm4'][0], alarm_data['alarm4'][1], alarm_data['alarm4'][2], alarm_data['alarm4'][3], 560)
alarm5 = alarm(alarm_data['alarm5'][0], alarm_data['alarm5'][1], alarm_data['alarm5'][2], alarm_data['alarm5'][3], 650)

alarm_list = [alarm1, alarm2, alarm3, alarm4, alarm5]


def tone_return(sno):
    if sno == 1:
        return pygame.mixer.Sound("tones/sound.wav")
    elif sno == 2:
        return pygame.mixer.Sound("tones/back.wav")
    elif sno == 3:
        return pygame.mixer.Sound("tones/carbin.wav")
    elif sno == 4:
        return pygame.mixer.Sound("tones/eptic.wav")
    elif sno == 5:
        return pygame.mixer.Sound("tones/moon.wav")
    elif sno == 6:
        return pygame.mixer.Sound("tones/watch.wav")
    elif sno == 7:
        return pygame.mixer.Sound("tones/wistle.wav")
    elif sno == 8:
        return pygame.mixer.Sound("tones/follow.wav")
    elif sno == 9:
        return pygame.mixer.Sound("tones/propaganda.wav")
    elif sno == 10:
        return pygame.mixer.Sound("tones/ride it.wav")
    elif sno == 11:
        return pygame.mixer.Sound("tones/start.wav")
    elif sno == 12:
        return pygame.mixer.Sound("tones/suns.wav")
    elif sno == 13:
        return pygame.mixer.Sound("tones/xilla.wav")


pickle_in = open("data/alarm_prop.pickle", "rb")
alarm_prop = pickle.load(pickle_in)
pickle_in.close()
current_tone = tone_return(alarm_prop['tone_number'])


def setting_window():
    global current_tone
    pickle_in = open("data/alarm_prop.pickle", "rb")
    alarm_prop = pickle.load(pickle_in)
    pickle_in.close()

    root = tk.Tk()
    root.title("Settings")
    root.geometry("400x500+700+100")
    canvas = tk.Canvas(root, height=500, width=400, bg='#282828')
    tone_number = tk.IntVar(canvas, alarm_prop['tone_number'])
    snooz_val = tk.IntVar(canvas, value=alarm_prop['snooz_time'])
    x = 50

    class tone:
        def __init__(self, sno, y, path, name):
            self.tone = pygame.mixer.Sound(path)
            self.sno = sno
            self.name = name
            self.x = 2
            self.y = y
            self.button_state = True
            self.play_img = tk.PhotoImage(file="images/speaker.png")
            self.play = tk.Button(root, image=self.play_img, command=lambda: self.play_stop_tone())
            self.play.place(x=self.x + 160, y=self.y)
            self.stop_img = tk.PhotoImage(file="images/stop.png")

        def play_stop_tone(self):
            if self.button_state:
                self.stop = tk.Button(root, image=self.stop_img, command=lambda: self.play_stop_tone())
                self.stop.place(x=self.x + 160, y=self.y)
                self.button_state = not self.button_state
                play_tone(self.tone, self.sno)
            else:
                self.play = tk.Button(root, image=self.play_img, command=lambda: self.play_stop_tone())
                self.play.place(x=self.x + 160, y=self.y)
                self.button_state = not self.button_state
                pygame.mixer.Sound.stop(self.tone)

    tone1 = tone(1, x + 30 * 0, "tones/sound.wav", 'Hope')
    tone2 = tone(2, x + 30 * 1, "tones/back.wav", 'Back Home')
    tone3 = tone(3, x + 30 * 2, "tones/carbin.wav", 'Carbin')
    tone4 = tone(4, x + 30 * 3, "tones/eptic.wav", 'The End')
    tone5 = tone(5, x + 30 * 4, "tones/moon.wav", 'Moon Love')
    tone6 = tone(6, x + 30 * 5, "tones/watch.wav", 'Watch This')
    tone7 = tone(7, x + 30 * 6, "tones/wistle.wav", 'Wistle War')
    tone8 = tone(8, x + 30 * 7, "tones/follow.wav", 'Follow')
    tone9 = tone(9, x + 30 * 8, "tones/propaganda.wav", 'Propaganda')
    tone10 = tone(10, x + 30 * 9, "tones/ride it.wav", 'Ride It')
    tone11 = tone(11, x + 30 * 10, "tones/start.wav", 'Start It Over')
    tone12 = tone(12, x + 30 * 11, "tones/suns.wav", 'Suns Up')
    tone13 = tone(13, x + 30 * 12, "tones/xilla.wav", 'XILLA!')

    tone_list = [tone1, tone2, tone3, tone4, tone5, tone6, tone7, tone8, tone9, tone10, tone11, tone12, tone13]

    def play_tone(tone, sno):
        for i in tone_list:
            pygame.mixer.Sound.stop(i.tone)
            i.button_state = False

        for i in range(len(tone_list)):
            if i == sno - 1:
                tone_list[i].button_state = True

        for i in tone_list:
            if not i.button_state:
                i.play_stop_tone()

        for i in range(len(tone_list)):
            if i == sno - 1:
                tone_list[i].button_state = False

        pygame.mixer.Sound.play(tone)

    def ok(snooz_time, tone):
        global current_tone
        alarm_prop = {"snooz_time": int(snooz_time), "tone_number": tone, }
        pickle_out = open("data/alarm_prop.pickle", "wb")
        pickle.dump(alarm_prop, pickle_out)
        pickle_out.close()
        current_tone = tone_return(alarm_prop['tone_number'])
        root.destroy()

        for i in tone_list:
            pygame.mixer.Sound.stop(i.tone)

    tones = {tone1.name: [tone1.y, 1],
             tone2.name: [tone2.y, 2],
             tone3.name: [tone3.y, 3],
             tone4.name: [tone4.y, 4],
             tone5.name: [tone5.y, 5],
             tone6.name: [tone6.y, 6],
             tone7.name: [tone7.y, 7],
             tone8.name: [tone8.y, 8],
             tone9.name: [tone9.y, 9],
             tone10.name: [tone10.y, 10],
             tone11.name: [tone11.y, 11],
             tone12.name: [tone12.y, 12],
             tone13.name: [tone13.y, 13],
             }
    song_label = tk.Label(canvas, text="Select Tone", font=('TkFixedFont', 25), bg='#282828', fg='#0099cc').place(x=7,
                                                                                                                  y=1)
    snooz_label = tk.Label(canvas, text="Snooz\nDuration", font=('TkFixedFont', 13), bg='#282828', fg='#C8E6FF').place(
        x=220,
        y=150)
    snooz_entry = tk.Entry(canvas, text='45', width=3, textvariable=snooz_val, font=('TkFixedFont', 15)).place(x=310,
                                                                                                               y=160)
    min_label = tk.Label(canvas, text="min", font=('TkFixedFont', 13), bg='#282828', fg='#C8E6FF').place(x=360, y=160)

    ok_button = tk.Button(canvas, text="OK", font=('TkFixedFont', 20),
                          command=lambda: ok(snooz_val.get(), tone_number.get())).place(x=320, y=440)
    for (text, value) in tones.items():
        tk.Radiobutton(canvas, text=text, variable=tone_number, font=('TkFixedFont', 14), bg='#282828', fg='#0099cc',
                       activeforeground='#C8E6FF', activebackground='#282828', highlightthickness=0,
                       value=value[1]).place(y=value[0], x=2)
    canvas.pack()
    root.mainloop()

    for i in tone_list:
        pygame.mixer.Sound.stop(i.tone)

def set_alarm_trig():
    for i in alarm_list:
        if i.hours == 0 and i.minutes == 0  and i.ampm == 'AM':
            i.hours = set_alarm_obj.hrs
            i.minutes = set_alarm_obj.min
            i.ampm = set_alarm_obj.ampm
            i.isActive = True
            i.sw_image = i.on_sw_image if i.isActive else i.off_sw_image
            break

    alarm_data = {
        "alarm1": [alarm1.hours, alarm1.minutes, alarm1.ampm, alarm1.isActive],
        "alarm2": [alarm2.hours, alarm2.minutes, alarm2.ampm, alarm2.isActive],
        "alarm3": [alarm3.hours, alarm3.minutes, alarm3.ampm, alarm3.isActive],
        "alarm4": [alarm4.hours, alarm4.minutes, alarm4.ampm, alarm4.isActive],
        "alarm5": [alarm5.hours, alarm5.minutes, alarm5.ampm, alarm5.isActive],
    }

    pickle_out = open("data/alarm_data.pickle", "wb")
    pickle.dump(alarm_data, pickle_out)
    pickle_out.close()


def reset(alarm_name):
    if alarm_name == 'alarm1':
        for i in range(len(alarm_list)-1):
            alarm_list[i].hours = alarm_list[i+1].hours
            alarm_list[i].minutes = alarm_list[i+1].minutes
            alarm_list[i].ampm = alarm_list[i+1].ampm

    elif alarm_name == 'alarm2':
        for i in range(1, len(alarm_list)-1):
            alarm_list[i].hours = alarm_list[i+1].hours
            alarm_list[i].minutes = alarm_list[i+1].minutes
            alarm_list[i].ampm = alarm_list[i+1].ampm

    elif alarm_name == 'alarm3':
        for i in range(2, len(alarm_list)-1):
            alarm_list[i].hours = alarm_list[i+1].hours
            alarm_list[i].minutes = alarm_list[i+1].minutes
            alarm_list[i].ampm = alarm_list[i+1].ampm

    elif alarm_name == 'alarm4':
        for i in range(3, len(alarm_list)-1):
            alarm_list[i].hours = alarm_list[i+1].hours
            alarm_list[i].minutes = alarm_list[i+1].minutes
            alarm_list[i].ampm = alarm_list[i+1].ampm


    alarm5.hours = 0
    alarm5.minutes = 0
    alarm5.ampm = 'AM'

    for i in alarm_list:
        if i.hours == 0 and i.minutes == 0:
            i.isActive = False

        i.sw_image = i.on_sw_image if i.isActive else i.off_sw_image


    alarm_data = {
        "alarm1": [alarm1.hours, alarm1.minutes, alarm1.ampm, alarm1.isActive],
        "alarm2": [alarm2.hours, alarm2.minutes, alarm2.ampm, alarm2.isActive],
        "alarm3": [alarm3.hours, alarm3.minutes, alarm3.ampm, alarm3.isActive],
        "alarm4": [alarm4.hours, alarm4.minutes, alarm4.ampm, alarm4.isActive],
        "alarm5": [alarm5.hours, alarm5.minutes, alarm5.ampm, alarm5.isActive],
    }

    pickle_out = open("data/alarm_data.pickle", "wb")
    pickle.dump(alarm_data, pickle_out)
    pickle_out.close()


class set_alarm:
    def __init__(self, y, hrs, min, ampm):
        self.y = y
        self.hrs = hrs
        self.min = min
        self.ampm = ampm

        self.add_hr = pygame.image.load('images/arrup.png')
        self.add_hr.set_colorkey(white)
        self.sub_hr = pygame.image.load('images/arrdw.png')
        self.sub_hr.set_colorkey(white)
        self.add_hr_x = 85 - self.add_hr.get_width() // 2
        self.add_hr_y = y - self.add_hr.get_height() // 2
        self.sub_hr_x = 85 - self.sub_hr.get_width() // 2
        self.sub_hr_y = y + 100 - self.sub_hr.get_height() // 2

        self.add_min = pygame.image.load('images/arrup.png')
        self.add_min.set_colorkey(white)
        self.sub_min = pygame.image.load('images/arrdw.png')
        self.sub_min.set_colorkey(white)
        self.add_min_x = 225 - self.add_min.get_width() // 2
        self.add_min_y = y - self.add_min.get_height() // 2
        self.sub_min_x = 225 - self.sub_min.get_width() // 2
        self.sub_min_y = y + 100 - self.sub_min.get_height() // 2

        self.ampm_up = pygame.image.load('images/arrup.png')
        self.ampm_up.set_colorkey(white)
        self.ampm_dw = pygame.image.load('images/arrdw.png')
        self.ampm_dw.set_colorkey(white)
        self.ampm_up_x = 365 - self.ampm_up.get_width() // 2
        self.ampm_up_y = y - self.ampm_up.get_height() // 2
        self.ampm_dw_x = 365 - self.ampm_dw.get_width() // 2
        self.ampm_dw_y = y + 100 - self.ampm_dw.get_height() // 2

        self.hrs_font = pygame.font.Font(ubuntu_font, 50)
        self.hrs_text = self.hrs_font.render('', True, green, bg)
        self.hrs_textRect = self.hrs_text.get_rect()
        self.hrs_textRect.center = 60 - self.hrs_text.get_width() // 2, y + 22 + self.hrs_text.get_height() // 2

        self.colan_font = pygame.font.Font(ubuntu_font, 70)
        self.colan_text = self.colan_font.render(':', True, green, bg)
        self.colan_textRect = self.colan_text.get_rect()
        self.colan_textRect.center = 160 - self.colan_text.get_width() // 2, y + 5 + self.colan_text.get_height() // 2

        self.min_font = pygame.font.Font(ubuntu_font, 50)
        self.min_text = self.min_font.render('', True, green, bg)
        self.min_textRect = self.min_text.get_rect()
        self.min_textRect.center = 195 - self.min_text.get_width() // 2, y + 22 + self.min_text.get_height() // 2

        self.ampm_font = pygame.font.Font(ubuntu_font, 50)
        self.ampm_text = self.ampm_font.render('', True, green, bg)
        self.ampm_textRect = self.ampm_text.get_rect()
        self.ampm_textRect.center = 325 - self.ampm_text.get_width() // 2, y + 22 + self.ampm_text.get_height() // 2

        self.set_button = button((200, 200, 200), (0, 0, 0), width - 150, y + 30, 135, 40, 'Set Alarm')

    def action(self, button):

        if button == 'add_hr':
            if self.hrs < 12:
                self.hrs += 1
            else:
                self.hrs = 1

        if button == 'sub_hr':
            if self.hrs > 1:
                self.hrs -= 1
            else:
                self.hrs = 12

        if button == 'add_min':
            if self.min < 60:
                self.min += 1
            else:
                self.min = 0

        if button == 'sub_min':
            if self.min > 0:
                self.min -= 1
            else:
                self.min = 60

        if button == 'ampm_up' or button == 'ampm_dw':
            self.ampm = 'AM' if self.ampm == 'PM' else 'PM'

    def isOver(self, pos):
        if self.add_hr_x < pos[0] < self.add_hr_x + self.add_hr.get_width():
            if self.add_hr_y < pos[1] < self.add_hr_y + self.add_hr.get_height():
                return 'add_hr'
        if self.sub_hr_x < pos[0] < self.sub_hr_x + self.sub_hr.get_width():
            if self.sub_hr_y < pos[1] < self.sub_hr_y + self.sub_hr.get_height():
                return 'sub_hr'

        if self.add_min_x < pos[0] < self.add_min_x + self.add_hr.get_width():
            if self.add_min_y < pos[1] < self.add_min_y + self.add_min.get_height():
                return 'add_min'
        if self.sub_min_x < pos[0] < self.sub_min_x + self.sub_min.get_width():
            if self.sub_min_y < pos[1] < self.sub_min_y + self.sub_min.get_height():
                return 'sub_min'

        if self.ampm_up_x < pos[0] < self.ampm_up_x + self.ampm_up.get_width():
            if self.ampm_up_y < pos[1] < self.ampm_up_y + self.ampm_up.get_height():
                return 'ampm_up'
        if self.ampm_dw_x < pos[0] < self.ampm_dw_x + self.ampm_dw.get_width():
            if self.ampm_dw_y < pos[1] < self.ampm_dw_y + self.ampm_dw.get_height():
                return 'ampm_dw'




time = datetime.datetime.now()
sys_hrs, sys_min, ampm = time.hour if time.hour <= 12 else time.hour - 12, time.minute, 'AM' if time.hour < 12 else 'PM'

set_alarm_obj = set_alarm(80, sys_hrs, sys_min, ampm)



def alarm_window():
    pygame.display.set_caption('Alarm')
    while True:
        global s_hrs, s_min, s_milli, s_sec, s_duration, s_stopwatch_run, s_active_status, s_state, s_spl_lap, s_counter, s_cap_count, s_start_time, s_resttime, time
        alarm_button.text_color = (151, 147, 245)
        time = datetime.datetime.now()
        sys_hrs, sys_min, ampm = time.hour if time.hour <= 12 else time.hour - 12, time.minute, 'AM' if time.hour < 12 else 'PM'
        window.fill(bg)

        window.blit(set_alarm_obj.add_hr, (set_alarm_obj.add_hr_x, set_alarm_obj.add_hr_y))
        window.blit(set_alarm_obj.sub_hr, (set_alarm_obj.sub_hr_x, set_alarm_obj.sub_hr_y))

        window.blit(set_alarm_obj.add_min, (set_alarm_obj.add_min_x, set_alarm_obj.add_min_y))
        window.blit(set_alarm_obj.sub_min, (set_alarm_obj.sub_min_x, set_alarm_obj.sub_min_y))

        window.blit(set_alarm_obj.ampm_up, (set_alarm_obj.ampm_up_x, set_alarm_obj.ampm_up_y))
        window.blit(set_alarm_obj.ampm_dw, (set_alarm_obj.ampm_dw_x, set_alarm_obj.ampm_dw_y))

        set_alarm_hrs = set_alarm_obj.hrs_font.render("%02d" % set_alarm_obj.hrs, True, line, bg)
        window.blit(set_alarm_hrs, set_alarm_obj.hrs_textRect)

        colan_text = set_alarm_obj.colan_font.render(":", True, line, bg)
        window.blit(colan_text, set_alarm_obj.colan_textRect)

        set_alarm_min = set_alarm_obj.min_font.render("%02d" % set_alarm_obj.min, True, line, bg)
        window.blit(set_alarm_min, set_alarm_obj.min_textRect)

        set_alarm_ampm = set_alarm_obj.ampm_font.render(set_alarm_obj.ampm, True, line, bg)
        window.blit(set_alarm_ampm, set_alarm_obj.ampm_textRect)

        set_alarm_obj.set_button.draw(window, bg)
        clock_button.draw(window, bg)
        alarm_button.draw(window, bg)
        stopwatch_button.draw(window, bg)
        timer_button.draw(window, bg)

        window.blit(alarm1.sw_image, (alarm1.sw_x, alarm1.sw_y))
        window.blit(alarm2.sw_image, (alarm2.sw_x, alarm2.sw_y))
        window.blit(alarm3.sw_image, (alarm3.sw_x, alarm3.sw_y))
        window.blit(alarm4.sw_image, (alarm4.sw_x, alarm4.sw_y))
        window.blit(alarm5.sw_image, (alarm5.sw_x, alarm5.sw_y))

        alarm_str1 = alarm1.alarm_font.render("%02d:%02d %s" % (alarm1.hours, alarm1.minutes, alarm1.ampm), True, line,
                                              bg)
        window.blit(alarm_str1, alarm1.alarm_textRect)

        alarm_str2 = alarm2.alarm_font.render("%02d:%02d %s" % (alarm2.hours, alarm2.minutes, alarm2.ampm), True, line,
                                              bg)
        window.blit(alarm_str2, alarm2.alarm_textRect)

        alarm_str3 = alarm3.alarm_font.render("%02d:%02d %s" % (alarm3.hours, alarm3.minutes, alarm3.ampm), True, line,
                                              bg)
        window.blit(alarm_str3, alarm3.alarm_textRect)

        alarm_str4 = alarm4.alarm_font.render("%02d:%02d %s" % (alarm4.hours, alarm4.minutes, alarm4.ampm), True, line,
                                              bg)
        window.blit(alarm_str4, alarm4.alarm_textRect)

        alarm_str5 = alarm5.alarm_font.render("%02d:%02d %s" % (alarm5.hours, alarm5.minutes, alarm5.ampm), True, line,
                                              bg)
        window.blit(alarm_str5, alarm5.alarm_textRect)

        window.blit(alarm1.rst_image, (alarm1.rst_x, alarm1.rst_y))
        window.blit(alarm2.rst_image, (alarm2.rst_x, alarm2.rst_y))
        window.blit(alarm3.rst_image, (alarm3.rst_x, alarm3.rst_y))
        window.blit(alarm4.rst_image, (alarm4.rst_x, alarm4.rst_y))
        window.blit(alarm5.rst_image, (alarm5.rst_x, alarm5.rst_y))

        alarm1.comparison(sys_hrs, sys_min, ampm)
        alarm2.comparison(sys_hrs, sys_min, ampm)
        alarm3.comparison(sys_hrs, sys_min, ampm)
        alarm4.comparison(sys_hrs, sys_min, ampm)
        alarm5.comparison(sys_hrs, sys_min, ampm)

        setting_img = pygame.image.load('images/setting.png')
        setting_img.set_colorkey(white)
        setting_x, setting_y = 550 - setting_img.get_width() // 2, 30 - setting_img.get_height() // 2
        window.blit(setting_img, (setting_x, setting_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                if set_alarm_obj.set_button.isOver(pos):
                    set_alarm_obj.set_button.color = (151, 147, 245)
                else:
                    set_alarm_obj.set_button.color = (200, 200, 200)

                if clock_button.isOver(pos):
                    clock_button.text_color = (151, 147, 245)
                else:
                    clock_button.text_color = (200, 200, 200)

                if stopwatch_button.isOver(pos):
                    stopwatch_button.text_color = (151, 147, 245)
                else:
                    stopwatch_button.text_color = (200, 200, 200)

                if timer_button.isOver(pos):
                    timer_button.text_color = (151, 147, 245)
                else:
                    timer_button.text_color = (200, 200, 200)

            if event.type == pygame.MOUSEBUTTONDOWN:
                set_alarm_obj.action(set_alarm_obj.isOver(pos))
                if set_alarm_obj.set_button.isOver(pos):
                    set_alarm_trig()

                if alarm1.isOverSW(pos):
                    alarm1.sw_clicked()

                if alarm1.isOverRST(pos):
                    reset('alarm1')

                if alarm2.isOverSW(pos):
                    alarm2.sw_clicked()

                if alarm2.isOverRST(pos):
                    reset('alarm2')

                if alarm3.isOverSW(pos):
                    alarm3.sw_clicked()

                if alarm3.isOverRST(pos):
                    reset('alarm3')

                if alarm4.isOverSW(pos):
                    alarm4.sw_clicked()

                if alarm4.isOverRST(pos):
                    reset('alarm4')

                if alarm5.isOverSW(pos):
                    alarm5.sw_clicked()

                if alarm5.isOverRST(pos):
                    reset('alarm5')

                if pos[0] > setting_x and pos[0] < setting_x + setting_img.get_width():
                    if pos[1] > setting_y and pos[1] < setting_y + setting_img.get_height():
                        setting_window()

        pygame.display.update()


alarm_window()
