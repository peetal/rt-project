#import ctypes
#xlib = ctypes.cdll.LoadLibrary('libX11.so')
#xlib.XInitThreads()
from psychopy import core, gui, visual, data, logging, info
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import time, json, os
import numpy as np
import pandas as pd

#------------------------------------------------------------------------------
# Basic inforamation
#------------------------------------------------------------------------------

# the directory of the current experiment
expDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(expDir)

# Store info about the experiment session
expInfo = {'sub_id': '', 
           'session': ''}
expInfo['psychopy_version'] = info.psychopyVersion
expInfo['expName'] = "Realtime_scantest"
expInfo['date'] = data.getDateStr()  # add a simple timestamp
dlg = gui.DlgFromDict(dictionary=expInfo, sort_keys=False, title="Realtime_scantest")
if dlg.OK == False:
    core.quit()  # user pressed cancel



#------------------------------------------------------------------------------
# Setup parameters
#------------------------------------------------------------------------------

# Declare primary task parameter
params = {
    # experiment parameters
    'exp_name': expInfo['expName'],
    'date': expInfo['date'],
    'psychopy_version': expInfo['psychopy_version'],
    # stimuli parameters
    'n_rounds': 4,
    'intro_duration': 8.0,
    'task_duration': 20.0,
    'between_block_duration': 12.0,
    # display parameters
    'full_screen': True,
    'screen_id': 0,
    'screen_resolution': (3072,1920),
    'frame_rate': 0.0,
    'frame_duration': 0.0,
    'frame_tolerance': 0.001,
    # timing log
    'intro_start_time': [],
    'intro_end_time': [],
    'task_start_time': [],
    'task_end_time': [],
    'IBI_start_time': [],
    'IBI_end_time': []
}

#------------------------------------------------------------------------------
# Task stimuli and instruction 
#------------------------------------------------------------------------------
# extremely simple task, so just code here: 

task_image = os.path.join(expDir, "image.png")
wait_trigger_text = 'Please wait for the experiment to start :)'
ext_text = 'Focusing on the external details: Explore what each person is doing. '
int_text = 'Ignore the image and focusing on internal thoughts! Retrieve the episode of the last you were in a crowede restaurant.'

#------------------------------------------------------------------------------
# Setup results file
#------------------------------------------------------------------------------

out_dir = os.path.join(expDir, f"sub_{expInfo['sub_id']}", f"session_{expInfo['session']}")
if not os.path.isdir(out_dir): 
    os.makedirs(out_dir)
out_log = os.path.join(out_dir, "timing_info_logs.json")
out_csv = os.path.join(out_dir, "timing_output.csv")

#------------------------------------------------------------------------------
# Helper function
#------------------------------------------------------------------------------

# while performing this routine, update frame-wise information after each flip 
# for a monitor with 60hz refresh rate, the duration of each frame is around 16ms
def timing_per_flip(routinue_clock, frame_id):
    # get current time relative to routine clock
    t_elapsed = routinue_clock.getTime()
    # next flip time relative to routine clock
    t_this_flip = win.getFutureFlipTime(clock=routinue_clock)
    # next flip time relative to global clock
    t_this_flip_global = win.getFutureFlipTime(clock=None)
    # number of completed frames (0 is the first frame)
    frame_id += 1

    return t_this_flip, t_this_flip_global, frame_id, t_elapsed

# before starting a routine, initiate all component of this routine. 
def initialize_routinue_status(components, routinue_clock):
    # initialize components' attributes
    for comp in components:
        comp.t_start = None
        comp.t_stop = None
        comp.t_start_global = None
        comp.t_stop_global = None
        comp.status = NOT_STARTED
    # initialize variables
    # get the expected time of the next screen refresh
    time_to_first_frame = win.getFutureFlipTime(clock='now')
    # reset clock (t0 is time of first possible flip)
    routinue_clock.reset(-time_to_first_frame) # the routine clock starts not exactly at 0, but the first flip. 

def start_component(component, flip_time, frame_id):
    # exact frame index
    component.frame_start_id = frame_id
    # stimuli onset time (relative to scan trigger)
    # need to be initialized with some value since the first comparision will occur before
    # the first actual flip
    # before the final shift, t_start and t_start_global will be the same value
    component.t_start = flip_time
    win.timeOnFlip(component, 't_start')
    # stimuli onset time (relative to global clock)
    component.t_start_global = flip_time
    win.timeOnFlip(component, 't_start_global')

def update_component_timing(component, frame_id):
    # keep track the latest flip (for non-slip routinue)
    component.frame_stop_id = frame_id
    # stimuli onset time (relative to scan trigger)
    win.timeOnFlip(component, 't_stop')
    # stimuli onset time (relative to global clock)
    win.timeOnFlip(component, 't_stop_global')

def shift_time_to_trigger(components, t_sync):
    for comp in components:
        if hasattr(comp, 't_start'):
            comp.t_start -= t_sync
        if hasattr(comp, 't_stop'):
            comp.t_stop -= t_sync


def wait_trigger():

    # initialize routine clock
    routinue_clock = core.Clock()

    # initialize constants
    continue_routine = True
    frame_id = -1

    # initialize stimuli: wait trigger
    stim_wait = visual.TextStim(
        win=win,
        name='stim_wait',
        text=wait_trigger_text,
        font='Arial',
        pos=(0, 0),
        height=0.1,
        color='black'
    )
    # trigger keyboard
    wait_trigger = keyboard.Keyboard()

    # initialize components attributes and some variables
    routine_components = [stim_wait, wait_trigger]
    initialize_routinue_status(routine_components, routinue_clock)

    # run routine
    while continue_routine:
        # get timing
        t_this_flip, t_this_flip_global, frame_id, _ = timing_per_flip(routinue_clock, frame_id)
        # wait for stimuli to start (if there's a delay inside the routinue)
        if (stim_wait.status == NOT_STARTED) and (t_this_flip >= 0.0 - 0.001):
            start_component(stim_wait, t_this_flip_global, frame_id)
            stim_wait.status = STARTED
        # draw stimuli for each frame if the elapsed time less than designed duration
        if stim_wait.status == STARTED:
            stim_wait.draw()
            # update timing information
            update_component_timing(stim_wait, frame_id)
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            core.quit()
        # refresh the screen
        win.flip()
        # deal with response
        kb_wait_on_flip = False
        if (wait_trigger.status == NOT_STARTED) and (t_this_flip >= 0.0 - 0.001):
            start_component(wait_trigger, t_this_flip_global, frame_id)
            wait_trigger.status = STARTED
            # start keyboard checking and timing on next flip
            kb_wait_on_flip = True
            # t=0 on next screen flip
            win.callOnFlip(wait_trigger.clock.reset)
            # clear events on next screen flip
            win.callOnFlip(wait_trigger.clearEvents, eventType='keyboard')
        if (wait_trigger.status == STARTED) and (not kb_wait_on_flip):
            update_component_timing(wait_trigger, frame_id)
            # record responses
            key_press = wait_trigger.getKeys(keyList=['apostrophe'], waitRelease=False)
            # only keep the last key press
            if len(key_press):
                # a response ends the routine
                continue_routine = False


def run_task(task_cond):

    # initialize routine clock
    routine_countdown.reset()
    routine_countdown.add(params['intro_duration'] + params['task_duration'])
    routinue_clock = core.Clock()

    # initialize constants
    continue_routine = True
    frame_id = -1

    if task_cond == "external": 
        this_text = ext_text
    if task_cond == "internal":
        this_text = int_text
    # initialize stimuli: recall cue
    stim_txt = visual.TextStim(
        win=win,
        name='stim_txt',
        text=this_text,
        font='Arial',
        pos=(0, 0),
        height=0.1,
        color='black')

    stim_cue = visual.ImageStim(
        win=win,
        name='stim_cue', 
        image=task_image, 
        mask=None,
        ori=0, pos=(0, 0), size=(1.5, 1.5),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=512, interpolate=True, depth=-1.0)

    # initialize components attributes and some variables
    routine_components = [stim_txt, stim_cue]
    initialize_routinue_status(routine_components, routinue_clock)


    # run routine
    while continue_routine and routine_countdown.getTime() > 0:
        # get timing
        t_this_flip, t_this_flip_global, frame_id, _ = timing_per_flip(routinue_clock, frame_id)
        # wait for stimuli to start (if there's a delay inside the routinue)
        if (stim_txt.status == NOT_STARTED) and (t_this_flip >= 0.0 - 0.001):
            start_component(stim_txt, t_this_flip_global, frame_id) # component.t_start and component.t_start_globle to be t_this_flip_global
            stim_txt.status = STARTED
        # draw stimuli for each frame if the elapsed time less than designed duration
        if stim_txt.status == STARTED:
            if t_this_flip_global <= stim_txt.t_start_global + params['intro_duration'] - 0.001:
                # END THIS and update stopping timing information
                update_component_timing(stim_txt, frame_id) # update the end time for each flip 
                stim_txt.draw()
                
        if (stim_cue.status == NOT_STARTED) and (t_this_flip >= params['intro_duration'] - 0.001):
            start_component(stim_cue, t_this_flip_global, frame_id)
            stim_cue.status = STARTED
        if stim_cue.status == STARTED:
            if t_this_flip_global <= stim_cue.t_start_global + params['task_duration'] - 0.001:
                # END THIS and update stopping timing information
                update_component_timing(stim_cue, frame_id) # update the end time for each flip 
                stim_cue.draw() # cannot use autodraw here, otherwise the end time cannot be recorded 
                
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            core.quit()
        # refresh the screen
        win.flip()

    # shift time stamp for t_start and t_stop, make t0 = scanner trigger time
    shift_time_to_trigger(routine_components, params['trigger_time_global'])
    params['intro_start_time'].append(stim_txt.t_start)
    params['intro_end_time'].append(stim_txt.t_stop)
    params['task_start_time'].append(stim_cue.t_start)
    params['task_end_time'].append(stim_cue.t_stop)

def run_ibi():

    # initialize routine clock
    routine_countdown.reset()
    routine_countdown.add(params['between_block_duration'])
    routinue_clock = core.Clock()

    # initialize constants
    continue_routine = True
    frame_id = -1

    # initialize stimuli: fixation
    stim_fixation = visual.TextStim(
        win=win,
        name='stim_fixation',
        text='+',
        font='Arial',
        pos=(0, 0),
        height=0.1,
        color='black'
    )

    # initialize components attributes and some variables
    routine_components = [stim_fixation]
    initialize_routinue_status(routine_components, routinue_clock)

    # run routine
    while continue_routine and routine_countdown.getTime() > 0:
        # get timing
        t_this_flip, t_this_flip_global, frame_id, _ = timing_per_flip(routinue_clock, frame_id)
        # wait for stimuli to start (if there's a delay inside the routinue)
        if (stim_fixation.status == NOT_STARTED) and (t_this_flip >= 0.0 - 0.001):
            start_component(stim_fixation, t_this_flip_global, frame_id)
            stim_fixation.status = STARTED
        # draw stimuli for each frame if the elapsed time less than designed duration
        if stim_fixation.status == STARTED:
            if t_this_flip_global <= stim_fixation.t_start_global + params['between_block_duration'] - 0.001:
                stim_fixation.draw()
                # update timing information
                update_component_timing(stim_fixation, frame_id)
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            core.quit()
        # refresh the screen
        win.flip()

    # shift time stamp for t_start and t_stop, make t0 = scanner trigger time
    shift_time_to_trigger(routine_components, params['trigger_time_global'])
    params['IBI_start_time'].append(stim_fixation.t_start)
    params['IBI_end_time'].append(stim_fixation.t_stop)



#------------------------------------------------------------------------------
# Main experiment
#------------------------------------------------------------------------------

# Initialize window #
win = visual.Window(
    size=params['screen_resolution'],
    fullscr=params['full_screen'],
    screen=params['screen_id'],
    winType='pyglet',
    allowGUI=True,
    allowStencil=False,
    monitor='testMonitor',
    color=[0, 0, 0],
    colorSpace='rgb',
    blendMode='avg',
    useFBO=True,
    units='height'
)
# store frame rate of monitor
#params['frame_rate'] = win.getActualFrameRate()
#params['frame_duration'] = 1.0 / round(params['frame_rate'])

# Initialize keyboard #
defaultKeyboard = keyboard.Keyboard()

wait_trigger()
params['trigger_time_global'] = logging.defaultClock.getTime()

# clock to track time after MRI scanner pulse
global_clock = core.Clock()
# clock to track time remaining of each (non-slip) routine
routine_countdown = core.CountdownTimer()

for round in range(params['n_rounds']):
    run_task("external")
    run_ibi()
    run_task("internal")
    run_ibi()


results = pd.DataFrame({#"round" : list(range(params['n_rounds'])),
                      "intro_start" : params['intro_start_time'],
                      "intro_end" : params['intro_end_time'],
                      "task_start" : params['task_start_time'],
                      "task_end" : params['task_end_time'],
                      "IBI_start": params['IBI_start_time'],
                      "IBI_end": params['IBI_end_time']})
results.to_csv(out_csv, index=False, na_rep='n/a')



#------------------------------------------------------------------------------
# Quit experiment
#------------------------------------------------------------------------------
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting

win.flip()
# Close window
win.close()
core.quit()


