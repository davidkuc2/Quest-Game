init python:
    renpy.register_shader("custom.green_outline", variables="""
        uniform float u_outline_width;
        uniform vec4 u_outline_color;
        uniform sampler2D tex0;
        uniform vec2 res0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_300="""
        v_tex_coord = a_tex_coord;
    """, fragment_300="""
        vec2 one_pixel = vec2(1.0) / res0;
        vec4 color = texture2D(tex0, v_tex_coord);
        
        if (color.a > 0.1) {
            gl_FragColor = color;
            return;
        }
        
        float alpha = 0.0;
        alpha = max(alpha, texture2D(tex0, v_tex_coord + vec2(u_outline_width * one_pixel.x, 0.0)).a);
        alpha = max(alpha, texture2D(tex0, v_tex_coord - vec2(u_outline_width * one_pixel.x, 0.0)).a);
        alpha = max(alpha, texture2D(tex0, v_tex_coord + vec2(0.0, u_outline_width * one_pixel.y)).a);
        alpha = max(alpha, texture2D(tex0, v_tex_coord - vec2(0.0, u_outline_width * one_pixel.y)).a);
        
        if (alpha > 0.1) {
            gl_FragColor = u_outline_color;
        } else {
            gl_FragColor = color;
        }
    """)

transform equipped_outline:
    shader "custom.green_outline"
    u_outline_width 5.0
    u_outline_color (0.0, 0.5, 0.0, 1.0)

transform no_outline:
    shader "renpy.texture"

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
        
        fixed:
            use call_image_button_no_target(arrow_left, SetScreenVariable("current_page", current_page - 1))
    
    if current_page < total_pages - 1:
        
        fixed:
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
                            $ img = f.image + ("_hover.png" if hovered_follower == f else "_idle.png")
                            if follower == f:
                                add img align (0.5, 0.5) at equipped_outline
                            else:
                                add img align (0.5, 0.5) at no_outline
                        else:
                            add f.image + "_locked.png" align (0.5, 0.5)

                $ current_slot = current_page * items_per_page + i + 1
                text str(current_slot) + "/" + str(total_slots) color "#000000" xalign 0.5 yalign 0.95 size 30
    
    use call_image_button_no_target(arrow_down, [Hide("follower_logbook"), Show("call_gui")])
    key "f" action [Hide("follower_logbook"), Show("call_gui")]
    key "game_menu" action [Hide("follower_logbook"), Show("call_gui")]