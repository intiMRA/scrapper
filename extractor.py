import re
nonKeyWords = ["natural",
               "hand cooked",
               "style",
               "food",
               "flavoured",
               "breakfast",
               "professional",
               "classic",
               "nz",
               "on",
               "the",
               "go",
               "original",
               "&",
               "and",
               "fruit",
               "block",
               "with",
               "a",
               "cup",
               "pack",
               "premium",
               "roasted",
               "feast",
               "smooth",
               "label",
               "flavor",
               "de",
               "luxe",
               "years",
               "ages",
               "kids",
               "bp",
               "nutty",
               "salty",
               "tidy",
               "easy",
               "savory",
               "stretchy",
               "fresh",
               "fruit",
               "hazy",
               "simple",
               "hit",
               "in",
               "processed",
               "pro",
               "silky",
               "subtle",
               "really",
               "good",
               "to",
               "ready",
               "eat",
               "rich",
               "mighty",
               "be",
               "new",
               "zealand",
               "real",
               "crimpy",
               "fired",
               "buttersoft",
               "works",
               "luxury",
               "ply",
               "gourmet",
               "quality",
               "twin",
               "pack",
               "portions",
               "honest",
               "squeezed",
               "rapid",
               "bliss",
               "rapid",
               "bliss",
               "crooked",
               "canterbury",
               "baked",
                "moro",
               "king",
               "supersoft",
               "variety",
               "mi",
               "goreng",
               "monte",
               "carlo",
               "our",
               "of",
               "lives",
               "fifth",
               "generation",
               "bits",
               "stovetop",
               "crispy",
               "crumbed",
               "amendment",
               "american",
               "b-ready",
               "cheeza-peno",
               "freddo",
               "sharepack",
               "share",
               "lowering",
               "cholesterol",
               "ultrathin",
               "mellow",
               "bubbly",
               "pakari",
               "glacier",
               "blast",
               "pressed",
               "seasoned",
               "trouble",
               "super",
               "lots",
               "three",
               "mineral",
               "franklin",
               "canadian",
               "wurly",
               "colombian",
               "smoooooth",
               "fierce",
               "backyard",
               "pukekohe",
               "vicars",
               "choice",
               "range",
               "zingy",
               "slightly",
               "lindor",
               "freshburst",
               "alternative",
               "horowhenua",
               "sante",
               "added",
               "large",
               "beauty",
               "harvest",
               "duo",
               "cheerios",
               "bouquet",
               "sexy",
               "hawkes",
               "bay",
               "feel",
               "oxygenated",
               "napisan",
               "oxiaction",
               "deodorant",
               "kisses",
                "anti-perspirant",
               "caress",
               "cluster",
               "ripened"
               "vine",
               "fighter",
               "enamel",
               "munchy",
               "wide",
               "dispenser"
               "barossa",
               "waxed",
               "pinky",
               "everyday",
               "nights",
               "bemighty",
               "homestyle",
               "flexia",
               "softfolds",
               "beret",
               "durance",
               "x",
               "adder",
               "dreams",
               "plax",
               "merely",
               "musk",
               "bluey",
               "everything",
               "kalamata",
               "jumbo",
               "supreme",
               "hundreds",
               "thousands",
               "multipack",
               "fabulicious",
               "artisan",
               "imperial",
               "throaties",
               "savoury",
               "better",
               "naturally",
               "n",
               "fix",
               "uno",
               "squeezie",
               "smooth",
               "chunky",
               "for",
               "total"
               ]
maybes = [
    "naturally",
    "single",
    "n",
    "fix",
    "uno",
    "chunky",
    "for",
    "top",
    "plus",
    "total"
]
nw = open("newWorldData.csv", "r")
cd = open("countDownData.csv", "r")

def strip(word: str):
    # if len(re.findall(r'[0-9]+[aA-zZ]+', word)) > 0:
    #     return ""
    return word.replace("'", "").replace(",", "").replace(".", "").lower()

nwl = nw.readlines()
cdl = cd.readlines()



# counts = {}
# for line in nwl:
#     l = line.split(",")
#     words = l[0].split(" ")
#     for w in words:
#         w = strip(w)
#         if w in nonKeyWords or len(re.findall(r'[0-9]+', w)) > 0:
#             continue
#         if w not in counts.keys():
#             counts[w] = 0
#         counts[w] = counts[w] + 1
#
# for item in sorted(counts, key=lambda x: counts[x]):
#     if counts[item] > 2:
#         print(item, counts[item])


for m in maybes:
    print(m)
    for line in nwl:
        l = strip(line.split(",")[0]).lower().split(" ")
        if m in l:
            print(l)
    print("-"*100)

nw.close()
cd.close()