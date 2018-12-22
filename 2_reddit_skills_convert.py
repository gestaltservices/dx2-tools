import csv
import collections
import shutil

skillIndex = 6
archetypeIndex = 7
gachaIndex = 8


def GetName(n):
    if n[:2] == ", ":
        return n[2:]
    return n


def SkillList(a: int):
    with open('SMT Dx2 Database - Skills.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ls = list(reader)
        count = 0
        for item in ls:
            skillName = item[1]
            add_transfer = []
            add_innate = []
            if count > 0:
                for demon in demons:
                    # get demon hyperlink
                    if a == 0:
                        demonLink = demon.name.lower()
                        demonLink = demonLink.replace("'", "_")
                        demonLink = demonLink.replace(" ", "_")
                        demonName = "[" + demon.name + "]" + "(https://www.reddit.com/r/Dx2SMTLiberation/wiki/demons/" + demonLink + ")"
                    elif a == 1:
                        demonName = "[" + demon.name + "]"
                    elif a == 2:
                        demonName = "[[" + demon.name + "]]"

                    # transferable skills
                    if demon.s1 == skillName:
                        add_transfer.append((ls[count][gachaIndex]) + demonName)
                    elif demon.gr == skillName:
                        add_transfer.append((ls[count][gachaIndex]) + demonName + " (Red Gacha)")
                    elif demon.gy == skillName:
                        add_transfer.append((ls[count][gachaIndex]) + demonName + " (Yellow Gacha)")
                    elif demon.gp == skillName:
                        add_transfer.append((ls[count][gachaIndex]) + demonName + " (Purple Gacha)")
                    elif demon.gt == skillName:
                        add_transfer.append((ls[count][gachaIndex]) + demonName + " (Teal Gacha)")

                    # non transferable skills
                    elif (demon.s2 == skillName) or (demon.s3 == skillName):
                        add_innate.append((ls[count][archetypeIndex]) + demonName)
                    elif demon.ca == skillName:
                        add_innate.append((ls[count][archetypeIndex]) + demonName + " (Clear Archetype)")
                    elif demon.cr == skillName:
                        add_innate.append((ls[count][archetypeIndex]) + demonName + " (Red Archetype)")
                    elif demon.cy == skillName:
                        add_innate.append((ls[count][archetypeIndex]) + demonName + " (Yellow Archetype)")
                    elif demon.cp == skillName:
                        add_innate.append((ls[count][archetypeIndex]) + demonName + " (Purple Archetype)")
                    elif demon.ct == skillName:
                        add_innate.append((ls[count][archetypeIndex]) + demonName + " (Teal Archetype)")

                # print(", ".join(str(x) for x in add_transfer))
                ls[count][gachaIndex] = (", ".join(str(x) for x in add_transfer))
                ls[count][archetypeIndex] = (", ".join(str(x) for x in add_innate))
            count += 1

        count = 0
        # for item in l:
        #    if count != 0:
        #        if len(item[gachaIndex]) > 10:
        #            l[count][gachaIndex] = str(l[count][gachaIndex])[:-2]
        #        if len(item[archetypeIndex]) > 10:
        #            l[count][archetypeIndex] = str(l[count][archetypeIndex])[:-2]
        #    count += 1

        return ls


with open('SMT Dx2 Database - Demons.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    ls = list(reader)
    # remove first row of list
    ls.pop(0)
    Demon = collections.namedtuple('Demon', 'name s1 s2 s3 ca cr cy cp ct gr gy gp gt')
    demons = []
    for item in ls:
        if len(item[0]) < 50:
            d = Demon(name=item[0], s1=item[17], s2=item[18],
            s3=item[19], ca=item[20], cr=item[21], cy=item[22], cp=item[23], ct=item[24], gr=item[25], gy=item[26], gp=item[27], gt=item[28])
            demons.append(d)
            # print(d)

# print(SkillList(False))
wr = csv.writer(open('_skills.csv', 'w', newline=''), delimiter=',')
wr.writerows(SkillList(0))

wr = csv.writer(open('_mediawiki skills.csv', 'w', newline=''), delimiter=',')
wr.writerows(SkillList(2))

wr = csv.writer(open('Documents\\GitHub\\einherjar-bot\\dSkills.csv', 'w', encoding='utf8', newline=''), delimiter=',')
wr.writerows(SkillList(1))
shutil.copyfile('SMT Dx2 Database - Skills.csv', 'Documents\\GitHub\\dx2_fusion\\py\\skills.csv')
shutil.copyfile('SMT Dx2 Database - FormattedDemons.csv', 'Documents\\GitHub\\einherjar-bot\\dDemons.csv')
