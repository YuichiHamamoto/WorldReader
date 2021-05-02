def num2words(num):
	under_20 = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
	tens = ['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
	above_100 = {100: 'hundred',1000:'thousand', 1000000:'million', 1000000000:'billion'}
 
	if num < 20:
		 return under_20[num]
	
	if num < 100:
		return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
 
	# find the appropriate pivot - 'million' in 3,603,550, or 'thousand' in 603,550
	pivot = max([key for key in above_100.keys() if key <= num])
 
	return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))

def obj_count_natural(name, count):
    if count == 1:
        return 'one "{}"'.format(name)
    else:
        return '{} "{}s"'.format(num2words(count), name)

# there are xxx, yyy, and zzz
def make_object_sentence(obj_freq):
    if len(obj_freq) == 0:
        return ""

    obj_freq = [(k, v) for k, v in obj_freq.items()]

    totalNum = 0
    for obj in obj_freq:
        totalNum += obj[1]

    if totalNum == 1:
        return 'There is one {}.'.format(obj_freq[0][0])

    if len(obj_freq) == 1: 
        return 'There are {}.'.format(obj_count_natural(obj_freq[0][0], obj_freq[0][1]))

    obj_freq = sorted(obj_freq, key=lambda x: x[1], reverse=True)

    if len(obj_freq) == 2:
        return 'There are {} and {}.'.format(obj_count_natural(obj_freq[0][0], obj_freq[0][1]), obj_count_natural(obj_freq[1][0], obj_freq[1][1]))

    sentence = "There are "
    for obj in obj_freq[:-1]:
        sentence += '{}, '.format(obj_count_natural(obj[0], obj[1])) 
    obj = obj_freq[-1]
    sentence += 'and {}.'.format(obj_count_natural(obj[0], obj[1]))

    return sentence

# aaa have ccc
def make_logo_sentence(words):
    if len(words) == 0:
        return ""
    if len(words) == 1:
        return 'One of the objects has a logo of "{}".'.format(words[0])
    if len(words) == 2:
        return 'Some of the objects have logos of "{}" and "{}".'.format(words[0], words[1])
    
    sentence = 'Some of the objects have logos of '
    for word in words[:-1]:
        sentence += '"{}", '.format(word)
    word = words[-1]
    sentence += 'and "{}".'.format(word)

    return sentence

# aaa have ccc
def make_situation_sentence(words):
    if len(words) == 0:
        return ""
    if len(words) == 1:
        return 'The situation can be described by "{}".'.format(words[0])
    if len(words) == 2:
        return 'The situation can be described by "{}" and "{}".'.format(words[0], words[1])

    sentence = "The situation can be described by "
    for word in words[:-1]:
        sentence += '"{}", '.format(word)
    word = words[-1]
    sentence += 'and "{}".'.format(word)

    return sentence

def make_sentense_from_raw(data):
    import visionres_parser
    data = visionres_parser.parse(data)
    return "{}  {}  {}".format(
        make_situation_sentence(data['situation']), 
        make_object_sentence(data['objects']), 
        make_logo_sentence(data['logos'])
    )

if __name__ == '__main__':
    print(make_situation_sentence(["glass", "hand", "water"]))
    print(make_logo_sentence(["dr pepper", "something", "yes"]))
    print(make_object_sentence({
        "bottle": 5,
        "phone": 6,
        "pen": 1
    }))
    # print(make_situation_sentence(["shit", "poop", "sports"]))