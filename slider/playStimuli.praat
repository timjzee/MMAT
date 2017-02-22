path$ = "."

# Parameters to script

form Get parameters
    word stimulus_to_play aap
    word version_to_play a_and_b
    real shift_of_c 100
endform

# Procedures

procedure shiftStimulus: .stimulus$, .step
    # applies the PSOLA resynthesis
    selectObject: "Manipulation " + .stimulus$
    .new_name$ = .stimulus$ + "_shifted"
    Copy: .new_name$
    Extract pitch tier
    .fin_step = .step + 0.00000001
    .num_points = Get number of points
    for k from 1 to .num_points
        .time_point = Get time from index: k
        .point_start = .time_point - 0.001
        .point_end = .time_point + 0.001
        .hz_old = Get value at index: k
        .erb_old = 16.7 * log10(1 + .hz_old / 165.4)
        .erb_new = .erb_old + .fin_step
        .hz_new = 165.4 * (10^(0.06 * .erb_new) - 1)
        .hz_step = .hz_new - .hz_old
        Shift frequencies: .point_start, .point_end, .hz_step, "Hertz"
    endfor
    selectObject: "Manipulation " + .new_name$
    plusObject: "PitchTier " + .new_name$
    Replace pitch tier
    selectObject: "Manipulation " + .new_name$
    Get resynthesis (overlap-add)
    selectObject: "Manipulation " + .new_name$
    plusObject: "PitchTier " + .new_name$
    Remove
endproc

# Frame

Read from file: path$ + "/test_stimuli/" + stimulus_to_play$ + ".Manipulation"

if version_to_play$ = "a_and_b"
    shift_of_a = -0.4
    shift_of_b = 0.8
    @shiftStimulus: stimulus_to_play$, shift_of_a
    selectObject: "Sound " + shiftStimulus.new_name$
    Rename: stimulus_to_play$ + "_A"
    @shiftStimulus: stimulus_to_play$, shift_of_b
    selectObject: "Sound " + shiftStimulus.new_name$
    Rename: stimulus_to_play$ + "_B"
    Create Sound from formula: "silence", 1, 0, 0.5, 44100, "0"
    selectObject: "Sound " + stimulus_to_play$ + "_A"
    Play
    selectObject: "Sound " + "silence"
    Play
    selectObject: "Sound " + stimulus_to_play$ + "_B"
    Play
elsif version_to_play$ = "b_and_c"
    shift_of_b = 0.8
    @shiftStimulus: stimulus_to_play$, shift_of_b
    selectObject: "Sound " + shiftStimulus.new_name$
    Rename: stimulus_to_play$ + "_B"
    @shiftStimulus: stimulus_to_play$, shift_of_c
    selectObject: "Sound " + shiftStimulus.new_name$
    Rename: stimulus_to_play$ + "_C"
    Create Sound from formula: "silence", 1, 0, 0.5, 44100, "0"
    selectObject: "Sound " + stimulus_to_play$ + "_B"
    Play
    selectObject: "Sound " + "silence"
    Play
    selectObject: "Sound " + stimulus_to_play$ + "_C"
    Play
elsif version_to_play$ = "c"
    @shiftStimulus: stimulus_to_play$, shift_of_c
    selectObject: "Sound " + shiftStimulus.new_name$
    Play
endif
