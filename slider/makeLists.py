import random

bins = [[0.8, 1.28], [1.28, 1.76], [1.76, 2.24], [2.24, 2.72], [2.72, 3.2]]
num_PP = 20


def getWords():
    f = open("../wordlist_final.txt", "r")
    wrds = [i[:-1] for i in f]
    f.close()
    return wrds


def getMirror(base, values):
    """Make a mirror list from the supplied list and values."""
    mirror = []
    for i in base:
        pair = [j for j in values if j[0] == i[0]][0]
        mirror.insert(0, pair)
    return mirror


def writeFile(ls, shift, iteration, status):
    if iteration == 1:
        list_num = 0
    elif iteration == 2:
        list_num = 10
    list_num += (shift - 1) * 2
    if status == "orig":
        list_num += 1
    elif status == "mirr":
        list_num += 2
    if list_num < 10:
        list_name = "list0" + str(list_num) + ".csv"
    else:
        list_name = "list" + str(list_num) + ".csv"
    f = open("./lists/" + list_name, "w")
    f.write("stimulus,starting_erb\n")
    for pair in ls:
        f.write("{},{}\n".format(pair[0], pair[1]))
    f.close()
    print(list_name + ":", "shift", shift, "iteration", iteration, "status", status)


def makeLists():
    for start_index in range(5):
        b = bins[start_index:5] + bins[0:start_index]
        for i in range((num_PP // 5) // 2):
            ls = []
            ls_mirror_values = []
            current_index = 0
            for word in words:
                erb = random.uniform(b[current_index][0], b[current_index][1])
                ls.append([word, erb])
                erb = random.uniform(b[current_index][0], b[current_index][1])
                ls_mirror_values.append([word, erb])
                if current_index >= 4:
                    current_index = 0
                else:
                    current_index += 1
            random.shuffle(ls)
            ls_mirror = getMirror(ls, ls_mirror_values)
            writeFile(ls, start_index + 1, i + 1, "orig")
            writeFile(ls_mirror, start_index + 1, i + 1, "mirr")


words = getWords()
makeLists()
