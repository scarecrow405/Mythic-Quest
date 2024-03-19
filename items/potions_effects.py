def get_next_level_experience_threshold(character):
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
        11: 12000,
        12: 15000,
        13: 18000,
        14: 22000,
        15: 26000,
        16: 31000,
        17: 37000,
        18: 44000,
        19: 52000,
        20: 61000,
        21: 71000,
        22: 82000,
        23: 94000,
        24: 107000,
        25: 122000,
        26: 138000,
        27: 155000,
        28: 173000,
        29: 192000,
        30: 212000,
        31: 233000,
        32: 255000,
        33: 278000,
        34: 302000,
        35: 327000,
        36: 353000,
        37: 380000,
        38: 408000,
        39: 437000,
        40: 467000,
        41: 498000,
        42: 530000,
        43: 563000,
        44: 597000,
        45: 632000,
        46: 668000,
        47: 705000,
        48: 743000,
        49: 782000,
        50: 822000,
    }

    current_max_level = 50
    exp_threshold = level_thresholds.get(min(character.level + 1, current_max_level))

    return exp_threshold


def apply_experience_potion(character, potion):
    exp_threshold = get_next_level_experience_threshold(character)
    exp_boost = exp_threshold * potion.boost_amount_percentage / 100
    return exp_boost


def apply_health_potion(character, potion):
    max_health_threshold = character.max_health
    max_health_boost = max_health_threshold * potion.boost_amount_percentage / 100
    return max_health_boost


def apply_strength_potion(character, potion):
    strength_threshold = character.strength
    strength_boost = strength_threshold * potion.boost_amount_percentage / 100
    return strength_boost


def apply_agility_potion(character, potion):
    agility_threshold = character.agility
    agility_boost = agility_threshold * potion.boost_amount_percentage / 100
    return agility_boost


def apply_damage_potion(character, potion):
    damage_threshold = character.damage
    damage_boost = damage_threshold * potion.boost_amount_percentage / 100
    return damage_boost


def apply_armor_potion(character, potion):
    armor_threshold = character.armor
    armor_boost = armor_threshold * potion.boost_amount_percentage / 100
    return armor_boost


def apply_ultra_potion(character, potion):
    all_bonus_stats = []

    for stat_name, stat_value in get_list_of_character_stats(character).items():
        boost = stat_value * potion.boost_amount_percentage / 100
        all_bonus_stats.append(boost)

    return all_bonus_stats


def get_list_of_character_stats(character):
    character_stats = {
        'max_health': character.max_health,
        'strength': character.strength,
        'agility': character.agility,
        'damage': character.damage,
        'armor': character.armor,
    }

    return character_stats
