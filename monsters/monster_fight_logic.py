import random


def monster_fight(character, monster):
    # Calculate Win chance
    win_chance = calculate_win_chance(character.rating, monster.rating, character.level, monster.level)

    if random.randint(1, 100) <= win_chance:
        winner = character
    elif win_chance == 0:
        level_multiplier = abs(character.level - monster.level)
        lucky_chance = random.randint(1, 100 * level_multiplier)
        winner = character if lucky_chance == 1 else monster
    else:
        winner = monster

    gained_exp = 0
    gained_gold = 0

    if winner == character:
        # Monster DMG & Your DMG
        enemy_damage = monster.damage

        # Take Damage
        character.health = max(0, character.health - enemy_damage)

        # If character still alive
        if character.health > 0:
            # Gain EXP
            gained_exp = fight_experience_gain(character.level, monster.level)
            character.experience += gained_exp

            # Gain LVL
            current_level = character.level
            character.level = get_character_level(character.experience)

            # Increase all stats if lvl up!
            if current_level != character.level:
                all_stats_increase(character)

            # Gain Gold
            gained_gold = gold_gained(monster.name)
            character.gold += gained_gold

    else:
        enemy_damage = monster.damage * 2
        # Take Increased Damage if winner is Monster
        character.health = max(0, character.health - enemy_damage)

    # Save into DB -----------------------<
    character.save()

    return winner, gained_exp, gained_gold, win_chance, enemy_damage


# Calculate win chance logic
def calculate_win_chance(character_rating, monster_rating, character_level, monster_level):
    rating_difference = monster_rating - character_rating
    level_difference = monster_level - character_level

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


def gold_gained(monster_name):
    base_gold_gain = {
        "Scarab Beetle": (100, 300),
        "Evil Mummy": (500, 1500),
        "Anubis": (2000, 6000),
        "Judge the Destroyer": (999999, 99999999),
    }

    base_range = base_gold_gain.get(monster_name)

    min_gold_gain = int(base_range[0])
    max_gold_gain = int(base_range[1])

    gold_gain = random.randint(min_gold_gain, max_gold_gain)
    return gold_gain


def fight_experience_gain(player_level, monster_level):
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

    level_difference = abs(player_level - monster_level)
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
