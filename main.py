from rich import * #console styling
from rich.console import Console
from rich.rule import Rule
import censusname as names #name generation
import random 
import rcoc #random countries and cities
import time
import math

allpeople = []
console = Console()

class person: #use this to make a new person
    def __init__(self, requiredlastname=None, requiredage=0, requiredgender=f"{random.choice(["male", "female"])}", requiredbirthcountry=None, requiredbirthcity=None, requiredcurrentcity=None, requiredcurrentcountry=None, relationship="self", relationshipquality=100):
        self.firstname = names.generate(nameformat="{given}", given=requiredgender)
        self.lastname = requiredlastname if requiredlastname else names.generate(nameformat="{surname}", given=requiredgender)
        self.fullname = " ".join([self.firstname, self.lastname])
        self.age = requiredage
        self.gender = requiredgender
        self.currentcountry = requiredcurrentcountry if requiredcurrentcountry else rcoc.get_random_country()
        self.currentcity = requiredcurrentcity if requiredcurrentcity else rcoc.get_random_city_by_country(self.currentcountry)
        self.birthcountry = requiredbirthcountry if requiredbirthcountry else (rcoc.get_random_country() if random.randrange(1, 6) == 1 else self.currentcountry)
        self.birthcity = requiredbirthcity if requiredbirthcity else rcoc.get_random_city_by_country(self.birthcountry)
        self.birthplace = ", ".join([self.birthcity, self.birthcountry])
        self.alive = True
        self.relationship = relationship
        self.relationquality = relationshipquality
        allpeople.append(self)
class company:
    def __init__(type):
        match type:
            case "Tech":
                return "Tech Co."
class choice:
    def __init__(self, name, effects=None, response=""):
        self.name = name
        self.effects = effects
        self.response = response
    def choose(self):
        print(f"{self.response}")
class event:
    def __init__(self, description, choices, condition=True):
        self.description = description
        self.choices = choices
        self.condition = condition
    def show(self):
        console.print(f"[bold purple]{self.description}[/bold purple] What do you do?")
        num = 1
        for i in self.choices:
            console.print(f"{num}. {i.name}")
            num += 1
        choice = console.input("Type the number of the choice you want:")
        self.choices[int(choice)-1].choose()

def progressbar(totalpercent, currentpercent, segments, color): #returns a progress bar to showcase percentages
    final = f"[{color}]"
    div = totalpercent / segments
    amountcolored = round(currentpercent / div)
    b = []
    c = []
    for i in range(amountcolored):
        b.append("█")
    for i in range(segments-amountcolored):
        c.append("█")
    b = "".join(b)
    c = "".join(c)
    final = "".join([final, b, f"[/{color}]", c])
    return final
def displayperson(p): #displays all data of a person
    if p.gender == "female":
        console.print(" ".join([p.fullname, f"(♀️ {p.age})"]), style="bold magenta on black")
    else:
        console.print(" ".join([p.fullname, f"(♂️ {p.age})"]), style="bold blue on black")
    if p.relationship == "self":
        console.print(f"[bold red]Relationship to player[/bold red]: [bold green]Self[/bold green]")
    else:
        console.print(f"[bold red]Relationship to player[/bold red]: [bold green]Player's {p.relationship}[/bold green] {progressbar(100, p.relationquality, 15, "bold blue")} ([bold blue]{p.relationquality}%[/bold blue] relationship quality)")
    console.print(" ".join(["[bold red]Birthplace[/bold red]:", f"[green]{p.birthplace}[/green]"]))
    console.print(f"Currently lives in [bold red]{p.currentcity}, {p.currentcountry}[/bold red]", end="\n \n")
def displayrelations(): #menu to find people
    console.clear()
    number = 1
    console.print("All people you have known or do know: \n")
    console.print(Rule(characters="~", style="blue"))
    for p in allpeople:
        console.print(f"[cyan]{number}[/cyan]. [bold purple]{p.fullname}[/bold purple] ([bold blue]{(p.relationship).title()}[/bold blue])")
        console.print(Rule(characters="~", style="blue"))
        number += 1
    person = console.input("\nType a person's number to see more details:")
    console.clear()
    displayperson(allpeople[int(person) - 1])
    a = console.input("Type anything to go back to menu:")
    console.clear()
    displayrelations()
def nextyear(): #ages everyone
    for i in allpeople:
        if i.alive:
            i.age += 1
        if not i.age <= 65 and random.randrange(1, round(1000 / i.age)) == 1:
            i.alive = False
player = person() #generating family and self
player.currentcity = player.birthcity
player.currentcountry = player.birthcountry
mother = person(requiredlastname=player.lastname, requiredgender="female", relationship="mother", requiredcurrentcity=player.birthcity, requiredcurrentcountry=player.birthcountry, relationshipquality=random.randrange(85, 100))
father = person(requiredgender="male", relationship="father", requiredlastname=player.lastname, requiredcurrentcity=player.birthcity, requiredcurrentcountry=player.birthcountry, relationshipquality=random.randrange(85, 100))
console.print(f"You are [bold purple]{player.fullname}[/bold purple]. You were born in [bold red]{player.birthplace}[/bold red] to your parents [bold purple]{mother.firstname}[/bold purple] and [bold purple]{father.firstname}[/bold purple].", end="\n \n")
numofsibs = random.randrange(0, 4)
a = random.randrange(4, 8)
mother.age, father.age = random.randrange(21, 30) + a * numofsibs, random.randrange(21, 30) + a * numofsibs
for i in range(numofsibs): #siblings
    newsib = person(requiredlastname=player.lastname, relationship="sibling", requiredage=((mother.age - 20 - random.randrange(0, 4)) - (i * a)), requiredbirthcountry=player.currentcountry, relationshipquality=random.randrange(50, 100))
    if newsib.age <= 18 and random.randrange(1,2) == 1:
        newsib.currentcountry = player.currentcountry
        newsib.currentcity = player.currentcity
events = [event("You stubbed your toe on a [bold red]table's leg[/bold red].", [choice("Get help from Mom.", response="Mom helped you!"), choice("Get help from Dad.", response="Dad helped you!")])]
events[0].show()
while player.alive: #main loop
    pass