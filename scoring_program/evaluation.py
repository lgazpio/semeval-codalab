#!/usr/bin/env python
import sys
import os.path
import random
import subprocess
import re

# as per the metadata file, input and output directories are the arguments
[_, input_dir, output_dir, program_dir] = sys.argv

# unzipped submission data is always in the 'res' subdirectory
# unzipped reference data is always in the 'ref' subdirectory

scores = []
overall = True
tracks = []
trackNames = ["1", "2", "3a", "3b", "4", "5", "6"]
trackExtension = ["1.ar-ar", "2.ar-en", "3a.sp-sp", "3b.sp-sp", "4.sp-en", "5.en-en", "6.su-su"]

for trackName in trackExtension:
    sys_name = "STS.sys.track" + trackName + ".txt"
    gs_name = "STS.gs.track"  + trackName + ".txt"

    system = os.path.join(input_dir, 'res', sys_name)
    gold = os.path.join(input_dir, 'ref', gs_name)

    if os.path.exists(system):
        sys.stdout.write("{0} found\n".format(system))
        checkOutput = subprocess.check_output([os.path.join(program_dir, "check.pl"), system])
        sys.stdout.write(checkOutput)
        sys.stdout.write("\n")
        if ("OK!" not in checkOutput):
            sys.exit("Input has incorrect format. Check input before submitting!!")

        result = subprocess.check_output([os.path.join(program_dir, "correlation.pl"), gold, system])
        result = re.findall("\d+\.\d+", result)
        sys.stdout.write(str(result))
        sys.stdout.write("\n")

        if (len(result) != 1):
            sys.exit("Input has incorrect number of lines. Check input before submitting!!")
        tracks.append(True)
        scores.append(result[0])

    else:
        sys.stdout.write("{0} not found\n".format(system))
        overall = False
        tracks.append(False)
        scores.append(0)


#with open(submission_path) as submission_file:
#    submission = submission_file.read()


#with open(os.path.join(input_dir, 'ref', 'truth.txt')) as truth_file:
#    truth = truth_file.read()

# the scores for the leaderboard must be in a file named "scores.txt"

with open(os.path.join(output_dir, 'scores.txt'), 'w') as out:
    if (overall):
        out.write("Primary:{0}\n".format( (float(scores[0]) + float(scores[1]) + (float(scores[2]) + float(scores[3])) / 2 + float(scores[4]) + float(scores[5]) + float(scores[6])) / 6 ))
    else:
        out.write("Primary:0.0\n")

    for trackName in trackNames:
        index = trackNames.index(trackName)
        if (tracks[index]):
            out.write("Track" + trackName + ":{0}\n".format(scores[index]))
        else:
            out.write("Track" + trackName + ":0.0\n")
