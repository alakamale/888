import datetime, pytz
import re
from slugify import slugify

from src.models.events import Events
from src.models.selection import Selection
from src.models.sports import Sports


class CoreOps:
    def __init__(self):
        pass

    @staticmethod
    def verify_input(expected, actual):
        if any(x.lower() == actual.lower() for x in expected):
            return True
        return False

    @staticmethod
    def validate_datetime(date_n_time):
        timeformat = "%Y-%m-%d %H:%M"
        try:
            validtime = datetime.datetime.strptime(date_n_time, timeformat)
            return True
        except ValueError:
            print("ERROR : Invalid Date time format. Enter date an time YYYY-MM-DD Hour:Minute ")

    @staticmethod
    def get_sport_data():
        Sports.name = input("\tEnter Sport name: ").title()
        Sports.slug = slugify(Sports.name)
        Sports.active = True
        return Sports.name, Sports.slug, Sports.active

    @staticmethod
    def get_event_data():
        Events.name = input("\tEnter Event name : ")
        Events.slug = slugify(Events.name)
        Events.active = True

        while True:
            Events.event_type = input("\tEnter Event type(Preplay, Inplay) : ")
            if not CoreOps.verify_input(["preplay", "inplay"], Events.event_type):
                print("ERROR: Sorry, Incorrect response.")
                continue
            else:
                break

        while True:
            Events.status = input("\tEnter Event status(Pending, Started, Ended or Cancelled) : ")
            if not CoreOps.verify_input(["Pending", "Started", "Ended", "Cancelled"], Events.status):
                print("ERROR : Sorry, Incorrect response.")
                continue
            else:
                break

        while True:
            date_n_time = input("\tEnter date and time in YYYY-MM-DD Hour:Minute format : ")
            if CoreOps.validate_datetime(date_n_time):
                year, month, day, hour, min = re.split('-| |:', date_n_time)
                Events.scheduled_Start = "{}-{}-{} {}:{}".format(year, month, day, hour, min)
                break
            else:
                print("ERROR : Sorry, Incorrect response.")
                continue

        if Events.status == "Started":
            fmt = "%Y-%m-%d %H:%M"
            Events.actual_Start = datetime.datetime.now(pytz.timezone('UTC')).strftime(fmt)
        else:
            Events.actual_Start = "0000-00-00 00:00"

        return Events.name, Events.slug, Events.active, Events.event_type, Events.status, Events.scheduled_Start, Events.actual_Start

    @staticmethod
    def get_selection_data(event_name):
        Selection.Name = input("\tEnter Selection name : ")
        Selection.event_Name = event_name

        while True:
            try:
                Selection.price = float(input("\tEnter ticket price : "))
                break
            except ValueError:
                print("ERROR : Sorry, Incorrect response.")
                continue

        Selection.active = True
        while True:
            Selection.outcome = input("\tEnter Selection outcome(Unsettled, Void, Lose or Win) : ")
            if not CoreOps.verify_input(["Unsettled", "Void", "Lose", "Win"], Selection.outcome):
                print("ERROR : Sorry, Incorrect response.")
                continue
            else:
                break
        return Selection.Name, Selection.event_Name, Selection.price, Selection.active, Selection.outcome

    @staticmethod
    def name_selection(id_lst):
        tup_to_lst = [item for t in id_lst for item in t]
        unq_lst = list(dict.fromkeys(tup_to_lst))
        for count, item in enumerate(unq_lst, 1):
            print("{}. {}".format(count, item))

        while True:
            try:
                ch = int(input("\tSelect # from menu: "))
                id_name = (unq_lst[ch - 1])
                break
            except ValueError:
                print("ERROR : Sorry, Incorrect response.")
                continue
            except IndexError:
                print("ERROR : Sorry, Incorrect response.")
                continue
        return id_name

    @staticmethod
    def select_feild_to_update(table_name, header_lst, data_lst):
        table_dict = {}
        tup_to_lst = [item for t in data_lst for item in t]
        unq_lst = list(dict.fromkeys(tup_to_lst))
        table_dict = dict(zip(header_lst[1:], unq_lst[1:]))

        print("-" * 11)
        print("Update Menu")
        print("-" * 11)
        while True:
            try:
                for count, key, value in zip(range(0, len(header_lst[1:])), header_lst[1:], unq_lst[1:]):
                    print("{}. {} -> {}".format(count + 1, key, value))
                key_index = int(input("\tSelect # from menu to update: "))

                if header_lst[key_index] in table_dict.keys():
                    table_dict[header_lst[key_index]] = input("\tEnter new value for {} : ".format(header_lst[key_index]))
                    if input('# Do you want to continue updating?  ') == 'y':
                        continue
                    else:
                        return table_dict
                else:
                    print("ERROR : Sorry, Incorrect response.")
                    continue
            except ValueError:
                print("ERROR : Sorry, Incorrect response.")
                continue
            except IndexError:
                print("ERROR : Sorry, Incorrect response.")
                continue
