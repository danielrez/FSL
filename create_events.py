import os
from glob import glob
import pandas as pd

model = 1
duration = 6
weigth = 1


def create_events(subject_dir, behav_dir):
    for file_regex, task_sequence in subject_dir._task_mapping.iteritems():
        run_files = sorted(glob(os.path.join(behav_dir, '{}*.txt'.format(task_sequence))))
        print "{}->{}".format(file_regex, run_files)
        for run_number, run_file in enumerate(run_files):
            df = pd.read_csv(run_file, '\t')
            cond = df.StimVar.unique()
            cond.sort()
            for cond_num, cond_name in enumerate(cond):
                onsets = df[df.StimVar.eq(cond[cond_num])].Onset
                durations = [duration] * onsets.shape[0]
                weights = [weigth] * onsets.shape[0]
                file_name = "cond{:0>3d}.txt".format(cond_name)
                print ">>> condition mapping: {}->{}".format(file_regex, cond_name)
                onsetsfile = open(
                    "{}/model{:0>3d}/onsets/{}/{}".format(subject_dir.model_dir(), model, task_sequence, file_name),
                    "w")
                onsetsfile.write("{}\t{}\t{}\n".format('onset', 'duration', 'weight'))
                for rows, onT in enumerate(onsets):
                    onsetsfile.write("{}\t{}\t{}\n".format(onsets.values[rows], durations[rows], weights[rows]))
                onsetsfile.close()
