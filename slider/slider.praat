# variables

path$ = "/Users/tim/GitHub/MMAT/slider/"
screen_width = 100
screen_height = 100
slider_width = 40
slider_start = (screen_width - slider_width) / 2
slider_end = slider_start + slider_width
slider_y = screen_height / 2
erb_shift_range = 4

form Participant info
    integer List_number 1
endform



# procedures

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


procedure initializeExperiment: .list_num
    # Loads stimulus list into table, loads stimulus files and determines number of trials
    if .list_num > 9
        .num_str$ = string$ (.list_num)
    else
        .num_str$ = "0" + string$ (.list_num)
    endif
    .output_name$ = "output_" + .num_str$
    writeFileLine: path$ + .output_name$, "trial_number,stimulus_name,erb_shift"
    Read Table from comma-separated file: path$ + "list" + .num_str$ + ".csv"
    selectObject: "Table " + "list" + .num_str$
    .num_trials = Get number of rows
    for i to .num_trials
        selectObject: "Table " + "list" + .num_str$
        .name$ = Get value: i, "stimuli"
        Read from file: path$ + "test_stimuli/" + .name$ + ".Manipulation"
        @shiftStimulus: .name$, -0.4
        selectObject: "Sound " + shiftStimulus.new_name$
        Rename: .name$ + "_A"
        @shiftStimulus: .name$, 0.8
        selectObject: "Sound " + shiftStimulus.new_name$
        Rename: .name$ + "_B"
    endfor
    Create Sound from formula: "silence", 1, 0, 0.5, 44100, "0"
endproc


procedure welcomeScreen
    # initializes demo window and shows welcome screen with explanation
    demo Axes: 0, screen_width, 0, screen_height
    # demo Select outer viewport: 0, screen_width, 0, screen_height
    demo Select inner viewport: 0, screen_width, 0, screen_height
    demo Draw inner box
    demo Insert picture from file: path$ + "welcome_text.png", screen_width / 5, screen_width - (screen_width / 5), screen_height / 5, screen_height - (screen_height / 5)
    demo Paint rectangle: "grey", screen_width - (screen_width / 5), screen_width, 0, screen_height / 10
    demo Text: screen_width - (screen_width / 10), "centre", 0 + (screen_height / 20), "half", "Volgende"
    while demoWaitForInput ( )
        goto END_WELCOME demoClickedIn (screen_width - (screen_width / 5), screen_width, 0, screen_height / 10)
    endwhile
    label END_WELCOME
    demo Erase all
endproc


procedure redrawSlider: .xcor
    demo Paint rectangle: "white", slider_start - 5, slider_end + 5, slider_y - 5, slider_y + 5
    demo Draw line: slider_start, slider_y, slider_end, slider_y
    demo Paint circle: "purple", .xcor, slider_y, 1
endproc


procedure playStimuli: .stim_name$
    selectObject: "Sound " + .stim_name$ + "_A"
    Play
    selectObject: "Sound " + "silence"
    Play
    selectObject: "Sound " + .stim_name$ + "_B"
    Play
    selectObject: "Sound " + "silence"
    Play
    selectObject: "Sound " + .stim_name$ + "_X"
    Play
    Remove
endproc


procedure runTrial: .stim_name$
    demo Erase all
    demo Draw inner box
    demo Draw line: slider_start, slider_y, slider_end, slider_y
    demo Paint circle: "purple", slider_start + (slider_width / 2), slider_y, 1
    demo Paint rectangle: "grey", screen_width - (screen_width / 5), screen_width, 0, screen_height / 10
    demo Text: screen_width - (screen_width / 10), "centre", 0 + (screen_height / 20), "half", "Volgende"
    demoShow()

    .lower_or_higher = randomInteger(0,1)
    if .lower_or_higher = 1
        .random_shift = randomUniform(0.8, 1.5)
    elif .lower_or_higher = 0
        .random_shift = randomUniform(2.5, 3.2)
    endif
    @shiftStimulus: .stim_name$, .random_shift
    selectObject: "Sound " + shiftStimulus.new_name$
    Rename: .stim_name$ + "_X"
    @playStimuli: .stim_name$

    .min_shift = .random_shift - (erb_shift_range / 2)
    while demoWaitForInput ( )
        if demoClickedIn (slider_start, slider_end, slider_y - 10, slider_y + 10)
            .xcor = demoX ( )
            @redrawSlider: .xcor
            demoShow()
            .slider_prop = (.xcor - slider_start) / slider_width
            .erb_shift = .min_shift + (erb_shift_range * .slider_prop)
            @shiftStimulus: .stim_name$, .erb_shift
            selectObject: "Sound " + shiftStimulus.new_name$
            Rename: .stim_name$ + "_X"
            @playStimuli: .stim_name$
        elif demoClickedIn (screen_width - (screen_width / 5), screen_width, 0, screen_height / 10)
            goto END_TRIAL
        endif
    endwhile
    label END_TRIAL
endproc

procedure endScreen
    demo Erase all
    demo Draw inner box
    demo Text: screen_width / 2, "centre", screen_height / 2, "half", "Bedankt voor je deelname!"
    demo Paint rectangle: "grey", screen_width - (screen_width / 5), screen_width, 0, screen_height / 10
    demo Text: screen_width - (screen_width / 10), "centre", 0 + (screen_height / 20), "half", "Afsluiten"
    while demoWaitForInput ( )
        goto END demoClickedIn (screen_width - (screen_width / 5), screen_width, 0, screen_height / 10)
    endwhile
    label END
    demo Erase all
endproc

# main loop

@initializeExperiment: list_number
@welcomeScreen

for trial_num from 1 to initializeExperiment.num_trials
    selectObject: "Table " + "list" + initializeExperiment.num_str$
    stimulus_name$ = Get value: trial_num, "stimuli"
    @runTrial: stimulus_name$
    appendFileLine: path$ + initializeExperiment.output_name$, trial_num, ",", stimulus_name$, ",", runTrial.erb_shift
endfor

@endScreen
