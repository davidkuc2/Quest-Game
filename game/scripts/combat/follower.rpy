init python:
    import copy

    class Follower_Character(Combat_Character):
        def __init__(self, name, max_hp, hp, atk, damage, weakness, resistance, element, power, grade=0, image=None, unlocked=False):
            Combat_Character.__init__(self, name, max_hp, hp, atk, damage, grade, image)
            self.weakness = weakness
            self.resistance = resistance
            self.element = element
            self.power = power
            self.unlocked = unlocked

        def unlock(self):
            self.unlocked = True
            if self not in all_followers:
                all_followers.append(self)
                renpy.notify("New Follower: " + self.name)

    class Power():
        def __init__(self, name, label_name):
            self.name = name
            self.label_name = label_name

    def equip_follower(new_follower):
        global follower
        
        if follower == new_follower:
            unequip_follower()
        else:
            # If we are equipping a different follower, swap them
            follower = new_follower
            renpy.restart_interaction()

    def unequip_follower():
        global follower
        # Reset to a dummy/empty follower
        follower = Follower_Character("", 0, 0, 0, 0, [], [], [], None, 0, None)
        renpy.restart_interaction()


# Define Followers
default follower = Follower_Character("", 0, 0, 0, 0, [], [], [], None, 0, None)
default green_slime = Follower_Character("Green Slime", 10, 10, 2, 0, ["fire"], ["water", "slime"], ["slime"], None, 1, "images/enemies/green_slime", False)
default all_followers = []


# Define Powers
default power_heal = Power("Heal", "power_heal")
default power_smite = Power("Smite", "power_smite")


# Screen for the follower's turn
screen follower_turn:
    modal True
    zorder 101

    use call_image_button_no_target(attack, Call("follower_attack"))
    if follower.power:
        use call_image_button_no_target(power, If((turn_count - 1) % 3 == 0, power.action, None))


# Follower Attack
label follower_attack:                                              # follower turn after same logic

    $ roll = renpy.random.randint(1, 10)
    if any(elem in enemy.weakness for elem in follower.element):
        "The enemy is susceptible to your follower's element!"
        $ follower.damage = follower.atk*2
    elif any(elem in enemy.resistance for elem in follower.element):
        "The enemy is resistant to your follower's element!"
        $ follower.damage = int(follower.atk/2)
    else:
        $ follower.damage = follower.atk

    if roll == 10:
        "Critical Hit!"
        $ follower.damage = int(follower.damage*1.5)

    $ enemy.hp -= follower.damage
    if enemy.hp < 0:
        $ enemy.hp = 0
    "Your follower deals [follower.damage] damage to the enemy!"
            
    if enemy.hp > 0:
        return
    else:
        "You win!"
        jump combat_reward

# Follower Powers
label follower_power:

    if follower.power:
        call expression follower.power.label_name
    else:
        "Your follower has no power to use!"
    return

# Healing
label power_heal:
    $ heal_amount = int(follower.grade*2)
    $ player_combat.hp += heal_amount
    if player_combat.hp > player_combat.max_hp:
        $ player_combat.hp = player_combat.max_hp
    "Your follower heals you for [heal_amount] HP!"
    return

# Defence
label power_defend:
    "Your follower protects you!"
    $ player_combat.defence = True
    return

# Powerful Attack
label power_smite:
    "Your follower charges a powerful strike!"
    
    if any(elem in enemy.weakness for elem in follower.element):
        "The enemy is susceptible to your follower's element!"
        $ follower.damage = follower.grade*2+follower.atk*2
    elif any(elem in enemy.resistance for elem in follower.element):
        "The enemy is resistant to your follower's element!"
        $ follower.damage = int(follower.grade*2+follower.atk/2)
    else:
        $ follower.damage = follower.grade*2+follower.atk

    $ roll = renpy.random.randint(1, 10)
    if roll == 10:
        "Critical Hit!"
        $ follower.damage = int(follower.damage * 1.5)

    $ enemy.hp -= follower.damage
    if enemy.hp < 0:
        $ enemy.hp = 0
    "Your follower deals [follower.damage] damage to the enemy!"
            
    if enemy.hp > 0:
        return
    else:
        "You win!"
        jump combat_reward

# Double Attack
label power_multi_attack:
    "Your follower attacks twice!"
    call follower_attack   
    call follower_attack
    return