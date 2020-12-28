#!/usr/bin/env python3

import sys

compendium = {}
opencc_json_template = """
{
  "name": "XXX IVD collection",
  "segmentation": {
    "type": "mmseg",
    "dict": {
      "type": "text",
      "file": "XXX.txt"
    }
  },
  "conversion_chain": [{
    "dict": {
      "type": "text",
      "file": "XXX.txt"
    }
  }]
}
""".strip()

with open(sys.argv[1], 'r') as file:
	for line in file:
		if line == '#EOF':
			break

		if line.startswith('#'):
			continue

		ch_seq, collection_name, id = line.split('; ')
		ch_seq = [chr(int(ch, 16)) for ch in ch_seq.split(' ')]

		if not collection_name in compendium:
			compendium[collection_name] = {}

		if not ch_seq[0] in compendium[collection_name]:
			compendium[collection_name][ch_seq[0]] = []

		compendium[collection_name][ch_seq[0]].append(''.join(ch_seq))

for collection_name in compendium:
	with open(collection_name + '.json', 'w') as file:
		file.write(opencc_json_template.replace('XXX', collection_name))

	with open(collection_name + '.txt', 'w') as file:
		for ch_seiji in compendium[collection_name]:
			file.write(ch_seiji + '\t' + ' '.join([ch_seiji] + compendium[collection_name][ch_seiji]) + '\n')