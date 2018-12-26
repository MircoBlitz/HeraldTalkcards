import json, urllib.request, dateutil.parser, datetime

class Cards:
    # Initializer / Instance Attributes
    def __init__(self):
        self.halfnarp = "https://erdgeist.org/35C3/halfnarp/talks_35C3.json"
        self.chaoswest = "https://fahrplan.chaos-west.de/35c3chaoswest/schedule/export/schedule.json"
        with urllib.request.urlopen(self.halfnarp) as halfnarp_json:
            self.halfnarpdata = json.loads(halfnarp_json.read().decode())
        with urllib.request.urlopen(self.chaoswest) as chaoswest_json:
            self.chaoswestdata = json.loads(chaoswest_json.read().decode())
        self.days = {
            "27" : "1",
            "28" : "2",
            "29" : "3",
            "30" : "4",
        }
        self.data = {}
        self.parse_halfnarp()
        self.parse_chaoswest()

    def parse_halfnarp(self):
        for element in self.halfnarpdata:
            start_time = dateutil.parser.parse(element["start_time"])
            duration = element["duration"] / 60
            end_time = start_time + datetime.timedelta(minutes = duration)
            day = self.days[start_time.strftime("%d")]
            block = self.get_block_id_halfnarp(start_time, element["room_name"][0])
            blockID = block["room"] + block["day"] + "." + block["block"]
            data = {
                blockID: {
                    "day": day,
                    "start": start_time.strftime("%H:%M"),
                    "end": end_time.strftime("%H:%M"),
                    "duration": str(duration) + "m",
                    "block": block,
                    "speaker": element["speaker_names"],
                    "room": element["room_name"],
                    "track": element["track_name"],
                    "language": element["language"],
                    "title": element["title"],
                    "abstract": element["abstract"],             
                }
            }
            self.data.update(data)

    def get_block_id_halfnarp(self, date, room):
        blocks = { 1: "00:10:00", 
                   2: "00:30:00", 
                   3: "00:40:00", 
                   4: "01:10:00", 
                   5: "11:00:00", 
                   6: "11:30:00", 
                   7: "12:30:00", 
                   8: "12:50:00", 
                   9: "13:30:00", 
                   10: "14:10:00", 
                   11: "14:30:00", 
                   12: "16:10:00", 
                   13: "17:10:00", 
                   14: "17:30:00", 
                   15: "18:10:00", 
                   16: "18:30:00", 
                   17: "18:50:00", 
                   18: "19:10:00", 
                   19: "20:50:00", 
                   20: "21:50:00", 
                   21: "22:10:00", 
                   22: "22:50:00", 
                   23: "23:10:00", 
                   24: "23:30:00", 
                   25: "23:50:00"
        }
        blocktranslate = { 1: "night1", 
                           2: "night1", 
                           3: "night2", 
                           4: "night2", 
                           5: "opening", 
                           6: "1.1", 
                           7: "1.2", 
                           8: "1.2", 
                           9: "1.3", 
                           10: "1.3", 
                           11: "1.4", 
                           12: "2.1", 
                           13: "2.2", 
                           14: "2.2", 
                           15: "2.3", 
                           16: "2.3", 
                           17: "2.3", 
                           18: "2.4", 
                           19: "3.1", 
                           20: "3.2", 
                           21: "3.2", 
                           22: "3.3", 
                           23: "3.3", 
                           24: "3.3", 
                           25: "3.4"
        }
        for key, value in blocks.items():
            if date.strftime("%H:%M:%S") == value:
                if key < 4:
                    block = "3"
                elif key < 12:
                    block = "1"
                elif key < 19:
                    block = "2"
                else:
                    block = "3"
                if key < 5:
                    differdate = date - datetime.timedelta(days=1)
                    day = self.days[differdate.strftime("%d")]
                else:
                    day = self.days[date.strftime("%d")]
                ret = { 
                    "day": day,
                    "room" : room,
                    "block" : blocktranslate[key]
                }
                return ret


    def parse_chaoswest(self):
        old_day = 0
        old_block = 0
        subversion = 0
        for element in self.chaoswestdata["schedule"]["conference"]["days"]:
            for talk in element["rooms"]["Chaos West Bühne"]:
                start_time = dateutil.parser.parse(talk["date"])
                start_h = start_time.strftime("%H")
                if start_h != "00" and start_h != "02":
                    day = self.days[start_time.strftime("%d")]
                    if old_day != day:
                        subversion = 0
                        old_block = 0
                        old_day = day
                    if int(start_h) >= 10 and int(start_h) <16:
                        blk = 1
                    elif int(start_h) >= 16 and int(start_h) < 20:
                        blk = 2
                    else: 
                        blk = 3

                    if old_block != blk:
                        old_block = blk
                        subversion = 1
                    else:
                        subversion += 1
                    duration = talk["duration"].split(":")[1]
                    end_time = start_time + datetime.timedelta(minutes = int(duration))
                    block = {"day": day, "room": "CW", "block": str(blk) + "." + str(subversion) }
                    blockID = block["room"] + block["day"] + "." + block["block"]
                    speaker = ""
                    for persons in talk["persons"]:
                        if len(speaker) > 1:
                            speaker = speaker + " / "
                        speaker = speaker + persons["name"]                    
                    data = {
                        blockID: {
                            "day": day,
                            "start": start_time.strftime("%H:%M:%S"),
                            "end": end_time.strftime("%H:%M:%S"),
                            "duration": str(duration) + "m",
                            "block": block,
                            "speaker": speaker,
                            "room": talk["room"],
                            "track": "",
                            "language": talk["language"],
                            "title": talk["title"],
                            "abstract": talk["abstract"],             
                        }
                    }
                    self.data.update(data)

    def get_data(self):
        return self.data

    def search_data(self, what, value):
        out = {}
        for key in self.data:
            if what == "room":
                if self.data[key]["block"]["room"] == str(value):
                    out.update({key: self.data[key]})
            elif what == "day":
                if self.data[key]["day"] == str(value):
                    out.update({key: self.data[key]})
            elif isinstance(what, list):
                if (self.data[key]["block"]["room"] == str(value[0])) and (self.data[key]["day"] == str(value[1])):
                    out.update({key: self.data[key]})
        return out
