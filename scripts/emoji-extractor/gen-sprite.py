#!/usr/bin/env python2

import os
from PIL import Image
import argparse
import xml.etree.ElementTree as ElementTree

parser = argparse.ArgumentParser(prog='gen-sprite', description="""Generate sprites from extracted emojis.""")
parser.add_argument('-e', '--emojis', help='folder where emojis are stored', default='output/', required=False)
parser.add_argument('-i', '--xml', help='XML containing emojis map', default='emoji-categories.xml', required=False)
parser.add_argument('-s', '--size', help='Maximum number of emojis per line', default='15', required=False)
args = parser.parse_args()

xml = ElementTree.parse(args.xml).getroot()

for group in xml:
    groupName = group.attrib['name']
    emojis = []
    for item in group:
        emoji = item.text.replace(',', '_u').lower()
        if '|' not in emoji and os.path.isfile(args.emojis + 'emoji_u' + emoji + '.png'):
            emojis.append(args.emojis + 'emoji_u' + emoji + '.png')
    images = [Image.open(filename) for filename in emojis]

    if len(images) > 0:
        print "Generating sprite for " + groupName
        masterWidth  = (128 * int(args.size))
        lines = float(len(images)) / float(args.size)
        if not lines.is_integer():
            lines += 1
            lines = int(lines)
        masterHeight = int(128 * lines)
        master = Image.new(
            mode='RGBA',
            size=(masterWidth, masterHeight),
            color=(0,0,0,0)
        )

        offset = -1
        for count, image in enumerate(images):
            location = 128 * count % masterWidth
            if location == 0:
                offset += 1
                location = 0
            master.paste(image, (location, 128 * offset))
        master.save(groupName + '.png', 'PNG')
    else:
        print 'Ignoring ' + groupName + '...'
