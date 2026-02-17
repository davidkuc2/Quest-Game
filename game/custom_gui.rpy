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
    # DRAG AND DROP LOGIC FUNCTIONS
    # -------------------------------------------------------------------------

    def equip_item(item, slot_key):
        """Moves item from Grid List to Equipped Dict"""
        
        # 1. Check if something is already equipped; if so, unequip it first (Swap)
        current_equipped = inventory.equipped.get(slot_key)
        if current_equipped:
            unequip_item(current_equipped)

        # 2. Handle the item coming from Inventory Grid
        # We need to decide if we split the stack or move the whole object
        if item in inventory.items:
            if item.quantity > 1:
                # Stack Split Logic: Keep one in grid, move clone to slot
                item.quantity -= 1
                
                item_to_equip = copy.copy(item)
                item_to_equip.quantity = 1
                item_to_equip.is_equipped = True
            else:
                # Single Item Logic: Remove from grid entirely
                inventory.items.remove(item)
                item_to_equip = item
                item_to_equip.is_equipped = True
            
            # 3. Place in slot
            inventory.equipped[slot_key] = item_to_equip
            renpy.restart_interaction()

    def unequip_item(item_obj):
        """Moves item from Equipped Dict back to Grid List"""
        
        # 1. Find which slot holds this item and clear it
        found_slot = None
        for slot, equipped_item in inventory.equipped.items():
            if equipped_item == item_obj:
                inventory.equipped[slot] = None
                found_slot = slot
                break
        
        if not found_slot:
            return # Item wasn't actually equipped?

        item_obj.is_equipped = False

        # 2. Add back to grid
        # Check if a stack of this item already exists in grid to merge with
        found_stack = False
        for inv_item in inventory.items:
            # Match by name (and ensure we don't match other equipped items if logic fails)
            if inv_item.name == item_obj.name: 
                inv_item.quantity += 1
                found_stack = True
                break
        
        # If no stack exists, append the item object back to the list
        if not found_stack:
            inventory.items.append(item_obj)
            
        renpy.restart_interaction()

    def item_dragged(drags, drop):
        """Callback for RenPy draggroup"""
        
        if not drop:
            return

        dragged_item_obj = drags[0].drag_name
        target_name = drop.drag_name

        # --- CASE 1: EQUIPPING (Dragging onto a slot) ---
        if isinstance(target_name, str) and "_slot" in target_name:
            
            # Extract slot type from "weapon_slot" -> "weapon"
            slot_type = target_name.replace("_slot", "")
            
            # Check if the dragged item is actually compatible
            if hasattr(dragged_item_obj, "slot") and dragged_item_obj.slot == slot_type:
                equip_item(dragged_item_obj, slot_type)
            else:
                renpy.notify("Wrong slot!")
            return

        # --- CASE 2: UNEQUIPPING (Dragging from slot to grid area) ---
        # We check if the dragged object is currently inside the equipped list
        if dragged_item_obj in inventory.equipped.values():
            # If we dropped it on the grid background or another non-slot area
            if target_name == "inventory_grid":
                unequip_item(dragged_item_obj)
                return

    def item_clicked(drags):
        item = drags[0].drag_name
        screen = renpy.get_screen("inventory")
        if screen:
            if screen.scope.get("selection_mode"):
                return item
            # Optional: Set a variable to track what is being clicked
            # screen.scope["dragging_item"] = item
            renpy.restart_interaction()
        return None


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
default cheating = True # Set to True for testing

# -------------------------------------------------------------------------
# SCREENS
# -------------------------------------------------------------------------

screen inventory(selection_mode=False):
    default hovered_item = None
    default scroll_offset = 0
    default dragging_item = None

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

    # Grid Calculations
    $ cols = 6
    $ cell_size = 250 
    $ start_x = 60
    $ start_y = 100
    $ view_h = 800
    
    $ total_rows = (len(inventory.items) + cols - 1) // cols
    $ content_h = total_rows * cell_size
    $ max_scroll = max(0, content_h - view_h)

    draggroup:
        # --- DROP SLOTS ---
        drag:
            drag_name "weapon_slot"
            xpos 1670 ypos 53
            xsize 200 ysize 200
            draggable False
            droppable True
            child Solid("#0000")
        drag:
            drag_name "armor_slot"
            xpos 1670 ypos 311
            xsize 200 ysize 200
            draggable False
            droppable True
            child Solid("#0000")
        drag:
            drag_name "accessory_slot"
            xpos 1670 ypos 569
            xsize 200 ysize 200
            draggable False
            droppable True
            child Solid("#0000")
        
        # General Drop Area (Background of the grid)
        # This allows you to drag an equipped item back to "the bag" to unequip it
        drag:
            drag_name "inventory_grid"
            xpos start_x ypos start_y
            xsize (cols * cell_size) ysize view_h
            draggable False
            droppable True
            child Solid("#0000")

        # --- GRID ITEMS (INVENTORY.ITEMS) ---
        for i, item in enumerate(inventory.items):
            $ row = i // cols
            $ col = i % cols
            $ x = start_x + col * cell_size
            $ y = start_y + row * cell_size - scroll_offset
            
            if -cell_size < (y - start_y) < view_h:
                if isinstance(item, Equippable):
                    # Visual Stack: This renders the item 'underneath' the top one
                    # It creates the illusion of a stack remaining when you drag the top one
                    if item.quantity > 1:
                        drag:
                            pos (x, y)
                            draggable False
                            droppable False
                            vbox:
                                hbox:
                                    add item.image zoom 0.86
                                    # If we are dragging this specific item, show quantity-1, else show full quantity
                                    text str(item.quantity - 1 if dragging_item == item else item.quantity):
                                        size 25
                                        align (1.0, 0.0)

                    # The Interactable Top Item
                    drag:
                        drag_name item
                        # Unique ID based on ID + Quantity + Location Context
                        # This ensures if quantity changes, the drag object resets to grid
                        id "inv_{}_{}".format(id(item), item.quantity)
                        pos (x, y)
                        draggable True
                        droppable False
                        dragged item_dragged
                        activated item_clicked
                        
                        hovered If(dragging_item == None, SetScreenVariable("hovered_item", item), NullAction())
                        unhovered If(dragging_item == None, SetScreenVariable("hovered_item", None), NullAction())

                        vbox:
                            hbox:
                                add (item.image_hover if (hovered_item == item or dragging_item == item) else item.image) zoom 0.86
                                if item.quantity == 1:
                                    text str(item.quantity):
                                        size 25
                                        align (1.0, 0.0)
                            text item.name:
                                size 25
                                xalign 0.5

        # --- EQUIPPED ITEMS (INVENTORY.EQUIPPED) ---
        for slot, item in inventory.equipped.items():
            if item:
                if slot == "weapon":
                    $ equipped_x, equipped_y = 1770, 153
                elif slot == "armor":
                    $ equipped_x, equipped_y = 1770, 411
                elif slot == "accessory":
                    $ equipped_x, equipped_y = 1770, 669
                
                drag:
                    drag_name item
                    # Unique ID for equipped items specifically
                    # Prevents it from conflicting with grid items
                    id "equip_{}_{}".format(slot, id(item)) 
                    pos (equipped_x, equipped_y)
                    anchor (0.5, 0.5)
                    draggable True
                    droppable False 
                    dragged item_dragged
                    activated item_clicked
                    
                    hovered If(dragging_item == None, SetScreenVariable("hovered_item", item), NullAction())
                    unhovered If(dragging_item == None, SetScreenVariable("hovered_item", None), NullAction())

                    add (item.image_hover if (hovered_item == item or dragging_item == item) else item.image) zoom 0.86

    # --- NON-EQUIPPABLE ITEMS ---
    for i, item in enumerate(inventory.items):
        $ row = i // cols
        $ col = i % cols
        $ x = start_x + col * cell_size
        $ y = start_y + row * cell_size - scroll_offset
        
        if -cell_size < (y - start_y) < view_h:
            if not isinstance(item, Equippable):
                button:
                    pos (x, y)
                    action If(selection_mode, Return(item), NullAction())

                    hovered If(dragging_item == None, SetScreenVariable("hovered_item", item), NullAction())
                    unhovered If(dragging_item == None, SetScreenVariable("hovered_item", None), NullAction())

                    vbox:
                        hbox:
                            add (item.image_hover if hovered_item == item else item.image) zoom 0.86
                            text str(item.quantity):
                                size 25
                                align (1.0, 0.0)
                        text item.name:
                            size 25
                            xalign 0.5

    # Scrolling
    key "mousedown_4" action SetScreenVariable("scroll_offset", max(0, scroll_offset - 50))
    key "mousedown_5" action SetScreenVariable("scroll_offset", min(max_scroll, scroll_offset + 50))

    # Close Actions
    # Assumed usage of your custom button
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