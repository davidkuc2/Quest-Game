init python:
    import copy

    class Player_Character(Combat_Character):
        def __init__(self, name, max_hp, hp, attack_dice, damage=0, grade=1, defence=False, charisma=0,
            attack_bonus_flat=0, attack_bonus_dice_list=None, attack_multiplier=1.0):
            Combat_Character.__init__(self, name, max_hp, hp, attack_dice, damage, grade)
            self.defence = defence              # used in combat to lower damage taken
            self.charisma = charisma            # used for out of combat interactions
            # Buffs only apply to the player
            self.attack_bonus_flat = attack_bonus_flat
            self.attack_bonus_dice_list = attack_bonus_dice_list if attack_bonus_dice_list is not None else []
            self.attack_multiplier = attack_multiplier

# Define Player 
default player_combat = Player_Character("[player_name]", 10, 10, "1d6", 0, 1, False, 0, 0, None, 1.0)


# Screen for the player's turn
screen player_turn:
    modal True
    zorder 101

    use call_image_button_no_target(attack, [Call("player_attack"), Hide("player_turn")])
    use call_image_button_no_target(defend, If(not player_combat.defence, [defend.action, Hide("player_turn")], None))


# Player Attack
label player_attack:                                                        # player turn

    $ base_damage_roll = roll_dice(player_combat.attack_dice)
    $ bonus_dice_roll = roll_dice("+".join(player_combat.attack_bonus_dice_list)) if player_combat.attack_bonus_dice_list else 0
    $ total_base_damage = (base_damage_roll + bonus_dice_roll + player_combat.attack_bonus_flat) * player_combat.attack_multiplier

    $ equipped_weapon = inventory.equipped.get("weapon")                    # get currently equipped weapon
    if equipped_weapon and any(elem in enemy.weakness for elem in equipped_weapon.element):       # check for weakness
        "The enemy is susceptible to your weapon element!"
        $ player_combat.damage = int(total_base_damage * 2)
    elif equipped_weapon and any(elem in enemy.resistance for elem in equipped_weapon.element):   # check for resistance
        "The enemy is resistant to your weapon element!"
        $ player_combat.damage = int(total_base_damage / 2)
    else:
        $ player_combat.damage = int(total_base_damage)

    $ roll = renpy.random.randint(1, 10)                                    # randomize for crit
    if roll == 10:                                                          # try crit hit
        "Critical Hit!"
        if player_combat.damage > 0:
            $ player_combat.damage = max(int(player_combat.damage * 1.5), player_combat.damage + 1)

    $ enemy.hp -= player_combat.damage                                      # apply damage 
    if enemy.hp < 0:
        $ enemy.hp = 0
    "You deal [player_combat.damage] damage to the enemy!"

    if enemy.hp > 0:                                                        # check if enemy is alive and continue
        return
    else:
        "You win!"
        jump combat_reward                                                  # end combat

#Player Defence
label player_defend:                                                        # defend next attack

    "You steady yourself for the next attack!"
    $ player_combat.defence = True
    return
