import praw
import csv
import time

bot = praw.Reddit(user_agent='Dx2 SMT wiki bot',
client_id='',
client_secret='',
username='',
password='')


with open('SMT Dx2 Database - FormattedDemons.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    list = list(reader)
    # remove first row of list
    list.pop(0)
    count = 0
    demons = []
    for item in list:
        if len(item[0]) < 50:
            base = item[1] + "|" + item[2] + "|" + '☆' * int(item[3]) + "|" + item[29]
            stats = item[4] + "|" + item[5] + "|" + item[6] + "|" + item[7] + "|" + item[8] + "|" + item[9]
            elements = item[10] + "|" + item[11] + "|" + item[12] + "|" + item[13] + "|" + item[14] + "|" + item[15] + "|" + item[16]
            transfer = item[17]
            skillsBasic = item[18] + "\n" + item[19]
            skillsArchetype = "Common (Clear)|" + item[20] + "\nAragami (Red)|" + item[21] + "\nProtector (Yellow)|" + item[22] + "\nPsychic (Purple)|" + item[23] + "\nElementalist (Teal)|" + item[24]
            skillsGacha = "Aragami (Red)|" + item[25] + "\nProtector (Yellow)|" + item[26] + "\nPsychic (Purple)|" + item[27] + "\nElementalist (Teal)|" + item[28]
            demonItem = "## **" + item[0] + "**   \n\n### Overview   \n\n**Wiki page**: https://dx2wiki.com/index.php/" +item[0] + "   \n\n" + "Race|Grade|Rarity|AI\n:-:|:-:|:-:|:-:\n" + base\
             + "\n\n\n###6☆ Max Level Stats\n\nHP|Strength|Magic|Vitality|Agility|Luck\n:-:|:-:|:-:|:-:|:-:|:-:\n"
            demonItem = demonItem + stats + "\n\n\n###Elemental Resistances\n\nPhysical|Fire|Ice|Electricity|Force|Light|Dark\n:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:\n"
            demonItem = demonItem + elements + "\n\n\n###Transferable Skill\n\nEN|JP|MP Cost|Description\n:-:|:-:|:-:|:-:\n"
            demonItem = demonItem + transfer + "\n\n\n###Innate Skills\n\nEN|JP|MP Cost|Description\n:-:|:-:|:-:|:-:\n"
            demonItem = demonItem + skillsBasic + "\n\n\n###Archetype Skills\n\nArchetype|EN|JP|MP Cost|Description\n:-:|:-:|:-:|:-:|:-:\n"
            demonItem = demonItem + skillsArchetype + "\n\n\n###Gacha Skills\n\nArchetype|EN|JP|MP Cost|Description\n:-:|:-:|:-:|:-:|:-:\n" + skillsGacha + "\n\n"
            pageName = item[0]
            pageName = pageName.replace("'", "_")
            print(pageName)
            print(demonItem)
            sub = bot.subreddit('Dx2SMTLiberation')
            page = sub.wiki["demons/" + pageName]
            page.edit(demonItem, reason="Bot is editing demon page")
            time.sleep(1)
