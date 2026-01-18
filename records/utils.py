import json, os, xml.etree.ElementTree as ET

def save_to_json(data, path): # <-- Добавлен аргумент path
    arr=[]
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            arr=json.load(f)
    arr.append(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)

def save_to_xml(data, path): # <-- Добавлен аргумент path
    if os.path.exists(path):
        tree=ET.parse(path)
        root=tree.getroot()
    else:
        root=ET.Element('records')
        tree=ET.ElementTree(root)
    
    r=ET.SubElement(root,'record')
    for k,v in data.items():
        e=ET.SubElement(r,k)
        e.text=v
    tree.write(path, encoding='utf-8', xml_declaration=True)