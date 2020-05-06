import json
import datetime
import os.path
from datetime import datetime, date, timedelta
import math
import random

class TimeConverter():

    def compare_times(self, hour1=0, minute1=0, hour2=0, minute2=0):
        time1 = int(hour1) * 60 + int(minute1)
        time2 = int(hour2) * 60 + int(minute2)
        return time1 > time2


class BotFunctions():
    # Variables
    tc = TimeConverter()
    after_10_15 = tc.compare_times(hour1=datetime.now(
    ).hour, hour2=22, minute1=datetime.now().minute, minute2=15)

    bossy_bdo = None
    days_of_the_week = ["Monday", "Tuesday",
                        "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.today().weekday()

    # Read json file upon init
    def __init__(self):
        with open("bosses.json", "r") as bossy:
            self.bossy_bdo = json.load(bossy)

        self.filename = "notepad.json"
        self.if_file_exists()
        with open(self.filename, "r", encoding="utf8") as opened_messages:
            self.decoded_messages = json.load(opened_messages)
        self.key = ""
        self.value = ""
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.after_10_15 = TimeConverter().compare_times(hour1=datetime.now().hour,
                                                       hour2=22,
                                                       minute1=datetime.now().minute,
                                                       minute2=15)
        self.no_boss_within_5_hours = self.compare_time(self.todays_next_boss()[1]) > 300 #default False

    def compare_time(self, time_1):
        """
        Różnica czasu w minutach między time1 a time2
        :param time1: czas bossa z bosses.json
        :param time2: aktualny czas z self.actual_time
        :return:
        """
        time_1 = time_1
        if time_1 == 0:
            time_1 = "00:00"
        time_1 = datetime.strptime(time_1, "%H:%M")
        time_2 = datetime.strptime(self.actual_date()[1], "%H:%M")
        new_time = time_1 - time_2

        return new_time.seconds/60

    def message_show(self, *args):
        arguments = list(args[0])
        keys = self.decoded_messages["notepad"].keys()
        if len(arguments) < 2:
            return f"```Wpisz nazwę wiadomości```"
        else:
            key = arguments[1]
        if key not in keys:
            return "```Brak takiej wiadomosci```"
            pass
        else:
            key = arguments[1]
            return f"```{self.decoded_messages['notepad'][key]}```"

    def message_send(self, *args):
        arguments = list(args[0])
        keys = self.decoded_messages["notepad"].keys()
        if len(arguments) < 2:
            return f"```Wpisz nazwę wiadomości```"
        else:
            key = arguments[1]
        if key not in keys:
            return "```Brak takiej wiadomosci```"
            pass
        else:
            key = arguments[1]
            return self.decoded_messages["notepad"][key]

    def message_list(self, *args):
        arguments = list(args[0])
        keys = self.decoded_messages["notepad"].keys()
        answer = ""
        for x in keys:
            if x == "key" or x == "value":
                continue
            else:
                answer += x + ' | '
        return f"Istniejące wiadomości: ```{answer}```"

    def message_del(self, *args):
        arguments = list(args[0])
        if len(arguments) < 2:
            keys = self.decoded_messages["notepad"].keys()
            answer = ""
            for x in keys:
                if x == "key" or x == "value":
                    continue
                else:
                    answer += x + ' | '
            return f"```Wpisz nazwę wiadomości, którą chcesz usunąć\n\n{answer}```"
        else:
            key = arguments[1]
            data = self.decoded_messages
            for element in data["notepad"].copy():
                if key not in data["notepad"].copy():
                    return f"```Brak {key} na liście wiadomości```"
                else:
                    if key == element:
                        del data["notepad"][key]
                with open(self.filename, 'w', encoding="utf8") as file:
                    file = json.dump(data, file)
            return f"```Usunięto wiadomość: {key}```"

    def message_add(self, *args):
        arguments = list(args[0])
        if len(arguments) < 2:
            return "```Wpisz tytuł wiadomości```"
        elif len(arguments) < 3:
            return "```Wpisz wiadomość```"
        else:
            key = arguments[1]
            value = arguments[2]
            self.decoded_messages["notepad"][key] = value
            with open(self.filename, 'w', encoding="utf8") as modified_messages:
                json.dump(self.decoded_messages, modified_messages, ensure_ascii=False)
            return f"Zapisano wiadomość ```{key}``` ```{value}```"

    def actual_date(self):
        """
        self.actual_time()[i]
        next_day_name = messages.days[int(messages.actual_date()[2])+1]
        0 - day_name
        1 - hour_minutes
        2 - day_index
        3 - hour_minutes_seconds
        :return: tuple
        """
        date_time = datetime.now()

        day = date_time.strftime("%A")
        hour = date_time.strftime("%H:%M")
        hour_minutes_seconds = date_time.strftime("%H:%M:%S")
        day_index = date_time.weekday()
        return (day, hour, day_index, hour_minutes_seconds)

    def roles(self):
        roles = ["Turysta", "Dzika Kocica", "Dziki Programista", "Pepega"]
        return roles

    def if_file_exists(self):
        keys = "{\"key\" : \"value\"}"
        if os.path.exists(self.filename):
            pass #print(f"Plik {self.filename} istnieje")
        else:
            try:
                print(f"Plik {self.filename} nie istnieje. Tworzę nowy.")
                with open("notepad.json", 'w') as f:
                    f.write(keys)
            except FileNotFoundError:
                print(f"Nie można utworzyć pliku {self.filename}")

    def next_boss(self):
        if not self.after_10_15:
            if not self.no_boss_within_5_hours:
                return [self.todays_next_boss()[0], self.todays_next_boss()[1]]
            else:
                return [self.first_boss_tomorrow()[0], self.first_boss_tomorrow()[1]]

    def todays_next_boss(self):
        """
        Funkcja zwraca dzisiejszego następnego bossa
        :return:
        0 - wiadomosc
        1 - czas bossa
        """
        next_boss = ""
        todays_day = self.actual_date()[0]
        todays_bosses = self.bossy_bdo["bosses"]["days"][todays_day]
        for i in range(len(todays_bosses)):
            time = todays_bosses[i][1].split(":")
            next_boss = todays_bosses[i][0]
            next_boss_time = 0

            if (TimeConverter().compare_times(hour1=time[0],
                                              hour2=datetime.now().hour,
                                              minute1=int(time[1]) + 5,
                                              minute2=datetime.now().minute)):
                next_boss = todays_bosses[i][0]
                next_boss_time = todays_bosses[i][1]
                break

        return [f"\nAktualna godzina: {self.actual_date()[1]}, Dzień: {self.actual_date()[0]}\n" \
                f"\n**Nastepny boss:**\n\n{next_boss} - {time[0]}:{time[1]}", next_boss_time]

    def first_boss_tomorrow(self):
        """
        Funkcja zwraca pierwszego jutrzejszego bossa
        :return:
        0 - boss_name
        1 - boss_time
        """
        next_day_index = self.actual_date()[2] + 1
        next_day_name = self.days[next_day_index]
        next = self.bossy_bdo["bosses"]["days"][next_day_name][0][0]
        time = self.bossy_bdo["bosses"]["days"][next_day_name][0][1]

        return [f"\nAktualna godzina: {self.actual_date()[1]}, Dzień: {next_day_name}\n\n**Nastepny boss:**\n\n{next} - {time}", time]

    def all_todays_bosses(self):
        """
        time_change == [0 - normal bosses, 1 - 1 hour faster, 2 - 1 hour slower
        :return:
        """
        time_change = 0
        next_boss_index = self.todays_next_index()
        bosses = f"\n**Dzisiejsze bossy:** \nAktualna godzina: {self.actual_date()[1]}\n\n"
        todays_day = self.days_of_the_week[int(datetime.now().weekday())]
        todays_bosses = self.bossy_bdo["bosses"]["days"][todays_day]
        for i in range((len(todays_bosses))):
            if (i == next_boss_index):
                bosses += f"**{todays_bosses[i][0]}: {todays_bosses[i][1]} - nastepny/obecny boss\n**"
            else:
                bosses += f"{todays_bosses[i][0]}: {todays_bosses[i][1]}\n"
        if time_change == 0:
            return bosses
        elif time_change == 1:
            return bosses + "\nUWAGA. Aktualnie zmieniono czas z letniego na zimowy.\nDo środy, bossy respią się godzinę szybciej, niż jest to pokazane wyżej."
        else:
            return bosses + "\nUWAGA. Aktualnie zmieniono czas z zimowego na letni.\nDo środy, bossy respią się godzinę później, niż jest to pokazane wyżej."

    def todays_next_index(self):
        index = None
        if (not self.after_10_15):
            todays_day = self.days_of_the_week[int(datetime.now().weekday())]
            todays_bosses = self.bossy_bdo["bosses"]["days"][todays_day]

            for i in range(len(todays_bosses)):
                time = todays_bosses[i][1].split(":")
                if (self.tc.compare_times(hour1=time[0], hour2=datetime.now().hour, minute1=int(time[1]) + 10,
                                          minute2=datetime.now().minute)):
                    index = i
                    break
        return index

    def all_tomorrows_bosses(self):
        next_boss_index = self.todays_next_index()
        bosses = "\n**Jutrzejsze bossy:** \n\n"
        if (datetime.now().weekday() == 6):
            tomorrow = self.days_of_the_week[0]
        else:
            tomorrow = self.days_of_the_week[int(
                datetime.now().weekday()) + 1]

        tomorrows_bosses = self.bossy_bdo["bosses"]["days"][tomorrow]
        for i in range((len(tomorrows_bosses))):
            bosses += f"{tomorrows_bosses[i][0]}: {tomorrows_bosses[i][1]}\n"

        return bosses

    def reset_nick(self, nickname):
        new_nick = ""
        pt_list = ['[PT 1] ', '[PT 2] ', '[PT 3] ']
        try:
            for pt in pt_list:
                if pt in nickname:
                    new_nick = nickname[7:]
                elif pt not in nickname:
                    continue
                else:
                    new_nick = nickname
            return new_nick
        except UnboundLocalError:
            return nickname

    def add_party(self, nick, party):
        party_dict = {1: '[PT 1] ', 2: '[PT 2] ', 3: '[PT 3] '}
        nick = self.reset_nick(nick)
        nick = party_dict[party] + nick
        return str(nick)

    @staticmethod
    def help():

        help_list = """```
.b - pokazuje bossy na dziś, wraz z aktualnym\n 
.jutro - pokazuje bossy na jutro\n
.next - pokazuje następnego bossa\n
------------------\n
.pt1 - party 1\n
.pt2 - party 2\n
.pt3 - party 3\n
.reset - reset party
------------------\n
.discord - zaproszenie na discorda\n
------------------\n
.msg - lista wiadomości
-----------------\n
.clear - usuwa wiadomości
```
        """
        return help_list



    def klik(self, *args):
        arguments = list(args[0])
        fs = arguments[0]
        numbers = []
        for _ in range(int(fs)):
            nr = random.choice(range(1,101))
            while nr in numbers:
                nr = random.choice(range(1,101))
            numbers.append(nr)
            numbers.sort()
        wylosowana_liczba = random.choice(range(1,101))
        if wylosowana_liczba in numbers:
            #print("TRUE", numbers, wylosowana_liczba)
            return [True, fs, numbers, wylosowana_liczba]
        else:
            #print("FALSE", numbers, wylosowana_liczba)
            return [False, fs, numbers, wylosowana_liczba]

    def rozsypanka(self, *args):
        try:
            with open('rozsypanka.json', "r", encoding="utf8") as rozsypanka:
                self.json = json.load(rozsypanka)
        except FileNotFoundError:
            print("File not found")

        if not args:
            answer = []
            odp = ""
            for x in self.json['rozsypanka']['slowo']:
                answer.append(x)
                random.shuffle(answer)
            for x in answer:
                odp += x
            return odp

        try:
            arguments = args[0]
            if arguments[0] == "show":
                slowo = self.json['rozsypanka']['slowo']
                return slowo

            elif arguments[0] == "add":
                value = arguments[1]
                self.json['rozsypanka']['slowo'] = value
                with open('rozsypanka.json', 'w', encoding="utf8") as rozsypanka:
                    json.dump(self.json, rozsypanka, ensure_ascii=False)
                return f"```Dodano nowe słowo```"

            else:
                odp = arguments[0]
                slowo = self.json['rozsypanka']['slowo']
                if odp == slowo.lower():
                    return "```Prawidłowa odpowiedź :)```"
                else:
                    return "```Błędna odpowiedź :)```"

        except IndexError:
            pass

    def calc(self, *args):
        arguments = list(args[0])

        if len(arguments) == 1:
            return "Musisz podać 2 argumenty. Np. .calc 652 mln | .calc 1.5 b"
        elif len(arguments) == 2:
            value = arguments[0]
            multiply = arguments[1]
            try:
                if multiply == "mln":
                    mln = int(value) * 1000000
                    odp = (0.845) * int(mln)
                    odp = "%.0f" % odp
                    odp = int(odp) / 1000000

                    odp2 = (0.650) * int(mln)
                    odp2 = "%.0f" % odp2
                    odp2 = int(odp2) / 1000000
                    return [odp, odp2, value, multiply]
                elif multiply == "b":
                    b = float(value) * 1000000000
                    odp = (0.845) * float(b)
                    odp = "%.0f" % odp
                    odp = int(odp) / 1000000000

                    odp2 = (0.650) * float(b)
                    odp2 = "%.0f" % odp2
                    odp2 = int(odp2) / 1000000000
                    return [odp, odp2, value, multiply]
            except Exception as e:
                print(e)
        else:
            return "Błąd"