import mwclient
import csv
import collections
import logging
logging.basicConfig(level=logging.WARNING)


def effect(r):
    if r[0] == "+":
        return "<nowiki>+</nowiki>" + r[1:]
    elif r[0] == "-":
        return "<nowiki>-</nowiki>" + r[1:]
    return r


def resist(r):
    if r == "-":
        return "<nowiki>-</nowiki>"
    elif r == "rs":
        return "Resist"
    elif r == "wk":
        return "Weak"
    elif r == "nu":
        return "Null"
    elif r == "rp":
        return "Repel"
    elif r == "dr":
        return "Drain"
    return "{{ResistColor|1=" + str(r) + "}}"


def skill(s):
    if s == "":
        return "N/A"
    elif s == "Berserker":
        return "Berserker (Skill)"
    return s


def ai(s):
    if s == "":
        return "?"
    return s


def skill_type(s):
    if s == "phys":
        return "Physical"
    elif s == "fire":
        return "Fire"
    elif s == "ice":
        return "Ice"
    elif s == "elec":
        return "Electricity"
    elif s == "force":
        return "Force"
    elif s == "light":
        return "Light"
    elif s == "dark":
        return "Dark"
    elif s == "almighty":
        return "Almighty"
    elif s == "ailment":
        return "Ailment"
    elif s == "recovery":
        return "Recovery"
    elif s == "support":
        return "Support"
    elif s == "passive":
        return "Passive"


def targetting(s):
    return str(s)


def aether(s, r):
    # Yellow/Purple/Blue/Red
    if s == "Entity" or s == "Zealot" or s == "Enigma" or s == "UMA" or s == "Rumor" or s == "Hero" or s == "Fiend":
        if r == 5:
            return "\n|awaken1=L-Light|awaken2=L-Dark|awaken3=L-Lawful|awaken4=L-Chaotic|awaken1amnt=15L|awaken2amnt=15L|awaken3amnt=15L|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=L-Light|awaken2=L-Dark|awaken3=L-Lawful|awaken4=L-Chaotic|awaken1amnt=5L|awaken2amnt=5L|awaken3amnt=5L|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=M-Light|awaken2=M-Dark|awaken3=M-Lawful|awaken4=M-Chaotic|awaken1amnt=10M|awaken2amnt=10M|awaken3amnt=10M|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=M-Light|awaken2=M-Dark|awaken3=M-Lawful|awaken4=M-Chaotic|awaken1amnt=5M|awaken2amnt=5M|awaken3amnt=5M|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Light|awaken2=S-Dark|awaken3=S-Lawful|awaken4=S-Chaotic|awaken1amnt=5S|awaken2amnt=5S|awaken3amnt=5S|awaken4amnt=5S"
    elif s == "Dragon" or s == "Kishin" or s == "Lady" or s == "Fury":
        # Chaotic Good (Red + Yellow)
        if r == 5:
            return "\n|awaken1=M-Light|awaken2=L-Light|awaken3=M-Chaotic|awaken4=L-Chaotic|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Light|awaken2=L-Light|awaken3=M-Chaotic|awaken4=L-Chaotic|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Light|awaken2=M-Light|awaken3=S-Chaotic|awaken4=M-Chaotic|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Light|awaken2=M-Light|awaken3=S-Chaotic|awaken4=M-Chaotic|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Light|awaken2=S-Chaotic|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Haunt" or s == "Tyrant" or s == "Foul":
        # Chaotic Evil (Red + Purple)
        if r == 5:
            return "\n|awaken1=M-Dark|awaken2=L-Dark|awaken3=M-Chaotic|awaken4=L-Chaotic|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Dark|awaken2=L-Dark|awaken3=M-Chaotic|awaken4=L-Chaotic|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Dark|awaken2=M-Dark|awaken3=S-Chaotic|awaken4=M-Chaotic|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Dark|awaken2=M-Dark|awaken3=S-Chaotic|awaken4=M-Chaotic|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Dark|awaken2=S-Chaotic|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Avian" or s == "Megami" or s == "Herald":
        # Lawful Good (Blue + Yellow)
        if r == 5:
            return "\n|awaken1=M-Light|awaken2=L-Light|awaken3=M-Lawful|awaken4=L-Lawful|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Light|awaken2=L-Light|awaken3=M-Lawful|awaken4=L-Lawful|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Light|awaken2=M-Light|awaken3=S-Lawful|awaken4=M-Lawful|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Light|awaken2=M-Light|awaken3=S-Lawful|awaken4=M-Lawful|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Light|awaken2=S-Lawful|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Vile":
        # Lawful Evil (Blue + Purple)
        if r == 5:
            return "\n|awaken1=M-Dark|awaken2=L-Dark|awaken3=M-Lawful|awaken4=L-Lawful|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Dark|awaken2=L-Dark|awaken3=M-Lawful|awaken4=L-Lawful|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Dark|awaken2=M-Dark|awaken3=S-Lawful|awaken4=M-Lawful|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Dark|awaken2=M-Dark|awaken3=S-Lawful|awaken4=M-Lawful|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Dark|awaken2=S-Lawful|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Wilder" or s == "Jaki":
        # Neutral Evil (Green + Purple)
        if r == 5:
            return "\n|awaken1=M-Dark|awaken2=L-Dark|awaken3=M-Neutral|awaken4=L-Neutral|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Dark|awaken2=L-Dark|awaken3=M-Neutral|awaken4=L-Neutral|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Dark|awaken2=M-Dark|awaken3=S-Neutral|awaken4=M-Neutral|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Dark|awaken2=M-Dark|awaken3=S-Neutral|awaken4=M-Neutral|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Dark|awaken2=S-Neutral|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Genma" or s == "Holy" or s == "Avatar" or s == "Deity":
        # Neutral Good (Green + Yellow)
        if r == 5:
            return "\n|awaken1=M-Light|awaken2=L-Light|awaken3=M-Neutral|awaken4=L-Neutral|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Light|awaken2=L-Light|awaken3=M-Neutral|awaken4=L-Neutral|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Light|awaken2=M-Light|awaken3=S-Neutral|awaken4=M-Neutral|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Light|awaken2=M-Light|awaken3=S-Neutral|awaken4=M-Neutral|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Light|awaken2=S-Neutral|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Night" or s == "Femme" or s == "Brute" or s == "Fallen":
        # Neutral Chaotic (Green + Red)
        if r == 5:
            return "\n|awaken1=M-Neutral|awaken2=L-Neutral|awaken3=M-Chaotic|awaken4=L-Chaotic|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Neutral|awaken2=L-Neutral|awaken3=M-Chaotic|awaken4=L-Chaotic|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Neutral|awaken2=M-Neutral|awaken3=S-Chaotic|awaken4=M-Chaotic|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Neutral|awaken2=M-Neutral|awaken3=S-Chaotic|awaken4=M-Chaotic|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Neutral|awaken2=S-Chaotic|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Yoma" or s == "Divine":
        # Neutral Lawful (Green + Blue)
        if r == 5:
            return "\n|awaken1=M-Neutral|awaken2=L-Neutral|awaken3=M-Lawful|awaken4=L-Lawful|awaken1amnt=20M|awaken2amnt=15L|awaken3amnt=20M|awaken4amnt=15L"
        elif r == 4:
            return "\n|awaken1=M-Neutral|awaken2=L-Neutral|awaken3=M-Lawful|awaken4=L-Lawful|awaken1amnt=15M|awaken2amnt=5L|awaken3amnt=15M|awaken4amnt=5L"
        elif r == 3:
            return "\n|awaken1=S-Neutral|awaken2=M-Neutral|awaken3=S-Lawful|awaken4=M-Lawful|awaken1amnt=5S|awaken2amnt=10M|awaken3amnt=5S|awaken4amnt=10M"
        elif r == 2:
            return "\n|awaken1=S-Neutral|awaken2=M-Neutral|awaken3=S-Lawful|awaken4=M-Lawful|awaken1amnt=10S|awaken2amnt=5M|awaken3amnt=10S|awaken4amnt=5M"
        elif r == 1:
            return "\n|awaken1=S-Neutral|awaken2=S-Lawful|awaken1amnt=10S|awaken2amnt=10S"
    elif s == "Fairy" or s == "Beast" or s == "Snake":
        # Neutral (Green)
        if r == 5:
            return "\n|awaken1=M-Neutral|awaken2=L-Neutral|awaken1amnt=40M|awaken2amnt=30L"
        elif r == 4:
            return "\n|awaken1=M-Neutral|awaken2=L-Neutral|awaken1amnt=30M|awaken2amnt=10L"
        elif r == 3:
            return "\n|awaken1=S-Neutral|awaken2=M-Neutral|awaken1amnt=10S|awaken2amnt=20M"
        elif r == 2:
            return "\n|awaken1=S-Neutral|awaken2=M-Neutral|awaken1amnt=20S|awaken2amnt=10M"
        elif r == 1:
            return "\n|awaken1=S-Neutral|awaken1amnt=20S"
    print(s + " is missing!")
    return ""


def fill_demons(cat):
    with open('SMT Dx2 Database - MediawikiDemons.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ls = list(reader)
        # remove first row of list
        ls.pop(0)
        count = 0
        for item in ls:
            if len(item[0]) < 50:
                
                demonText = "{{DemonTabs|base{{BASENAME}} }}"
                demonText = demonText + "\n{{Demon\n|id= " + ""
                demonText = demonText + "\n|jpname= " + ""
                demonText = demonText + "\n|name= " + item[0]
                demonText = demonText + "\n|release_version= " + "1.0"
                demonText = demonText + "\n|link_altema= " + " "
                demonText = demonText + "\n|art= " + "{{PAGENAME}}.jpg"

                demonText = demonText + "\n|phys= " + resist(item[4])
                demonText = demonText + "\n|fire= " + resist(item[5])
                demonText = demonText + "\n|ice= " + resist(item[6])
                demonText = demonText + "\n|elec= " + resist(item[7])
                demonText = demonText + "\n|force= " + resist(item[8])
                demonText = demonText + "\n|light= " + resist(item[9])
                demonText = demonText + "\n|dark= " + resist(item[10])

                demonText = demonText + "\n|race= " + item[1]
                demonText = demonText + "\n|grade= " + item[2]
                demonText = demonText + "\n|rarity= " + item[3]
                demonText = demonText + "\n|ai= " + item[29]

                demonText = demonText + "\n|max_hp= " + str(item[11])
                demonText = demonText + "\n|max_str= " + str(item[12])
                demonText = demonText + "\n|max_mag= " + str(item[13])
                demonText = demonText + "\n|max_vit= " + str(item[14])
                demonText = demonText + "\n|max_agi= " + str(item[15])
                demonText = demonText + "\n|max_luck= " + str(item[16])

                demonText = demonText + "\n|patk= " + str(item[30])
                demonText = demonText + "\n|pdef= " + str(item[31])
                demonText = demonText + "\n|matk= " + str(item[32])
                demonText = demonText + "\n|mdef= " + str(item[33])

                demonText = demonText + "\n|transfer_skill= " + skill(item[17])
                demonText = demonText + "\n|innate_skill1= " + skill(item[18])
                demonText = demonText + "\n|innate_skill2= " + skill(item[19])

                demonText = demonText + "\n|a_clear= " + skill(item[20])
                demonText = demonText + "\n|a_red= " + skill(item[21])
                demonText = demonText + "\n|a_yellow= " + skill(item[22])
                demonText = demonText + "\n|a_purple= " + skill(item[23])
                demonText = demonText + "\n|a_teal= " + skill(item[24])

                demonText = demonText + "\n|g_red= " + skill(item[25])
                demonText = demonText + "\n|g_yellow= " + skill(item[26])
                demonText = demonText + "\n|g_purple= " + skill(item[27])
                demonText = demonText + "\n|g_teal= " + skill(item[28])

                demonText = demonText + aether(item[1], int(item[3]))

                demonText = demonText + "\n|}}"

                demonText = demonText + "\n[[Category: Demons]]"
                demonText = demonText + "\n[[Category:" + item[1] + "]]"
                demonText = demonText + "\n[[Category:" + item[3] + " Star Demons]]"
                demonText = demonText + "\n[[Category:" + item[29] + " AI]]"

                # if cat == True:
                #    page = site.pages['Category:' + item[1]]
                #    page.save("", 'Bot: Category Creation.')

                print('editing entry ' + str(count) + " - " + item[0])

                page = site.pages[item[0]]
                page.save(demonText, 'Bot: Demon update.')

                if cat is True:
                    page = site.pages[item[0]+"/Lore"]
                    page.save("{{DemonTabs|base={{BASENAME}}|active=lore }}\n__TOC__\n== Official Profile ==", 'Bot: Lore page creation.')
                    page = site.pages[item[0]+"/Builds"]
                    page.save("{{DemonTabs|base={{BASENAME}}|active=builds }}\n__TOC__\n\n== Role Summary ==\n\n== PvE Builds ==\n\n== PvP Builds ==", 'Bot: Builds page creation.')

            count += 1


def fill_skills():
    with open('SMT Dx2 Database - Skills.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ls = list(reader)
        count = 0
        for item in ls:
            # count > 0
            if count > 0:
                skillName = str(item[1])
                if skillName == "Berserker":
                    skillName = "Berserker (Skill)"

                skillType = skill_type(item[0])
                skillCost = str(item[3])
                skillCost = skillCost.replace(" MP","")
                skillDescription = str(item[4])
                skillDescription = skillDescription.replace('\n', '<br />')
                skillTarget = targetting(item[5])
                skillLevel = targetting(item[6])
                if len(skillLevel) < 1:
                    skillLevel = "<nowiki>-</nowiki>"
					
                skillOutput = "{{SkillTable\n|skill="+skillName+"\n|type="+skillType+"\n|cost="+skillCost+"\n|sp="+skillLevel+"\n|target="+skillTarget+"\n|description="+skillDescription+"\n}}"

                # skillOutput = skillOutput + "\n|}}\n[[Category: Skills]]"
                # skillOutput = skillOutput + "\n[[Category:" + skillType + " Skills]]"

                page = site.pages[skillName]
                page.save(skillOutput, 'Bot: Skill page update.')

                if skillName == "Berserker (Skill)":
                    skillName = "Berserker"
                add_innate = []
                add_clear = []
                add_red = []
                add_yellow = []
                add_teal = []
                add_purple = []
                # Transferable Table
                transfer_table = "{{TransferTable\n|title=Demons to transfer skill from\n|type=Default / Gacha Archetype"
                for demon in demons:
                    demonName = "[[" + demon.name + "]]"
                    if demon.s1 == skillName:
                        add_clear.append("\n|d" + str(len(add_clear)) + "=" + demonName)
                    elif demon.gr == skillName:
                        add_red.append("\n|d" + str(len(add_red)) + "r=" + demonName)
                    elif demon.gy == skillName:
                        add_yellow.append("\n|d" + str(len(add_yellow)) + "y=" + demonName)
                    elif demon.gt == skillName:
                        add_teal.append("\n|d" + str(len(add_teal)) + "t=" + demonName)
                    elif demon.gp == skillName:
                        add_purple.append("\n|d" + str(len(add_purple)) + "p=" + demonName)

                transfer_table = transfer_table + ",".join(str(x) for x in add_clear)
                transfer_table = transfer_table + ",".join(str(x) for x in add_red)
                transfer_table = transfer_table + ",".join(str(x) for x in add_yellow)
                transfer_table = transfer_table + ",".join(str(x) for x in add_teal)
                transfer_table = transfer_table + ",".join(str(x) for x in add_purple) + "\n|}}"

                del add_innate[:]
                del add_clear[:]
                del add_red[:]
                del add_yellow[:]
                del add_teal[:]
                del add_purple[:]
                # Owned Table
                innate_table = "\n\n{{OwnedTable\n|title=Demons with skill\n|type=Awakened Archetype"
                for demon in demons:
                    demonName = "[[" + demon.name + "]]"
                    if (demon.s2 == skillName) or (demon.s3 == skillName):
                        add_innate.append("\n|d" + str(len(add_innate)) + "i=" + demonName)
                    elif demon.ca == skillName:
                        add_clear.append("\n|d" + str(len(add_clear)) + "=" + demonName)
                    elif demon.cr == skillName:
                        add_red.append("\n|d" + str(len(add_red)) + "r=" + demonName)
                    elif demon.cy == skillName:
                        add_yellow.append("\n|d" + str(len(add_yellow)) + "y=" + demonName)
                    elif demon.cp == skillName:
                        add_purple.append("\n|d" + str(len(add_purple)) + "p=" + demonName)
                    elif demon.ct == skillName:
                        add_teal.append("\n|d" + str(len(add_teal)) + "t=" + demonName)

                innate_table = innate_table + ",".join(str(x) for x in add_innate)
                innate_table = innate_table + ",".join(str(x) for x in add_clear)
                innate_table = innate_table + ",".join(str(x) for x in add_red)
                innate_table = innate_table + ",".join(str(x) for x in add_yellow)
                innate_table = innate_table + ",".join(str(x) for x in add_purple)
                innate_table = innate_table + ",".join(str(x) for x in add_teal) + "\n|}}"

                if skillName == "Berserker":
                    skillName = "Berserker (Skill)"
                page = site.pages[skillName + "/Demons"]
                page.save(transfer_table + innate_table, 'Bot: Demon table update.')
                print('edited entry ' + str(count) + " - " + skillName)
            count += 1


def fill_demons_main():
    with open('SMT Dx2 Database - MediawikiDemonsWithoutStats.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ls = list(reader)
        # remove first row of list
        ls.pop(0)
        showText = """ {| class="wikitable sortable" style="text-align:center; width: 100%;"\n|-\n
! Name !!Race !!Grade !!Rarity !!AI !!6★ HP !!6★ Strength !!6★ Magic
!6★ Vitality !!6★ Agility !!6★ Luck
![[File:Physical.png|20px|link=]] !![[File:Fire.png|20px|link=]]
![[File:Ice.png|20px|link=]] !![[File:Electricity.png|20px|link=]]
![[File:Force.png|20px|link=]] !![[File:Light.png|20px|link=]]
![[File:Dark.png|20px|link=]] !!6★ PATK
!6★ PDEF !!6★ MATK !!6★ MDEF\n|- style="vertical-align:middle;" """
        for item in ls:
            if len(item[0]) < 50 and len(item[0]) > 2:
                demonText = "\n|{{ListDemon|demon=" + item[0]
                demonText = demonText + "|race= " + item[1]
                demonText = demonText + "|grade= " + item[2]
                demonText = demonText + "|rarity= " + item[3]
                demonText = demonText + "|ai= " + item[29]
                demonText = demonText + "|hp= " + str(item[11])
                demonText = demonText + "|str= " + str(item[12])
                demonText = demonText + "|mag= " + str(item[13])
                demonText = demonText + "|vit= " + str(item[14])
                demonText = demonText + "|agi= " + str(item[15])
                demonText = demonText + "|luck= " + str(item[16])
                demonText = demonText + "|phys= " + resist(item[4])
                demonText = demonText + "|fire= " + resist(item[5])
                demonText = demonText + "|ice= " + resist(item[6])
                demonText = demonText + "|elec= " + resist(item[7])
                demonText = demonText + "|force= " + resist(item[8])
                demonText = demonText + "|light= " + resist(item[9])
                demonText = demonText + "|dark= " + resist(item[10])
                demonText = demonText + "|patk= " + str(item[30])
                demonText = demonText + "|pdef= " + str(item[31])
                demonText = demonText + "|matk= " + str(item[32])
                demonText = demonText + "|mdef= " + str(item[33])

                showText = showText + demonText + '}}\n|- style="vertical-align:middle;"'

        page = site.pages["Demon List"]
        page.save(showText + "}", 'Bot: Demon list update.')


def fill_skills_main():
    with open('_mediawiki skills.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ls = list(reader)
        # remove first row of list
        previousType = ""
        addText = ""
        showText = ""
        count = 0
        for item in ls:
            if count != 0:
                if previousType != item[0]:
                    # print(item[0])
                    previousType = item[0]
                    if previousType == "phys":
                        addText = "===Physical Skills==="
                    elif previousType == "fire":
                        addText = "\n|}\n<br>\n===Fire Skills==="
                    elif previousType == "ice":
                        addText = "\n|}\n<br>\n===Ice Skills==="
                    elif previousType == "elec":
                        addText = "\n|}\n<br>\n===Electricity Skills==="
                    elif previousType == "force":
                        addText = "\n|}\n<br>\n===Force Skills==="
                    elif previousType == "light":
                        addText = "\n|}\n<br>\n===Light Skills==="
                    elif previousType == "dark":
                        addText = "\n|}\n<br>\n===Dark Skills==="
                    elif previousType == "almighty":
                        addText = "\n|}\n<br>\n===Almighty Skills==="
                    elif previousType == "ailment":
                        addText = "\n|}\n<br>\n===Status Ailment Skills==="
                    elif previousType == "recovery":
                        addText = "\n|}\n<br>\n===Recovery Skills==="
                    elif previousType == "support":
                        addText = "\n|}\n<br>\n===Support Skills==="
                    elif previousType == "passive":
                        addText = "\n|}\n<br>\n===Passive Skills==="
                    addText = addText + """\n{| class="wikitable sortable" style="width: 100%;"\n|-\n\n!Name !!JP Name !!MP Cost !!Effect !!Target !!Skill Points !!Learned By !!Transferable From\n|- style="vertical-align:middle;"""

                showText = showText + addText
                addText = ""
                showText = showText + "\n|-\n|" + item[1] + "\n|" + item[2] + "\n|" + item[3] + "\n|" + effect(item[4]) + "\n|" + item[5] + "\n|" + item[6] + "\n|" + item[7] + "\n|" + item[8]
            count = count + 1

        page = site.pages["Skill List (Bot)"]
        page.save(showText + "\n|}", 'Bot: Skill list update.')

def remove_pages():
    with open('SMT Dx2 Database - Skills.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ls = list(reader)
        count = 0
        for item in ls:
            if count > 0:
                skillName = str(item[1])
                page = site.pages[skillName + "/Skill"]
                page.delete(reason='bot error')
            count += 1


# CODE STARTS HERE
with open('SMT Dx2 Database - Demons.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    ls = list(reader)
    # remove first row of list
    ls.pop(0)
    Demon = collections.namedtuple('Demon', 'name s1 s2 s3 ca cr cy cp ct gr gy gp gt')
    demons = []
    for item in ls:
        if len(item[0]) < 50:
            d = Demon(name=item[0], s1=item[17], s2=item[18], s3=item[19], ca=item[20], cr=item[21], cy=item[22], cp=item[23], ct=item[24], gr=item[25], gy=item[26], gp=item[27], gt=item[28])
            demons.append(d)


site = mwclient.Site(('https', 'dx2wiki.com'), path='/')
site.login('Dissi-bot', 'Put your own bot & password here')

#remove_pages()
fill_skills()
fill_demons(False)
fill_demons_main()
fill_skills_main()
