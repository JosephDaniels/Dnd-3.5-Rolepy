Inventory(object):
    def __init__(self):
        ## All inventory slots expect an item object of type wearable
        ## see equip_item() for more details
        self.inventory_items = []
        self.carrying_capacity = 0 # Maximum defined by character strength and limited by what your bags can hold
        self.underwear = {
            chest = None, # bra for example
            crotch = None, # panties for example
            feet = None
            }
        self.wear = { ## Long dresses and robes might take up both torso and pants slot
            eyes = None, # glasses for example
            face = None, # masks only
            head = None, # hats only
            neck = None, # scarves and necklaces
            chest = None, # shirts and dresses
            waist = None, # belt slot
            wrist = None, # bracelets
            legs = None, # pantaloons
            feet = None, # shoes, boots, slippers
            hands = None # gloves
            ring_1 = None
            ring_2 = None
            }
        self.overwear = {
            chest = None, # jackets and coats
            back = None, # capes and cloaks
            }
        self.armour = {
            head = None, # helmet
            neck = None, # gorget
            shoulders = None, # pauldrons
            chest = None, # breast plate or chain mail
            arms = None, # arm plate and bracers
            legs = None, # leg plate
            feet = None, # armored footwear, replaces shoes
            hands = None # gauntlets
            }
        self.weapon_loadout = {
            right_hand = None,
            left_hand = None,
            sheath = None,
            2nd_sheath = None
            quiver = None
            }

    def equip_item(self, item, item_layer, equip_location):
        if item in self.inventory_items:  # You physically have the item
            if item.valid_equip_location == equip_location:
                self.item_layer[equip_location] = item
            self.inventory_items.pop(item)

def test():
    pass

if __name__ == "__main__":
    test()