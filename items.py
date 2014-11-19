from apps.elements.models import Resource, SpawnOutskirt




def add_all_resources():
    metal = (
        #name, tier, category, volume, weight, description 
        ("Copper Ore", Resource.TIER_1, Resource.METAL, 6, "Scarce Vein",           0.5*60,      1*60), 
        ("Tin Ore", Resource.TIER_1, Resource.METAL, 5, "Deserted Shaft",           0.45*60,      1*60), 
        ("Iron Ore", Resource.TIER_2, Resource.METAL, 6, "Gloomy Cavity",           0.4*60,      2*60), 
        ("Silver Ore", Resource.TIER_2, Resource.METAL, 5, "Substantial Lode",      0.35*60,      2*60), 
        ("Aluminium Ore", Resource.TIER_3, Resource.METAL, 4, "Old Mining Shaft",   0.3*60,      4*60), 
        ("Dark Iron Ore", Resource.TIER_3, Resource.METAL, 3, "Rich Cavity",        0.25*60,      4*60), 
        ("Titanium Ore", Resource.TIER_4, Resource.METAL, 2, "Superficial Burrow",  0.1*60,      8*60), 
        ("Gold Ore", Resource.TIER_4, Resource.METAL, 1, "Ancient Cavern",          0.05*60,      8*60), 
    )
    
    wood = (
        ("Spruce Wood", Resource.TIER_1, Resource.WOOD, 220, "Measly Forest",        0.3*60,     1*60), 
        ("Pine Wood", Resource.TIER_1, Resource.WOOD, 220, "Thin Woods",             0.25*60,     1*60), 
        ("Birch Wood", Resource.TIER_2, Resource.WOOD, 220, "Thick Forest",          0.2*60,     2*60), 
        ("Cedar Wood", Resource.TIER_2, Resource.WOOD, 220, "Leaf Woods",            0.15*60,     2*60), 
        ("Oak Wood", Resource.TIER_3, Resource.WOOD, 220, "Deep Woods",              0.1*60,     4*60), 
        ("Maple Wood", Resource.TIER_3, Resource.WOOD, 220, "Squalid Forest",        0.08*60,     4*60), 
        ("Teak Wood", Resource.TIER_4, Resource.WOOD, 220, "Green Forest",           0.06*60,     8*60), 
        ("Mahogany Wood", Resource.TIER_4, Resource.WOOD, 220, "Rough Jungle",       0.04*60,     8*60), 
    )
    
    stone = (
        ("Sandstone", Resource.TIER_1, Resource.STONE, 80, "Sandy Slope",            0.3*60,      1*60), 
        ("Limestone", Resource.TIER_1, Resource.STONE, 80, "Excavated Hill",         0.25*60,      1*60), 
        ("Clay", Resource.TIER_2, Resource.STONE, 80, "Riverbed",                    0.2*60,      2*60), 
        ("Marl", Resource.TIER_2, Resource.STONE, 80, "Cliffed Coast",               0.15*60,      2*60), 
        ("Marble", Resource.TIER_3, Resource.STONE, 80, "White Quarry",              0.1*60,      4*60), 
        ("Gneiss", Resource.TIER_3, Resource.STONE, 80, "Rocky Grounds",             0.08*60,      4*60), 
        ("Obsidian", Resource.TIER_4, Resource.STONE, 80, "Bedrock",                 0.04*60,      8*60), 
        ("Granite", Resource.TIER_4, Resource.STONE, 80, "Fossil Dig",               0.06*60,      8*60), 
    )
    
    animal = (
        ("Rabbit", Resource.TIER_1, Resource.ANIMAL, 1, "Sand Dunes",                0.2*60,      1*60), 
        ("Chicken", Resource.TIER_1, Resource.ANIMAL, 1, "Grassy Prairie",           0.2*60,      1*60), 
        ("Fox", Resource.TIER_2, Resource.ANIMAL, 40, "Damp Grassland",               0.15*60,      2*60), 
        ("Dog", Resource.TIER_2, Resource.ANIMAL, 40, "Outskirts",                    0.15*60,      2*60), 
        ("Deer", Resource.TIER_3, Resource.ANIMAL, 120, "Hillside Forest",             0.1*60,      4*60), 
        ("Horse", Resource.TIER_3, Resource.ANIMAL, 180, "Grazed Field",               0.1*60,      4*60), 
        ("Bear", Resource.TIER_4, Resource.ANIMAL, 180, "Salmon Creek",                0.05*60,      8*60), 
        ("Mammoth", Resource.TIER_4, Resource.ANIMAL, 800, "Borean Tundra",            0.01*60,      8*60), 
    )

    food = (
        ("Potato", Resource.TIER_1, Resource.FOOD, 1, "Dry Patch",                 0.5*60,      0*60), 
        ("Apple", Resource.TIER_1, Resource.FOOD, 1, "Sunny Orchard",              0.5*60,      0*60), 
        ("Corn", Resource.TIER_2, Resource.FOOD, 1, "Ordinary Cornfield",          0.5*60,    0*60), 
        ("Grapes", Resource.TIER_2, Resource.FOOD, 1, "Red Vineyard",              0.5*60,    0*60), 
        ("Rice", Resource.TIER_3, Resource.FOOD, 1, "Flooded Plot",                0.5*60,   0*60), 
        ("Peach", Resource.TIER_3, Resource.FOOD, 1, "Foraged Acreage",            0.5*60,   0*60), 
        ("Wheat", Resource.TIER_4, Resource.FOOD, 1, "Vast Farmstead",             0.5*60,    0*60), 
        ("Pumpkin", Resource.TIER_4, Resource.FOOD, 1, "Large Pumpkinfield",       0.25*60,    0*60), 
    )

    all_resources = metal + wood + stone + animal + food      
    
    for resource in all_resources:
        Resource.objects.create(
            name = resource[0],
            tier = resource[1],
            category = resource[2],
            description = "",
            volume = resource[3],
            
            location = resource[4],
            heroes_min = 3,
            heroes_max = 6,
            gather_speed = resource[5],
            stamina_cost = resource[6],
        )
    

add_all_resources()



def add_spawn_outskirts():
    spawns = (
        #difficulty, tier_1, tier_2, tier_3, tier_4
        (1,     100,    0,      0,      0),
        (2,     100,    0,      0,      0),
        (3,     100,    50,     0,      0),
        (4,     100,    50,     0,      0),
        (5,     50,     100,    0,      0),
        (6,     50,     100,    0,      0),
        (7,     25,     100,    50,     0),
        (8,     25,     100,    50,     0),
        (9,     0,      50,     100,    0),
        (10,    0,      50,     100,    0),
        (11,    0,      25,     100,    25),
        (12,    0,      25,     100,    25),
        (13,    0,      0,      50,     50),
        (14,    0,      0,      50,     50),
        (15,    0,      0,      50,     100),
        (16,    0,      0,      50,     100),
        (17,    0,      0,      0,      100),
        (18,    0,      0,      0,      100),
    )
    
    for spawn in spawns:
        SpawnOutskirt.objects.create(
            difficulty = spawn[0],
            tier_1 = spawn[1],
            tier_2 = spawn[2],
            tier_3 = spawn[3],
            tier_4 = spawn[4],
        )


add_spawn_outskirts()
