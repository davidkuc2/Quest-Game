init python:
    import copy

    class Follower_Character(Combat_Character):
        def __init__(self, name, max_hp, hp, attack_dice, damage, weakness, resistance, element, power, rarity, grade=1, image=None, lootable=False, min_tier=0, unlocked=False):
            Combat_Character.__init__(self, name, max_hp, hp, attack_dice, damage, grade, image)
            self.weakness = weakness
            self.resistance = resistance
            self.element = element
            self.power = power
            self.rarity = rarity
            self.lootable = lootable
            self.min_tier = min_tier
            self.unlocked = unlocked
            
            # Automatically add to the global list (excluding the dummy follower)
            if self.name != "":
                all_followers.append(self)

        def unlock(self):
            if not self.unlocked:
                self.unlocked = True
                renpy.notify("New Follower: " + self.name)

            if not renpy.store.follower_logbook_unlocked:
                renpy.store.follower_logbook_unlocked = True
                renpy.notify("Follower Logbook Unlocked!")

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
        follower = Follower_Character("", 0, 0, "", 0, [], [], [], None, 0, 1)
        renpy.restart_interaction()

# Define Powers
default power_heal = Power("Heal", "power_heal")
default power_defend = Power("Defend", "power_defend")
default power_smite = Power("Smite", "power_smite")
default power_multi_attack = Power("Multi Attack", "power_multi_attack")

# Set Global Progression for Lootboxes
default current_loot_tier = 0

# Define Followers
default all_followers = []
default follower = Follower_Character("", 0, 0, "", 0, [], [], [], None, 0, 1)

# Story Followers
default green_slime = Follower_Character("Green Slime", 20, 20, "1D4", 0, ["Fire", "Acid"], ["Iron"], ["Slime"], None, "common", 1, "images/followers/green_slime")
default minotaur = Follower_Character("Minotaur", 10, 10, "1d10", 0, [], [], [], None, "common", 2, "images/followers/minotaur")
default orc = Follower_Character("Orc", 12, 12, "1d8", 0, [], [], [], None, "common", 2, "images/followers/orc")
default fairy = Follower_Character("Fairy", 15, 15, "1d4", 0, ["Force"], [], [], power_heal, "common", 1, "images/followers/fairy")
default seaserpent = Follower_Character("Sea Serpent", 12, 12, "1d8", 0, ["Fire, Ice"], ["Water"], ["Water"], power_smite, "rare", 3, "images/followers/seaserpent")
default seawitch = Follower_Character("Sea Witch", 10, 10, "1d10", 0, ["Fire", "Ice"], ["Water"], ["Water"], power_smite, "epic", 5, "images/followers/seawitch")
default sphinx = Follower_Character("Sphinx", 10, 10, "1d10", 0, ["Force"], ["Earth", "Stone", "Necrotic"], ["Earth", "Stone"], power_defend, "epic", 5, "images/followers/sphinx")
default zombie = Follower_Character("Zombie", 16, 16, "1d6", 0, ["Force"], ["Necrotic", "Iron"], ["Earth", "Necrotic"], None, "rare", 4, "images/followers/zombie")
default mage = Follower_Character("Mage", 10, 10, "1d10", 0, [], [], [], power_multi_attack, "legendary", 7, "images/followers/mage")
default valkyrie = Follower_Character("Valkyrie", 10, 10, "1d10", 0, [], ["Iron", "Force"], ["Stone", "Iron"], power_smite, "epic", 6, "images/followers/valkyrie")
default night_elf = Follower_Character("Night Elf", 18, 18, "1d4", 0, ["Psychic"], ["Dream"], ["Dream"], None, "rare", 3, "images/followers/night_elf")
default guard_elf = Follower_Character("Guard Elf", 12, 12, "1d8", 0, [], [], ["Iron"], power_defend, "rare", 4, "images/followers/guard_elf")
default demon = Follower_Character("Demon", 10, 10, "1d12", 0, ["Holy"], ["Nectoric", "Fire", "Ice"], ["Necrotic", "Fire", "Ice"], power_multi_attack, "legendary", 7, "images/followers/demon")
default angel = Follower_Character("Angel", 10, 10, "1d12", 0, [], ["Holy", "Fire", "Dream"], ["Holy"], power_heal, "legendary", 8, "images/followers/angel")


# Screen for the follower's turn
screen follower_turn:
    modal True
    zorder 101

    use call_image_button_no_target(attack, [Call("follower_attack"), Hide("follower_turn")])
    if follower.power:
        use call_image_button_no_target(power, If((turn_count - 1) % 3 == 0, [power.action, Hide("follower_turn")], None))


# Follower Attack
label follower_attack:                                              # follower turn after same logic

    $ base_damage_roll = roll_dice(follower.attack_dice)

    if any(elem in enemy.weakness for elem in follower.element):
        "The enemy is susceptible to your follower's element!"
        $ follower.damage = base_damage_roll * 2
    elif any(elem in enemy.resistance for elem in follower.element):
        "The enemy is resistant to your follower's element!"
        $ follower.damage = int(base_damage_roll / 2)
    else:
        $ follower.damage = base_damage_roll

    $ roll = renpy.random.randint(1, 10)
    if roll == 10:
        "Critical Hit!"
        if follower.damage > 0:
            $ follower.damage = max(int(follower.damage * 1.5), follower.damage + 1)

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
    $ heal_amount = int(roll_dice(follower.attack_dice) * follower.grade)
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

    $ base_damage_roll = roll_dice(follower.attack_dice)
    
    if any(elem in enemy.weakness for elem in follower.element):
        "The enemy is susceptible to your follower's element!"
        $ follower.damage = follower.grade * 2 + base_damage_roll * 2
    elif any(elem in enemy.resistance for elem in follower.element):
        "The enemy is resistant to your follower's element!"
        $ follower.damage = int(follower.grade * 2 + base_damage_roll / 2)
    else:
        $ follower.damage = follower.grade * 2 + base_damage_roll

    $ roll = renpy.random.randint(1, 10)
    if roll == 10:
        "Critical Hit!"
        if follower.damage > 0:
            $ follower.damage = max(int(follower.damage * 1.5), follower.damage + 1)

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