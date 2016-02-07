# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import unittest

from obspy import read_inventory, read_events
from obspy.imaging.ray_paths import plot_rays


class PathPlottingTestCase(unittest.TestCase):
    """
    Test suite for obspy.core.util.geodetics
    """
    def test_pathplotting(self):
        inv = read_inventory('data/IU.xml')
        cat = read_events()
        #plot_rays(inventory=inv, catalog=cat, phase_list=['PcP'],
        #          kind='mayavi', colorscheme='dark')
        plot_rays(inventory=inv, evlat=20., evlon=10., evdepth_km=200.,
                  phase_list=['PKP', 'PKIKP', 'PKJKP', 'PcP', 'PKiKP'],
                  kind='mayavi')


def suite():
    return unittest.makeSuite(PathPlottingTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
