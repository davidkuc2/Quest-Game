init python:
    import random
    import copy

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

    def get_loot_from_box(box_type):
        """
        Determines a rarity and selects a random item from the corresponding loot table.
        Falls back to lower rarities if the target rarity pool is empty.
        """
        # 1. Determine rarity of the reward
        rarity = get_lootbox_rarity()

        # 2. Get the list of possible items for this box type and rarity
        possible_rarities = ["unique", "legendary", "epic", "rare", "common"]
        try:
            rarity_index = possible_rarities.index(rarity)
        except ValueError:
            rarity_index = 4 # Fallback to common

        item_pool = []
        # 3. Start from the determined rarity and go down to common to find a non-empty pool
        for i in range(rarity_index, len(possible_rarities)):
            current_rarity = possible_rarities[i]
            pool = renpy.store.loot_tables[box_type][current_rarity]
            if pool:
                item_pool = pool
                break # Found a non-empty pool

        if not item_pool:
            renpy.notify("No lootable items found for box type '{}' at rarity '{}' or lower.".format(box_type, rarity))
            return None

        # 4. Pick a random item from the pool
        won_item_template = random.choice(item_pool)

        # 5. Return a copy of the item to avoid modifying the original definition
        if isinstance(won_item_template, Follower_Character):
            return won_item_template
        else:
            won_item = copy.copy(won_item_template)
            won_item.quantity = 1
            return won_item

    def get_random_dummy_item(box_type, rarity, exclude=None):
        """
        Selects a random item for visual purposes in the lootbox strip.
        Falls back to lower rarities if the target rarity pool is empty.
        Can exclude a specific item from the selection.
        """
        possible_rarities = ["unique", "legendary", "epic", "rare", "common"]
        try:
            rarity_index = possible_rarities.index(rarity)
        except ValueError:
            rarity_index = 4 # Fallback to common

        item_pool = []
        # Start from the determined rarity and go down to common to find a non-empty pool
        for i in range(rarity_index, len(possible_rarities)):
            current_rarity = possible_rarities[i]
            pool = renpy.store.loot_tables.get(box_type, {}).get(current_rarity, [])
            if pool:
                item_pool = pool
                break # Found a non-empty pool

        if not item_pool:
            return None

        if exclude:
            possible_items = [item for item in item_pool if item != exclude]
            if possible_items:
                return random.choice(possible_items)
        
        # If no exclusion or if exclusion left pool empty, choose from original pool
        return random.choice(item_pool)

    def initiate_lootbox(box_type):
        global lootbox_strip, lootbox_target_x, won_lootbox, current_reward, is_new_reward
        
        # 1. Determine the reward
        reward = get_loot_from_box(box_type)
        if not reward:
            renpy.show_screen("inventory")
            return

        current_reward = reward

        # 2. Check if the reward is new, then add/unlock it.
        if isinstance(reward, Follower_Character):
            is_new_reward = not reward.unlocked
            reward.unlock()
        else:
            # Check inventory grid
            item_in_grid = next((i for i in inventory.items if i.name == reward.name), None)
            # Check equipped items
            item_equipped = any(e for e in inventory.equipped.values() if e and e.name == reward.name)
            
            is_new_reward = not (item_in_grid or item_equipped)
            
            inventory.add_item(reward)

        # 3. Prepare the visual animation
        strip = []
        for i in range(TOTAL_BOXES):
            if i == WINNER_INDEX:
                strip.append(LootboxItem(reward))
            else:
                last_item_in_strip = strip[-1].item if strip else None
                # Get a random rarity and a corresponding dummy item for visual flair
                dummy_rarity = get_lootbox_rarity()
                dummy_item = get_random_dummy_item(box_type, dummy_rarity, exclude=last_item_in_strip)
                
                # If a dummy item was found, use it. Otherwise, use the actual reward as a fallback visual.
                if dummy_item:
                    strip.append(LootboxItem(dummy_item))
                else:
                    strip.append(LootboxItem(reward))
        
        lootbox_strip = strip
        
        # Calculate the target X position for the strip
        box_center_in_strip = (WINNER_INDEX * (LOOTBOX_WIDTH + LOOTBOX_SPACING)) + (LOOTBOX_WIDTH / 2)
        lootbox_target_x = int(960 - box_center_in_strip)
        won_lootbox = lootbox_strip[WINNER_INDEX]

        renpy.show_screen("lootbox")

    def show_lootbox_reward():
        if isinstance(current_reward, Follower_Character):
            renpy.show_screen("show_follower_reward", follower=current_reward, is_new=is_new_reward)
        else:
            renpy.show_screen("show_item_reward", item=current_reward, is_new=is_new_reward)

    class LootboxItem():
        def __init__(self, item_obj):
            self.item = item_obj
            self.rarity = getattr(item_obj, 'rarity', 'common')
            self.background_image = "images/lootboxes/lootbox_" + self.rarity + ".png"

default lootbox_strip = []
default lootbox_target_x = 0
default won_lootbox = None
default current_reward = None
default is_new_reward = False

screen lootbox():
    modal True
    zorder 101
    add "images/lootboxes/background.png"

    # The spinning strip
    hbox:
        yalign 0.5
        spacing LOOTBOX_SPACING
        
        # Apply the animation
        at lootbox_spin(lootbox_target_x, SPIN_DURATION)
        
        for box in lootbox_strip:
            fixed:
                xysize (LOOTBOX_WIDTH, LOOTBOX_HEIGHT)
                yalign 0.5

                # Rarity background
                add box.background_image

                # Item/Follower image, centered inside the box
                $ display_item = box.item
                if isinstance(display_item, Follower_Character):
                    add display_item.image + "_idle.png" xalign 0.5 yalign 0.5 maxsize (180, 180)
                elif display_item:
                    add display_item.image xalign 0.5 yalign 0.5 maxsize (180, 180)

    # Skip Button
    use call_image_button(skip)

    # Timer to show the reward screen shortly after the spin finishes
    timer (SPIN_DURATION + 1.0) action [Hide("lootbox"), Function(show_lootbox_reward)]

transform lootbox_spin(target_x, duration):
    subpixel True
    xpos 0
    ease duration xpos target_x

screen show_item_reward(item, is_new):
    modal True
    zorder 102
    window:
        xalign 0.5
        yalign 0.5
        vbox:
            xalign 0.5
            spacing 20
            if is_new:
                text "New Item!" size 40 xalign 0.5
            else:
                text "Duplicate Item" size 40 xalign 0.5
            add item.image xalign 0.5
            text item.name size 30 xalign 0.5
            textbutton "OK" action [Hide("show_item_reward"), Show("inventory")] xalign 0.5

screen show_follower_reward(follower, is_new):
    modal True
    zorder 102

    window:
        xalign 0.5
        yalign 0.5
        
        vbox:
            xalign 0.5
            spacing 20
            
            if is_new:
                text "New Follower!" size 40 xalign 0.5
            else:
                text "You already unlocked this follower" size 30 xalign 0.5
            
            add follower.image + "_idle.png" xalign 0.5 maxsize (200, 200)
            
            text follower.name size 30 xalign 0.5
            
            textbutton "OK" action [Hide("show_follower_reward"), Show("inventory")] xalign 0.5