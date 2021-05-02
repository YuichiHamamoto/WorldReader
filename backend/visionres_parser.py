import json
import operator

def parse(data):

    objects = dict()
    objects2 = list()
    situation = list()
    logos = list()

    labelData = data['labelAnnotations']
    if 'labelAnnotations' in data:
        targets = data['labelAnnotations']
        if len(targets) > 5:
            targets = targets[:5]

            for label in targets:
                situation.append(label['description'].lower())
        
        elif len(targets) > 0:
            
            for label in data['labelAnnotations']:
                situation.append(label['description'].lower())

    if 'logoAnnotations' in data:      
        for label in (data['logoAnnotations']):
            logos.append(label['description'].lower())

    for objData in data['localizedObjectAnnotations']:
        objName = objData['name'].lower()
        if objName in objects:
            objects[objName] += 1
        else:
            objects[objName] = 1

    # advanced object sentense
    # if 'localizedObjectAnnotations' in data:
    #     objects2 = data['localizedObjectAnnotations']
    #     parent_objects = [[] for i in range(len(objects2))]

    #     for i in range(len(objects2)):
    #         if objects2[i] is None:
    #             continue
    #         for j in range(len(objects2)):
    #             if objects2[j] is None:
    #                 continue

    #             i_leftDown = objects2[i]["boundingPoly"]["normalizedVertices"][0]
    #             j_leftDown = objects2[j]["boundingPoly"]["normalizedVertices"][0]
    #             i_rightUp = objects2[i]["boundingPoly"]["normalizedVertices"][2]
    #             j_rightUp = objects2[j]["boundingPoly"]["normalizedVertices"][2]

    #             # check if convex is inside
    #             if i_leftDown['x'] < j_leftDown['x'] and i_leftDown['y'] < j_leftDown['y'] and i_rightUp['x'] > j_rightUp['x'] and i_rightUp['y'] > j_rightUp['y']:
                    
    #                 parent_objects[i].append(objects2[j]['name'].lower())
    #                 objects2[j] = None

    # print(objects2)
    # print(parent_objects)

    # objects
    # for i in range(len(objects2)):
        


    keys = list()

    for label in (situation):
        y = label.split()
        for x in (y):
            keys.append(x)

    
    # Small optimization

    keySituation = dict()
    fiveKeys = list()

    for x in keys:
        if x in keySituation:
            keySituation[x] += 1
        else:
            keySituation[x] = 1
    sorted_keySituation = sorted(keySituation.items(), key=operator.itemgetter(1),reverse = True)

    if len(sorted_keySituation) >= 5:
        for x in sorted_keySituation[:5]:
            fiveKeys.append(x)

    situation2 = list()
    fiveKeySolution = list()
    for a in fiveKeys:
        situation2.append(a[0])

    for s in situation2:
        for t in situation:
            if s.lower() in t.lower():
                fiveKeySolution.append(t)
                for u in situation:
                    if s.lower() in u.lower():
                        subsub = u.split()
                        for v in subsub:
                            for w in situation:
                                if v.lower() in w.lower():
                                    if w in situation:
                                        situation.remove(w)
    return {
        'objects': objects,
        'situation': fiveKeySolution,
        'logos': logos
    }

if __name__ == "__main__":
    with open('testtrump_visionres.json') as f:
        data = json.load(f)
    data = parse(data)

    # from sentense_maker import *

    # print("{}  {}  {}".format(
    #     make_situation_sentence(data['situation']), 
    #     make_object_sentence(data['objects']), 
    #     make_logo_sentence(data['logos'])
    # ))