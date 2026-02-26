screen follower_logbook:
    modal True
    zorder 100

    default current_page = 0
    default hovered_follower = None
    
    add "images/inventory/follower_logbook_background.png"

    # --- PAGINATION LOGIC ---
    $ items_per_page = 2
    # Calculate total pages (at least 1)
    $ total_pages = max(1, (len(all_followers) + items_per_page - 1) // items_per_page)
    $ total_slots = total_pages * items_per_page

    # Navigation Arrows
    if current_page > 0:
        # Position the left arrow (adjust xpos/ypos as needed for your UI)
        fixed:
            align (0.1, 0.5)
            xysize (100, 100)
            use call_image_button_no_target(arrow_left, SetScreenVariable("current_page", current_page - 1))
    
    if current_page < total_pages - 1:
        # Position the right arrow
        fixed:
            align (0.9, 0.5)
            xysize (100, 100)
            use call_image_button_no_target(arrow_right, SetScreenVariable("current_page", current_page + 1))

    # --- FOLLOWER DISPLAY ---
    hbox:
        xfill True
        yalign 0.5
        
        $ start_idx = current_page * items_per_page
        $ end_idx = min(start_idx + items_per_page, len(all_followers))
        
        $ followers_on_page = all_followers[start_idx:end_idx]
        # Create a list for the page, padding with None for empty slots
        $ page_items = followers_on_page + [None] * (items_per_page - len(followers_on_page))

        for i, f in enumerate(page_items):
            # Create a container for each slot that is half the screen width
            fixed:
                xsize 960 # 1920 / 2

                if f is not None:
                    button:
                        align (0.5, 0.5)
                        xysize (400, 600) # Adjust size to match your follower images
                        action If(f.unlocked, Function(equip_follower, f), NullAction())
                        
                        hovered SetScreenVariable("hovered_follower", f)
                        unhovered SetScreenVariable("hovered_follower", None)
                        
                        if f.unlocked:
                            if hovered_follower == f:
                                add f.image + "_hover.png" align (0.5, 0.5)
                            else:
                                add f.image + "_idle.png" align (0.5, 0.5)
                            if follower == f:
                                add f.image + "_equipped.png" align (0.5, 0.5)
                        else:
                            add f.image + "_locked.png" align (0.5, 0.5)

                $ current_slot = current_page * items_per_page + i + 1
                text str(current_slot) + "/" + str(total_slots) color "#000000" xalign 0.5 yalign 0.95 size 30
    
    use call_image_button_no_target(arrow_down, [Hide("follower_logbook"), Show("call_gui")])
    key "f" action [Hide("follower_logbook"), Show("call_gui")]
    key "game_menu" action [Hide("follower_logbook"), Show("call_gui")]

# Unlocking follower_logbook at first follower
