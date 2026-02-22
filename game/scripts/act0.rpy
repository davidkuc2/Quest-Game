# Arrival in the world of Hermea
label arrival:
    scene arrival with Dissolve(.5)
    show milim_idle at right with Dissolve(.5)
    milim "Greetings human, welcome to this world. Do you remember your name?"
    $ player_name = renpy.input("What is your name?",length = 25).strip()
    if player_name == "David von Bogaren":
        milim "How interestingly fitting. I will allow it."
    else:
        milim "Now that isnt a noble name at all."
    
    default arrival_menu_choices = set()

    label arrival_menu:
        menu:
            set arrival_menu_choices
            "Where am I?":
                milim "You are on the glorious continent of Hermea, in the kingdom Hermea."
                jump arrival_menu
            "Who are you?":
                milim "I am Milim, the chairman of the mages tower of Tamra. Which we are currently inside of."
                jump arrival_menu
            "Safe this world, what do you mean?":
                milim "There is a gruesome threat in our beautiful kingdom. Hordes upon hordes of grotesque monsters which need to be subuded"
                jump arrival_menu

    milim "Enough about this for now. I think it will be more practical to show you. Follow me."
    jump arrival_tamra_church

# Tamra_Tutorial Screen with unlocks
default church_unlocked = False
default guild_unlocked = False
default blacksmith_unlocked = False

screen tamra_tutorial: 
    if church_unlocked == True:
        use call_image_button_no_target(church, Jump("church_introduction"))
    if guild_unlocked == True:
        use call_image_button_no_target(guild, Jump("guild_introduction"))
    if blacksmith_unlocked == True:
        use call_image_button_no_target(blacksmith, Jump("blacksmith_introduction"))

# Introduction to the church
label arrival_tamra_church:
    scene tamra with Dissolve(.5)
    show milim_idle at right with Dissolve(.5)
    milim "This is the village of Tamra. Well some even consider it a small city. It is where you will be living and working from now on."
    milim "First up we will need to get you some documents. Lets head to the church."
    milim "The church is the big building, south of the village plaza. Click on it." 
    hide milim_idle with Dissolve(.5)
    $ church_unlocked = True
    call screen tamra_tutorial

label church_introduction:
    scene church with Dissolve(.5)
    show milim_idle at right with Dissolve(.5)
    milim "Larisa, I would like to speak with you. There is someone who needs your help."
    show larisa_idle at left with moveinleft
    larisa "Hello Milim, how nice to see you. Might I ask who your friend is?"
    milim "His name is David von Bogaren and he needs some official documents."
    larisa "Is that so? Intriguing. I will see what I can do but what do I get in return?"
    
    default church_menu_choices = set()

    label church_menu:
        menu:
            set church_menu_choices
            "I promise to repay you some day.":
                larisa "Repay me? I am after no worldy payment dear."
                jump church_menu
            "What do you want in return?":
                larisa "How about you offer me your service someday once you have become an adventurer?"
                menu:
                    "Yes":
                        larisa "Perfect. Then let me get you some documents ready."
                    "No":
                        larisa "In that case I dont think I am able to help you."
                        milim "He will offer his help if it is equivalent to your service today, dont worry."
                        larisa "Fine but only because its you. Let me get those documents ready for you."

    hide larisa_idle with Dissolve(.5)
    milim "It wont be too much, dont worry. After all you are under the mages tower's protection."
    player "I hope so."
    show larisa_idle at left with Dissolve(.5) 
    larisa "Here you go."
    $ inventory_unlocked = True
    $ inventory.add_item(documents)
    show screen call_gui
    milim "How about you open your inventory at the top left and take a look?"
    milim "Great. Now that you have your documents we can register you at the adventurers guild."
    $ church_unlocked, guild_unlocked = False, True
    jump arrival_tamra_guild

# Adventurers guild Screen with unlocks
default reception_unlocked = False
default quest_board_unlocked = False
default tavern_unlocked = False

screen guild:
    if reception_unlocked == True:
        use call_image_button_no_target(reception, Jump("reception_introduction"))
    if quest_board_unlocked == True:
        use call_image_button_no_target(quest_board, Jump("quest_board_introduction"))
    if tavern_unlocked == True:
        use call_image_button_no_target(arrow_left, Jump("tavern_introduction"))

# Introduction to the adventurers guild
label arrival_tamra_guild:
    scene tamra with Dissolve(.5)
    show milim_idle at right with Dissolve(.5)
    milim "You will be working as an adventurer from now on, taking on quests in the name of the mages tower and slaying monsters."
    milim "For this you will need to be registered as an official guild member."
    milim "The adventurers guild is the building north of the plaza. Click on it to enter."
    call screen tamra_tutorial

label guild_introduction:
    scene guild with Dissolve(.5)
    show milim_idle at right with Dissolve(.5)
    milim "There is a lot to do inside the guild but I guess it is best to let them introduce themselves."
    show heidra_idle at left with moveinleft
    heidra "Welcome to the adventurers guild. I am Heidra, the guild receptionist. How can I help you?"
    milim "Now come on, dont be shy, you can talk for yourself."
    menu:
        "W-w-well I... I want... ahem.":
            heidra "You want to register as an adventurer, dont you?"
            milim "He isnt normally like that, dont worry."
        "I am here to register as an adventurer.":
            pass            
    heidra "Well then follow me. I will tell you all about the guild while we are at it."
    milim "Meet me outside once you are done"
    hide milim_idle with moveoutright 
    heidra "If you ever have any questions, just come see me at the front desk. Lets go there to finish your registration."
    $ reception_unlocked = True
    call screen guild 

label reception_introduction:
    scene guild_reception with Dissolve(.5)
    show heidra_idle at left with Dissolve(.5)
    heidra "This is my humble office. Feel free to visit me anytime. So now for your registration..."
    jump verification

label verification:
    heidra "Please show me your legal documents. No worries, it is just a formality for me to check them." 
    hide screen call_gui
    call screen inventory(selection_mode=True) with Dissolve(.5)
    if _return == documents:
        show screen call_gui
        heidra "Wonderful, let me take a quick look at them. Since you are with the mages tower, there likely wont be any issues."
    else:
        show screen call_gui
        heidra "This is not what I needed, please give me your documents."
        jump verification
    $ inventory.add_item(guild_certificate)
    heidra "All done. Now this right here is your verification as a member of our guild. Dont lose it."
    heidra "Now let me show you around and explain how life as an adventurer works."
    $ reception_unlocked, quest_board_unlocked = False, True
    jump guild_introduction_part2

label guild_introduction_part2:
    scene guild with Dissolve(.5)
    show heidra_idle at left with Dissolve(.5)
    heidra "As an adventurer you would normally take on jobs from the quest board at the right."
    call screen guild with Dissolve(.5)

label quest_board_introduction:
    scene guild_questboard with Dissolve(.5)
    heidra "This is where quests will appear. They arent as relevant to you as you will most likely get your quests directly from the mages tower."
    heidra "Quests appear from grade 0 to grade 9. Grade 0 is the easiest and grade 9 the hardest."
    heidra "You are currently a grade 1 adventurer. With each quest you complete, you will gain rewards and grade points."
    heidra "A grade 1 quest awards one grade 1 point. Once you have 20 points of a grade you will be promoted to the next grade."
    heidra "Even as a grade 1 you could still take on a grade 9 quest but we highly discourage that if you want to stay alive."
    $ quests_unlocked = True
    heidra "You can see your active quests in the quest menu at the top."
    $ quest_board_unlocked, tavern_unlocked = False, True
    jump guild_introduction_part3

label guild_introduction_part3:
    scene guild with Dissolve(.5)
    show heidra_idle at right with Dissolve(.5)
    heidra "Lastly there is the tavern, the most known part of the guild I guess."
    call screen guild

label tavern_introduction:
    scene guild_tavern with Dissolve(.5)
    show heidra_idle at left with Dissolve(.5)
    heidra "Here you can not only buy food and beverages but also make connections with other adventurers."
    heidra "Some look for partners or groups to go on quests together. Less reward but also less risk."
    jump guild_introduction_end

label guild_introduction_end:
    scene guild with Dissolve(.5)
    show heidra_idle at left with Dissolve(.5)
    heidra "Now that is it for now. Do you have any other questions before I let you go?"
    call menu_guild_questions
    
label menu_guild_questions:
    menu:
        "No thank you":
            heidra "Alright then, good luck on your journey from now on."
            $ guild_unlocked, blacksmith_unlocked = False, True
            jump arrival_tamra_blacksmith
        "Are there other branches of the guild?":
            heidra "Well of course there are. In any city or major village you will find a branch or at least a quest board."
            call menu_guild_questions
        "Is there a place to sleep here?":
            heidra "Of course. See that door at the back? We have some rooms you can rent for cheap."
            call menu_guild_questions

label arrival_tamra_blacksmith:
    scene tamra with Dissolve(.5)
    show milim_idle at right with Dissolve(.5)
    milim "What took you so long, I could have done half a days work in that time. Well I guess you need to get used to this world after all."
    milim "Now then, follow me. A real adventurer needs some good gear to start on his journey. Lets head to the blacksmith."
    milim "It is the building west of the plaza. Click on it to enter."
    call screen tamra_tutorial

label blacksmith_introduction:
    scene blacksmith with Dissolve(.5)
    show milim_idle at left with Dissolve(.5)
    milim "It is always so hot in here, I hate it. Hello, anyone there?"
    show mern_idle at right with moveinright
    mern "Welcome to my blacksmithy Milim. How can I assist you today?"
    milim "I am looking to get some equipment for this new adventurer of ours. Think you can help him?"
    mern "If anyone can, it will always be me. Let me take a good look."
    show mern_idle:
        ease 0.5 zoom 1.5 yalign 1.0
        pause 1.0
        ease 0.5 zoom 1.0 yalign 1.0
    pause 2.0
    mern "He is rather tall but ugly as most humans. I think I have just the right equipment for him."
    hide mern_idle with moveoutright
    pause 1.0
    show mern_idle at right with moveinright
    $ inventory.add_item(iron_sword, iron_armor)
    mern "Here you go, take these."
    mern "I think they will do for now, right?"
    menu:
        "Yes":
            mern "Great, then lets talk about the payment."
        "No":
            mern "Great, then lets talk about the payment."
    milim "How much do you want?"
    mern "It is good qualitly, completely new and handmade by none other than myself. Ten coins." 
    milim "Ten? I can buy myself a whole dwarf for that much. Seven and one for goodwill."
    mern "Tsk, fine."
    jump arrival_tamra_end

label arrival_tamra_end:
    scene tamra with Dissolve(.5)
    milim "Phew, finally done, that was quite an ordeal. I need to rest now. If you have any other questions, come find me at the mages tower."
    show screen call_gui
    jump tamra   