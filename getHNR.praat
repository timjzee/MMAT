# Script that collects Harmonics-to-Noise Ratio (HNR) of the 6 middle harmonic periods in pitch resynthesized words.
# This script should be used on words to which a second resynthesis has been applied that brings them back to their original mean pitch.
# Only then can the HNR of these files be fairly compared to each other and to the original file.

# Paths to directories on computer

input_path$ = "/Users/tim/Documents/sound_files/MMAT/output/"
output_path$ = "/Users/tim/Documents/sound_files/MMAT/"
writeFileLine: output_path$ + "hnr_values.csv", "name,manipulation,HNR"

# Create list of file names and loop through those file names

list_of_files = Create Strings as file list: "list", input_path$
number_of_files = Get number of strings

for i to number_of_files
    selectObject: list_of_files
    filename$ = Get string: i
    Read from file: input_path$ + "/" + filename$
    object_name$ = selected$("Sound")
    split_index = index (object_name$, "_")
    manipulation$ = right$ (object_name$, length (object_name$) - split_index)
    To PointProcess (periodic, cc): 75, 300
    analysis_points = 6
    number_of_points = Get number of points
    discarded_points = number_of_points - analysis_points
    first_point = abs (discarded_points / 2)
    last_point = first_point + analysis_points
    harmonicity_start = Get time from index: first_point
    harmonicity_end = Get time from index: last_point
    selectObject: "Sound " + object_name$
    # To Harmonicity (cc): 0.01, 75, 0.1, 1
    To Harmonicity (ac): 0.01, 75, 0.1, 4.5
    hnr = Get mean: harmonicity_start, harmonicity_end
    appendFileLine: output_path$ + "hnr_values.csv", object_name$ + "," + manipulation$ + ",", hnr
endfor
