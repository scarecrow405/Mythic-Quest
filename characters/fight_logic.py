import random
from math import ceil


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


def get_character_level(character_experience):
    level_thresholds = {
        1: 100,
        2: 200,
        3: 400,
        4: 800,
        5: 1600,
        6: 2500,
        7: 4000,
        8: 6400,
        9: 8100,
        10: 10000,
    }
    level = 1

    for lvl, threshold in level_thresholds.items():
        if character_experience >= threshold:
            level = lvl
    return level
