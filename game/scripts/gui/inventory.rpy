init offset = 1

init python:
    import copy

    # --- Inventory Class ---
    class Inventory(): 
        def __init__(self, money=0):
            self.items = []
            self.money = money 
            # Initialize equipped slots
            self.equipped = {
                "weapon": None,
                "armor": None,
                "accessory": None
            }

        def add_item(self, *items):
            for item in items:
                # Check for existing stack in the grid (ignore equipped items)
                existing_item = next((i for i in self.items if i.name == item.name), None)
                if existing_item:
                    existing_item.quantity += item.quantity
                else:
                    self.items.append(item)

        def has_item(self, item):
            return item in self.items

        def remove_item(self, item):                           
            if item.quantity >= 2:
                item.quantity -= 1
            elif item.quantity == 1:
                if item in self.items:
                    self.items.remove(item)

    # --- Shop Class ---
    class Shop(Inventory):
        def __init__(self, money, price_multiplier, initial_items=None):
            Inventory.__init__(self, money)
            self.price_multiplier = price_multiplier
            
            if initial_items:
                for item, qty in initial_items:
                    shop_item = copy.copy(item)
                    shop_item.quantity = qty
                    self.add_item(shop_item)

        def buy_item(self, item):
            cost = int(item.cost * self.price_multiplier)
            if inventory.money >= cost:
                bought_item = copy.copy(item)
                bought_item.quantity = 1
                inventory.add_item(bought_item)
                
                # Logic to reduce shop stock
                if item.quantity > 1:
                    item.quantity -= 1
                else:
                    self.items.remove(item)

                inventory.money -= cost
                self.money += cost
                renpy.restart_interaction()
            else:
                renpy.notify("I don't have enough money")

        def sell_item(self, item):
            cost = int(item.cost / self.price_multiplier)
            if self.money >= cost:
                inventory.remove_item(item)
                
                sold_item = copy.copy(item)
                sold_item.quantity = 1
                self.add_item(sold_item)
                
                inventory.money += cost
                self.money -= cost
                renpy.restart_interaction()
            else:
                renpy.notify("The merchant doesn't have enough money")

    # -------------------------------------------------------------------------
    # INVENTORY LOGIC FUNCTIONS
    # -------------------------------------------------------------------------

    def equip_item(item, slot_key):

        # If a different item is already equipped in the target slot, unequip it first.
        current_equipped = inventory.equipped.get(slot_key)
        if current_equipped and current_equipped != item:
            unequip_item(current_equipped)

        # Handle the item coming from the inventory grid.
        if item in inventory.items:
            if item.quantity > 1:
                # If item is in a stack, split the stack.
                item.quantity -= 1
                item_to_equip = copy.copy(item)
                item_to_equip.quantity = 1
            else:
                # If it's a single item, remove it from the grid.
                inventory.items.remove(item)
                item_to_equip = item

            item_to_equip.is_equipped = True
            inventory.equipped[slot_key] = item_to_equip

            # Apply Item Buffs
            if item_to_equip.buff:
                for stat, value in item_to_equip.buff.items():
                    if hasattr(player_combat, stat):
                        current_val = getattr(player_combat, stat)
                        setattr(player_combat, stat, current_val + value)
                        # If Max HP is increased, heal the player by that amount
                        if stat == "max_hp":
                            player_combat.hp += value

            renpy.restart_interaction()

    def unequip_item(item_obj):

        # Find which slot holds this item and clear it.
        found_slot = None
        for slot, equipped_item in inventory.equipped.items():
            if equipped_item == item_obj:
                inventory.equipped[slot] = None
                found_slot = slot
                break

        if not found_slot:
            return  # Item wasn't actually equipped.

        # Remove Item Buffs
        if item_obj.buff:
            for stat, value in item_obj.buff.items():
                if hasattr(player_combat, stat):
                    current_val = getattr(player_combat, stat)
                    setattr(player_combat, stat, current_val - value)
                    # If Max HP is decreased, clamp current HP
                    if stat == "max_hp":
                        if player_combat.hp > player_combat.max_hp:
                            player_combat.hp = player_combat.max_hp

        item_obj.is_equipped = False

        # Add the item back to the inventory grid, merging with existing stacks if possible.
        existing_item = next((i for i in inventory.items if i.name == item_obj.name), None)
        if existing_item:
            existing_item.quantity += item_obj.quantity
        else:
            inventory.items.append(item_obj)

        renpy.restart_interaction()

    # Called when an item in the inventory screen is clicked
    def inventory_item_interact(item): 

        if isinstance(item, Equippable):
            if item.is_equipped:
                # If a currently equipped item is clicked, unequip it.
                unequip_item(item)
            else:
                # If an item in the grid is clicked, equip it.
                # The equip_item function handles swapping if the slot is occupied.
                equip_item(item, item.slot)


# -------------------------------------------------------------------------
# VARIABLES & INSTANCES
# -------------------------------------------------------------------------

# Define Inventory
default inventory = Inventory(0)

# Define Shops
default blacksmith_shop = Shop(100, 1.3, [(iron_sword, 2), (iron_armor, 2)])


screen inventory(selection_mode=False):
    default hovered_item = None

    tag inventory
    zorder 1000
    modal True

    add "images/inventory/background.png"

    # Overlays for empty slots
    if not inventory.equipped.get("weapon"):
        add "images/inventory/weapon_overlay.png"
    if not inventory.equipped.get("armor"):
        add "images/inventory/armor_overlay.png"
    if not inventory.equipped.get("accessory"):
        add "images/inventory/accessory_overlay.png"

    # Display Money
    hbox:
        xalign 0.05
        yalign 0.95
        spacing 10
        add "images/inventory/coin.png":
            zoom 0.25
        if inventory.money > 0:
            text "[inventory.money]" color "#000000" yalign 0.5
        else:
            text "[inventory.money]" color "#ff0000" yalign 0.5

    # --- EQUIPPED ITEMS ---
    fixed:
        for slot, item in inventory.equipped.items():
            if item:
                if slot == "weapon":
                    $ pos = (1670, 53)
                elif slot == "armor":
                    $ pos = (1670, 311)
                elif slot == "accessory":
                    $ pos = (1670, 569)

                button:
                    pos pos
                    xysize (200, 200)
                    # In selection mode, you can't interact with equipped items.
                    # Otherwise, clicking unequips the item.
                    action If(selection_mode, NullAction(), Function(inventory_item_interact, item))

                    hovered SetScreenVariable("hovered_item", item)
                    unhovered SetScreenVariable("hovered_item", None)

                    add (item.image_hover if hovered_item == item else item.image) zoom 0.86 xalign 0.5 yalign 0.5

    # --- INVENTORY GRID ---
    vpgrid:
        cols 6
        xpos 60
        ypos 100
        xsize (6 * 250)
        ysize 800
        scrollbars None
        mousewheel True

        for item in inventory.items:
            button:
                style "empty"
                xysize (250, 250)
                # In selection mode, clicking returns the item.
                # Otherwise, it calls the interaction function.
                action If(selection_mode, Return(item), Function(inventory_item_interact, item))

                hovered SetScreenVariable("hovered_item", item)
                unhovered SetScreenVariable("hovered_item", None)

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 5

                    fixed:
                        xysize (215, 215)  # Corresponds to zoom 0.86 of a 250px image

                        add (item.image_hover if hovered_item == item else item.image) zoom 0.86

                        text str(item.quantity):
                            size 25
                            xalign 1.0
                            yalign 0.0

                    text item.name:
                        size 25
                        xalign 0.5
                        text_align 0.5

    # Close Actions
    use call_image_button_no_target(arrow_down, [Hide("inventory"), Show("call_gui")])
    key "e" action [Hide("inventory"), Show("call_gui")]
    key "game_menu" action [Hide("inventory"), Show("call_gui")]


screen shop(shop):
    tag menu
    modal True
    default hovered_item = None
    on "show" action Hide("call_gui")
    on "hide" action Show("call_gui")

    # Left Side - Player Inventory
    add "images/inventory/background_shop.png" xcenter 0.25 yalign 0.5

    text "Player":
        xcenter 0.25
        ypos 50
        size 40
        color "#000000"

    # Player Money
    hbox:
        xpos 150
        xanchor 1.0
        yalign 0.95
        spacing 10
        add "images/inventory/coin.png":
            zoom 0.25
        if inventory.money > 0:
            text "[inventory.money]" color "#000000" yalign 0.5
        else:
            text "[inventory.money]" color "#ff0000" yalign 0.5

    # Player Items
    vpgrid:
        cols 5
        spacing 20
        xpos 50
        ypos 150
        xmaximum 850
        ymaximum 800
        scrollbars "vertical"
        mousewheel True
        draggable True

        for i in inventory.items:
            button:
                action Function(shop.sell_item, i)
                hovered SetScreenVariable("hovered_item", i)
                unhovered SetScreenVariable("hovered_item", None)
                vbox:
                    hbox:
                        add (getattr(i, "image_hover", i.image) if hovered_item == i else i.image) zoom 0.86
                        text str(i.quantity): 
                            size 25 
                            align (1.0, 0.0)
                    text i.name: 
                        size 25
                        xalign 0.5

    # Right Side - Shop Inventory
    add "images/inventory/background_shop.png" xcenter 0.75 yalign 0.5

    text "Shop":
        xcenter 0.75
        ypos 50
        size 40
        color "#000000"

    # Shop Money
    hbox:
        xpos 1850
        xanchor 1.0
        yalign 0.95
        spacing 10
        add "images/inventory/coin.png":
            zoom 0.25
        if shop.money > 0:
            text "[shop.money]" color "#000000" yalign 0.5
        else:
            text "[shop.money]" color "#ff0000" yalign 0.5

    # Shop Items
    vpgrid:
        cols 5
        spacing 20
        xpos 1010
        ypos 150
        xmaximum 850
        ymaximum 800
        scrollbars "vertical"
        mousewheel True
        draggable True

        for i in shop.items:
            button:
                action Function(shop.buy_item, i)
                hovered SetScreenVariable("hovered_item", i)
                unhovered SetScreenVariable("hovered_item", None)
                vbox:
                    hbox:
                        add (getattr(i, "image_hover", i.image) if hovered_item == i else i.image) zoom 0.86
                        text str(i.quantity): 
                            size 25 
                            align (1.0, 0.0)
                    text i.name: 
                        size 25
                        xalign 0.5

    # Close Shop
    use call_image_button_no_target(arrow_down, Return())
    key "game_menu" action Return()