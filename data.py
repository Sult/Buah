from apps.heroes.models import StatPerLevel, HeroMathValues, HeroName
from apps.towns.models import TownMathValues, Town, Tavern, TavernHero
from apps.users.models import UserMathValues, Profile
from django.contrib.auth.models import User

##################### user shizzlemcnizzle ####################
#starting values
def user_math_values():
    UserMathValues.objects.create(
        version=1,
        starting_munny = 15000,
        #heroes
        heroes_owned_max = 5,
        heroes_owned_per_level = 1,
        heroes_active_max = 3,
        heroes_active_per_level = 0.29,
    )

user_math_values()




#################### Heroes Objects ######################

def add_first_hero_version():
    HeroMathValues.objects.create(
    )


def add_hero_names():
    some_names = ("Lois Williams", "Jessica Green","Thomas Ramirez","Eugene Smith","Joe Sanders","Jesse King","Stephanie Russell","Cheryl Sanchez","Andrew Garcia","Anthony Rodriguez","Ronald Nelson","Benjamin Edwards","Adam Morgan","Michael Wright","Victor Howard","Cynthia Thompson","James Butler","Kevin Campbell","Deborah Cooper","Lawrence Jones","Bruce Griffin","Teresa Harris","Craig Wilson","Theresa Moore","Steven Hughes","Paul Ross","Kathleen Richardson","Billy Bryant","William Hall","Gary Price","Tina Bennett","Debra Stewart","Arthur Coleman","Roger Morris","Betty Gray","Katherine Turner","Patricia Ward","Sandra Bailey","Janice Alexander","Denise Torres","Christina Henderson","Kelly Perry","John Thomas","Joan Lee","Nicholas Parker","Rose Young","Willie Phillips","Jerry Flores","Edward Reed","Melissa Hill","Bobby Jenkins","Anne White","Chris Taylor","Phillip Rogers","Gregory Mitchell","Jason Walker","Heather Lewis","Ernest Collins","Jack Martin","Brandon Carter","Barbara Foster","Rebecca Robinson","Raymond Lopez","Jacqueline Powell","Karen Simmons","Ann Miller","Gerald Kelly","Beverly Johnson","Christopher Davis","Sarah Gonzalez","Fred Hernandez","Lori Brooks","Irene Evans","Scott Baker","Albert Scott","Susan Washington","Amy Diaz","Mark Long","Russell Jackson","Donald Wood","Todd Anderson","Paula Cox","Alan Roberts","David Brown","Joshua Rivera","Brenda Allen","Daniel Perez","Jeremy Bell","Norma Patterson","Julie Peterson","Louis Barnes","Philip Cook","Christine Watson","Kenneth Adams","Anna Clark","Nicole Martinez","Henry Gonzales","Douglas James","Lisa Murphy")
    for name in some_names:
        HeroName.objects.create(name=name)

add_hero_names()
    

def add_stats_per_level():
    """ adding all combinations of StatPerLevel """
    
    all_attributes = (
        #quality, attribute, start_value, level_bonus, multiplier
        #(StatPerLevel.VERY_BAD, StatPerLevel.STRENGTH, 15, 1, 1.05),
        #(StatPerLevel.BAD, StatPerLevel.STRENGTH, 17, 2, 1.08),
        #(StatPerLevel.DECENT, StatPerLevel.STRENGTH, 19, 3, 1.11),
        #(StatPerLevel.GOOD, StatPerLevel.STRENGTH, 21, 4, 1.14),
        #(StatPerLevel.EXCELLENT, StatPerLevel.STRENGTH, 23, 5, 1.17),
        
        #(StatPerLevel.VERY_BAD, StatPerLevel.CHARISMA, 15, 1, 1.05),
        #(StatPerLevel.BAD, StatPerLevel.CHARISMA, 17, 2, 1.08),
        #(StatPerLevel.DECENT, StatPerLevel.CHARISMA, 19, 3, 1.11),
        #(StatPerLevel.GOOD, StatPerLevel.CHARISMA, 21, 4, 1.14),
        #(StatPerLevel.EXCELLENT, StatPerLevel.CHARISMA, 23, 5, 1.17),
        
        #(StatPerLevel.VERY_BAD, StatPerLevel.WISDOM, 15, 1, 1.05),
        #(StatPerLevel.BAD, StatPerLevel.WISDOM, 17, 2, 1.08),
        #(StatPerLevel.DECENT, StatPerLevel.WISDOM, 19, 3, 1.11),
        #(StatPerLevel.GOOD, StatPerLevel.WISDOM, 21, 4, 1.14),
        #(StatPerLevel.EXCELLENT, StatPerLevel.WISDOM, 23, 5, 1.17),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.MOVEMENT_SPEED, 7, 0.5, 0.7),
        (StatPerLevel.BAD, StatPerLevel.MOVEMENT_SPEED, 9, 1, 0.8),
        (StatPerLevel.DECENT, StatPerLevel.MOVEMENT_SPEED, 11, 1.5, 0.9),
        (StatPerLevel.GOOD, StatPerLevel.MOVEMENT_SPEED, 13, 2, 1),
        (StatPerLevel.EXCELLENT, StatPerLevel.MOVEMENT_SPEED, 15, 2.5, 1.1),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.CRAFTING_SPEED, 7, 0.5, 0.7),
        (StatPerLevel.BAD, StatPerLevel.CRAFTING_SPEED, 9, 1, 0.8),
        (StatPerLevel.DECENT, StatPerLevel.CRAFTING_SPEED, 11, 1.5, 0.9),
        (StatPerLevel.GOOD, StatPerLevel.CRAFTING_SPEED, 13, 2, 1),
        (StatPerLevel.EXCELLENT, StatPerLevel.CRAFTING_SPEED, 15, 2.5, 1.1),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.GATHERING_SPEED, 7, 0.5, 0.7),
        (StatPerLevel.BAD, StatPerLevel.GATHERING_SPEED, 9, 1, 0.8),
        (StatPerLevel.DECENT, StatPerLevel.GATHERING_SPEED, 11, 1.5, 0.9),
        (StatPerLevel.GOOD, StatPerLevel.GATHERING_SPEED, 13, 2, 1),
        (StatPerLevel.EXCELLENT, StatPerLevel.GATHERING_SPEED, 15, 2.5, 1.1),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.HITPOINTS, 32, 10, 1.09),
        (StatPerLevel.BAD, StatPerLevel.HITPOINTS, 38, 12, 1.12),
        (StatPerLevel.DECENT, StatPerLevel.HITPOINTS, 44, 14, 1.15),
        (StatPerLevel.GOOD, StatPerLevel.HITPOINTS, 50, 16, 1.18),
        (StatPerLevel.EXCELLENT, StatPerLevel.HITPOINTS, 56, 18, 1.21),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.CRITICAL, 1, 0.5, 0.5),
        (StatPerLevel.BAD, StatPerLevel.CRITICAL, 2, 1, 0.6),
        (StatPerLevel.DECENT, StatPerLevel.CRITICAL, 3, 1.5, 0.7),
        (StatPerLevel.GOOD, StatPerLevel.CRITICAL, 4, 2, 0.8),
        (StatPerLevel.EXCELLENT, StatPerLevel.CRITICAL, 5, 2.5, 0.9),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.DEFENSE, 4, 1.5, 0.6),
        (StatPerLevel.BAD, StatPerLevel.DEFENSE, 6, 2.5, 0.7),
        (StatPerLevel.DECENT, StatPerLevel.DEFENSE, 8, 3.5, 0.8),
        (StatPerLevel.GOOD, StatPerLevel.DEFENSE, 10, 4.5, 0.9),
        (StatPerLevel.EXCELLENT, StatPerLevel.DEFENSE, 12, 5.5, 1),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.POWER, 10, 4.5, 0.7),
        (StatPerLevel.BAD, StatPerLevel.POWER, 11, 5.5, 0.8),
        (StatPerLevel.DECENT, StatPerLevel.POWER, 12, 6.5, 0.9),
        (StatPerLevel.GOOD, StatPerLevel.POWER, 13, 7.5, 1),
        (StatPerLevel.EXCELLENT, StatPerLevel.POWER, 14, 8.5, 1.1),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.HIT_CHANCE, 8, 2.5, 0.6),
        (StatPerLevel.BAD, StatPerLevel.HIT_CHANCE, 9, 3, 0.65),
        (StatPerLevel.DECENT, StatPerLevel.HIT_CHANCE, 10, 3.5, 0.7),
        (StatPerLevel.GOOD, StatPerLevel.HIT_CHANCE, 11, 4, 0.75),
        (StatPerLevel.EXCELLENT, StatPerLevel.HIT_CHANCE, 12, 4.5, 0.8),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.BLOCK, 4, 1, 0.3),
        (StatPerLevel.BAD, StatPerLevel.BLOCK, 7, 2, 0.4),
        (StatPerLevel.DECENT, StatPerLevel.BLOCK, 10, 3, 0.5),
        (StatPerLevel.GOOD, StatPerLevel.BLOCK, 13, 4, 0.6),
        (StatPerLevel.EXCELLENT, StatPerLevel.BLOCK, 16, 5, 0.7),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.CARGO, 10, 1, 0.4),
        (StatPerLevel.BAD, StatPerLevel.CARGO, 12, 1.5, 0.45),
        (StatPerLevel.DECENT, StatPerLevel.CARGO, 14, 2, 0.5),
        (StatPerLevel.GOOD, StatPerLevel.CARGO, 16, 2.5, 0.55),
        (StatPerLevel.EXCELLENT, StatPerLevel.CARGO, 18, 3, 0.6),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.WEIGHT, 4, 2, 0.35),
        (StatPerLevel.BAD, StatPerLevel.WEIGHT, 5, 2.5, 0.4),
        (StatPerLevel.DECENT, StatPerLevel.WEIGHT, 6, 3, 0.45),
        (StatPerLevel.GOOD, StatPerLevel.WEIGHT, 7, 3.5, 0.5),
        (StatPerLevel.EXCELLENT, StatPerLevel.WEIGHT, 8, 4, 0.55),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.TRADE_ORDERS, 2, 3.5, 0.5),
        (StatPerLevel.BAD, StatPerLevel.TRADE_ORDERS, 3, 4.5, 0.6),
        (StatPerLevel.DECENT, StatPerLevel.TRADE_ORDERS, 4, 5.5, 0.7),
        (StatPerLevel.GOOD, StatPerLevel.TRADE_ORDERS, 5, 6.5, 0.8),
        (StatPerLevel.EXCELLENT, StatPerLevel.TRADE_ORDERS, 6, 7.5, 0.9),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.TAX_REDUCTION, 4, 2.5, 0.25),
        (StatPerLevel.BAD, StatPerLevel.TAX_REDUCTION, 5, 3.5, 0.35),
        (StatPerLevel.DECENT, StatPerLevel.TAX_REDUCTION, 6, 4.5, 0.45),
        (StatPerLevel.GOOD, StatPerLevel.TAX_REDUCTION, 7, 5.5, 0.55),
        (StatPerLevel.EXCELLENT, StatPerLevel.TAX_REDUCTION, 8, 6.5, 0.65),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.CONTRACTS, 0, 0.1, 0.3),
        (StatPerLevel.BAD, StatPerLevel.CONTRACTS, 0, 0.3, 0.4),
        (StatPerLevel.DECENT, StatPerLevel.CONTRACTS, 0, 0.5, 0.5),
        (StatPerLevel.GOOD, StatPerLevel.CONTRACTS, 0, 0.7, 0.6),
        (StatPerLevel.EXCELLENT, StatPerLevel.CONTRACTS, 0, 0.9, 0.7),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.EFFICIENCY, 10, 1, 0.4),
        (StatPerLevel.BAD, StatPerLevel.EFFICIENCY, 12, 1.5, 0.47),
        (StatPerLevel.DECENT, StatPerLevel.EFFICIENCY, 14, 2, 0.54),
        (StatPerLevel.GOOD, StatPerLevel.EFFICIENCY, 16, 2.5, 0.61),
        (StatPerLevel.EXCELLENT, StatPerLevel.EFFICIENCY, 18, 3, 0.68),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.MULTITASKING, 10, 0, 0.4),
        (StatPerLevel.BAD, StatPerLevel.MULTITASKING, 12, 0, 0.47),
        (StatPerLevel.DECENT, StatPerLevel.MULTITASKING, 14, 0, 0.54),
        (StatPerLevel.GOOD, StatPerLevel.MULTITASKING, 16, 0, 0.61),
        (StatPerLevel.EXCELLENT, StatPerLevel.MULTITASKING, 18, 0, 0.68),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.ENDURANCE, 4, 1, 0.4),
        (StatPerLevel.BAD, StatPerLevel.ENDURANCE, 6, 2, 0.47),
        (StatPerLevel.DECENT, StatPerLevel.ENDURANCE, 8, 3, 0.54),
        (StatPerLevel.GOOD, StatPerLevel.ENDURANCE, 10, 4, 0.61),
        (StatPerLevel.EXCELLENT, StatPerLevel.ENDURANCE, 12, 5, 0.68),
        
        (StatPerLevel.VERY_BAD, StatPerLevel.LUCK, 4, 1, 0.4),
        (StatPerLevel.BAD, StatPerLevel.LUCK, 5, 2, 0.44),
        (StatPerLevel.DECENT, StatPerLevel.LUCK, 6, 3, 0.48),
        (StatPerLevel.GOOD, StatPerLevel.LUCK, 7, 4, 0.52),
        (StatPerLevel.EXCELLENT, StatPerLevel.LUCK, 8, 5, 0.56),
        
        #(StatPerLevel.VERY_BAD, StatPerLevel., , , ),
        #(StatPerLevel.BAD, StatPerLevel., , , ),
        #(StatPerLevel.DECENT, StatPerLevel., , , ),
        #(StatPerLevel.GOOD, StatPerLevel., , , ),
        #(StatPerLevel.EXCELLENT, StatPerLevel., , , ),
    )
    
    for attribute in all_attributes:
        StatPerLevel.objects.create(
            quality = attribute[0],
            attribute = attribute[1],
            start_value = attribute[2],
            level_bonus = attribute[3],
            multiplier = attribute[4],
        )


add_stats_per_level()










#################### Town Objects ######################
#starting values
def add_first_town_version():
    TownMathValues.objects.create(
        version = 1,
        tavern_refresh_min = 20*60,
        tavern_refresh_max = 60*60,
        tavern_heroes_min = 7,
        tavern_heroes_max = 14,
    )

add_first_town_version()











def add_admin():
    user = User.objects.create_user('Ikke', "slikke@ikkes.pikke", "1234")
    Profile.create_profile(user)
add_admin()
