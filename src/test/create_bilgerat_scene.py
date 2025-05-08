from scene import Scene

bilgerat_scene = Scene(
    name="Bilgerat's Cellar",
    description="Below the crooked floorboards of a crumbling shack lies Bilgerat’s private cellar—musty, dimly lit, and suspiciously well-stocked. The air is thick with the scent of old wood, pork grease, and candlewax. Dust motes drift lazily through narrow shafts of light from a cracked window, while the locked cellar door creaks ominously with every passing breeze above.",
    characters=[
        "Doormouse: Alert, Watchful, Fast - A twitchy little gray rodent with bright, intelligent eyes. Skitters between shadows, hides under table or in cabinet.",
        "Cat: Playful - A black-and-white mouser with one torn ear, fond of knocking over things and tormenting the doormouse."
    ],
    objects=[
        "Table: Rickety and uneven; one leg has been reinforced with a bone.",
        "Journal: Bound in cracked leather. Smeared, encrypted, disturbing.",
        "Quill: Black feather, sharpened cruel point.",
        "Cup (Water): Chipped, half-full. Surprisingly clean.",
        "Plate (Porkchop): Grease congealing. Still warm.",
        "Knife: Dull, dried blood at the tip.",
        "Fork: Two tines bent. Probably used for defense.",
        "Chair: One-legged, awkwardly propped.",
        "Cabinet: Creaky, odd smells. Holds rot and mystery.",
        "Shelf: Jars, candles, and skulls—some disturbingly human.",
        "Cheese: Moldy, gnawed. Maybe bait.",
        "Bed: Hay-stuffed, decade-old sheets. Goblin sweat and regret.",
        "Window: Barred, tiny, grime-streaked panes.",
        "Cellar Door (Locked): Thick iron latch. Reinforced. Scratches on the inside.",
        "Candle: Nearly spent. Flickers with invisible breath."
    ],
    lighting="dim",
    time_of_day="night"
)

# Save the scene
bilgerat_scene.save_to_file("../scenes/bilgerats_cellar.json")
