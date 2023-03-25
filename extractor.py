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
               "real"
               ]
# maybes = []
# nw = open("newWorldData.csv", "r")
# cd = open("countDownData.csv", "r")
#
# def strip(word: str):
#     # if len(re.findall(r'[0-9]+[aA-zZ]+', word)) > 0:
#     #     return ""
#     return word.replace("'", "").replace(",", "").replace(".", "").lower()
#
# nwl = nw.readlines()
# cdl = cd.readlines()
# # counts = {}
# # for line in nwl:
# #     l = line.split(",")
# #     words = l[0].split(" ")
# #     for w in words:
# #         w = strip(w)
# #         if w in nonKeyWords:
# #             continue
# #         if w not in counts.keys():
# #             counts[w] = 0
# #         counts[w] = counts[w] + 1
# #
# # for item in sorted(counts, key=lambda x: counts[x]):
# #     if counts[item] > 1:
# #         print(item, counts[item])
# for m in maybes:
#     m = " "+m
#     print(m)
#     for line in nwl:
#         l = strip(line.split(",")[0])
#         if m in l:
#             print(l)
#     print("-"*100)
#
# nw.close()
# cd.close()