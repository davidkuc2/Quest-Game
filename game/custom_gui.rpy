# -------------------------------------------------------------------------
# CLASSES & LOGIC
# -------------------------------------------------------------------------
init python:
    import copy

    # --- Item Classes ---
    class Item():
        def __init__(self, name, cost, quantity, image, image_hover):
            self.name = name
            self.quantity = quantity 
            self.cost = cost  
            self.image = image    
            self.image_hover = image_hover
            self.is_equipped = False # Helper flag

    class Equippable(Item):
        def __init__(self, name, cost, quantity, image, image_hover, slot):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.slot = slot

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

    # --- Quest Class ---
    class Quest():
        def __init__(self, name, description):
            self.name = name
            self.description = description
            
    def give_quest(quest_to_add):
        if quest_to_add not in quests:
            quests.append(quest_to_add)

    def remove_quest(quest_to_remove):
        if quest_to_remove in quests:
            quests.remove(quest_to_remove)

    # -------------------------------------------------------------------------
    # INVENTORY LOGIC FUNCTIONS
    # -------------------------------------------------------------------------

    def equip_item(item, slot_key):

        # 1. If a different item is already equipped in the target slot, unequip it first.
        current_equipped = inventory.equipped.get(slot_key)
        if current_equipped and current_equipped != item:
            unequip_item(current_equipped)

        # 2. Handle the item coming from the inventory grid.
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
            renpy.restart_interaction()

    def unequip_item(item_obj):

        # 1. Find which slot holds this item and clear it.
        found_slot = None
        for slot, equipped_item in inventory.equipped.items():
            if equipped_item == item_obj:
                inventory.equipped[slot] = None
                found_slot = slot
                break

        if not found_slot:
            return  # Item wasn't actually equipped.

        item_obj.is_equipped = False

        # 2. Add the item back to the inventory grid, merging with existing stacks if possible.
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

# Define Quests
default quests = []
default mern_ressources = Quest("Mern's Ressources", "Find suitable ressources and give them to Mern")

# Define Items
default documents = Item("documents", 0, 1, "images/inventory/documents.png", "images/inventory/documents_hover.png")
default guild_certificate = Item("guild certificate", 0, 1, "images/inventory/guild_certificate.png", "images/inventory/guild_certificate_hover.png")

# Define Equippables
default sword = Equippable("sword", 10, 1, "images/inventory/sword.png", "images/inventory/sword_hover.png", "weapon")
default armor = Equippable("armor", 20, 1, "images/inventory/armor.png", "images/inventory/armor_hover.png", "armor")

# Define Shops
default blacksmith_shop = Shop(100, 1.3, [(sword, 2), (armor, 2)])

# Game State Flags
default inventory_unlocked = False
default world_map_unlocked = False
default quests_unlocked = False
default cheating = True 

# -------------------------------------------------------------------------
# SCREENS
# -------------------------------------------------------------------------

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
    key "i" action [Hide("inventory"), Show("call_gui")]
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


screen quest_menu():
    modal True
    zorder 1000
    add "background_quest"

    viewport:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 900
        scrollbars None
        mousewheel True
        draggable True

        vbox:
            spacing 20
            for q in quests:
                vbox:
                    text q.name color "#000000" size 40 bold True
                    text q.description color "#000000" size 30 xsize 900
                    null height 20

    use call_image_button_no_target(arrow_down, [Hide("quest_menu"), Show("call_gui")])

    key "q" action [Hide("quest_menu"), Show("call_gui")]
    key "game_menu" action [Hide("quest_menu"), Show("call_gui")]


screen call_gui:
    modal False 
    zorder 100

    # Custom GUI with keybinds
    if inventory_unlocked == True:
        use call_image_button(backpack)
        key "i" action [Show("inventory"), Hide("call_gui")]

    if world_map_unlocked == True:
        use call_image_button(open_map)
        key "m" action [Show("worldmap"), Hide("call_gui")]

    if cheating == True:
        key "c" action [Show("cheat_menu"), Hide("call_gui")]

    if quests_unlocked == True:
        use call_image_button(quest_menu)
        key "q" action [Show("quest_menu"), Hide("call_gui")]


screen cheat_menu():
    modal True
    zorder 100
    add "cheat_menu"

    vbox:
        align (0.5, 0.5)
        spacing 20

        if world_map_unlocked == False:
            textbutton "enable worldmap" action SetVariable("world_map_unlocked", True)
        textbutton "skip tutorial" action [SetVariable("inventory_unlocked", True), SetVariable("quests_unlocked", True), Hide("cheat_menu"), Show("call_gui"), Jump("tamra")]
        textbutton "+100 coins" action [SetField(inventory, "money", inventory.money + 100)]

    key "c" action [Hide("cheat_menu"), Show("call_gui")]
    key "game_menu" action [Hide("cheat_menu"), Show("call_gui")]