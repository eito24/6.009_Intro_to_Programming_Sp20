#!/usr/bin/env python3
import os
import lab
import pickle
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)


def _tuple_close(t1, t2):
    return (len(t1) == len(t2)
            and all(abs(i - j) <= 1e-9 for i, j in zip(t1, t2)))


class Lab3Test(unittest.TestCase):
    cache = {}

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        if self.dataset not in self.cache:
            nodes_fname = f'resources/{self.dataset}.nodes'
            ways_fname = f'resources/{self.dataset}.ways'
            self.cache[self.dataset] = lab.build_auxiliary_structures(nodes_fname, ways_fname)
        self.aux = self.cache[self.dataset]


    def compare_output(self, inputs, test_num, type_):
        exp_fname = f'test_data/test_{self.dataset}_{test_num:02d}_{type_}.pickle'
        with open(exp_fname, 'rb') as f:
            expected_path = pickle.load(f)
        self.compare_result_expected(inputs, expected_path, type_)


    def compare_result_expected(self, inputs, expected_path, type_):
        test_func = lab.find_short_path if type_ == 'short' else lab.find_fast_path
        result_path = test_func(self.aux, *inputs)
        if expected_path is None:
            self.assertEqual(result_path, expected_path)
        else:
            self.assertEqual(len(result_path), len(expected_path), 'Path lengths differ')
            all_good = True
            for ix, (v1, v2) in enumerate(zip(result_path, expected_path)):
                if not _tuple_close(v1, v2):
                    all_good = False
                    break
            self.assertTrue(all_good, f'Paths differ at position {ix}.  Expected {v2}, got {v1}.')


class Test00_MITShortPaths(Lab3Test):
    dataset = 'mit'

    def test_00_short(self):
        # Should take the most direct path: New House, Kresge, North Maseeh, Lobby 7, Building 26, 009 OH
        loc1 = (42.355, -71.1009) # New House
        loc2 = (42.3612, -71.092) # 34-501
        expected_path = [
            (42.355, -71.1009), (42.3575, -71.0952), (42.3582, -71.0931),
            (42.3592, -71.0932), (42.36, -71.0907), (42.3612, -71.092),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'short')

    def test_01_short(self):
        # Should take path Building 35, Lobby 7, North Maseeh, South Maseeh
        # Tests that edges only connect consecutive nodes on a way
        loc1 = (42.3603, -71.095) # near Building 35
        loc2 = (42.3573, -71.0928) # Near South Maseeh
        expected_path = [
            (42.3601, -71.0952), (42.3592, -71.0932),
            (42.3582, -71.0931), (42.3575, -71.0927),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'short')

    def test_02_short(self):
        # Should take path Kresge, North Maseeh, South Maseeh, New House
        # Tests that one-ways are only allowed to go in certain direction
        loc1 = (42.3576, -71.0952) # Kresge
        loc2 = (42.355, -71.1009) # New House
        expected_path = [
            (42.3575, -71.0952), (42.3582, -71.0931),
            (42.3575, -71.0927), (42.355, -71.1009),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'short')

    def test_03_short(self):
        # Should take path Kresge, North Maseeh, Lobby 7, Building 26
        # Tests that for non-exact
        # Tests that nodes that aren't in any way are not used
        loc1 = (42.3576, -71.0951) #close to Kresge
        loc2 = (42.3605, -71.091) # is near an invalid node: Unreachable Node
        expected_path = [
            (42.3575, -71.0952), (42.3582, -71.0931),
            (42.3592, -71.0932), (42.36, -71.0907),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'short')

    def test_04_short(self):
        # Should return None
        # Tests node with no outgoing edges
        loc1 = (42.3575, -71.0956) # Parking Lot - end of a oneway and not on any other way
        loc2 = (42.3575, -71.0940) #close to Kresge
        self.compare_result_expected((loc1, loc2), None, 'short')


class Test01_MidwestShortPaths(Lab3Test):
    dataset = 'midwest'

    def test_00_short(self):
        inps = ((41.375288, -89.459541), (41.452802, -89.443683))
        self.compare_output(inps, 0, 'short')

    def test_01_short(self):
        inps = ((41.505515, -89.463392), (41.43567, -89.394277))
        self.compare_output(inps, 1, 'short')

    def test_02_short(self):
        inps = ((41.367973, -89.478311), (41.446346, -89.317066))
        self.compare_output(inps, 2, 'short')


class Test02_CambridgeShortPaths(Lab3Test):
    dataset = 'cambridge'

    def test_00_short(self):
        inps = ((42.359242, -71.093765), (42.358984, -71.114862))
        self.compare_output(inps, 0, 'short')

    def test_01_short(self):
        inps = ((42.359242, -71.093765), (42.360485, -71.108349))
        self.compare_output(inps, 1, 'short')

    def test_02_short(self):
        inps = ((42.360485, -71.108349), (42.359242, -71.093765))
        self.compare_output(inps, 2, 'short')

    def test_03_short(self):
        inps = ((42.403524, -71.23408), (42.348838, -71.093667))
        self.compare_output(inps, 3, 'short')

    def test_04_short(self):
        inps = ((42.336, -71.1678), (42.3398, -71.1063))
        self.compare_output(inps, 4, 'short')

    def test_05_short(self):
        inps = ((42.3398, -71.1063), (42.336, -71.1678))
        self.compare_output(inps, 5, 'short')


class Test03_MITFastPaths(Lab3Test):
    dataset = 'mit'

    def test_00_fast(self):
        # Should take the a longer, but faster path: New House, Kresge, North Maseeh, Lobby 7, Building 35, 009 OH
        loc1 = (42.355, -71.1009) # New House
        loc2 = (42.3612, -71.092) # 34-501
        expected_path = [
            (42.355, -71.1009), (42.3575, -71.0927), (42.3582, -71.0931),
            (42.3592, -71.0932), (42.3601, -71.0952), (42.3612, -71.092),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'fast')

    def test_01_fast(self):
        # Should take path Building 26, 009 OH, Building 35, Lobby 7
        # Tests that the 'maxspeed_mph' is used instead of highway type speed limit
        # also tests that in the prescence of a repeated way, the highest speed limit is preferred
        loc1 = (42.36, -71.0907) # near Lobby 26
        loc2 = (42.3592, -71.0932) # Near Lobby 7
        expected_path = [
            (42.36, -71.0907), (42.3612, -71.092),
            (42.3601, -71.0952), (42.3592, -71.0932),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'fast')

    def test_02_fast(self):
        # Should take path Kresge, North Maseeh, South Maseeh, New House
        # Tests that one-ways are only allowed to go in certain direction
        loc1 = (42.3576, -71.0952) # Kresge
        loc2 = (42.355, -71.1009) # New House
        expected_path = [
            (42.3575, -71.0952), (42.3582, -71.0931),
            (42.3575, -71.0927), (42.355, -71.1009),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'fast')

    def test_03_fast(self):
        # Should take path Kresge, North Maseeh, Lobby 7, Building 35, 009 Oh
        # Tests that for non-exact
        # Tests that nodes that aren't in any way are not used
        loc1 = (42.3576 , -71.0951) #close to Kresge
        loc2 = (42.3609, -71.0911) # is near an invalid node: Unreachable Node
        expected_path = [
            (42.3575, -71.0952), (42.3582, -71.0931), (42.3592, -71.0932),
            (42.3601, -71.0952), (42.3612, -71.092),
        ]
        self.compare_result_expected((loc1, loc2), expected_path, 'fast')


class Test04_MidwestFastPaths(Lab3Test):
    dataset = 'midwest'

    def test_00_fast(self):
        inps = ((41.375288, -89.459541), (41.452802, -89.443683))
        self.compare_output(inps, 0, 'fast')

    def test_01_fast(self):
        inps = ((41.505515, -89.463392), (41.43567, -89.394277))
        self.compare_output(inps, 1, 'fast')

    def test_02_fast(self):
        inps = ((41.367973, -89.478311), (41.446346, -89.317066))
        self.compare_output(inps, 2, 'fast')


class Test05_CambridgeFastPaths(Lab3Test):
    dataset = 'cambridge'

    def test_00_fast(self):
        inps = ((42.359242, -71.093765), (42.358984, -71.114862))
        self.compare_output(inps, 0, 'fast')

    def test_01_fast(self):
        inps = ((42.359242, -71.093765), (42.360485, -71.108349))
        self.compare_output(inps, 1, 'fast')

    def test_02_fast(self):
        inps = ((42.360485, -71.108349), (42.359242, -71.093765))
        self.compare_output(inps, 2, 'fast')

    def test_03_fast(self):
        inps = ((42.403524, -71.23408), (42.348838, -71.093667))
        self.compare_output(inps, 3, 'fast')

    def test_04_fast(self):
        inps = ((42.336, -71.1678), (42.3398, -71.1063))
        self.compare_output(inps, 4, 'fast')

    def test_05_fast(self):
        inps = ((42.3398, -71.1063), (42.336, -71.1678))
        self.compare_output(inps, 5, 'fast')

class ExtraTests(Lab3Test):
    dataset = 'cambridge'

    def test_get_closest(self):
        """
        Checks calculation of closest location.

        To use this checker, you will need to include a get_closest(aux, loc)
        function in your lab.py that returns the closest valid location to loc,
        based on or derived from your auxiliary data structures.
        """
        for loc1, expect in [((42.403524, -71.23408), (42.4034984, -71.2340812)),
                             ((42.358984, -71.114862), (42.3589638, -71.1148676)),
                             ((42.360485, -71.108349), (42.360057, -71.107667)),
                             ((42.359242, -71.093765), (42.359273, -71.0937599)),
        ]:
            result = lab.get_closest(self.aux, loc1)
            self.assertEqual(result, expect,
                             f'wrong closest node to {loc1}; should be {expect} not {result}')

    def test_check_connection(self):
        """
        Checks that important connections exist (or can be derived) from your
        auxiliary data structures.

        Your lab.py will need a check_connection(aux, loc1, loc2) function that
        returns True if a direct connection exists *from* loc1 *to* loc2.

        Sometimes helps to detect if one or both of one-way and two-way
        connections are missing from auxiliary data structures.
        """
        type_ = 'short'
        for test_num in range(6):
            exp_fname = f'test_data/test_{self.dataset}_{test_num:02d}_{type_}.pickle'
            with open(exp_fname, 'rb') as f:
                expected_path = pickle.load(f)
                for loc1, loc2 in zip(expected_path, expected_path[1:]):
                    self.assertTrue(lab.check_connection(self.aux, loc1, loc2),
                                    f'Connection missing in data structure from {loc1} to {loc2}.')

    def test_check_travel_time(self):
        """
        Checks calculation of the correct travel time for a direct connection.

        Your lab.py will need a function check_travel_time(aux, loc1, loc2)
        that returns the travel time for the direct connection from loc1 to
        loc2.
        """
        for loc1, loc2, expect_time in [
                ((42.359273, -71.0937599), (42.3593888, -71.0938665), 0.00038699088507177437),
                ((42.3596544, -71.0941734), (42.3596942, -71.0942229), 0.00014936443563067184),
                ((42.3608275, -71.0960005), (42.3607589, -71.0961583), 0.00037381747406156504),
                ((42.3591157, -71.0998222), (42.359019, -71.100017), 0.00047916740513217435),
                ((42.3576712, -71.1028038), (42.3575951, -71.1029482), 0.00036215017932078456),
                ((42.3590402, -71.1143993), (42.3589638, -71.1148676), 0.000979219117634969),
                ((42.3796478, -71.0955666), (42.3796808, -71.0956795), 0.00020652700597133508)]:
            result_time = lab.check_travel_time(self.aux, loc1, loc2)
            self.assertTrue(abs(result_time - expect_time) <= 1e-12,
                             f'Wrong travel time from {loc1} to {loc2}, should be {expect_time} not {result_time}')

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
