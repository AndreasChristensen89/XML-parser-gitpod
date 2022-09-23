import xml.etree.ElementTree as xml

def handle_uploaded_publication_file(f):
    mytree = xml.parse(f)
    myroot = mytree.getroot()

    dict = {}
    key = 1
    keys = []
    values = []
    for x in myroot[0]:
        if len(x) == 0:
            if x.text != None and x.text != "":
                array = ['publication', x.tag[32:], x.text]
                values.append(array)
                keys.append(key)
                key += 1
        else:
            for i in x:
                if len(i) == 0:
                    if i.text != None and i.text != "":
                        array_sub = [x.tag[32:], i.tag[32:], i.text]
                        values.append(array_sub)
                        keys.append(key)
                        key += 1
                else:
                    for j in i:
                        if len(j) == 0:
                            if j.text != None and j.text != "":
                                array_next_sub = [i.tag[32:], j.tag[32:], j.text]
                                values.append(array_next_sub)
                                keys.append(key)
                                key += 1
    
    for i in range(len(keys)):
        dict[keys[i]] = values[i]

    return dict


def handle_uploaded_experiment_file(f):
    mytree = xml.parse(f)
    myroot = mytree.getroot()

    dict = {}
    key = 1
    keys = []
    values = []
    
    for x in myroot[0]:
        if len(x) == 0:
            if x.text != None and x.text != "":
                dict_array = ['experiment', x.tag[32:], x.text]
                values.append(dict_array)
                keys.append(key)
                key += 1
        else:
            for i in x:
                if len(i) == 0:
                    if i.text != None and i.text != "":
                        dict_array = [x.tag[32:], i.tag[32:], i.text]
                        values.append(dict_array)
                        keys.append(key)
                        key += 1
                else:
                    for j in i:
                        if len(j) == 0:
                            if j.text != None and j.text != "":
                                dict_array = [i.tag[32:], j.tag[32:], j.text]
                                values.append(dict_array)
                                keys.append(key)
                                key += 1
                        else:
                            for k in j:
                                if len(k) == 0:
                                    if k.text != None and k.text != "":
                                        dict_array = [j.tag[32:], k.tag[32:], k.text]
                                        values.append(dict_array)
                                        keys.append(key)
                                        key += 1
                                else:
                                    for l in k:
                                        if len(l) == 0:
                                            if l.text != None and l.text != "":
                                                dict_array = [k.tag[32:], l.tag[32:], l.text]
                                                values.append(dict_array)
                                                keys.append(key)
                                                key += 1
                                        else:
                                            for m in l:
                                                if len(m) == 0:
                                                    if m.text != None and m.text != "":
                                                        dict_array = [l.tag[32:], m.tag[32:], m.text]
                                                        values.append(dict_array)
                                                        keys.append(key)
                                                        key += 1
                                                else:
                                                    for n in m:
                                                        if len(n) == 0:
                                                            if n.text != None and n.text != "":
                                                                array_next_sub = [m.tag[32:], n.tag[32:], n.text]
                                                                values.append(array_next_sub)
                                                                keys.append(key)
                                                                key += 1

    
    for i in range(len(keys)):
        dict[keys[i]] = values[i]

    return dict


def handle_uploaded_file(f):
    mytree = xml.parse(f)
    myroot = mytree.getroot()

    dict = {}
    key = 1
    keys = []
    values = []
    double_check = []
    for element in myroot.iter():
        if element.text != None and not "  " in element.text:
            
            # certain fields are names the same way, therefore we need to find the parent to compare
            for child in myroot.iter():
                if child.findall(element.tag):
                    if [child.tag[32:], element.tag] not in double_check:
                        double_check.append([child.tag[32:], element.tag])
                        parent = child.tag[32:]
                        break
                    else:
                        continue
            array = [parent, element.tag[32:], element.text]
            values.append(array)
            keys.append(key)
            key += 1

    for i in range(len(keys)):
        dict[keys[i]] = values[i]

    return dict


def handle_bibtex(f):   
    fields = ["title", "journal", "volume", "pages", "year", "doi", "abstract"]
    
    bibtex_content = {}
    key = 1
    keys = []
    values = []

    for x in f:
        if not str(x).find("=") == -1:
            name = str(x)[2:str(x).find("=") - 1]
            content = str(x)[str(x).find("{")+1:str(x).find("}")]
            if name == "author":
                content = content.replace(" and ", ",").split(",")
                first_names = ""
                last_names = ""
                for name in content:
                    first_names += name[0:2]+","
                    last_names += name[3:]+","
                values.append(["author", "first_name", first_names[0:-1]])
                values.append(["author", "last_name", last_names[0:-1]])
                keys.append(key)
                key += 1
                keys.append(key)
                key += 1
            elif name == "keywords":
                content = content.replace(", ", ",")
                values.append([name, 'keyword', content])
                keys.append(key)
                key += 1
            elif name in fields:
                if name == "pages":
                    values.append(["publication", 'first_page', content])
                else:
                    values.append(["publication", name, content])
                keys.append(key)
                key += 1
    
    for i in range(len(keys)):
        bibtex_content[keys[i]] = values[i]

    return bibtex_content
            
