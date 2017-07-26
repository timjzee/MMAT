erb_steps [1] = -0.4
erb_steps [2] = 0.8
erb_steps [3] = 1.82

path$ = "/Users/tim/Documents/sound_files/MMAT/manipulation_files/"
dest_path$ = "/Users/tim/GitHub/MMAT/"

writeFileLine: dest_path$ + "stimuli_pitch.csv", "item,category,hz"

Create Strings as file list: "filelist", path$

n = Get number of strings

for i from 1 to n
	select Strings filelist
	filepath$ = Get string: i
	filepath$ = path$ + filepath$
	Read from file: filepath$
	manipulation_name$ = selected$("Manipulation")
	item_name$ = manipulation_name$ - right$(manipulation_name$,1)
	selectObject: "Manipulation " + manipulation_name$
	Extract pitch tier
	for j from 1 to 3
		erb_step = erb_steps [j]
		category$ = string$ (j)
		selectObject: "PitchTier " + manipulation_name$
		new_name$ = item_name$ + "_" + category$
		Copy: new_name$
		num_points = Get number of points
		for k from 1 to num_points
			time_point = Get time from index: k
			point_start = time_point - 0.001
			point_end = time_point + 0.001
			hz_old = Get value at index: k
			erb_old = 16.7 * log10(1 + hz_old / 165.4)
			erb_new = erb_old + erb_step
			hz_new = 165.4 * (10^(0.06*erb_new) - 1)
			hz_step = hz_new - hz_old
			Shift frequencies: point_start, point_end, hz_step, "Hertz"
		endfor
		mean_erb = Get mean (points): 0, 0
		appendFileLine: dest_path$ + "stimuli_pitch.csv", item_name$ + "," + category$ + ",", mean_erb
	endfor
endfor
