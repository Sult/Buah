from django.template.defaultfilters import slugify

from apps.towns.models import Town, Tavern, OutskirtBuilding
from apps.users.models import Npc, Tribe




def add_tribes_shells():
    
    tribes = (
        #name, focus
        ("Warhead", Tribe.COMBAT),
        ("Bannergaurds", Tribe.COMBAT),
        ("Moonforge", Tribe.CRAFTING),
        ("Harbringers of Faith", Tribe.TRADING),
        ("Brave from the Sea", Tribe.TRADING),
        ("Warcry", Tribe.COMBAT),
        ("Charred Desire", Tribe.CRAFTING),
        ("Visions of the Lost", Tribe.TRADING),
        ("Venomforce", Tribe.COMBAT),
        ("Concealed Faith", Tribe.CRAFTING),
        ("Immortals", Tribe.COMBAT),
        ("Cycle of Gold", Tribe.TRADING),
        ("Gentle Fire", Tribe.CRAFTING),
        ("Misery of Wealth", Tribe.TRADING),
        ("Mystical Life", Tribe.COMBAT),
        ("Dark Smiths", Tribe.CRAFTING),
    )
    
    for tribe in tribes:
        Tribe.objects.create(
            name = tribe[0],
            description = "",
            focus = tribe[1],
        )


def add_leader_npcs():
    some_npcs = (
        #name, tribe
        ("Soam Ironhammer",	"Warhead"),
        ("Anthor Shieldgrip",	"Bannergaurds"),
        ("Breadon Essah",	"Moonforge"),
        ("Tiffany Vynorlan",	"Harbringers of Faith"),
        ("Alexes Nahatis",	"Brave from the Sea"),
        ("Charles Balog",	"Warcry"),
        ("Jarson Tjalk",	"Charred Desire"),
        ("Arina Goldtail",	"Visions of the Lost"),
        ("Eddar Rainbone",	"Venomforce"),
        ("Dallin Sky",	"Concealed Faith"),
        ("Seban IronCrest",	"Immortals"),
        ("Kok Mirza",	"Cycle of Gold"),
        ("Salema Fahri",	"Gentle Fire"),
        ("Lorch Rambton",	"Misery of Wealth"),
        ("Darwin Baxter",	"Mystical Life"),
        ("Merric Durgar",	"Dark Smiths"),
        
    )
    
    for npc in some_npcs:
        Npc.objects.create(
            name = npc[0],
            description = "",
            tribe = Tribe.objects.get(name=npc[1]),
        )


def fill_tribe_shells():
    tribes = (
        #tribe, leader, likes, hates
        ("Warhead", "Soam Ironhammer", "Bannergaurds", "Harbringers of Faith"),
        ("Bannergaurds", "Anthor Shieldgrip", "Warhead", "Moonforge"),
        ("Moonforge", "Breadon Essah", "Harbringers of Faith", "Bannergaurds"),
        ("Harbringers of Faith", "Tiffany Vynorlan", "Moonforge", "Warhead"),
        ("Brave from the Sea", "Alexes Nahatis", "Warcry", "Visions of the Lost"),
        ("Warcry", "Charles Balog", "Brave from the Sea", "Charred Desire"),
        ("Charred Desire", "Jarson Tjalk", "Visions of the Lost", "Brave from the Sea"),
        ("Visions of the Lost", "Arina Goldtail", "Charred Desire", "Warcry"),
        ("Venomforce", "Eddar Rainbone", "Concealed Faith", "Immortals"),
        ("Concealed Faith", "Dallin Sky", "Venomforce", "Cycle of Gold"),
        ("Immortals", "Seban IronCrest", "Cycle of Gold", "Venomforce"),
        ("Cycle of Gold", "Kok Mirza", "Immortals", "Concealed Faith"),
        ("Gentle Fire", "Salema Fahri", "Misery of Wealth", "Dark Smiths"),
        ("Misery of Wealth", "Lorch Rambton", "Gentle Fire", "Mystical Life"),
        ("Mystical Life", "Darwin Baxter", "Dark Smiths", "Misery of Wealth"),
        ("Dark Smiths", "Merric Durgar", "Mystical Life", "Gentle Fire"),
    )
    
    for tribe in tribes:
        edit_tribe = Tribe.objects.get(name=tribe[0])
        edit_tribe.leader = Npc.objects.get(name=tribe[1])
        edit_tribe.likes = Tribe.objects.get(name=tribe[2])
        edit_tribe.hates = Tribe.objects.get(name=tribe[3])
        edit_tribe.save()
        print tribe[1]


def add_other_npcs():
    npcs = (
        #warhead
        ("Gregor Barrin", "Warhead"),
        ("Elmer Bullseye", "Warhead"),
        ("Kailyn Centyre", "Warhead"),
        ("Thorburn Phantom", "Warhead"),
    )
    
    for npc in npcs:
        Npc.objects.create(name=npc[0], tribe=Tribe.objects.get(name=npc[1]))
    
    
    
    
        

add_tribes_shells()
add_leader_npcs()    
fill_tribe_shells()
add_other_npcs()


    

def add_warhead_towns():
    towns = (
        #name, owner, difficulty,   #ouskirts townhall, barrracks, tradehouse
        ("Kelna", "Soam Ironhammer", 8,         2, 6, 1),
        ("Blackpool", "Gregor Barrin", 4,       2, 3, 1),
        ("Inverness", "Elmer Bullseye", 1,      1, 1, 1),                   #startingtown
        ("Festiniog", "Thorburn Phantom", 1,    1, 1, 1),
        ("Aquarin", "Thorburn Phantom", 3,      1, 2, 2),
    )
    
    for town in towns:
        new = Town.objects.create(
            slug = slugify(town[0]),
            controlled = False,
            owner_npc = Npc.objects.get(name=town[1]),
            difficulty = town[2],
            #coordinates = models.ForeignKey(Coordinates)
            name = town[0],
            description = "",
        )
        
        #create tavern
        Tavern.objects.create(town=new)
        
        #create outskirts (townhall, barracks, mineter)
        OutskirtBuilding.objects.create(town=new, level=town[3], building=OutskirtBuilding.TOWNHALL)
        OutskirtBuilding.objects.create(town=new, level=town[4], building=OutskirtBuilding.BARRACKS)
        OutskirtBuilding.objects.create(town=new, level=town[5], building=OutskirtBuilding.TRADEHOUSE)


add_warhead_towns()
        
        
        
        
        
        
    
    
    
