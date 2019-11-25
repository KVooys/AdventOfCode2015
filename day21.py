"""
--- Day 21: RPG Simulator 20XX ---
Little Henry Case got a new video game for Christmas. It's an RPG, and he's stuck on a boss. He needs to know what equipment to buy at the shop. He hands you the controller.

In this game, the player (you) and the enemy (the boss) take turns attacking. The player always goes first. Each attack reduces the opponent's hit points by at least 1. The first character at or below 0 hit points loses.

Damage dealt by an attacker each turn is equal to the attacker's damage score minus the defender's armor score. An attacker always does at least 1 damage. So, if the attacker has a damage score of 8, and the defender has an armor score of 3, the defender loses 5 hit points. If the defender had an armor score of 300, the defender would still lose 1 hit point.

Your damage score and armor score both start at zero. They can be increased by buying items in exchange for gold. You start with no items and have as much gold as you need. Your total damage or armor is equal to the sum of those stats from all of your items. You have 100 hit points.

Here is what the item shop is selling:

Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
You must buy exactly one weapon; no dual-wielding. Armor is optional, but you can't use more than one. You can buy 0-2 rings (at most one for each hand). You must use any items you buy. The shop only has one of each item, so you can't buy, for example, two rings of Damage +3.

For example, suppose you have 8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage, and 2 armor:

The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.
In this scenario, the player wins! (Barely.)

You have 100 hit points. The boss's actual stats are in your puzzle input. What is the least amount of gold you can spend and still win the fight?
"""

import re
import pprint
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations, product
# part 1: this will mostly involve parsing all the different inputs and finding weapon/armor/ring combinations in a sane way, then finding from the cheapest.

with open("input/day21.txt") as input_file:
    inp = input_file.readlines()


RAW_WEAPONS = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
""".split("\n")

RAW_ARMOR = """
Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
""".split("\n")

RAW_RINGS = """
Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
""".split("\n")

SAMPLE_PLAYER = """
Hit Points: 8
Damage: 5
Armor: 5
""".split("\n")[1:-1]

SAMPLE_BOSS = """
Hit Points: 12
Damage: 7
Armor: 2
""".split("\n")[1:-1]

@dataclass
class Item:
    name: str
    cost: int
    damage: int
    armor: int

@dataclass
class Character:
    HP: int = 100
    damage: int = 0
    armor: int = 0


def parse_items(items, item_dict):
    # function to parse items into a dict
    # Rings have slightly different syntax so the matching has an optional group which makes it look a bit messy
    item_pattern = r"(\w+)\s(\+\d){0,1}\s+(\d+)\s+(\d+)\s+(\d+)"

    # first line is blank, 2nd line is description, take first item & remove colon at the end
    category = items[1].split(" ")[0][:-1]
    for item in items[2:-1]:
        m = re.match(item_pattern, item)
        # special case for rings
        if m.groups()[1] != None:
            name = m.groups()[0] + " " + m.groups()[1]
        else:
            name = m.groups()[0]
        cost, damage, armor = [int(i) for i in m.groups()[2:5]]
        item_dict[category][name] = Item(name=name, cost=cost, damage=damage, armor=armor)

def parse_character(character):
    HP, damage, armor =  [int(line.split(": ")[1]) for line in character]
    return Character(HP=HP, damage=damage, armor=armor)

# find combinations of items
def item_combos(item_dict, num_armor, num_rings):
    for weapon in item_dict["Weapons"].keys():
        # armor is optional
        for armor in [c1 for c1 in combinations(item_dict["Armor"], num_armor)]:
            # rings can be 0, 1 or 2
            for rings in [c2 for c2 in combinations(item_dict["Rings"], num_rings)]:
                combo_list.append((weapon, armor, rings))


def get_all_combos():
    for num_armor in range(0, 2):
        for num_rings in range(0, 3):
            item_combos(item_dict, num_armor, num_rings)

# Predicting the fight outcome is actually not that hard, and simulating the entire fight is unnecessary
# There are 2 important stats: how many turns the player lives, and how many turns the boss lives. 
# They are determined by their HP, damage and armor.
# Since the player gets to start, as long as they live >= x turns and the boss lives x turns or less, the player wins
def simulate_fight(this_player, this_boss):
    # Each attack reduces the opponent's hit points by at least 1
    player_turns = this_player.HP / max(1, (this_boss.damage - this_player.armor))
    boss_turns = this_boss.HP / max(1, (this_player.damage - this_boss.armor))
    # let's keep this function simple and just return True if the player wins
    return player_turns >= boss_turns

def simulate_all_fights(combo_list, boss):
    # some unrealistic number
    lowest_cost = 10000

    for weapon, armor, rings in combo_list:
        # we start with an unequipped player every time
        player = Character(HP=100, damage=0, armor=0)
        

        # keep track of money spent
        total_cost = 0

        # first we "buff" the player by adding the item stats to theirs
        current_weapon = item_dict["Weapons"][weapon]
        player.damage += current_weapon.damage
        total_cost += current_weapon.cost
        if armor:
           current_armor = item_dict["Armor"][armor[0]]
           player.armor += current_armor.armor
           total_cost += current_armor.cost
        if rings:
            for ring in rings:
                current_ring = item_dict["Rings"][ring]
                player.damage += current_ring.damage
                player.armor += current_ring.armor
                total_cost += current_ring.cost
        

        # only simulate the fights if the cost might be the new lowest
        if total_cost <= lowest_cost:
            # print(player, weapon, armor, rings, total_cost)
            # only register costs where the player wins
            if simulate_fight(player, boss): 
                lowest_cost = min(total_cost, lowest_cost)
    return lowest_cost

item_dict = defaultdict(dict)
combo_list = []
parse_items(RAW_WEAPONS, item_dict)
parse_items(RAW_ARMOR, item_dict)
parse_items(RAW_RINGS, item_dict)
# player = parse_character(SAMPLE_PLAYER)
# boss = parse_character(SAMPLE_BOSS)
real_boss = parse_character(inp)
get_all_combos()
print(simulate_all_fights(combo_list, real_boss))

"""
--- Part Two ---
Turns out the shopkeeper is working with the boss, and can persuade you to buy whatever items he wants. The other rules still apply, and he still only has one of each item.

What is the most amount of gold you can spend and still lose the fight?
"""

# part 2 can be solved by rewriting the simulate_all_fights function slightly to account for this newly introduced unfairness:

def simulate_all_unfair_fights(combo_list, boss):
    highest_cost = 0

    for weapon, armor, rings in combo_list:
        # we start with an unequipped player every time
        player = Character(HP=100, damage=0, armor=0)
        

        # keep track of money spent
        total_cost = 0

        # first we "buff" the player by adding the item stats to theirs
        current_weapon = item_dict["Weapons"][weapon]
        player.damage += current_weapon.damage
        total_cost += current_weapon.cost
        if armor:
           current_armor = item_dict["Armor"][armor[0]]
           player.armor += current_armor.armor
           total_cost += current_armor.cost
        if rings:
            for ring in rings:
                current_ring = item_dict["Rings"][ring]
                player.damage += current_ring.damage
                player.armor += current_ring.armor
                total_cost += current_ring.cost
        
        # only simulate fights if the cost might be the new highest
        if total_cost >= highest_cost:
            # only register costs where the player loses
            if not simulate_fight(player, boss):
                highest_cost = max(total_cost, highest_cost)
    return highest_cost

print(simulate_all_unfair_fights(combo_list, real_boss))

# Some food for (after)thought: using itertools.product could have been another way than to generate the combo_list
# They are the same speed, but the syntax would be slightly nicer
# something like this (still need to filter out duplicate rings and add None values to the armor and rings dicts)
# combo_list = [i for i in product(item_dict["Weapons"], item_dict["Armor"], item_dict["Rings"], item_dict["Rings"])]
