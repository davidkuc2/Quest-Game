init python:
    import copy

    class Enemy_Character(Combat_Character):
        def __init__(self, name, max_hp, hp, atk, damage, weakness, resistance, element, grade=0, image=None):
            Combat_Character.__init__(self, name, max_hp, hp, atk, damage, grade, image)
            self.weakness = weakness            # doubles damage taken
            self.resistance = resistance        # halves damage taken
            self.element = element              # doubles damage dealt 


# Define Enemies
default enemy = Enemy_Character("", 0, 0, 0, [], [], [], 0, "")


# Enemy Turn
label enemy_turn:                                                   # enemy turn after same logic      

    $ target = player_combat                                        # allows to set target

    if follower.hp > 0:
        $ roll = renpy.random.randint(1, 2)
        if roll == 1:
            $ target = player_combat
            "The enemy targets you!"
        else:
            $ target = follower
            "The enemy targets your follower!"
    else:
        "The enemy targets you!"

    $ roll = renpy.random.randint(1, 10)
    $ equipped_armor = inventory.equipped.get("armor")              # get currently equipped armor
    if equipped_armor and any(elem in equipped_armor.resistance for elem in enemy.element):
        "Your armor is resistant to the enemy's element!"
        $ enemy.damage = int(enemy.atk/2)
    elif equipped_armor and any(elem in equipped_armor.weakness for elem in enemy.element):
        "Your armor is susceptible to the enemy's element!"
        $ enemy.damage = enemy.atk*2
    else:
        $ enemy.damage = enemy.atk

    if roll == 10:
        "Critical Hit!"
        $ enemy.damage = int(enemy.damage*1.5)

    if target == player_combat and player_combat.defence == True:
        "You defend some of the damage!"
        $ enemy.damage = int(enemy.damage/1.5)
        $ player_combat.defence = False

    $ target.hp -= enemy.damage
    if target.hp < 0:
        $ target.hp = 0
    "The enemy deals [enemy.damage] damage!"

    if player_combat.hp > 0:
        return
    else:
        "You lose!"
        jump combat_loss

    if follower.hp > 0:
        return
    else:
        "Your follower falls and can no longer assist you!"
        return