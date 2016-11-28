stepsize = 0.2

path$ = "/Users/tim/Documents/sound_files/MMAT/manipulation_files/"
dest_path$ = "/Users/tim/Documents/sound_files/MMAT/output/"

Create Strings as file list: "filelist", path$

n = Get number of strings

for i from 1 to n
	select Strings filelist
	filepath$ = Get string: i
	filepath$ = path$ + filepath$
	Read from file: filepath$
	manipulation_name$ = selected$("Manipulation")
	selectObject: "Manipulation " + manipulation_name$
	Extract pitch tier

	for j from -2 to 4
		selectObject: "PitchTier " + manipulation_name$
		diff = j + 2
		diff$ = string$ (diff)
		new_name$ = manipulation_name$ - right$(manipulation_name$,1) + "_" + diff$
		Copy: new_name$
		erb_step = j * stepsize + 0.00000001
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
		selectObject: "Manipulation " + manipulation_name$
		plusObject: "PitchTier " + new_name$
		Replace pitch tier
		selectObject: "Manipulation " + manipulation_name$
		Get resynthesis (overlap-add)
		Rename: new_name$
		Save as WAV file: dest_path$ + new_name$ + ".wav"
	endfor
endfor
