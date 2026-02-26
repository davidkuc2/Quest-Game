# Define Characters
init offset = -1

init python:
    import re

    class Combat_Character():
        def __init__(self, name, max_hp, hp, attack_dice, damage=0, grade=0, image=None,
            attack_bonus_flat=0, attack_bonus_dice_list=None, attack_multiplier=1.0):
            self.name = name
            self.max_hp = max_hp
            self.hp = hp
            self.attack_dice = attack_dice
            self.attack_bonus_flat = attack_bonus_flat
            self.attack_bonus_dice_list = attack_bonus_dice_list if attack_bonus_dice_list is not None else []
            self.damage = damage     
            self.grade = grade
            self.image = image

    def roll_dice(dice_string):
        if not isinstance(dice_string, str) or not dice_string:
            return 0

        # Regex to parse strings like "d6", "1d6", "2d8+2"
        match = re.match(r"(\d*)d(\d+)(?:\s*\+\s*(\d+))?", dice_string.lower().strip())
        if not match:
            return 0

        num_dice_str, num_sides_str, modifier_str = match.groups()

        num_dice = int(num_dice_str) if num_dice_str else 1
        num_sides = int(num_sides_str)
        modifier = int(modifier_str) if modifier_str else 0

        if num_sides == 0:
            return modifier

        total = sum(renpy.random.randint(1, num_sides) for _ in range(num_dice))
        return total + modifier

    def combat_reset():
        player_combat.hp = player_combat.max_hp
        follower.hp = follower.max_hp
        player_combat.attack_bonus_flat = 0
        player_combat.attack_bonus_dice_list = []
        player_combat.attack_multiplier = 1.0
        enemy.hp = enemy.max_hp


default turn_count = 1

# Fight Display
screen fight:
    

    # Enemy Image - Center Left
    add enemy.image xalign 0.2 yalign 0.5 zoom 0.5
        
    # Follower Image - Center Right
    if follower.image and follower.hp > 0:
        add follower.image + "_idle.png" xalign 0.8 yalign 0.5 zoom 0.5
        
    # Enemy HP Bar - Top Left
    if enemy.max_hp > 0:
        vbox:
            xalign 0.05 yalign 0.05
            spacing 5
            
            text enemy.name size 30 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            
            bar:
                value enemy.hp
                range enemy.max_hp
                xsize 400
                ysize 40
                
            text "[enemy.hp] / [enemy.max_hp]" size 25 color "#ffffff" outlines [(2, "#000000", 0, 0)]

    # Follower HP Bar - Top Right
    if follower.max_hp > 0:
        vbox:
            xalign 0.95 yalign 0.05
            spacing 5
            
            text follower.name size 30 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            
            bar:
                value follower.hp
                range follower.max_hp
                xsize 400
                ysize 40
                
            text "[follower.hp] / [follower.max_hp]" size 25 color "#ffffff" outlines [(2, "#000000", 0, 0)]

    # Player HP Bar - Top Center
    vbox:
        xalign 0.5 yalign 0.05
        spacing 5
        
        text player_combat.name size 30 color "#ffffff" outlines [(2, "#000000", 0, 0)]
        
        bar:
            value player_combat.hp
            range player_combat.max_hp
            xsize 400
            ysize 40
            
        text "[player_combat.hp] / [player_combat.max_hp]" size 25 color "#ffffff" outlines [(2, "#000000", 0, 0)]


# Default fight 

default after_combat_label = None                           # set label in beginning of each fight to continue after 

label fight:
    hide screen call_gui
    
    $ turn_count = 1
    show screen fight
    while player_combat.hp > 0:                             # loop as long as alive
        "Your turn!"

        call screen player_turn

        if follower.hp > 0:                                 # use follower as long as alive
            "Your follower's turn!"
        
            call screen follower_turn

        if enemy.hp > 0:
            call enemy_turn
        $ turn_count += 1