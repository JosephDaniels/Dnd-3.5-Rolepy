names = [
    "gumbo",
    "bindle",
    "stiff",
    "dummy",
    "hombre",
    "dave",
    "tom",
    "jerry",
    "Alderna Arvillain"
]

# NPC Name Generator:
# a generator that creates npcs with Race, hair, build, eye, age, gender, name

# NOTE: will make so npcs are more/less likely to have grey/white hair if older/younger
# NOTE: will make so npcs of different races actually have proper age ranges for that race
# NOTE: it would be cool to add job descriptions...

import random

race_list = [
    "Human",
    "Half Elf",
    "Elf",
    "Dwarf",
    "Half Orc",
    "Gnome",
    "Halfling",
]

build_by_race = {
    "human": [
        "tall",
        "tall and lanky",
        "lanky",
        "athletic",
        "able bodied",
        "brawny",
        "burly",
        "full-figured",
        "short and stout",
        "chunky",
        "muscular",
        "flabby",
        "petite",
        "bony",
        "scrawny",
        "spindly",
        "lithe",
        "thin",
        "gaunt",
        "lean",
        "slender",
        "slim",
        "feeble",
        "sickly"],
    "half elf": [
        "flushed",
        "slim",
        "lanky",
        "athletic",
        "able bodied",
        "muscular",
        "flabby",
        "petite",
        "bony",
        "scrawny",
        "spindly",
        "lithe",
        "thin",
        "gaunt",
        "lean",
        "slender",
        "twiggy"],
    "elf": [
        "lanky",
        "athletic",
        "able bodied",
        "muscular",
        "flabby",
        "petite",
        "bony",
        "scrawny",
        "spindly",
        "lithe",
        "thin",
        "gaunt",
        "lean",
        "slender",
        "twiggy",
        "dainty",
        "delicate",
        "slight",
        "little",
        "gangly",
        "wan",
        "fragile",
        "emaciated",
        "frail",
        "graceful",
        "feeble",
        "weak looking",
        "slim",
        "puny",
        "feeble",
        "sickly"],
    "dwarf": [
        "able bodied",
        "brawny",
        "beefy",
        "burly",
        "rotund",
        "ample",
        "full-figured",
        "buxom",
        "pudgy",
        "husky",
        "stout",
        "short and stout",
        "chunky",
        "muscular",
        "thickset",
        "sturdy",
        "flabby",
        "fat",
        "plump",
        "stocky",
        "petite",
        "robust",
        "portly",
        "bulky",
        "hefty"],
    "half orc": [
        "lumbering",
        "skinny",
        "curvy",
        "slender",
        "chunky",
        "plump",
        "fat",
        "obese",
        "muscular",
        "shapely",
        "large",
        "massive"],
    "gnome": [
        "petite",
        "small",
        "tiny",
        "miniscule"],
    "halfling": [
        "petite",
        "small",
        "tiny",
        "miniscule"]
}

hair_len = [
    "short",
    "short cropped",
    "spiky",
    "shoulder length",
    "long",
]

hair_descriptions = [
    "wavy",
    "curly",
    "straight",
    "wispy",
    "windswept",
    "tumultuous",
    "braided",
    "pulled back",
    "neatly kept",
    "untidy",
    "greasy",
    "oily",
    "patches of",
    "blood matted",
    "limp",
    "thin",
    "unkempt",
    "thick",
    "unruly",
    "luscious",
    "silky",
    "soft",
]

hair_color_by_race = {
    "human": [
        "blonde",
        "light blonde",
        "strawberry blonde",
        "champagne",
        "ash",
        "dirty blonde",
        "pecan",
        "straw",
        "wheat coloured",
        "sandy",
        "amber",
        "butterscotch",
        "goldenrod",
        "faded marigold",
        "red",
        "brick red",
        "fiery red",
        "flaming red",
        "indian red",
        "crimson",
        "dark crimson",
        "reddish brown",
        "raw sienna",
        "burnt sienna",
        "burnt umber",
        "auburn",
        "copper",
        "maroon",
        "mahogany",
        "copper brown",
        "brown",
        "nutmeg",
        "walnut",
        "mousy brown",
        "chestnut",
        "roasted cinnamon",
        "chocolate",
        "cocoa",
        "coffee",
        "ash brown",
        "sepia",
        "black",
        "jet black",
        "smokey ash",
        "raven",
        "vermilion"],
    "human old": [
        "salt and pepper",
        "silver",
        "grey",
        "white",
        "snow white",
        "blondish-white"],
    "half elf old": [
        "snow white",
        "ivory",
        "silver",
        "grey"],
    "half elf": [
        "blonde",
        "light blonde",
        "strawberry blonde",
        "champagne",
        "ash",
        "dirty blonde",
        "pecan",
        "straw",
        "wheat coloured",
        "sandy",
        "amber",
        "butterscotch",
        "goldenrod",
        "faded marigold",
        "red",
        "brick red",
        "fiery red",
        "flaming red",
        "indian red",
        "crimson",
        "dark crimson",
        "reddish brown",
        "raw sienna",
        "burnt sienna",
        "burnt umber",
        "auburn",
        "copper",
        "maroon",
        "mahogany",
        "copper brown",
        "brown",
        "nutmeg",
        "walnut",
        "mousey brown",
        "chestnut",
        "roasted cinnamon",
        "chocolate",
        "cocoa",
        "coffee",
        "ash brown",
        "sepia",
        "black",
        "wine",
        "caramel",
        "jet black",
        "smokey ash",
        "raven",
        "vermilion"],
    "elf old": [
        "snow white",
        "ivory",
        "pale ivory",
        "muted grey",
        "ice grey",
        "ash grey",
        "grey"],
    "elf": [
        "rosewood",
        "sandlewood",
        "honey ash",
        "light blonde"
        "golden blonde",
        "cherry wine",
        "cherry wood",
        "coral",
        "brandy",
        "fennel",
        "wine",
        "nutmeg",
        "honey oak",
        "caramel",
        "ginger",
        "saffron",
        "burnished sun",
        "yellow maple",
        "clove",
        "coffee",
        "autumn red",
        "redwood",
        "rich chocolate",
        "dark redwood",
        "oak",
        "mahogany",
        "mauve",
        "taupe",
        "ebony",
        "midnight black"],
    "dwarf old": [
        "white",
        "flint grey",
        "slate",
        "shale",
        "adobe grey",
        "rainy grey",
        "cinder grey",
        "silver",
        "tarnished nickel"],
    "dwarf": [
        "brass",
        "copper",
        "gold",
        "dull birch",
        "sandstone",
        "antique brass",
        "old brick",
        "sunbaked clay",
        "smoke",
        "butter rum",
        "dark ale",
        "beer",
        "coal",
        "earthen brown",
        "brick red",
        "sierra",
        "maize",
        "clay brown",
        "rich chocolate",
        "harvest brown",
        "ginger",
        "walnut"],
    "half orc old": [
        "ashen grey",
        "dingy grey",
        "dirty white",
        "fading brown",
        "white",
        "grey"],
    "half orc": [
        "dingy brown",
        "murky chestnut",
        "rust",
        "mud",
        "pistachio",
        "saddlebrown",
        "dull brown",
        "oily brown",
        "chartreuse",
        "mustard tan",
        "mustard",
        "moss",
        "dull lime",
        "brownish-green",
        "greenish-yellow",
        "puce",
        "olive drab",
        "khaki green",
        "tawny brown",
        "soot",
        "charcoal",
        "oily smoke",
        "coal",
        "pitch black"],
    "gnome old": [
        "pewter",
        "grey",
        "snowy",
        "silver"
        "white"],
    "gnome": [
        "earthen",
        "pitch black",
        "mustard",
        "blonde",
        "light blonde",
        "champagne",
        "ash",
        "dirty blonde",
        "pecan",
        "straw",
        "wheat coloured",
        "sandy",
        "amber",
        "butterscotch",
        "goldenrod",
        "flaming red",
        "indian red",
        "crimson",
        "dark crimson",
        "reddish brown",
        "raw sienna",
        "burnt sienna",
        "burnt umber",
        "auburn",
        "copper",
        "maroon",
        "mahogany",
        "nutmeg",
        "walnut",
        "mousy brown",
        "chestnut",
        "roasted cinnamon",
        "chocolate",
        "cocoa",
        "coffee",
        "ash brown",
        "black",
        "jet black",
        "smokey ash",
        "raven",
        "vermillion"],
    "old halfling": [
        "cream",
        "snowdrop",
        "blondish-white",
        "faded ginger",
        "frosted white"],
    "halfling": [
        "cream",
        "daffodil",
        "buttercup",
        "dandelion",
        "gingerbread",
        "goldenrod",
        "marigold",
        "fox red",
        "maple",
        "amber",
        "henna",
        "copper",
        "copper brown",
        "walnut",
        "honey gold",
        "heather",
        "indian red",
        "spice brown",
        "mulberry",
        "ginger",
        "peanut",
        "autumn pumpkin",
        "carrot",
        "caramel"],
    # weird colours
    # have a small percentage chance of generating
    # for humans, elves, half elves or gnomes, but
    # NOT dwarves or half-orcs
    "special hair": [
        "blueish-white",
        "purpleish-blue",
        "pink",
        "cobalt",
        "navy blue",
        "cirulean",
        "blondish-white",
        "orange",
        "aquamarine",
        "sapphire",
        "ruby",
        "emerald",
        "violet",
        "teal",
        "amethyst",
        "raspberry",
        "plum",
        "fuschia",
        "turquoise",
        "cherry",
        "peacock blue",
        "jade",
        "spruce green",
        "garnet",
        "lavendar",
        "orchid pink",
        "pea green",
        "periwinkle",
        "salmon",
        "magenta",
        "rusty orange",
        "mint green",
        "pale pink",
        "peach",
        "primrose yellow",
        "royal blue",
        "midnight blue",
        "ultramarine",
        "wintergreen"
    ],
}

eye_desc = [
    "large",
    "round",
    "beady",
    "small",
    "tiny",
    "almond shaped",
    "oval",
    "heavy-lidded",
    "tired",
    "bright",
    "dancing",
    "excited",
    "smouldering",
    "deep",
    "sparkling",
    "little",
    "curious",
    "inquisitive",
    "angry",
    "weary",
]

eye_colors = [
    "blue",
    "grey",
    "green",
    "ultramarine",
    "ruby red",
    "hazel",
    "blue-grey",
    "light green",
    "crimson",
    "sky blue",
    "baby blue",
    "emerald green",
    "dark brown",
    "sapphire blue",
    "steely grey",
    "light purple",
    "fuschia",
    "maroon",
    "aquamarine",
    "turquoise",
    "light brown",
]
# age ranges for each race
# (later add several possible descriptors for each range to create variety)
age_ranges = {
    "human": {
        "baby": (0, 1),
        "toddler": (2, 3),
        "very young": (4, 6),
        "child": (7, 10),
        "pre-teen": (11, 12),
        "young teen": (13, 15),
        "teen": (16, 18),
        "young adult": (19, 24),
        "adult": (25, 35),
        "middle aged": (36, 49),
        "over the hill": (50, 64),
        "senior": (65, 79),
        "geriatric": (80, 120),
    },
    "half elf": {
        "baby": (0, 3),
        "toddler": (4, 5),
        "very young": (6, 8),
        "child": (9, 12),
        "pre-teen": (13, 16),
        "young teen": (17, 21),
        "teen": (22, 27),
        "young adult": (28, 34),
        "adult": (35, 61),
        "middle aged": (62, 92),
        "over the hill": (93, 124),
        "senior": (125, 184),
        "geriatric": (185, 200),
    },
    "elf": {
        "baby": (0, 5),
        "toddler": (6, 10),
        "very young": (11, 19),
        "child": (20, 29),
        "pre-teen": (30, 39),
        "young teen": (40, 55),
        "teen": (56, 74),
        "young adult": (75, 109),
        "adult": (110, 174),
        "middle aged": (175, 262),
        "over the hill": (263, 349),
        "senior": (350, 449),
        "geriatric": (450, 750),
    },
    "dwarf": {
        "baby": (0, 3),
        "toddler": (4, 7),
        "very young": (8, 12),
        "child": (13, 18),
        "pre-teen": (19, 23),
        "young teen": (24, 28),
        "teen": (29, 33),
        "young adult": (34, 39),
        "adult": (40, 124),
        "middle aged": (125, 187),
        "over the hill": (188, 249),
        "senior": (250, 349),
        "geriatric": (350, 450),
    },
    "half orc": {
        "baby": (0, 1),
        "toddler": (2, 3),
        "very young": (4, 6),
        "child": (7, 9),
        "pre-teen": (10, 11),
        "young teen": (12, 14),
        "teen": (15, 17),
        "young adult": (18, 19),
        "adult": (20, 29),
        "middle aged": (30, 44),
        "over the hill": (45, 59),
        "senior": (60, 79),
        "geriatric": (80, 90),
    },
    "gnome": {
        "baby": (0, 2),
        "toddler": (3, 6),
        "very young": (7, 10),
        "child": (11, 14),
        "pre-teen": (15, 19),
        "young teen": (20, 24),
        "teen": (25, 31),
        "young adult": (32, 39),
        "adult": (40, 99),
        "middle aged": (100, 149),
        "over the hill": (150, 199),
        "senior": (200, 299),
        "geriatric": (300, 400),
    },
    "halfling": {
        "baby": (0, 2),
        "toddler": (3, 5),
        "very young": (6, 8),
        "child": (9, 11),
        "pre-teen": (12, 14),
        "young teen": (15, 18),
        "teen": (19, 23),
        "young adult": (24, 29),
        "adult": (30, 49),
        "middle aged": (50, 74),
        "over the hill": (75, 99),
        "senior": (100, 149),
        "geriatric": (150, 175),
    },
}

ages = [
    "very young",
    "baby",
    "toddler",
    "child",
    "geriatric",
    "senior",
    "middle aged",
    "adult",
    "young",
    "teenaged",
    "rickety old",
    "retired",
]

male_names_by_race = {
    "human": [
        "Cedric",
        "Samson",
        "Jacob",
        "Jake",
        "Tom",
        "Dick",
        "Harry",
        "Ronald",
        "Mercutio",
        "Horatio",
        "Wilburforce",
        "Marcus",
        "Kelvin",
        "Kenneth",
        "Pip",
        "Frye",
        "Joe",
        "Joseph",
        "Edward",
        "Columbus",
        "Arthur",
        "Conan",
        "Doyle",
        "Mark",
        "Twain",
        "William",
        "Shakespeare",
        "Van",
        "Russel",
        "Sebastian",
        "Belvi",
        "Bernard",
        "Watson",
        "Cyril",
        "Cyrus",
        "Duncan",
        "Burton",
        "Barret",
        "Earle",
        "Forrest",
        "Strider",
        "Erwyn",
        "Jonah",
        "Agamem",
        "Mercallius",
        "Virgil",
        "Memron",
        "Shepp",
        "Manthrop",
        "Scallywag",
        "Barnabus",
        "Judas",
        "Hectar",
        "Charlemagne",
        "Calam",
        "Belork",
        "Mildor",
        "Bryyn",
        "Brock",
        "Westley"],
    "elf": [
        "Oducniob",
        "Anegert",
        "Girueh",
        "Ralliuh",
        "Odaroun",
        "Enurread",
        "Tocuhear",
        "Rahentar",
        "Elhaur",
        "Urigusaal",
        "Holrueh",
        "Larnir",
        "Rigrelt",
        "Imihr",
        "Lohand",
        "Rigrelt",
        "Atabion",
        "Casahan",
        "Legtiur"],
    "dwarf": [
        "Bedol",
        "Bitek",
        "Dakag",
        "Datgih",
        "Detyal",
        "Gdot",
        "Gof",
        "Grib",
        "Hedtin",
        "Korfi",
        "Liriko",
        "Nalrat",
        "Nengog",
        "Ngol",
        "Dhid",
        "Dollad",
        "Nkin",
        "Ragrur",
        "Rof",
        "Tned",
        "Tohul",
        "Dashor",
        "Drogg",
        "Eiro",
        "Eogi",
        "Gohon",
        "Hohfit",
        "Hvig",
        "Kuhri",
        "Lerob",
        "Tohrir",
        "Yonov",
        "Ryah",
        "Vdoh",
        "Raste",
        "Vikof",
        "Yeru",
        "Rnur",
        "Rsah",
        "Lamov",
        "Hkifot"],
    "half orc": [
        "Pigar",
        "Gagdush",
        "Braart",
        "Poshnak",
        "Rirg",
        "Vulo",
        "Krark",
        "Vrorz",
        "Ronk",
        "Grir",
        "Vring",
        "Pishnak",
        "Higar",
        "Erugrog",
        "Praak",
        "Kadish",
        "Ruurug",
        "Vrang",
        "Gignak",
        "Praagdish",
        "Hir",
        "Vridush",
        "Brorbag",
        "Brirz",
        "Gurz",
        "Kraurk",
        "Panak",
        "Ridish",
        "Brugor",
        "Gaalg",
        "Prurz",
        "Vrunak",
        "Eruur",
        "Bang",
        "Barz",
        "Vog",
        "Varug",
        "Guushnak",
        "Vigar",
        "Prilo",
        "Pagash",
        "Pronk",
        "Grur"],
    "gnome": [
        "Panward",
        "Horeak",
        "Tip",
        "Bellgretor",
        "Adoaver",
        "Vicril",
        "Norgold",
        "Travon",
        "Chip",
        "Panroar",
        "Elamros",
        "Nodrak",
        "Nodward",
        "Davgeon",
        "Shanan",
        "Udohand",
        "Marhorn",
        "Harmond",
        "Xavgeon",
        "Elamroar",
        "Udofalcon",
        "Seamourn",
        "Walril",
        "Oloros",
        "Vicrry",
        "Crudak",
        "Dobbin",
        "Thogretor",
        "Olonan",
        "Ricendithas",
        "Xangretor",
        "Walhand",
        "Nodgeon",
        "Adoster",
        "Petian",
        "Kevtiln",
        "Oloneiros",
        "Nerio",
        "Bornak",
        "Xavian",
        "Xavier",
        "Bellannan",
        "Nortiln",
        "Wilward",
        "Beltiln",
        "Wileon",
        "Bellerios",
        "Adofire",
        "Sharil",
        "Waleak",
        "Zanster"],
    "halfling": [
        "Adalgrim",
        "Adelard",
        "Alton",
        "Andwise",
        "Anson",
        "Balbo",
        "Bandobras",
        "Beau",
        "Bill",
        "Bingo",
        "Bodo",
        "Bolger",
        "Bungo",
        "Cade",
        "Calkin",
        "Cotman",
        "Cottar",
        "Drogo",
        "Dudo",
        "Eldon",
        "Falco",
        "Fastolph",
        "Filibert",
        "Flambard",
        "Fosco",
        "Garret",
        "Genrill",
        "Griffo",
        "Halfred",
        "Hildigrim",
        "Hob",
        "Holman",
        "Kepli",
        "Largo",
        "Longo",
        "Lotho",
        "Lyle",
        "Milo",
        "Minto",
        "Morro",
        "Mosco",
        "Mungo",
        "Odo",
        "Olo",
        "Osborn",
        "Otho",
        "Paldo",
        "Peregrin",
        "Pervince",
        "Pimpernell",
        "Polo",
        "Ponto",
        "Porto",
        "Posco",
        "Ronald",
        "Rorimac",
        "Roscoe",
        "Rufus",
        "Sam",
        "Sancho",
        "Saradac",
        "Seredoc",
        "Theadric",
        "Tolman",
        "Wellby",
        "Wilcome"],
    "half elf": [
        "gaylord treehug"
    ]
}

female_names_by_race = {
    "human": [
        "Mildred",
        "Mary Anna",
        "Samantha",
        "Abigail",
        "Jewel",
        "Sarai",
        "Elowyn",
        "Weayn",
        "Chenai",
        "Sarah",
        "Anna",
        "Cora",
        "Dianna",
        "Caroline",
        "Elvia",
        "Dolores",
        "Constance",
        "Charity",
        "Arielle",
        "Lucillia",
        "Noemi",
        "Solari",
        "Daniella",
        "Lotherina",
        "Crystal",
        "Sapphire",
        "Angel",
        "Mia",
        "Misty",
        "Shoshauna",
        "Lorna",
        "Trudy",
        "Vallerina",
        "Valerie",
        "Rashika",
        "Samma",
        "Melissa",
        "Mortitia",
        "Candisse",
        "Clarissa",
        "Marisa",
        "Marie",
        "Ella",
        "Gretel",
        "Irena",
        "Sabrina",
        "Laura",
        "Monique",
        "Julia",
        "Jacqueline"],
    "elf": [
        "Nannuah",
        "Areres",
        "Lanuyl",
        "Lauryll"
        "Inorarin",
        "Ibdaln",
        "Isabagaic",
        "Dinoet",
        "Aresaar",
        "Eluraor",
        "Eniblier",
        "Ihetaheln",
        "Leteuh",
        "Lilaur",
        "Ilyyma",
        "Ilaneir",
        "Dalicied",
        "Danall",
        "Idolluan",
        "Nashleen",
        "Nedael",
        "Radecird"],
    "half orc": [
        "Eruur",
        "Vigara",
        "Gruu",
        "Hig",
        "Haagdish",
        "Baool",
        "Karza",
        "Ridush",
        "Haadash",
        "Krarag",
        "Pigar",
        "Kik",
        "Eruol",
        "Kir",
        "Glort",
        "Grogpak",
        "Porash",
        "Bigar",
        "Paarz",
        "Giol",
        "Ginak",
        "Prarag",
        "Harz",
        "Pir",
        "Eraashnak",
        "Ginak",
        "Kalo",
        "Kirbag",
        "Brar",
        "Hidush",
        "Bourk",
        "Kaak",
        "Brirz",
        "Erong",
        "Hirg",
        "Gaol"],
    "dwarf": [
        "Ieta",
        "Irena",
        "Karene",
        "Yohae",
        "Dori",
        "Kofya",
        "Reese",
        "Maren",
        "Liya",
        "Liira",
        "Erocha",
        "Toira",
        "Iora",
        "Ira",
        "Vkyn",
        "Byoca",
        "Jyll",
        "Dolga",
        "Helga",
        "Tatab",
        "Tuse",
        "Eedi",
        "Fideh",
        "Sodi",
        "Taye",
        "Uuta",
        "Uori",
        "Rofina",
        "Auda",
        "Aani",
        "Garan",
        "Medukk",
        "Samara",
        "Yosash",
        "Riyi",
        "Nine",
        "Nabiv",
        "Hohna",
        "Shona",
        "Kasola",
        "Kekle",
        "Danre",
        "Femha",
        "Haki",
        "Lonfa",
        "Mafre",
        "Rehaha",
        "Rih",
        "Riha",
        "Mara",
        "Sovkuha",
        "Terbika",
        "Hcurni"],
    "gnome": [
        "Alilynn",
        "Krisnys",
        "Xyremita",
        "Eilthyra",
        "Victakain",
        "Caistina",
        "Yllacaryn",
        "Unaecaryn",
        "Janvyre",
        "Aludove",
        "Brestine",
        "Unaemita",
        "Ravalyassa",
        "Caronna",
        "Neriscaryn",
        "Gracekhan",
        "Eilnda",
        "Loraemita",
        "Therella",
        "Cailyassa",
        "Gurvyre",
        "Darsaadi",
        "Cordiana",
        "Tilly",
        "Stokain",
        "Brethana",
        "Yllaatra",
        "Prukahn",
        "Prukhana",
        "Markain",
        "Ravavyre",
        "Marella",
        "Fhavyre",
        "Zinnamorel",
        "Eillyn",
        "Ireatra",
        "Coratris",
        "Breatris",
        "Daratris",
        "Cailatris",
        "Eilcaryn",
        "Neristhana",
        "Stohana",
        "Fhalove",
        "Brenys",
        "Fhacaryn",
        "Fhaleatra",
        "Therthana",
        "Victacaryn",
        "Loraatis",
        "Irielynn"],
    "halfling": [
        "Adaldrida",
        "Amranth",
        "Amaryllis",
        "Angelica",
        "Aspodel",
        "Belba",
        "Belladonna",
        "Berylla",
        "Camellia",
        "Carissa",
        "Celandine",
        "Charmaine",
        "Cora",
        "Crystal",
        "Daisy",
        "Diamond",
        "Donamira",
        "Dora",
        "Eglantine",
        "Elanor",
        "Esmerelda",
        "Euphemia",
        "Gilly",
        "Gwiston",
        "Hilda",
        "Jillian",
        "Lavinia",
        "Lily",
        "Lidda",
        "Lobelia",
        "Malva",
        "Marigold",
        "May",
        "Melindy",
        "Mentha",
        "Merla",
        "Mimosa",
        "Mirabella",
        "Myrtle",
        "Pansy",
        "Pearl",
        "Pedderee",
        "Peony",
        "Petrilly",
        "Poppy",
        "Portia",
        "Primula",
        "Prisca",
        "Rose",
        "Ruby",
        "Seraphina",
        "Susannah",
        "Verna",
        "Viloet",
    ],
    "half elf": [
        "care fagwood",
        "caroline derpicus"
    ]
}

last_name_prefix = {
    "human": [
        "Smith",
        "Jacob",
        "Ander",
        "Micheal",
        "Snare",
        "Nick",
        "Vault",
        "Robert",
        "Bellia",
        "Bel",
        "Draft",
        "Corinth",
        "Sholla",
        "Soul",
        "Mana",
        "Brick",
        "Shale",
        "Earth",
        "Keen",
        "Lava",
        "Magma",
        "Plains",
        "Wicker",
        "Cobble",
        "Bleak",
        "Gam",
        "Wit",
        "River",
        "Song",
        "Ello",
        "Lytham",
        "Moon",
        "Forrest",
        "Pine",
        "Sand",
        "Desert",
        "Frost",
        "Heisen",
        "Schull",
        "Smar",
        "Raft"],
    "dwarf": [
        "Dark",
        "Blood",
        "Stone",
        "Rock",
        "Iron",
        "Nickel",
        "Copper",
        "Steel",
        "Brass",
        "Slate",
        "Shale",
        "Marble",
        "Ogre",
        "Grave",
        "Gravel",
        "Oak",
        "Axe",
        "Glitter",
        "God",
        "Doom",
        "Thunder",
        "Battle"],
    # need to add to half elf list
    "half elf": [
        "Mil",
        "Falcon",
        "Tale"],
    # elf_last_names_1
    "elf": [
        "Wisdom",
        "Forrest",
        "Arch"],
    # halforc_last_names_1
    "half orc": [
        "Gloop",
        "Breet",
        "Swamp",
        "Myre"],
    "gnome": [
        "Bee",
        "Tail",
        "Short",
        "Sand",
        "Trick",
        "Mongoth",
        "Foe",
        "Laugh",
        "Smile",
        "Home",
        "Silver",
        "Holly",
        "Mill",
        "Silent",
        "Tall",
        "Tumble",
        "Woods",
        "Sea",
        "Gravel",
        "Long",
        "Strife",
        "Steel",
        "Cup",
        "Goblins",
        "Brush",
        "Bush",
        "Tunnel",
        "Under",
        "Gold",
        "Vault",
        "Little",
        "Gladden",
        "Arcane",
        "Mage",
        "Spell",
        "Tinker",
        "Dig"],
    "halfling young": [
        "Amster",
        "Ashworthwy",
        "Bandawax",
        "Boffin",
        "Bolger",
        "Bracegirdle",
        "Brownlock",
        "Brushgather",
        "Bullroarer",
        "Bunce",
        "Burrows",
        "Chubb",
        "Cotton",
        "Dale",
        "Dudley",
        "Gammidge",
        "Gamwich",
        "Gardner",
        "Goodbarrel",
        "Goodbody",
        "Greenbottle",
        "Greenspan",
        "Grub",
        "Hamson",
        "Heathertoe",
        "Highhill",
        "Hilltopple",
        "Hornblower",
        "Jallisall",
        "Kaese Kalliwart",
        "Leagallow",
        "Lindenbrook",
        "Marmidas",
        "Melilot",
        "Millbridge",
        "Milliciny",
        "Montajay",
        "Newtan",
        "Oldfur",
        "Orgulas",
        "Ostgood",
        "Overhill",
        "Quettory",
        "Shortwick",
        "Sire",
        "Talbot",
        "Tealeaf",
        "Thorngage",
        "Tighfield",
        "Tosscobble",
        "Trill",
        "Underbough",
        "Weatherbee"],
    "halfling": [
        # (for adult to geriatric halflings)
        "Amber",
        "Brown",
        "Cold",
        "Crazy",
        "Curly",
        "Earth",
        "Far",
        "Fast",
        "Fat",
        "Fire",
        "Flow",
        "Forest",
        "Free",
        "Glitter",
        "Good",
        "Great",
        "Green",
        "Hairy",
        "Honor",
        "Healthy",
        "Home",
        "Hot",
        "Laughing",
        "Lightning",
        "Little",
        "Many",
        "Moon",
        "Nimble",
        "Plump",
        "Pretty",
        "Quick",
        "Rain",
        "Road",
        "Running",
        "Scatter",
        "Shadow",
        "Silver",
        "Simple",
        "Sky",
        "Slow",
        "Sly",
        "Smooth",
        "Spring",
        "Sprout",
        "Stout",
        "Sun",
        "Swift",
        "Tall",
        "Travelling",
        "Under",
        "Warm",
        "Water",
        "Wet",
        "Wild"],
}

last_name_suffix = {
    "human": [
        "son",
        "er",
        "",
        "itt",
        "edge",
        "wood",
        "stone",
        "iron",
        "copper",
        "brook",
        "brookes"
        "fier",
        "es",
        "teller",
        "ite",
        "ster",
        "black",
        "blake",
        "ame",
        "oak",
        "marsh",
        "ett",
        "kite",
        "frost",
        "walker"],
    # halfelf last name 2 list
    "half elf": [
        "ner",
        "ry",
        "spinner",
        "weaver",
        "aster"],
    # half orcs dont usually have last names
    "half orc": [
        "ecck",
        "eyyr",
        "erryn",
        "ook",
        "uek"],
    "elf": [
        "patience",
        "hawk",
        "dawn",
        "treader",
        "shining",
        "tracker",
        "stride",
        "tracer",
        "step",
        "prancer",
        "gait",
        "walker",
        "soul",
        "tread",
        "scape",
        "walker",
        "sword",
        "foot"],
    "dwarf": [
        "breaker",
        "slasher",
        "smith",
        "slab",
        "fist",
        "seeker",
        "cutter",
        "carver",
        "dweller",
        "hunter",
        "hammer",
        "smasher",
        "tracker",
        "crusher",
        "killer",
        "builder",
        "chopper",
        "chop",
        "beard",
        "warrior",
        "pick",
        "smiter",
        "blade",
        "clubber"],
    "gnome": [
        "toes",
        "short",
        "cloak",
        "sharp",
        "farmer",
        "shield",
        "skipper",
        "foot",
        "feet",
        "tall",
        "tankard",
        "crippler",
        "stinger",
        "foe",
        "laugher",
        "smiler",
        "grin",
        "knight",
        "stone",
        "forger",
        "touch",
        "beard",
        "eyes",
        "weaver",
        "ranger",
        "chuckle",
        "trapper",
        "belly",
        "heart",
        "lock",
        "ears",
        "dweller",
        "all",
        "rock",
        "pebble",
        "sand",
        "path"],
    "halfling": [
        # (adult to geriatric)
        "ale",
        "arrow",
        "body",
        "bones",
        "bottom",
        "bread",
        "brother",
        "burrow",
        "caller",
        "cloak",
        "digger",
        "drum",
        "eye",
        "fellow",
        "fingers",
        "flower",
        "foot",
        "fox",
        "ghost",
        "goat",
        "gold",
        "grass",
        "hand",
        "head",
        "heart",
        "hearth",
        "hill",
        "lady",
        "leaf",
        "letters",
        "maker",
        "man",
        "map",
        "mind",
        "one",
        "pipe",
        "shadow",
        "shaker",
        "sister",
        "skin",
        "sleep",
        "stick",
        "stoat",
        "swan",
        "talker",
        "taunt",
        "tender",
        "wanderer",
        "weed",
        "will",
        "wind",
        "wit",
        "wolf",
    ]
}

# note for job list:
# if in range very young, no job
# elif in range young, add "apprentice"
# elif in range young adult, add "journeyman"??? maybe
# elif in range 50-65(older middle aged?) add "master"
# elif in range "senior", add "retired master"
job_list = [
    # weapon or utility related jobs
    "armorer",
    "potion master",
    "shopkeeper",
    "shop clerk",
    "sword smith",
    "black smith",
    "toy maker",
    "stone cutter",
    "mason",
    "fletcher",
    "bow maker",
    "alchemist",
    "tanner",
    # travellers and people you might meet on the road
    "travelling merchant",
    "fortune teller",
    "gypsy",
    "bard",
    # town related jobs
    "librarian",
    "silver smith",
    "gold smith",
    "jeweller",
    "miner",
    "woodcutter",
    "town guard",
    "militia captain",
    "bartender",
    "innkeeper",
    "slave",
    "slave dealer",
    "tailor",
    "cobbler",
    "prostitute",
    "artist",
    "brewer",
    "winemaker",
    "butcher",
    "baker",
    "actor",
    "shipwright",
    "dock worker",
    "weaver",
    # country related jobs
    "farmer",
    "shepherd",
    "stable master",
    "stable boy",
    "farm hand",
    # aristocracy related jobs
    "beaurocrat",
    "secretary",
    "servant",
    "cook",
    "gardener",
    # church related jobs
    "abbot",
    "priest",
    "cleric",
    "monk",
]

names_by_gender = {
    "male": male_names_by_race,
    "female": female_names_by_race,
}

genders = ["male", "female"]


# Now generate this phrase:
# (male_name or female_name) is a (age) (female or male) (build) (race) with
# (hair_len) (hair_desc) (hair_color) hair and (eye_desc) (eye_color) eyes.

def npc_name_generator():
    ##determines two starting fields randomly
    race = random.choice(race_list)
    race = race.lower()
    gender = random.choice(genders)

    # Gets a suitable name based off their gender
    appropriate_name_list = names_by_gender[gender]
    # gets a name based off their their gender and race
    name = random.choice(appropriate_name_list[race])

    lastnameprefix = random.choice(last_name_prefix[race])
    lastnamesuffix = random.choice(last_name_suffix[race])

    # age = random.choice(ages)
    age = "adult"

    hair_color = random.choice(hair_color_by_race[race])
    hair_length = random.choice(hair_len)
    hair_description = random.choice(hair_descriptions)

    size = random.choice(build_by_race[race])

    eye_description = random.choice(eye_desc)
    eye_color = random.choice(eye_colors)
    string = ('%s %s%s is a %s %s %s %s with %s %s %s hair and %s %s eyes.' % (
        name,
        lastnameprefix,
        lastnamesuffix,
        size,
        gender,
        age,
        race,
        hair_length,
        hair_description,
        hair_color,
        eye_description,
        eye_color))
    print(string)


def save(filename, data):
    filename = filename
    f = open(filename, mode='w+')
    f.write(data)
    f.close()


def save_all_race_names_to_text():
    data = ""
    for race in race_list:
        race = race.lower()
        for gender in genders:
            # Get all the correct names for their gender
            appropriate_name_list = names_by_gender[gender]
            # Gets name list e.g. get all female night elf names
            name_list = appropriate_name_list[race]
            filename = "npc_names/%s_%s_names.txt" % (gender, race)
            for name in name_list:
                data = data + name + "\n"
            save(filename, data)
            data = ""


def save_all_lastnames_to_text():
    _data = ""
    for race in race_list:
        race = race.lower()
        last_name_prefixes = last_name_prefix[race]
        for prefix in last_name_prefixes:
            _data = _data + prefix + "\n"
        filename = "npc_names/%s_prefixes.txt" % (race)
        save(filename, _data)
        _data = ""

        last_name_suffixes = last_name_suffix[race]
        for suffix in last_name_suffixes:
            _data = _data + suffix + "\n"
        filename = "npc_names/%s_suffixes.txt" % (race)
        save(filename, _data)
        _data = ""


def save_all_hair_info_to_text():
    _data = ""
    for race in race_list:
        race = race.lower()
        hair_colours = hair_color_by_race[race]
        for hair_colour in hair_colours:
            _data = _data + hair_colour + "\n"
        filename = "npc_names/%s_hair_colours.txt" % (race)
        save(filename, _data)
        _data = ""

    for hair_length in hair_len:
        _data = _data + hair_length + "\n"
        filename = "npc_names/hair_lengths.txt"
        save(filename, _data)
        _data = ""

    for description in hair_descriptions:
        _data = _data + description + "\n"
        filename = "npc_names/hair_descriptions.txt"
        save(filename, _data)
        _data = ""


def save_all_size_info_to_text():
    _data = ""
    for race in race_list:
        race = race.lower()
        race_builds = build_by_race[race]
        for build in race_builds:
            _data = _data + build + "\n"
        filename = "npc_names/%s_race_builds.txt" % (race)
        save(filename, _data)
        _data = ""


def save_all_eye_descriptions():
    _data = ""
    for eye_description in eye_desc:
        _data = _data + eye_description + "\n"
    filename = "npc_names/eye_descriptions.txt"
    save(filename, _data)
    _data = ""


def save_all_eye_colours():
    _data = ""
    for eye_colour in eye_colors:
        _data = _data + eye_colour + "\n"
    filename = "npc_names/eye_colours.txt"
    save(filename, _data)
    _data = ""


def save_all_age_ranges():
    _data = ""
    for race in race_list:
        race = race.lower()
        for age_range in age_ranges[race]:
            lower_range, upper_range = age_ranges[race][age_range]
            _str = "%s %s = %i - %i\n" % (race, age_range, lower_range, upper_range)
            _data = _data + _str
        filename = "npc_names/%s_age_ranges.txt" % (race)
        save(filename, _data)
        _data = ""


def test_1():
    npc_name_generator()


def test_2():
    save_all_race_names_to_text()


def test_3():
    save_all_lastnames_to_text()


def test_4():
    save_all_hair_info_to_text()


def test_5():
    save_all_size_info_to_text()


def test_6():
    save_all_eye_descriptions()


def test_7():
    save_all_eye_colours()


def test_8():
    save_all_age_ranges()


if __name__ == "__main__":
    test_8()
