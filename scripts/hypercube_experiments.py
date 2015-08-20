
# coding: utf-8

# In[111]:

import scriptinit
import numpy as np
import argparse
import util
from hypercube import *
from experiment import *
from diagnostics import VisualizeTrajectoryController
from agent import DQN


# In[112]:

# step up argument parsing
parser = argparse.ArgumentParser()

def tup(s):
    try:
        s = s[1:-1]  # strip off the ( ) 
        return tuple(map(int, s.split(',')))
    except:
        raise argparse.ArgumentTypeError("Must give a tuple!")

# task arguments
parser.add_argument('-d', '--dimensions', type=tup, required=True)  # expects a (x, y, z, ...) tuple
parser.add_argument('-as', '--action_stochasticity', type=float, required=True)
parser.add_argument('-wp', '--wall_penalty', type=float, required=True)
parser.add_argument('-tp', '--time_penalty', type=float, required=True)
parser.add_argument('-r', '--reward', type=float, required=True)
parser.add_argument('-g', '--gamma', type=float, required=True)

# model arguments
parser.add_argument('-hd', '--hidden_dimension', type=int, required=True)
parser.add_argument('-lr', '--lr', type=float, required=True)
parser.add_argument('-eps', '--epsilon', type=float, required=True)

# experiment arguments
parser.add_argument('-me', '--max_episodes', type=int, required=True)
parser.add_argument('-rw', '--report_wait', type=int, required=True)
parser.add_argument('-sw', '--save_wait', type=int, required=True)
parser.add_argument('-vw', '--visualize_wait', type=int)
parser.add_argument('-fo', '--fully_observed', type=int, required=True) 
parser.add_argument('-ts', '--task_samples', type=int, required=True)


# In[113]:

if util.in_ipython():
    args = parser.parse_args(['-d','(5, 5)', '-as', '0.', '-wp', '-0.1', '-tp', '-0.1', '-r', '4', '-g', '0.9',
                              '-hd', '128', '-lr', '0.05', '-eps', '0.15', '-me', '100', '-rw', '2',
                              '-sw', '5', '-fo', '1', '-ts', '25'])
else:
    args = parser.parse_args()

hyperparams = vars(args)

# load into namespace and log to metadata
for var, val in hyperparams.iteritems():
    exec("{0} = hyperparams['{0}']".format(var))
    util.metadata(var, val)


# In[114]:

# set up the task
world = np.zeros(dimensions)
maze = HyperCubeMaze(dimensions=dimensions, action_stoch=action_stochasticity, grid=world)

# get training/test splits
# for debugging, let's just use a simple fixed goal (assumes the world is 2D!)
goal = np.random.randint(0, 2, size=(2 ** len(dimensions), 1))
while np.sum(goal) == 0.:
    goal = np.random.randint(0, 2, size=(2 ** len(dimensions), 1))

print 'GOAL VECTOR: ', goal


task = HyperCubeMazeTask(hypercubemaze=maze, initial_goal=goal,
                         wall_penalty=wall_penalty, time_penalty=time_penalty,
                         reward=reward, gamma=gamma, fully_observed=fully_observed)


# In[ ]:

# compile the agent
agent = DQN(task, hidden_dim=hidden_dimension, lr=lr, epsilon=epsilon)


# In[ ]:

# set up the experiment environment
controllers = [BasicController(report_wait=report_wait, save_wait=save_wait, max_episodes=max_episodes)]

if len(dimensions) == 2 and visualize_wait is not None and visualize_wait > 0:
    controllers.append(VisualizeTrajectoryController(visualize_wait=visualize_wait, dir_name='trajectories'))

observers = [HyperCubeObserver(report_wait=report_wait), AverageRewardObserver(report_wait=report_wait), AverageQValueObserver(task_samples=task_samples, report_wait=report_wait)]
experiment = Experiment(agent, task, controllers=controllers, observers=observers)


# In[ ]:

# launch experiment
experiment.run_experiments()


# In[66]:

# report results for each goal in the training set


# In[ ]:

# report results for each goal in the test set



# In[68]:



