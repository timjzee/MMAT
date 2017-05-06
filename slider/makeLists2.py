import random

ranges = [3.2, 3.8, 4.8, 6.8, 12.8]
num_PP = 20


def getWords():
    f = open("../wordlist_final.txt", "r")
    wrds = [i[:-1] for i in f]
    f.close()
    return wrds


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
    f = open("./lists2/" + list_name, "w")
    f.write("stimulus,erb_max\n")
    for pair in ls:
        f.write("{},{}\n".format(pair[0], pair[1]))
    f.close()
    print(list_name + ":", "shift", shift, "iteration", iteration, "status", status)


def makeLists():
    for start_index in range(5):
        r = ranges[start_index:5] + ranges[0:start_index]
        for i in range((num_PP // 5) // 2):
            ls = []
            current_index = 0
            for word in words:
                erb_range = r[current_index]
                ls.append([word, erb_range])
                if current_index >= 4:
                    current_index = 0
                else:
                    current_index += 1
            random.shuffle(ls)
            ls_mirror = list(reversed(ls))
            writeFile(ls, start_index + 1, i + 1, "orig")
            writeFile(ls_mirror, start_index + 1, i + 1, "mirr")


words = getWords()
makeLists()
