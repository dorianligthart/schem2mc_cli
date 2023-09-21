import os
import sys

# https://github.com/twoolie/NBT/blob/master/nbt/nbt.py
from nbt import nbt

def sort_palette(palette : list) -> list:
    newpalette = []
    palette_len = len(palette)
    for index in range(palette_len):
        for m in range(palette_len):
            value = int(palette[m].valuestr())
            if value >= palette_len or value < 0:
                return exit(33)
            if value is index:
                newpalette.append(palette[m].namestr())
    return (newpalette)

def convert_schem(path : str, air : bool, mode : str) -> str:
    if not os.path.exists(path):
        print("provide valid path.")
        exit(3)
    nbt_file = nbt.NBTFile(path, 'rb').parse_file()
    if not nbt_file:
        exit(21)
    palette = sort_palette(nbt_file["Palette"])
    for _ in nbt_file["BlockData"]:
        if _ > len(palette) or _ < 0:       
            exit(123)
    length = int(nbt_file["Length"].valuestr())
    width = int(nbt_file["Width"].valuestr())
    height = int(nbt_file["Height"].valuestr())
    offsetX = int(nbt_file["Metadata"]["WEOffsetX"].valuestr())
    offsetY = int(nbt_file["Metadata"]["WEOffsetY"].valuestr())
    offsetZ = int(nbt_file["Metadata"]["WEOffsetZ"].valuestr())
    if length * width * height is not len(nbt_file["BlockData"]):
        exit(420)
    k = 0
    for i in range(length * width * height):
        block = palette[nbt_file["BlockData"][i]]
        if air is True or block != "minecraft:air":
            z = int(i%length)
            x = int(i/length%width)
            y = int(i/length/width)
            blockentity = ""
            for k in range(len(nbt_file["BlockEntities"])):
                if (int(nbt_file["BlockEntities"][k]["Pos"][0]) == x and
                    int(nbt_file["BlockEntities"][k]["Pos"][1]) == y and
                    int(nbt_file["BlockEntities"][k]["Pos"][2]) == z):
                    # + parse(nbt_file["BlockEntities"][k])
                    blockentity = "{" + "}"
            print(f"setblock ~{x + offsetX} ~{y + offsetY} ~{z + offsetZ} {block}{blockentity}{mode}")
    return("hi")

### main:
if len(sys.argv) == 1 or sys.argv[1] == "--help":
    print("[Help Page]\n\'schem2mc_cli.py <filepath> --air= --obh=\'\noptional flags:\n\tair=[False | True], setblock airblocks or not.\n\tobh=[replace | keep | destroy], (OldBlockHandling), read minecraft setblock wiki.")
    exit(0)

#default value:
air = False
mode = " replace"
#   not so pretty flag check:
if len(sys.argv) == 3 or len(sys.argv) == 4: 
    if sys.argv[2] == "--air=True" or sys.argv[3] == "--air=True":
        air = True
    if sys.argv[2] == "--obh=keep" or sys.argv[3] == "--obh=keep":
        mode = " keep"
    elif sys.argv[2] == "--obh=destroy" or sys.argv[3] == "--obh=destroy":
        mode = " destroy"
convert_schem(sys.argv[1], air, mode)
