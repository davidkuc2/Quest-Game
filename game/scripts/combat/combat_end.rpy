# reward for win
label combat_reward:

    $ renpy.notify("You are victorious!")

    python:
        import random
        import copy

        # --- grant money depending on grade---
        money_reward = renpy.random.randint(10, 100) * player_combat.grade
        inventory.money += money_reward
        renpy.notify("You found {} coins!".format(money_reward))

        # --- grant lootboxes random depending on grade ---
        lootbox_types = [follower_lootbox, armor_lootbox, weapon_lootbox, accessory_lootbox]
        num_lootboxes = player_combat.grade
        lootbox_summary = {}

        for _ in range(num_lootboxes):
            chosen_lootbox_template = random.choice(lootbox_types)
            
            lootbox_to_add = copy.copy(chosen_lootbox_template)
            lootbox_to_add.quantity = 1
            inventory.add_item(lootbox_to_add)

            lootbox_summary[chosen_lootbox_template.name] = lootbox_summary.get(chosen_lootbox_template.name, 0) + 1

        if lootbox_summary:
            summary_text = "You received: " + ", ".join(["{}x {}".format(qty, name) for name, qty in lootbox_summary.items()])
            renpy.notify(summary_text)

    hide screen fight
    show screen call_gui
    $ combat_reset()                        # resets all characters back to default state 
    jump expression after_combat_label      # jump to the label name stored in the variable


# end game on loss 
label combat_loss:                          # kill the player at loss

    "You have lost the fight and died!"
    $ combat_reset()                        # reset all characters back to default state
    $ MainMenu(confirm=False)()             # return to main menu