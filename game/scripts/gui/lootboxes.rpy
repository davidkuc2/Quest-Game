init python:
    import random

    # Configuration
    LOOTBOX_WIDTH = 250
    LOOTBOX_HEIGHT = 200
    LOOTBOX_SPACING = 15
    WINNER_INDEX = 50       # The index of the box that will stop in the middle
    TOTAL_BOXES = 70        # Total number of boxes in the strip
    SPIN_DURATION = 6.0     # Duration of the spin animation

    def get_lootbox_rarity():
        # Odds: common 70%, rare 27 %, epic 2,75 %, legendary 0,24 %, unique 0,01 %
        roll = random.uniform(0, 100)
        
        if roll < 70:
            return "common"
        elif roll < 97:
            return "rare"
        elif roll < 99.75:
            return "epic"
        elif roll < 99.99:
            return "legendary"
        else:
            return "unique"

    class LootboxItem():
        def __init__(self, rarity):
            self.rarity = rarity
            self.image = "images/lootboxes/lootbox_" + rarity + ".png"

default lootbox_strip = []
default lootbox_target_x = 0
default won_lootbox = None

screen lootbox():
    modal True
    zorder 101
    default show_reward = False
    
    add "images/lootboxes/background.png"

    # The spinning strip
    hbox:
        yalign 0.5
        spacing LOOTBOX_SPACING
        
        # Apply the animation
        at lootbox_spin(lootbox_target_x, SPIN_DURATION)
        
        for box in lootbox_strip:
            add box.image:
                size (LOOTBOX_WIDTH, LOOTBOX_HEIGHT)
                yalign 0.5

    if show_reward:
        text "[won_lootbox.rarity.upper()]!":
            align (0.01, 0.01)
            size 50
            color "#ffffff"
            outlines [(2, "#000000", 0, 0)]

    timer SPIN_DURATION action SetScreenVariable("show_reward", True)
    # Timer to end the screen shortly after the spin finishes
    timer (SPIN_DURATION + 2.0) action Return()

transform lootbox_spin(target_x, duration):
    subpixel True
    xpos 0
    ease duration xpos target_x

label open_lootbox:
    
    # Generate the strip of lootboxes
    $ lootbox_strip = []
    python:
        for i in range(TOTAL_BOXES):
            lootbox_strip.append(LootboxItem(get_lootbox_rarity()))

    # Calculate the target X position for the strip
    # We want the center of the box at WINNER_INDEX to be at the center of the screen (960)
    # Center of box in strip = (Index * (Width + Spacing)) + (Width / 2)
    # Strip X = Screen Center - Box Center in Strip
    
    $ box_center_in_strip = (WINNER_INDEX * (LOOTBOX_WIDTH + LOOTBOX_SPACING)) + (LOOTBOX_WIDTH / 2)
    $ lootbox_target_x = int(960 - box_center_in_strip)
    $ won_lootbox = lootbox_strip[WINNER_INDEX]

    # Show the screen
    call screen lootbox
    
    return