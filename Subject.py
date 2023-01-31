

class Subject:
    teacher_id = 0
    discipline_id = 0
    type = ""
    name = ""
    place = ""
    groups = []
    day = 0
    pair = 0
    week = True

    def __init__(self, teacher, information, position, week):
        self.teacher_id = teacher
        self.week = (week % 2 != 0)
        self.day = position[0]
        self.pair = position[1]
        self.place = information[4]
        tmp = information[2][:3].lower()
        if tmp == 'лек' or tmp == 'лаб':
            self.type = tmp
            self.name = information[2][3:].lower()
        else:
            self.type = 'пр'
            self.name = information[2][2:].lower()
        self.groups = []
        information[0] = information[0].replace(", ",",")
        for i in information[0].split(","):
            self.groups.append(i)



    def __str__(self):
        return f"{self.week} {self.day} {self.pair}|{self.groups}|{self.type}. {self.name}|{self.place}|{self.teacher_id}"
