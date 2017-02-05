# variables

path$ = ""
screen_width = 100
screen_height = 100
slider_width = 40
slider_start = (screen_width - slider_width) / 2
slider_end = slider_start + slider_width
slider_y = screen_height / 2

# procedures

procedure getInfo
    # opens pop-up screen for participant info and stimulus list
endproc


procedure initializeExperiment
    # Loads stimulus list into table, loads stimulus files and determines number of trials,
endproc


procedure welcomeScreen
    # initializes demo window and shows welcome screen with explanation

    demo Axes: 0, screen_width, 0, screen_height
    # demo Select outer viewport: 0, screen_width, 0, screen_height
    demo Select inner viewport: 0, screen_width, 0, screen_height
endproc


procedure shiftStimulus
    # applies the PSOLA resynthesis
endproc


procedure redrawSlider: .xcor
    demo Paint rectangle: "white", slider_start - 5, slider_end + 5, slider_y - 5, slider_y + 5
    demo Draw line: slider_start, slider_y, slider_end, slider_y
    demo Paint circle: "purple", .xcor, slider_y, 1
endproc


procedure runTrial: .trial_num
    # draws the trial screen, plays the three stimuli at the start and every time the participant changes the slider, and waits for the participant to click the "next" button
    # in the initial presentation of the stimuli, the third stimulus should not be identical to the second stimulus, but should be randomly vary. This is done to prevent participants from making a similar sized manipulation in the same direction for each trial, as this could lead to a visually based strategy of putting the slider in the exact same spot.

    demo Erase all
    demo Draw inner box
    demo Draw line: slider_start, slider_y, slider_end, slider_y
    demo Paint circle: "purple", slider_start + (slider_width / 2), slider_y, 1
    while demoWaitForInput ( )
        if demoClickedIn (25, 75, 40, 60)
            xcor = demoX ( )
            @redrawSlider: xcor
        endif
    endwhile
endproc

procedure endScreen
endproc

# main loop

@getInfo
@initializeExperiment
writeFileLine:
@welcomeScreen

for trial_num from 1 to initializeExperiment.num_trials
    @runTrial: trial_num
    appendFileLine: path$ + file_name$, trial_num, ",", stimulus_name$, runTrial.erb_shift
endfor

@endScreen
