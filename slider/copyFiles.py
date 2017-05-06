import glob
import shutil


f = open("../wordlist_final.txt", "r")

words = [i[:-1] for i in f]
f.close()

source_path = "/Users/tim/Documents/sound_files/MMAT/manipulation_files/"
for word in words:
    source_file = glob.glob(source_path + word + "*")
    print(source_file)
    shutil.copyfile(source_file[0], "./stimuli/" + word + ".Manipulation")
