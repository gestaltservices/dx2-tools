import praw
import csv

bot = praw.Reddit(user_agent='Dx2 SMT wiki bot',
client_id='',
client_secret='',
username='',
password='')

with open('_skills.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    ls = list(reader)
    # remove first row of list
    wikiDisplay = "https://www.reddit.com/r/Dx2SMTLiberation/wiki/demons\n\n"
    previousType = ""
    addText = ""
    count = 0
    for item in ls:
        if count != 0:
            if previousType != item[0]:
                # print(item[0])
                previousType = item[0]
                if previousType == "phys":
                    addText = "###Physical Skills"
                elif previousType == "fire":
                    addText = "\n\n\n###Fire Skills"
                elif previousType == "ice":
                    addText = "\n\n\n###Ice Skills"
                elif previousType == "elec":
                    addText = "\n\n\n###Electricity Skills"
                elif previousType == "force":
                    addText = "\n\n\n###Force Skills"
                elif previousType == "light":
                    addText = "\n\n\n###Light Skills"
                elif previousType == "dark":
                    addText = "\n\n\n###Dark Skills"
                elif previousType == "almighty":
                    addText = "\n\n\n###Almighty Skills"
                elif previousType == "ailment":
                    addText = "\n\n\n###Status Ailment Skills"
                elif previousType == "recovery":
                    addText = "\n\n\n###Recovery Skills"
                elif previousType == "support":
                    addText = "\n\n\n###Support Skills"
                elif previousType == "passive":
                    addText = "\n\n\n###Passive Skills"
                addText = addText + "\n\nENG | JP | Effect | MP Cost | Targeting | Learned By | Transferable From |\n:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"

            wikiDisplay = wikiDisplay + addText
            addText = ""
            wikiDisplay = wikiDisplay + item[1] + "|" + item[2] + "|" + item[3] + "|" + item[4] + "|" + item[5] + "|" + item[6] + "|" + item[7] + "|\n"
        count = count + 1
print(wikiDisplay)
sub = bot.subreddit('Dx2SMTLiberation')
page = sub.wiki["skill-database"]
page.edit(wikiDisplay, reason="Bot Edit")
