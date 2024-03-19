import random
from math import ceil

from characters.get_character_level import get_character_level


def resolve_fight(character, enemy):
    # Calculate Win chance
    win_chance = calculate_win_chance(character.rating, enemy.rating, character.level, enemy.level)
    if random.randint(1, 100) <= win_chance:
        winner = character
    elif win_chance == 0:
        level_multiplier = abs(character.level - enemy.level)
        lucky_chance = random.randint(1, 100 * level_multiplier)
        winner = character if lucky_chance == 1 else enemy
    else:
        winner = enemy

    gained_exp = 0
    gained_gold = 0
    stolen_gold = 0

    if winner == character:
        # Enemy DMG & Your DMG
        enemy_damage = enemy.damage / 2
        your_damage = character.damage

        # Fight
        character.health = max(0, character.health - enemy_damage)

        # If character still alive
        if character.health > 0:
            enemy.health = max(0, enemy.health - your_damage)

            # Gain EXP
            gained_exp = fight_experience_gain(character.level, enemy.level)
            character.experience += gained_exp

            # Gain LVL
            current_level = character.level
            character.level = get_character_level(character.experience)

            # Increase all stats if lvl up!
            if current_level != character.level:
                all_stats_increase(character)

            # Gold Stolen
            if character.level >= enemy.level:
                stolen_gold_multiplier = max(1, abs(character.level - enemy.level)) / 50
            else:
                stolen_gold_multiplier = abs(character.level - enemy.level) / (enemy.level / 2) / 25

            stolen_gold_percentage = 1 - stolen_gold_multiplier
            stolen_gold = ceil(enemy.gold * stolen_gold_multiplier)

            character.gold = ceil(character.gold + stolen_gold)
            enemy.gold = ceil(enemy.gold * stolen_gold_percentage)

            # Gain Gold
            gained_gold = gold_gained(character.level)
            character.gold += gained_gold

    else:
        enemy_damage = enemy.damage * 1.3
        your_damage = character.damage / 2
        # Fight
        character.health = max(0, character.health - enemy_damage)
        if character.health > 0:
            enemy.health = max(0, enemy.health - your_damage)

    # Save into DB -----------------------<
    character.save()
    enemy.save()

    return winner, gained_exp, gained_gold, stolen_gold, win_chance


# Calculate win chance logic
def calculate_win_chance(character_rating, enemy_rating, character_level, enemy_level):
    rating_difference = enemy_rating - character_rating
    level_difference = enemy_level - character_level

    # Base win chance
    base_win_chance = 50

    rating_adjustment = min(abs(rating_difference) / random.randint(8, 13),
                            random.randint(18, 28))  # Maximum adjustment of 28%
    if rating_difference > 0:
        base_win_chance -= rating_adjustment
    elif rating_difference < 0:
        base_win_chance += rating_adjustment

    level_adjustment = min(abs(level_difference) * random.randint(3, 7),
                           random.randint(36, 46))  # Maximum adjustment of 46%
    if level_difference > 0:
        base_win_chance -= level_adjustment
    elif level_difference < 0:
        base_win_chance += level_adjustment

    return max(min(base_win_chance, 100), 0)  # Win chance is between 0 and 100%


def gold_gained(player_level):
    base_gold_gain = {
        1: (50, 300),
        2: (80, 400),
        3: (111, 500),
        4: (140, 600),
        5: (210, 700),
        6: (290, 900),
        7: (420, 1000),
        8: (509, 1100),
        9: (630, 1200),
        10: (780, 1300),
        11: (950, 1400),
        12: (1100, 1500),
        13: (1270, 1600),
        14: (1450, 1700),
        15: (1640, 1800),
        16: (1840, 1900),
        17: (2050, 2200),
        18: (2270, 2400),
        19: (2500, 2700),
        20: (2740, 2900),
        21: (2990, 3000),
        22: (3250, 3500),
        23: (3520, 3700),
        24: (3800, 4000),
        25: (4090, 4300),
        26: (4390, 4700),
        27: (4700, 5000),
        28: (5020, 5300),
        29: (5350, 5600),
        30: (5690, 6000),
        31: (6040, 6400),
        32: (6400, 6700),
        33: (6770, 7100),
        34: (7150, 7500),
        35: (7540, 7800),
        36: (7940, 8200),
        37: (8350, 8700),
        38: (8770, 9100),
        39: (9200, 9500),
        40: (9640, 9900),
        41: (10090, 10300),
        42: (10550, 11000),
        43: (11020, 11590),
        44: (11500, 11900),
        45: (11990, 12000),
        46: (12490, 13000),
        47: (13000, 13500),
        48: (13520, 14000),
        49: (14050, 14500),
        50: (14590, 15000),
    }

    base_range = base_gold_gain.get(player_level)

    min_experience_gain = int(base_range[0])
    max_experience_gain = int(base_range[1])

    gold_gain = random.randint(min_experience_gain, max_experience_gain)
    return gold_gain


def fight_experience_gain(player_level, opponent_level):
    base_experience_gain = {
        1: (10, 30),
        2: (20, 40),
        3: (30, 50),
        4: (40, 60),
        5: (50, 70),
        6: (60, 90),
        7: (70, 100),
        8: (80, 110),
        9: (90, 120),
        10: (100, 130),
        11: (110, 140),
        12: (120, 150),
        13: (130, 160),
        14: (140, 170),
        15: (150, 180),
        16: (160, 190),
        17: (170, 200),
        18: (180, 210),
        19: (190, 220),
        20: (200, 230),
        21: (210, 240),
        22: (220, 250),
        23: (230, 260),
        24: (240, 270),
        25: (250, 280),
        26: (260, 290),
        27: (270, 300),
        28: (280, 310),
        29: (290, 320),
        30: (300, 330),
        31: (310, 340),
        32: (320, 350),
        33: (330, 360),
        34: (340, 370),
        35: (350, 380),
        36: (360, 390),
        37: (370, 400),
        38: (380, 410),
        39: (390, 420),
        40: (400, 430),
        41: (410, 440),
        42: (420, 450),
        43: (430, 460),
        44: (440, 470),
        45: (450, 480),
        46: (460, 490),
        47: (470, 500),
        48: (480, 510),
        49: (490, 520),
        50: (500, 530),
    }

    base_range = base_experience_gain.get(player_level)

    level_difference = abs(player_level - opponent_level)
    modifier = max(0, 1 - (level_difference / 10))

    min_experience_gain = int(base_range[0] * modifier)
    max_experience_gain = int(base_range[1] * modifier)

    experience_gain = random.randint(min_experience_gain, max_experience_gain)
    return experience_gain


def all_stats_increase(character) -> None:
    base_increase = {
        "max_health": 25,
        "health": 25,
        "strength": 12,
        "agility": 7,
        "damage": 10,
        "armor": 5
    }

    character.max_health += base_increase.get("max_health") * character.level
    character.health += base_increase.get("health") * character.level
    character.strength += base_increase.get("strength") * character.level
    character.agility += base_increase.get("agility") * character.level
    character.damage += base_increase.get("damage") * character.level
    character.armor += base_increase.get("armor") * character.level
