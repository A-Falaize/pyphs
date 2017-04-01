#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

Here, we build the PHS core asssociated with the

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import sys
from pyphs import PHSNetlist, PHSGraph, PHSSimulation, signalgenerator


label = 'bjtamp'

os.chdir(os.path.dirname(sys.argv[0]))

path = os.getcwd()

netlist_filename = path + os.sep + label + '.net'

netlist = PHSNetlist(netlist_filename)

graph = PHSGraph(netlist=netlist)

core = graph.buildCore()

core.build_R()

config = {'fs': 48e3,
          'split': True,
          'progressbar': True,
          'timer': True,
          }

simu = PHSSimulation(core, config=config)

dur = 0.01

u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)


def sequ():
    for el in u():
        yield (0, 1e-3*el, 9.)


simu.init(sequ=sequ(), nt=int(dur*simu.fs))


simu.process()


simu.data.plot_powerbal(mode='multi')