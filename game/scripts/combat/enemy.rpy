init python:
    import copy

    class Enemy_Character(Combat_Character):
        def __init__(self, name, max_hp, hp, attack_dice, damage, weakness, resistance, element, grade=0, image=None):
            Combat_Character.__init__(self, name, max_hp, hp, attack_dice, damage, grade, image)
            self.weakness = weakness            # doubles damage taken
            self.resistance = resistance        # halves damage taken
            self.element = element              # doubles damage dealt 


# Define Enemies
default enemy = Enemy_Character("", 0, 0, "", 0, [], [], [], 0, "")


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

    $ base_damage_roll = roll_dice(enemy.attack_dice)
    $ bonus_dice_roll = roll_dice("+".join(enemy.attack_bonus_dice_list)) if enemy.attack_bonus_dice_list else 0
    $ total_base_damage = (base_damage_roll + bonus_dice_roll + enemy.attack_bonus_flat) * enemy.attack_multiplier

    if target == player_combat:
        $ equipped_armor = inventory.equipped.get("armor")              # get currently equipped armor
        if equipped_armor and any(elem in equipped_armor.resistance for elem in enemy.element):
            "Your armor is resistant to the enemy's element!"
            $ enemy.damage = int(total_base_damage / 2)
        elif equipped_armor and any(elem in equipped_armor.weakness for elem in enemy.element):
            "Your armor is susceptible to the enemy's element!"
            $ enemy.damage = total_base_damage * 2
        else:
            $ enemy.damage = total_base_damage

        if player_combat.defence == True:
            "You defend some of the damage!"
            $ enemy.damage = int(enemy.damage/1.5)
            $ player_combat.defence = False

    elif target == follower:
        if any(elem in follower.resistance for elem in enemy.element):
            "Your follower is resistant to the enemy's element!"
            $ enemy.damage = int(total_base_damage / 2)
        elif any(elem in follower.weakness for elem in enemy.element):
            "Your follower is susceptible to the enemy's element!"
            $ enemy.damage = total_base_damage * 2
        else:
            $ enemy.damage = total_base_damage

    $ roll = renpy.random.randint(1, 10)
    if roll == 10:
        "Critical Hit!"
        $ enemy.damage = int(enemy.damage*1.5)

    $ target.hp -= enemy.damage
    if target.hp < 0:
        $ target.hp = 0
    "The enemy deals [enemy.damage] damage!"

    if player_combat.hp <= 0:
        "You lose!"
        jump combat_loss

    # Check if the follower died this turn
    if target == follower and follower.hp <= 0:
        "Your follower falls and can no longer assist you!"

    return