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
        # Some alarm state variable
        self.hours = hours
        self.minutes = minutes
        self.ampm = ampm
        self.isActive = isActive

        # Importing the alarm on and off images
        self.on_sw_image = pygame.image.load('images/swon.png')
        self.on_sw_image.set_colorkey(white)
        self.off_sw_image = pygame.image.load('images/swoff.png')
        self.off_sw_image.set_colorkey(white)
        self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image  # selecting the image based in the state
        self.sw_x = 80 - self.sw_image.get_width() // 2  # dimension for the switch image
        self.sw_y = y - self.sw_image.get_height() // 2

        # importing the delete image and defining the coordinate
        self.rst_image = pygame.image.load('images/bin.png')
        self.rst_image.set_colorkey(white)
        self.rst_x = width - 70 - self.rst_image.get_width() // 2
        self.rst_y = y - self.rst_image.get_height() // 2

        # defining the property of the alarm label
        self.alarm_font = pygame.font.Font(ubuntu_font, 50)
        self.alarm_text = self.alarm_font.render('', True, green, bg)
        self.alarm_textRect = self.alarm_text.get_rect()
        self.alarm_textRect.center = 200 - self.alarm_text.get_width() // 2, y + 25 - self.alarm_text.get_height() // 2

    def ring_alarm(self, tone):

        # when the snooz button is pressed this function is called
        def snooz(snooze_time):
            # here the argument snooze_time is in min so we have to convert it to hrs and min
            snooze_hrs = snooze_time // 60
            snooze_min = snooze_time % 60

            # if the current minute plus the snooze_min exceed 60 then it is incremented by more then an hour, then do follow
            if snooze_min + self.minutes > 60:
                self.minutes += snooze_min - 60
                self.hours += 1
            else:
                self.minutes += snooze_min

            # if the current hour plus the snooze hour exceeds 12 mean there is change in AM and PM
            if snooze_hrs + self.hours > 12:
                self.hours += snooze_hrs - 12
                if self.ampm == 'AM':
                    self.ampm = 'PM'
                else:
                    self.ampm = 'AM'

            self.isActive = True
            self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image
            alarm_ring_win.destroy()

            # After snoozing update the data
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

        alarm_ring_win = tk.Tk()  # create the ring window
        alarm_ring_win.geometry("300x250+700+100")  # place the window
        pygame.mixer.Sound.play(tone)  # play the tone

        # fetch the snooze time
        pickle_in = open("data/alarm_prop.pickle", "rb")
        alarm_prop = pickle.load(pickle_in)
        pickle_in.close()
        snooze_time = alarm_prop['snooz_time']

        # tkinter stuffs
        canvas = tk.Canvas(alarm_ring_win, height=250, width=300, bg='#282828')
        alarm_label = tk.Label(canvas, text="ALARM", font=('ubuntu', 60), bg='#282828', fg='#C8E6FF')
        time_label = tk.Label(canvas, text="%02d:%02d %s" % (self.hours, self.minutes, self.ampm), font=('ubuntu', 40),
                              bg='#282828', fg='#C8E6FF')
        snooze_button = tk.Button(canvas, text="Snooze %d min" % snooze_time, font=('verdana', 15),
                                  activebackground="#666699",
                                  bg='#9793F5', command=lambda: snooz(snooze_time))
        close_button = tk.Button(canvas, text="Close", font=('verdana', 15), activebackground="#666699", bg='#9793F5',
                                 command=lambda: alarm_ring_win.destroy())
        canvas.pack()
        alarm_label.place(y=1, x=15)
        time_label.place(y=100, x=35)
        snooze_button.place(y=190, x=10)
        close_button.place(y=190, x=200)

        alarm_ring_win.mainloop()
        pygame.mixer.Sound.stop(tone)

    def comparison(self, sys_hrs, sys_min, sys_ampn):
        if self.hours == sys_hrs and self.minutes == sys_min and self.ampm == sys_ampn and self.isActive:
            self.isActive = False
            self.ring_alarm(current_tone)
            self.sw_image = self.on_sw_image if self.isActive else self.off_sw_image

    def isOverSW(self, pos):
        if self.sw_x < pos[0] < self.sw_x + self.sw_image.get_width():
            if self.sw_y < pos[1] < self.sw_y + self.sw_image.get_height():
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


# fech alarm data for the beginning
pickle_in = open("data/alarm_data.pickle", "rb")
alarm_data = pickle.load(pickle_in)
pickle_in.close()

# Create alarm object and define data to them
alarm1 = alarm(alarm_data['alarm1'][0], alarm_data['alarm1'][1], alarm_data['alarm1'][2], alarm_data['alarm1'][3], 290)
alarm2 = alarm(alarm_data['alarm2'][0], alarm_data['alarm2'][1], alarm_data['alarm2'][2], alarm_data['alarm2'][3], 380)
alarm3 = alarm(alarm_data['alarm3'][0], alarm_data['alarm3'][1], alarm_data['alarm3'][2], alarm_data['alarm3'][3], 470)
alarm4 = alarm(alarm_data['alarm4'][0], alarm_data['alarm4'][1], alarm_data['alarm4'][2], alarm_data['alarm4'][3], 560)
alarm5 = alarm(alarm_data['alarm5'][0], alarm_data['alarm5'][1], alarm_data['alarm5'][2], alarm_data['alarm5'][3], 650)

alarm_list = [alarm1, alarm2, alarm3, alarm4, alarm5]   # list for alarm object


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
        if i.hours == 0 and i.minutes == 0 and i.ampm == 'AM':
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
        for i in range(len(alarm_list) - 1):
            alarm_list[i].hours = alarm_list[i + 1].hours
            alarm_list[i].minutes = alarm_list[i + 1].minutes
            alarm_list[i].ampm = alarm_list[i + 1].ampm

    elif alarm_name == 'alarm2':
        for i in range(1, len(alarm_list) - 1):
            alarm_list[i].hours = alarm_list[i + 1].hours
            alarm_list[i].minutes = alarm_list[i + 1].minutes
            alarm_list[i].ampm = alarm_list[i + 1].ampm

    elif alarm_name == 'alarm3':
        for i in range(2, len(alarm_list) - 1):
            alarm_list[i].hours = alarm_list[i + 1].hours
            alarm_list[i].minutes = alarm_list[i + 1].minutes
            alarm_list[i].ampm = alarm_list[i + 1].ampm

    elif alarm_name == 'alarm4':
        for i in range(3, len(alarm_list) - 1):
            alarm_list[i].hours = alarm_list[i + 1].hours
            alarm_list[i].minutes = alarm_list[i + 1].minutes
            alarm_list[i].ampm = alarm_list[i + 1].ampm

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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

c_world_time = {
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
c_formatted_world_time = {
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
c_location = 'IST'


def get_time():
    time = datetime.datetime.now()  # Get current time
    sys_time = time.hour * 60 + time.minute  # Convert current in hrs+min to min
    gmt_time = sys_time - (c_world_time['IST'][1] * 60)  # Converting the time to GMT time
    temp_converted_time = gmt_time + (
                (c_world_time[c_location][1]) * 60)  # Convert the GMT time to the selected time zone
    # The Converted time is stored in temporary variable because it can get more than 24 hrs and less than 0 hrs

    # here we fix the above issue
    if temp_converted_time < 0:
        converted_time = temp_converted_time + 24 * 60
    elif temp_converted_time > 24 * 60:
        converted_time = temp_converted_time - 24 * 60
    else:
        converted_time = temp_converted_time

    converted_time_hrs, converted_time_min, converted_time_sec = int(converted_time / 60), int(
        converted_time % 60), time.second
    return converted_time_hrs if converted_time_hrs <= 12 else converted_time_hrs - 12, converted_time_min, converted_time_sec, "AM" if converted_time_hrs < 12 else "PM"


def change_zone():
    root = tk.Tk()

    def change_timezone(timezone):
        global c_location
        c_location = timezone
        root.destroy()

    canvas = tk.Canvas(root, height=500, width=200)
    GMT = tk.Button(canvas, text=c_world_time['GMT'][0], font=('verdana', 10), command=lambda: change_timezone('GMT'))
    ECT = tk.Button(canvas, text=c_world_time['ECT'][0], font=('verdana', 10), command=lambda: change_timezone('ECT'))
    EET = tk.Button(canvas, text=c_world_time['EET'][0], font=('verdana', 10), command=lambda: change_timezone('EET'))
    ART = tk.Button(canvas, text=c_world_time['ART'][0], font=('verdana', 10), command=lambda: change_timezone('ART'))
    EAT = tk.Button(canvas, text=c_world_time['EAT'][0], font=('verdana', 10), command=lambda: change_timezone('EAT'))
    MET = tk.Button(canvas, text=c_world_time['MET'][0], font=('verdana', 10), command=lambda: change_timezone('MET'))
    NET = tk.Button(canvas, text=c_world_time['NET'][0], font=('verdana', 10), command=lambda: change_timezone('NET'))
    PLT = tk.Button(canvas, text=c_world_time['PLT'][0], font=('verdana', 10), command=lambda: change_timezone('PLT'))
    IST = tk.Button(canvas, text=c_world_time['IST'][0], font=('verdana', 10), command=lambda: change_timezone('IST'))
    BST = tk.Button(canvas, text=c_world_time['BST'][0], font=('verdana', 10), command=lambda: change_timezone('BST'))
    VST = tk.Button(canvas, text=c_world_time['VST'][0], font=('verdana', 10), command=lambda: change_timezone('VST'))
    CTT = tk.Button(canvas, text=c_world_time['CTT'][0], font=('verdana', 10), command=lambda: change_timezone('CTT'))
    JST = tk.Button(canvas, text=c_world_time['JST'][0], font=('verdana', 10), command=lambda: change_timezone('JST'))
    ACT = tk.Button(canvas, text=c_world_time['ACT'][0], font=('verdana', 10), command=lambda: change_timezone('ACT'))
    AET = tk.Button(canvas, text=c_world_time['AET'][0], font=('verdana', 10), command=lambda: change_timezone('AET'))
    SST = tk.Button(canvas, text=c_world_time['SST'][0], font=('verdana', 10), command=lambda: change_timezone('SST'))
    NST = tk.Button(canvas, text=c_world_time['NST'][0], font=('verdana', 10), command=lambda: change_timezone('NST'))
    MIT = tk.Button(canvas, text=c_world_time['MIT'][0], font=('verdana', 10), command=lambda: change_timezone('MIT'))
    HST = tk.Button(canvas, text=c_world_time['HST'][0], font=('verdana', 10), command=lambda: change_timezone('HST'))
    AST = tk.Button(canvas, text=c_world_time['AST'][0], font=('verdana', 10), command=lambda: change_timezone('AST'))
    PST = tk.Button(canvas, text=c_world_time['PST'][0], font=('verdana', 10), command=lambda: change_timezone('PST'))
    PNT = tk.Button(canvas, text=c_world_time['PNT'][0], font=('verdana', 10), command=lambda: change_timezone('PNT'))
    MST = tk.Button(canvas, text=c_world_time['MST'][0], font=('verdana', 10), command=lambda: change_timezone('MST'))
    CST = tk.Button(canvas, text=c_world_time['CST'][0], font=('verdana', 10), command=lambda: change_timezone('CST'))
    EST = tk.Button(canvas, text=c_world_time['EST'][0], font=('verdana', 10), command=lambda: change_timezone('EST'))
    IET = tk.Button(canvas, text=c_world_time['IET'][0], font=('verdana', 10), command=lambda: change_timezone('IET'))
    PRT = tk.Button(canvas, text=c_world_time['PRT'][0], font=('verdana', 10), command=lambda: change_timezone('PRT'))
    CNT = tk.Button(canvas, text=c_world_time['CNT'][0], font=('verdana', 10), command=lambda: change_timezone('CNT'))
    AGT = tk.Button(canvas, text=c_world_time['AGT'][0], font=('verdana', 10), command=lambda: change_timezone('AGT'))
    BET = tk.Button(canvas, text=c_world_time['BET'][0], font=('verdana', 10), command=lambda: change_timezone('BET'))
    CAT = tk.Button(canvas, text=c_world_time['CAT'][0], font=('verdana', 10), command=lambda: change_timezone('CAT'))

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


c_frame_img = pygame.image.load('images/frame.png')
c_frame_img.set_colorkey(bg)

c_center_img = pygame.image.load('images/center.png')
c_center_img.set_colorkey(bg)

c_min_hand_img = pygame.image.load('images/min.png').convert()
c_min_hand_img.set_colorkey(white)

c_hrs_hand_img = pygame.image.load('images/hr.png').convert()
c_hrs_hand_img.set_colorkey(white)

c_sec_hand_img = pygame.image.load('images/sec.png').convert()
c_sec_hand_img.set_colorkey(white)

c_zone_change_button = button((200, 200, 200), (0, 0, 0), ((width // 2) - 110), (height - 90), 250, 40,
                              ' Change Time Zone ')

c_zone_font = pygame.font.Font(verdana_font, 28)
c_zone_text = c_zone_font.render('', True, green, bg)
c_zone_textRect = c_zone_text.get_rect()
c_zone_textRect.center = ((width // 2) - 122, height - 145)

c_time_font = pygame.font.Font(ubuntu_font, 50)
c_time_text = c_time_font.render('', True, green, bg)
c_time_textRect = c_time_text.get_rect()
c_time_textRect.center = ((width // 2) - 130, height - 200)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

capture_button = button((200, 200, 200), (0, 0, 0), 30, 635, 150, 55, 'Capture ')
capture_button.font_size = 35

reset_button = button((200, 200, 200), (0, 0, 0), 230, 635, 150, 55, ' Reset ')
reset_button.font_size = 35

start_button = button((200, 200, 200), (0, 0, 0), 430, 635, 150, 55, ' Start ')
start_button.font_size = 35

state_button = button(bg, (200, 200, 200), 50, 595, 110, 35, ' ')
state_button.font_size = 30

clock_button = button(bg, (200, 200, 200), 5, 0, 70, 30, ' Clock ')
alarm_button = button(bg, (200, 200, 200), 93, 0, 70, 30, ' Alarm ')
stopwatch_button = button(bg, (200, 200, 200), 188, 0, 130, 30, ' Stop Watch ')
timer_button = button(bg, (200, 200, 200), 335, 0, 70, 30, ' Timer ')


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


cap1 = capture(1, 210, 0, 0, 0, 0, 0)
cap2 = capture(2, 210, 0, 0, 0, 0, 0)
cap3 = capture(3, 210, 0, 0, 0, 0, 0)
cap4 = capture(4, 210, 0, 0, 0, 0, 0)
cap5 = capture(5, 210, 0, 0, 0, 0, 0)
cap6 = capture(6, 210, 0, 0, 0, 0, 0)
cap7 = capture(7, 210, 0, 0, 0, 0, 0)
cap8 = capture(8, 210, 0, 0, 0, 0, 0)
cap9 = capture(9, 210, 0, 0, 0, 0, 0)
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
s_duration, s_milli, s_sec, s_min, s_hrs, s_cap_count, s_start_time, s_resttime, s_counter = 0, 0, 0, 0, 0, 0, 0, 0, 0
s_stopwatch_run, s_active_status, s_state, s_spl_lap = False, False, False, True
s_cap_list = [cap1, cap2, cap3, cap4, cap5, cap6, cap7, cap8, cap9, cap10, cap11, cap12, cap13, cap14, cap15, cap16,
              cap17, cap18, cap19, cap20, cap21, cap22, cap23, cap24, cap25, cap26, cap27, cap28, cap29, cap30]
s_position = [240, 290, 340, 390, 440, 490, 540]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def update():
    global s_hrs, s_min, s_milli, s_sec, s_duration, s_stopwatch_run, s_active_status, s_state, s_spl_lap, s_counter, s_cap_count, s_start_time, s_resttime, time

    time = datetime.datetime.now()
    sys_hrs, sys_min, ampm = time.hour if time.hour <= 12 else time.hour - 12, time.minute, 'AM' if time.hour < 12 else 'PM'

    for i in alarm_list:
        i.comparison(sys_hrs, sys_min, ampm)

    if s_stopwatch_run:
        time = datetime.datetime.now()
        s_timenow = time.hour * 3600000000 + time.minute * 60000000 + time.second * 1000000 + time.microsecond
        s_duration = s_timenow - s_start_time
        s_milli = (((s_duration % 3600000000) % 60000000) % 1000000) // 10000
        s_sec = ((s_duration % 3600000000) % 60000000) // 1000000
        s_min = (s_duration % 3600000000) // 60000000
        if s_min == 60:
            s_state = True
        s_hrs = s_duration // 3600000000
    elif not s_active_status:
        pass
    else:
        time = datetime.datetime.now()
        s_timenow = time.hour * 3600000000 + time.minute * 60000000 + time.second * 1000000 + time.microsecond
        s_resttime = s_timenow - s_start_time - s_duration

    clock_button.draw(window, bg)
    alarm_button.draw(window, bg)
    stopwatch_button.draw(window, bg)
    timer_button.draw(window, bg)

def alarm_window():
    pygame.display.set_caption('Alarm')
    while True:
        alarm_button.text_color = (151, 147, 245)
        window.fill(bg)
        update()

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

                if clock_button.isOver(pos):
                    clock_window()
                if stopwatch_button.isOver(pos):
                    stopwatch_window()
                if timer_button.isOver(pos):
                    timer_window()

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


def clock_window():
    pygame.display.set_caption('Clock')  # Title of the window
    run = True
    while run:
        window.fill(bg)
        clock_button.text_color = (151, 147, 245)
        update()
        hrs_val, min_val, sec_val, after = get_time()

        window.blit(c_frame_img, (width // 2 - c_frame_img.get_width() // 2, 250 - c_frame_img.get_height() // 2))

        hrs_img_cpy = pygame.transform.rotate(c_hrs_hand_img, -((hrs_val * 30) + (min_val / 2)))
        window.blit(hrs_img_cpy, (width // 2 - hrs_img_cpy.get_width() // 2, 250 - hrs_img_cpy.get_height() // 2))

        min_img_cpy = pygame.transform.rotate(c_min_hand_img, -min_val * 6)
        window.blit(min_img_cpy, (width // 2 - min_img_cpy.get_width() // 2, 250 - min_img_cpy.get_height() // 2))

        sec_img_cpy = pygame.transform.rotate(c_sec_hand_img, -sec_val * 6)
        window.blit(sec_img_cpy, (width // 2 - sec_img_cpy.get_width() // 2, 250 - sec_img_cpy.get_height() // 2))

        window.blit(c_center_img, (width // 2 - c_center_img.get_width() // 2, 250 - c_center_img.get_height() // 2))

        c_zone_change_button.draw(window, bg)

        zone_str = c_zone_font.render(c_formatted_world_time[c_location], True, line, bg)
        window.blit(zone_str, c_zone_textRect)

        time_str = c_time_font.render("%02d:%02d:%02d %s" % (hrs_val, min_val, sec_val, after), True, line, bg)
        window.blit(time_str, c_time_textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if c_zone_change_button.isOver(pos):
                    change_zone()
                if alarm_button.isOver(pos):
                    alarm_window()
                if stopwatch_button.isOver(pos):
                    stopwatch_window()
                if timer_button.isOver(pos):
                    timer_window()

            if event.type == pygame.MOUSEMOTION:
                if c_zone_change_button.isOver(pos):
                    c_zone_change_button.color = (151, 147, 245)
                else:
                    c_zone_change_button.color = (200, 200, 200)

                if alarm_button.isOver(pos):
                    alarm_button.text_color = (151, 147, 245)
                else:
                    alarm_button.text_color = (200, 200, 200)

                if stopwatch_button.isOver(pos):
                    stopwatch_button.text_color = (151, 147, 245)
                else:
                    stopwatch_button.text_color = (200, 200, 200)

                if timer_button.isOver(pos):
                    timer_button.text_color = (151, 147, 245)
                else:
                    timer_button.text_color = (200, 200, 200)

        pygame.display.flip()


def stopwatch_window():
    pygame.display.set_caption('Stop Watch')
    global s_hrs, s_min, s_milli, s_sec, s_duration, s_stopwatch_run, s_active_status, s_state, s_spl_lap, s_counter

    def capture():
        global s_cap_count, s_hrs, s_min, s_milli, s_sec, s_duration, s_counter, time, s_start_time
        if s_stopwatch_run and s_cap_count < 30:
            s_cap_list[s_cap_count].sn_text = s_cap_list[s_cap_count].font3.render("%02d)" % s_cap_list[s_cap_count].sn,
                                                                                   True, line, bg)
            s_cap_list[s_cap_count].hrs_text = s_cap_list[s_cap_count].font0.render("%02d" % s_hrs, True, line, bg)
            s_cap_list[s_cap_count].min_text = s_cap_list[s_cap_count].font0.render("%02d" % s_min, True, line, bg)
            s_cap_list[s_cap_count].sec_text = s_cap_list[s_cap_count].font0.render("%02d" % s_sec, True, line, bg)
            s_cap_list[s_cap_count].milli_text = s_cap_list[s_cap_count].font0.render("%02d" % s_milli, True, line, bg)
            s_cap_count += 1
            if s_cap_count > 7:
                s_counter = s_cap_count - 7
            else:
                s_counter = 0
            if not s_spl_lap:
                s_duration, s_sec, s_min, s_milli, s_hrs = 0, 0, 0, 0, 0
                time = datetime.datetime.now()
                s_start_time = time.hour * 3600000000 + time.minute * 60000000 + time.second * 1000000 + time.microsecond

    def s_reset():
        global s_hrs, s_min, s_milli, s_sec, s_duration, s_stopwatch_run, s_active_status, s_state, s_cap_count, s_counter, s_resttime, s_start_time
        s_duration, s_sec, s_min, s_milli, s_hrs, s_cap_count, s_counter, s_resttime, s_start_time = 0, 0, 0, 0, 0, 0, 0, 0, 0
        s_stopwatch_run, s_active_status, s_state = False, False, False
        for i in s_cap_list:
            i.sn_text = i.font3.render("%02d)" % i.sn, True, line, bg)
            i.hrs_text = i.font0.render("%02d" % s_hrs, True, line, bg)
            i.min_text = i.font0.render("%02d" % s_min, True, line, bg)
            i.sec_text = i.font0.render("%02d" % s_sec, True, line, bg)
            i.milli_text = i.font0.render("%02d" % s_milli, True, line, bg)

    while s_run:
        global s_cap_count, s_start_time, s_resttime
        pos_counter = 0
        window.fill(bg)
        stopwatch_button.text_color = (151, 147, 245)
        time = datetime.datetime.now()
        sys_hrs, sys_min, ampm = time.hour if time.hour <= 12 else time.hour - 12, time.minute, 'AM' if time.hour < 12 else 'PM'
        clock_button.draw(window, bg)
        alarm_button.draw(window, bg)
        stopwatch_button.draw(window, bg)
        timer_button.draw(window, bg)

        for i in alarm_list:
            i.comparison(sys_hrs, sys_min, ampm)
        if s_stopwatch_run:
            time = datetime.datetime.now()
            s_timenow = time.hour * 3600000000 + time.minute * 60000000 + time.second * 1000000 + time.microsecond
            s_duration = s_timenow - s_start_time
            s_milli = (((s_duration % 3600000000) % 60000000) % 1000000) // 10000
            s_sec = ((s_duration % 3600000000) % 60000000) // 1000000
            s_min = (s_duration % 3600000000) // 60000000
            if s_min == 60:
                s_state = True
            s_hrs = s_duration // 3600000000
            start_button.text = ' Pause '
        elif not s_active_status:
            start_button.text = ' Start '
        else:
            time = datetime.datetime.now()
            s_timenow = time.hour * 3600000000 + time.minute * 60000000 + time.second * 1000000 + time.microsecond
            s_resttime = s_timenow - s_start_time - s_duration
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
                s_cap_list[i].recenter(s_position[pos_counter])
                s_cap_list[i].build()
                pos_counter += 1
        else:
            for i in range(s_cap_count):
                s_cap_list[i].recenter(s_position[i])
                s_cap_list[i].build()

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
                    time = datetime.datetime.now()
                    if not s_active_status:
                        s_start_time = time.hour * 3600000000 + time.minute * 60000000 + time.second * 1000000 + time.microsecond
                    s_start_time += s_resttime
                    s_stopwatch_run = not s_stopwatch_run
                    s_active_status = True
                    s_resttime = 0

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

                if clock_button.isOver(pos):
                    clock_window()
                if alarm_button.isOver(pos):
                    alarm_window()
                if timer_button.isOver(pos):
                    timer_window()

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


def timer_window():
    pygame.display.set_caption('Timer')  # Title of the window
    run = True
    while run:
        window.fill(bg)
        timer_button.text_color = (151, 147, 245)
        update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if clock_button.isOver(pos):
                    clock_window()
                if alarm_button.isOver(pos):
                    alarm_window()
                if stopwatch_button.isOver(pos):
                    stopwatch_window()

            if event.type == pygame.MOUSEMOTION:
                if clock_button.isOver(pos):
                    clock_button.text_color = (151, 147, 245)
                else:
                    clock_button.text_color = (200, 200, 200)

                if alarm_button.isOver(pos):
                    alarm_button.text_color = (151, 147, 245)
                else:
                    alarm_button.text_color = (200, 200, 200)

                if stopwatch_button.isOver(pos):
                    stopwatch_button.text_color = (151, 147, 245)
                else:
                    stopwatch_button.text_color = (200, 200, 200)

        pygame.display.update()


clock_window()
