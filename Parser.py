def CreateTimetableTemplate():
    Timetable = [["" for i in range(9)] for j in range(8)]
    Timetable[0] = ["", "1 пара", "2 пара", "3 пара", "4 пара", "5 пара", "6 пара", "7 пара", "8 пара"]
    days = ["", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    for i in range(0, 7):
        Timetable[i][0] = days[i]
    return Timetable
def GetTecherName(text):
    name = text.find("</FONT><FONT FACE=\"Times New Roman\" SIZE=6 COLOR=\"#ff00ff\">") + \
           len("</FONT><FONT FACE=\"Times New Roman\" SIZE=6 COLOR=\"#ff00ff\">") + 1
    name = text[name:text.find("<BR> Неделя")]
    return name
def GetTextFromRow(ln):
    return ln[ln.find("<P ALIGN=\"CENTER\">") + 18:ln.find("</FONT>")].replace("</TD>", ""). \
        replace("</br>", "").replace("</B></I>", "")
def CreateHTML(Timetable):
    text = "<HTML>\n"
    text += "<TABLE BORDER CELLSPACING=3 BORDERCOLOR=\"#000000\" CELLPADDING=2 WIDTH=801>\n"
    for i in range(len(Timetable)):
        text += "<TR>"
        for j in range(len(Timetable[i])):
            text += "<TD WIDTH=\"11%\" VALIGN=\"TOP\" HEIGHT=28>\n"
            text += "<P ALIGN=\"CENTER\"><FONT FACE=\"Arial\">"
            if (Timetable[i][j] == ""):
                Timetable[i][j] = "-"
            text += Timetable[i][j]
            text += "</FONT>"
            text += "</TD>"
        text += "</TR>"
    text += "</TABLE>\n"
    text += "</HTML>"
    return text

def Operate(fileName,group,week=1):
    Timetable = CreateTimetableTemplate();
    for i in range(1,574):
        try:
            with open("Data\\"+str(i)+".html") as f:
                t = f.read()
                r = 0
                c = 0
                name =GetTecherName(t)
                table = ""
                if(week==1):
                    table = t[t.find("<TABLE"):t.find("</TABLE>")]
                else:
                    table = t[t.rfind("<TABLE"):t.rfind("</TABLE>")]
                for s in table.split("<TR>"):
                    st = s.split('\n')
                    c = 0
                    for ln in st:
                        if (ln.find("Пары") == -1 and ln.find("<P ") != -1):
                            text = GetTextFromRow(ln)
                            if ((r > 2) and text != "-" and text.find("-") != -1 and text.find(group) != -1):
                                print(str(r - 2) + "|" + str(c) + "|" + text)
                                Timetable[r-2][c] += text + " преподаватель " + name+"\n"
                            if (text != ""):
                                c += 1
                    r += 1
        except:
            pass;

    text = CreateHTML(Timetable);
    with open(fileName,'w')as f:
        f.write(text)
    print(*Timetable, sep="\n")