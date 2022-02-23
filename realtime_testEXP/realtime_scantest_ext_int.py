# yeah
import ctypes
xlib = ctypes.cdll.LoadLibrary('libX11.so')
xlib.XInitThreads()
from psychopy import core, gui, visual, data, logging, info
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import json, os, glob
import time as pythontime
import numpy as np
import pandas as pd
from psychopy.hardware.emulator import launchScan

#------------------------------------------------------------------------------
# Basic inforamation
#------------------------------------------------------------------------------

# the directory of the current experiment
expDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(expDir)

# Store info about the experiment session
expInfo = {'sub_id': '', 
           'run': '',
           'cond': 'ext_int'}
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
    'n_trial': 2,
    'dummy_trials':8.0,
    'intro_duration': 8.0,
    'trial_duration': 20.0,
    'between_block_duration': 12.0,
    # display parameters
    'full_screen': True,
    'screen_id': 1,
    'screen_resolution': (720,480),
    'frame_rate': 0.0,
    'frame_duration': 0.0,
    'frame_tolerance': 0.001,
    # timing log
    'trial_start_time': [],
    'trial_end_time': [],
    # scan parameters
    'TR': 2.0,
    'sync_key': 'apostrophe',
    'n_volumes': 128,
}

#------------------------------------------------------------------------------
# Task stimuli and instruction 
#------------------------------------------------------------------------------
# extremely simple task, so just code here: 

wait_trigger_text = 'Please wait for the experiment to start :)'
ext_text = 'For this block, please focus on the EXTERNAL details of the presented image.'
int_text = 'For this block, please focus on the INTERNAL thoughts associated with the presented image.'

#------------------------------------------------------------------------------
# Setup results file
#------------------------------------------------------------------------------

out_dir = os.path.join(expDir, f"sub_{expInfo['sub_id']}", f"run_{expInfo['run']}")
if not os.path.isdir(out_dir): 
    os.makedirs(out_dir)
out_csv = os.path.join(out_dir, f"timing_output_{expInfo['cond']}.csv")
out_json = os.path.join(out_dir, f"timing_output_{expInfo['cond']}.json")

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


def instruction(text):

    # initialize routine clock
    routine_countdown.reset()
    routine_countdown.add(params['intro_duration'])
    routinue_clock = core.Clock()

    # initialize constants
    continue_routine = True
    frame_id = -1

    # initialize stimuli: wait trigger
    stim_instruction = visual.TextStim(
        win=win,
        name='stim_wait',
        text=text,
        font='Arial',
        pos=(0, 0),
        height=0.05,
        color='black'
    )

    # initialize components attributes and some variables
    initialize_routinue_status([stim_instruction], routinue_clock)

    # run routine
    while continue_routine and routine_countdown.getTime() > 0:
        # get timing
        t_this_flip, t_this_flip_global, frame_id, _ = timing_per_flip(routinue_clock, frame_id)
        # wait for stimuli to start (if there's a delay inside the routinue)
        if (stim_instruction.status == NOT_STARTED) and (t_this_flip >= 0.0 - 0.001):
            start_component(stim_instruction, t_this_flip_global, frame_id)
            stim_instruction.status = STARTED
        # draw stimuli for each frame if the elapsed time less than designed duration
        if stim_instruction.status == STARTED:
            if t_this_flip_global <= stim_instruction.t_start_global + params['intro_duration'] - 0.001:
                stim_instruction.draw()
                # update timing information
                update_component_timing(stim_instruction, frame_id)
        # check for quit (typically the Esc key)
        if global_keyboard.getKeys(keyList=['escape']):
            core.quit()
        elif global_keyboard.getKeys(keyList=['apostrophe'], clear = True):
            curtime = pythontime.time()
            pulse_timing.append(curtime)

        # refresh the screen
        win.flip()
    
    # shift time stamp for t_start and t_stop, make t0 = scanner trigger time
    shift_time_to_trigger([stim_instruction], params['scanner_trigger_time_global'])

def run_blank_period(time):

    # initialize routine clock
    routine_countdown.reset()
    routine_countdown.add(time)
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
    initialize_routinue_status([stim_fixation], routinue_clock)

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
            if t_this_flip_global <= stim_fixation.t_start_global + time - 0.001:
                stim_fixation.draw()
                # update timing information
                update_component_timing(stim_fixation, frame_id)
        # check for quit (typically the Esc key)
        if global_keyboard.getKeys(keyList=['escape']):
            core.quit()
        elif global_keyboard.getKeys(keyList=['apostrophe'], clear = True):
            curtime = pythontime.time()
            pulse_timing.append(curtime)
        # refresh the screen
        win.flip()

    # shift time stamp for t_start and t_stop, make t0 = scanner trigger time
    shift_time_to_trigger([stim_fixation], params['scanner_trigger_time_global'])

def run_trial(info):

    task_image = info['img']
    # initialize routine clock
    routine_countdown.reset()
    routine_countdown.add(params['trial_duration'])
    routinue_clock = core.Clock()

    # initialize constants
    continue_routine = True
    frame_id = -1

    stim_cue = visual.ImageStim(
        win=win,
        name='stim_cue', 
        image=task_image, 
        mask=None,
        ori=0, pos=(0, 0), size=(1.5, 1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=512, interpolate=True, depth=-1.0)

    # initialize components attributes and some variables
    routine_components = [stim_cue]
    initialize_routinue_status(routine_components, routinue_clock)


    # run routine
    while continue_routine and routine_countdown.getTime() > 0:
        # get timing
        t_this_flip, t_this_flip_global, frame_id, _ = timing_per_flip(routinue_clock, frame_id)
        # wait for stimuli to start (if there's a delay inside the routinue)
                
        if (stim_cue.status == NOT_STARTED) and (t_this_flip >= 0.0 - 0.001):
            start_component(stim_cue, t_this_flip_global, frame_id)
            stim_cue.status = STARTED
        if stim_cue.status == STARTED:
            if t_this_flip_global <= stim_cue.t_start_global + params['trial_duration'] - 0.001:
                # END THIS and update stopping timing information
                update_component_timing(stim_cue, frame_id) # update the end time for each flip 
                stim_cue.draw() # cannot use autodraw here, otherwise the end time cannot be recorded 
                
        # check for quit (typically the Esc key)
        if global_keyboard.getKeys(keyList=['escape']):
            core.quit()
        elif global_keyboard.getKeys(keyList=['apostrophe'], clear = True):
            curtime = pythontime.time()
            pulse_timing.append(curtime)
        # refresh the screen
        win.flip()

    # shift time stamp for t_start and t_stop, make t0 = scanner trigger time
    shift_time_to_trigger(routine_components, params['scanner_trigger_time_global'])
    params['trial_start_time'].append(stim_cue.t_start)
    params['trial_end_time'].append(stim_cue.t_stop)




#----------------------------------------------------------------------------
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
global_keyboard = keyboard.Keyboard()
pulse_timing = []

# Waiting for scanner #
# clock to track time after MRI scanner pulse
scan_clock = core.Clock()
# clock to track time remaining of each (non-slip) routine
routine_countdown = core.CountdownTimer()
mri_setting = {
    'TR': params['TR'],
    'volumes': params['n_volumes'],
    'sync': params['sync_key']
}
launchScan(win=win, settings=mri_setting, globalClock=scan_clock, mode='scan', wait_msg = wait_trigger_text)
params['scanner_trigger_time_global'] = logging.defaultClock.getTime()

# clock to track time after MRI scanner pulse
global_clock = core.Clock()
# clock to track time remaining of each (non-slip) routine
routine_countdown = core.CountdownTimer()

images = glob.glob(os.path.join(expDir, "stimuli", "*"))

run_blank_period(params['dummy_trials'])
for round in range(2):

    instruction(ext_text)
    for this_trial in range(params['n_trial']):
        info = {"img" : images[round*2 + this_trial]}
        run_trial(info)
    run_blank_period(params['between_block_duration'])

    instruction(int_text)
    for this_trial in range(params['n_trial']):
        info = {"img" : images[round*2 + this_trial]}
        run_trial(info)
    run_blank_period(params['between_block_duration'])
    
run_blank_period(params['dummy_trials'])


results = pd.DataFrame({#"round" : list(range(params['n_rounds']))
                      "task_start" : params['trial_start_time'],
                      "task_end" : params['trial_end_time']})
results.to_csv(out_csv, index=False, na_rep='n/a')

with open(out_json, 'w') as json_file:
  json.dump(pulse_timing, json_file)




#------------------------------------------------------------------------------
# Quit experiment
#------------------------------------------------------------------------------
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting

win.flip()
# Close window
win.close()
core.quit()


