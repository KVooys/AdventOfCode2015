"""
--- Day 22: Wizard Simulator 20XX ---
Little Henry Case decides that defeating bosses with swords and stuff is boring. Now he's playing the game with a wizard. Of course, he gets stuck on another boss and needs your help again.

In this version, combat still proceeds with the player and the boss taking alternating turns. The player still goes first. Now, however, you don't get any equipment; instead, you must choose one of your spells to cast. The first character at or below 0 hit points loses.

Since you're a wizard, you don't get to wear armor, and you can't attack normally. However, since you do magic damage, your opponent's armor is ignored, and so the boss effectively has zero armor as well. As before, if armor (from a spell, in this case) would reduce damage below 1, it becomes 1 instead - that is, the boss' attacks always deal at least 1 damage.

On each of your turns, you must select one of your spells to cast. If you cannot afford to cast any spell, you lose. Spells cost mana; you start with 500 mana, but have no maximum limit. You must have enough mana to cast a spell, and its cost is immediately deducted when you cast it. Your spells are Magic Missile, Drain, Shield, Poison, and Recharge.

Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
Effects all work the same way. Effects apply at the start of both the player's turns and the boss' turns. Effects are created with a timer (the number of turns they last); at the start of each turn, after they apply any effect they have, their timer is decreased by one. If this decreases the timer to zero, the effect ends. You cannot cast a spell that would start an effect which is already active. However, effects can be started on the same turn they end.

For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:

-- Player turn --
- Player has 10 hit points, 0 armor, 250 mana
- Boss has 13 hit points
Player casts Poison.

-- Boss turn --
- Player has 10 hit points, 0 armor, 77 mana
- Boss has 13 hit points
Poison deals 3 damage; its timer is now 5.
Boss attacks for 8 damage.

-- Player turn --
- Player has 2 hit points, 0 armor, 77 mana
- Boss has 10 hit points
Poison deals 3 damage; its timer is now 4.
Player casts Magic Missile, dealing 4 damage.

-- Boss turn --
- Player has 2 hit points, 0 armor, 24 mana
- Boss has 3 hit points
Poison deals 3 damage. This kills the boss, and the player wins.
Now, suppose the same initial conditions, except that the boss has 14 hit points instead:

-- Player turn --
- Player has 10 hit points, 0 armor, 250 mana
- Boss has 14 hit points
Player casts Recharge.

-- Boss turn --
- Player has 10 hit points, 0 armor, 21 mana
- Boss has 14 hit points
Recharge provides 101 mana; its timer is now 4.
Boss attacks for 8 damage!

-- Player turn --
- Player has 2 hit points, 0 armor, 122 mana
- Boss has 14 hit points
Recharge provides 101 mana; its timer is now 3.
Player casts Shield, increasing armor by 7.

-- Boss turn --
- Player has 2 hit points, 7 armor, 110 mana
- Boss has 14 hit points
Shield's timer is now 5.
Recharge provides 101 mana; its timer is now 2.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 1 hit point, 7 armor, 211 mana
- Boss has 14 hit points
Shield's timer is now 4.
Recharge provides 101 mana; its timer is now 1.
Player casts Drain, dealing 2 damage, and healing 2 hit points.

-- Boss turn --
- Player has 3 hit points, 7 armor, 239 mana
- Boss has 12 hit points
Shield's timer is now 3.
Recharge provides 101 mana; its timer is now 0.
Recharge wears off.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 2 hit points, 7 armor, 340 mana
- Boss has 12 hit points
Shield's timer is now 2.
Player casts Poison.

-- Boss turn --
- Player has 2 hit points, 7 armor, 167 mana
- Boss has 12 hit points
Shield's timer is now 1.
Poison deals 3 damage; its timer is now 5.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 1 hit point, 7 armor, 167 mana
- Boss has 9 hit points
Shield's timer is now 0.
Shield wears off, decreasing armor by 7.
Poison deals 3 damage; its timer is now 4.
Player casts Magic Missile, dealing 4 damage.

-- Boss turn --
- Player has 1 hit point, 0 armor, 114 mana
- Boss has 2 hit points
Poison deals 3 damage. This kills the boss, and the player wins.
You start with 50 hit points and 500 mana points. The boss's actual stats are in your puzzle input. What is the least amount of mana you can spend and still win the fight? (Do not include mana recharge effects as "spending" negative mana.)
"""

import pprint
from dataclasses import dataclass
from collections import defaultdict
from itertools import permutations
from time import sleep
# part 1:  this is another constraint optimization puzzle, similar to part 21.
# First I'll make a Spell class to keep track of things
# Since there's only 5 spells, I'll just add them by hand.

@dataclass
class Spell:
    name: str # keep track of name because the same effect cannot be active twice, might not be necessary
    cost: int
    damage: int = 0
    heal: int = 0
    effect: str = None
    duration: int = 0

# simple representation of spells & effects
spellbook = dict()
spellbook["Magic Missile"] = Spell(name="Magic Missile", cost=53, damage=4)
spellbook["Drain"] = Spell(name="Drain", cost=73, damage=2, heal=2)
spellbook["Shield"] = Spell(name="Shield", cost=113, effect="Shield", duration=6)
spellbook["Poison"] = Spell(name="Poison", cost=173, effect="Poison", duration=6)
spellbook["Recharge"] = Spell(name="Recharge", cost=229, effect="Recharge", duration=5)

# keep track of effects, in the form of {name: duration}
# all effects start inactive with 0 duration
current_effects = {
    "Shield": 0,
    "Poison": 0,
    "Recharge": 0
}

# Judging from the puzzle input:
# This time, the player has no armor and only 50 hp and the boss starts with 10 attack and 71 hp.
# There is no way to kill the boss before he kills you without armor, so keeping up Shield is probably mandatory.
# At the same time, there is no way to win by only spending 500 mana, so keeping up Recharge might also be mandatory.
# Finally, keeping up Poison would also be good since it does the most damage per mana spent.
# Poison does ~0.1 damage per mana, whereas Magic Missile does ~0.075.
# With all 3 effects active, there are Magic Missile & Drain left. Magic Missile is a lot more damage-per-mana efficient than Drain so should get priority.

# standard structure of a turn; effects activate twice, before both characters' turns
def simulate_turn():
    effect_tick()
    player_turn()
    effect_tick()
    boss_turn()

def effect_tick():
    print("Current effects:", current_effects)
    for name, duration in current_effects.items():
        # Resolve active over-time effects.
        if duration > 0:
            if name == "Recharge":
                player["mana"] += 101
            elif name == "Poison":
                boss["HP"] -= 3
            current_effects[name] -= 1
            
            if duration == 0:
                # Armor works differently; instead of an over-time effect, it provides a static +7 to armor. When it wears off, the armor is removed.
                if name == "Shield":
                    player["armor"] = 0
            
                
def player_turn():
    # check available spells first; all the spells without effects, and the effect spells that have no duration left
    available_spells = set()
    for spell in spellbook:
        if spellbook[spell].effect is None:
            available_spells.add(spell)
        elif current_effects[spell] == 0:
            available_spells.add(spell)

    # Cast an available spell
    # My first assumption is that effect spells should take precedence, poison, recharge and shield being the most important for doing damage while staying in the fight.
    # For now I'm going to ignore Drain as it's rarely going to be better than Magic Missile.
    for best_spell in ["Poison", "Recharge", "Shield", "Magic Missile"]:
        if best_spell in available_spells:
            print("Player casts", best_spell)
            # keep track of mana usage
            spent_mana = spellbook[best_spell].cost
            player["mana"] -= spent_mana
            global total_mana
            total_mana += spent_mana
            
            if spellbook[best_spell].effect != None:
                current_effects[best_spell] = spellbook[best_spell].duration
            boss["HP"] -= spellbook[best_spell].damage
            
            # special case for activating armor
            if best_spell == "Shield":
                player["armor"] = 7
            
            # after casting a spell, the player's turn ends
            break
           

# the boss only has 1 attack
def boss_turn():
    print("Boss attacks!")
    player["HP"] -= (boss["damage"] - player["armor"])


# starting stats
player = {"HP": 50, "mana": 500, "armor": 0}
boss = {"HP": 71, "damage": 10}
total_mana = 0

while boss["HP"] > 0:
    simulate_turn()
    pprint.pprint(player)
    pprint.pprint(boss)
    print(total_mana)
    sleep(1)

# Unfortunately the solution that loops while prioritising the 3 effects is not the best solution.
# TODO: create a permutation tree of some kind
# TODO: keep track of lowest mana score for winning branches