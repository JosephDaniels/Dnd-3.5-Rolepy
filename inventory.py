
inventory_body = 

Inventory(object):
    def __init__(self):
        ## All inventory slots expect an item object of type wearable
        ## see equip_item() for more details
        self.underwear = {
            self.chest = None, # bra for example
            self.crotch = None, # panties for example
            self.feet = None
            }
        self.wear = { ## Long dresses and robes might take up both torso and pants slot
            self.eyes = None, # glasses for example
            self.face = None, # masks only
            self.head = None, # hats only
            self.neck = None, # scarves and necklaces
            self.chest = None, # shirts and dresses
            self.waist = None, # belt slot
            self.wrist = None, # bracelets
            self.legs = None, # pantaloons
            self.feet = None, # shoes, boots, slippers
            self.hands = None # gloves
            self.ring_1 = None
            self.ring_2 = None
            }
        self.overwear = {
            self.chest = None, # jackets and coats
            self.back = None, # capes and cloaks
            }
        self.armour = {
            self.head = None, # helmet
            self.neck = None, # gorget
            self.shoulders = None, # pauldrons
            self.chest = None, # breast plate or chain mail
            self.arms = None, # arm plate and bracers
            self.legs = None, # leg plate
            self.feet = None, # armored footwear, replaces shoes
            self.hands = None # gauntlets
            }
        self.weapon_loadout = {
            self.right_hand = None,
            self.left_hand = None,
            self.sheath = None,
            self.2nd_sheath = None
            self.quiver = None
            }

    def equip_item(self, item, equip_location):
        
