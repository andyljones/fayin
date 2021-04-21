import requests
import xml.etree.ElementTree as ET
from io import BytesIO
from zipfile import ZipFile

URL = 'https://mnemosyne-proj.org/sites/default/files/cards/chinese_sentences.cards'

def xml_tree():
    resp = requests.get(URL)

    with ZipFile(BytesIO(resp.content)) as zf:
        cards = zf.read('cards.xml')

    return ET.parse(BytesIO(cards))
    
def raw_cards(tree):
    tags, facts = {}, {}
    cards = []
    for log in tree.getroot():
        t = log.get('type')
        if t == '10':
            tags[log.get('o_id')] = log.find('name').text
        elif t == '16':
            facts[log.get('o_id')] = (log.find('b').text, log.find('f').text)
        elif t == '6':
            tag_ids = log.get('tags').split(',')
            fact_id = log.get('fact')
            cards.append({'fact': facts[fact_id], 'tags': [tags[tid] for tid in tag_ids]})
        else:
            raise ValueError('Can\'t handle this log')
    
    return cards

if __name__ == '__main__':
    tree = xml_tree()
    raw = raw_cards(tree)

    subset = []
    for r in raw:
        if 'zh-en' in r['tags']:
            [desc] = [t for t in r['tags'] if t != 'zh-en'] 
            subset.append((r['fact'][1], desc))