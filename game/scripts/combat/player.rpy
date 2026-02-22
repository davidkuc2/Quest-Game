init python:
    import copy

    class Player_Character(Combat_Character):
        def __init__(self, name, max_hp, hp, atk, damage, grade=0, defence=False, charisma=0):
            Combat_Character.__init__(self, name, max_hp, hp, atk, damage, grade)
            self.defence = defence              # used in combat to lower damage taken
            self.charisma = charisma            # used for out of combat interactions


# Define Player 
default player_combat = Player_Character("[player_name]", 15, 15, 4, False, 0)


# Screen for the player's turn
screen player_turn:
    modal True
    zorder 101

    use call_image_button_no_target(attack, Call("player_attack"))
    use call_image_button(defend)


# Player Attack
label player_attack:                                                        # player turn

    $ roll = renpy.random.randint(1, 10)                                    # randomize

    $ equipped_weapon = inventory.equipped.get("weapon")                    # get currently equipped weapon
    if equipped_weapon and any(elem in enemy.weakness for elem in equipped_weapon.element):       # check for weakness
        "The enemy is susceptible to your weapon element!"
        $ player_combat.damage = player_combat.atk*2
    elif equipped_weapon and any(elem in enemy.resistance for elem in equipped_weapon.element):   # check for resistance
        "The enemy is resistant to your weapon element!"
        $ player_combat.damage = int(player_combat.atk/2)
    else:
        $ player_combat.damage = player_combat.atk

    if roll == 10:                                                          # try crit hit
        "Critical Hit!"
        $ player_combat.damage = int(player_combat.damage*1.5)

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
