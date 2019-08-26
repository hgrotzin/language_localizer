# Language Localizer
Blocked auditory language localizer for in-scanner use. 

Task Parameters
---------------
Three block types: rest, intact speech, and degraded speech (all in English). There are 10 14s blocks of rest and 16 18s blocks each for intact and degraded speech. A white fixation is on the screen for the entirety of the task. 2 runs - 21 blocks each. The first block in each run is a rest block. ~12 min total (~6 min for each run).

Stimuli are loaded into a local dictionary before the task begins so as not to affect timing during the actual task.

Runs
----
The pop-up window asks for run type: scanner or backup.
- Scanner runs the entire tasks - both runs with a pause in between to check in with subject. This uses language_AB.csv.
- Backup runs just the second run of the task - use this if PsychoPy crashes during the task and you only need to run the second half. This uses language_B.csv

Subject key responses
---------------------
Keys pressed can be edited in the code itself. Current target keys are 1, 2, 3, and 4. Space bar moves through the instructions and + moves through the trigger slide (space bar will also move past this slide for ease of testing/starting task outside of scanner - can remove this when task is ready for scanner runs to avoid human error).

References
----------
Task based on: 
Terri L. Scott, Jeanne Gallée & Evelina Fedorenko (2016): A new fun and robust version of an fMRI localizer for the frontotemporal language system, *Cognitive Neuroscience*. Auditory clips can be found here: https://evlab.mit.edu/papers/Scott_CogNeuro.
