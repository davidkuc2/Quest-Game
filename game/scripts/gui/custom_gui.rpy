# Game State Flags
default inventory_unlocked = False
default quests_unlocked = False
default world_map_unlocked = False
default follower_logbook_unlocked = False
default cheating = True 


screen call_gui:
    modal False 
    zorder 100

    # Custom GUI with keybinds
    if inventory_unlocked == True:
        use call_image_button(backpack)
        key "e" action [Show("inventory"), Hide("call_gui")]

    if world_map_unlocked == True:
        use call_image_button(open_map)
        key "m" action [Show("worldmap"), Hide("call_gui")]

    if cheating == True:
        key "c" action [Show("cheat_menu"), Hide("call_gui")]

    if quests_unlocked == True:
        use call_image_button(quest_menu)
        key "q" action [Show("quest_menu"), Hide("call_gui")]

    if follower_logbook_unlocked == True:
        use call_image_button(follower_logbook)
        key "f" action [Show("follower_logbook"), Hide("call_gui")]