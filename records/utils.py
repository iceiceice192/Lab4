
import json, os, xml.etree.ElementTree as ET
def save_to_json(data, path='data.json'):
    arr=[]
    if os.path.exists(path):
        arr=json.load(open(path,'r',encoding='utf-8'))
    arr.append(data)
    json.dump(arr,open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
def save_to_xml(data, path='data.xml'):
    if os.path.exists(path):
        tree=ET.parse(path); root=tree.getroot()
    else:
        root=ET.Element('records'); tree=ET.ElementTree(root)
    r=ET.SubElement(root,'record')
    for k,v in data.items():
        e=ET.SubElement(r,k); e.text=v
    tree.write(path,encoding='utf-8',xml_declaration=True)
