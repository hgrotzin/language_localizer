"""Task documentation"""

from __future__ import absolute_import, division, print_function

# import audio preferences from psychopy - may need to change 'pygame' to
# 'pyo' or 'sounddevice'
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
prefs.general['audioDevice'] = ['Built-in Output']

from psychopy import core, data, event, gui, logging, sound, visual
import numpy as np
import os
import sys
import time
import random
import pandas as pd

# change directory to current directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# store info about the experiment session
expName = 'LanguageLocalizer'
expInfo = {'participant' : '',
            'run' : ['Scanner', 'Backup']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if not dlg.OK:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['participant'] = str(expInfo['participant'])

# create filename with relevant info
if expInfo['run'] == 'Scanner':
    filename = os.path.join(_thisDir, 'tfMRI_output',
        '%s_%s_%s'%(expInfo['participant'],expInfo['expName'],expInfo['date']))
else:
    filename = os.path.join(_thisDir, 'tfMRI_output', 'backup',
        '%s_%s_%s'%(expInfo['participant'],expInfo['expName'],expInfo['date']))

outfile = "{}.csv".format(filename)

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # This outputs to the screen

# csv to be read
if expInfo['run'] == 'Scanner':
    filepaths = "OrderAB.csv"
    df_trials_AB = pd.read_csv(filepaths, index_col=False)
else:
    filepaths = "OrderB.csv"
    df_trials_backup = pd.read_csv(filepaths, index_col=False)

# create window - black screen
win = visual.Window(
    fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

# create text objects
instructions_text = visual.TextStim(win,
    text='Please listen to the following audio clips and press any button \
each at the end of each clip.',
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

experimenter_text = visual.TextStim(win, text="Waiting for the experimenter.",
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

trigger_text = visual.TextStim(win, text="Waiting for the scanner.",
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

fixation = visual.TextStim(win, text='+',
    pos=(0,0), colorSpace='rgb', color=1, height=0.15, wrapWidth=1.5, depth=0.0)

thanks_text = visual.TextStim(win, text='Thanks!',
    pos=(0,0), colorSpace='rgb', color=1, height=0.15, wrapWidth=1.5, depth=0.0)

def save_on_quit(df):
    """ If escape key is pressed, quit task and save data collected to csv.
    df : main dataframe that data is saved to """
    if event.getKeys(keyList=["escape"]):
        win.close()
        core.quit()

    df.to_csv(outfile, index=True)

def retrieve_key_response(df):
    """ Get keys pressed and reaction times. Returns local variables.
    df : pd.DataFrame
    key_pressed : list of recorded keys pressed by subject
    """
    key_pressed = event.getKeys(keyList=['1', '2', '3', '4'])

    if not key_pressed:
        key_pressed = None

    return key_pressed

def get_audio_stim_mapping(list_of_filepaths, win=win):
    """Return dictionary of audio files given pd.Series object of filepaths.
    """
    list_of_filepaths = list_of_filepaths.unique()
    return {fp: sound.Sound(fp) for fp in list_of_filepaths}

def trials(run_trial):
    """ Main function calls all the other functions to collect data, stats, and
        display images. Saves "total" stats to df_totals and saves both
        DataFrames as csv files.

    Parameters
    ----------
    run_trial : determines which dataframe

    Local Variables
    ---------------
    clock : experiment clock
    trial_clock : running time clock
    header_cols : list of names of data frame columns
    df_master : empty data frame to add collected data to
    stim_mapping : creates audio object from csv
    audio_clip : audio clips from csv
    trial_type : str of type of trial
    stim_time : int length of each audio clip
    run_type : str A or B run
    """
    clock = core.Clock()
    trial_clock = core.Clock()

    # set up empty DataFrame to store experiment data
    header_cols = ['all_keys_pressed', 'trial_type', 'running_time']
    df_master = pd.DataFrame(columns=header_cols)

    # retrieve stimuli dictionary
    stim_mapping = get_audio_stim_mapping(run_trial.loc[:, 'Stimulus'])

    # display fixation
    t0 = time.time()
    clock.reset()
    fixation.draw()
    win.flip()
    save_on_quit(df_master)

    # this loop runs the trials
    for index, this_trial in run_trial.iterrows():
        # retrieve variables from csv
        audio_clip = stim_mapping[this_trial['Stimulus']]
        trial_type = str(this_trial['Trial_Type'])
        stim_time = int(this_trial['Trial_Length_in_Seconds'])

        # to pause halfway through in between A and B runs
        if expInfo['run'] == 'Scanner':
            run_type = str(this_trial['Order'])
            if run_type == 'B':
                begin_slides()
                win.flip()
                fixation.draw()
                win.flip()
                trial_clock.reset()

        # play audio clips
        t0 = time.time()
        clock.reset()
        audio_clip.play()
        while time.time() - t0 <= stim_time:
            save_on_quit(df_master)

        # call retrieve_key_response and save key_pressed functions
        key_pressed = retrieve_key_response(df_master)

        # retrieve running time for each trial
        trial_time = trial_clock.getTime()

        # save after each trial
        df_master.loc[len(df_master), :] = [key_pressed, trial_type, trial_time]
    # create and save dataframe as csv file
    df_master.to_csv(outfile, index=True)

def print_instructions():
    """ Short function to display instructions slide """
    instructions_text.draw()
    win.flip()
    event.waitKeys(keyList=['1', '2', '3', '4', 'space'])

def begin_slides():
    """ Shortcut function to display beginning slide and trigger """
    experimenter_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    trigger_text.draw()
    win.flip()
    event.waitKeys(keyList=['num_add', '+', 'space'])

# run experiment
if expInfo['run'] == 'Scanner':
    print_instructions()
    begin_slides()
    trials(df_trials_AB)
else:
    begin_slides()
    trials(df_trials_backup)

logging.flush()

# display end slide
thanks_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

win.close()
core.quit()
