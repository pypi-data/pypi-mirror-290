import os
import json

from focont import foc, system


TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def test_01_01():
    filepath = TEST_DIR + '/aircraft_model.json'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_02():
    filepath = TEST_DIR + '/aircraft_model.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_03():
    filepath = TEST_DIR + '/unstable_aircraft_model.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_04():
    filepath = TEST_DIR + '/unstable_dt_aircraft_model.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_05():
    filepath = TEST_DIR + '/test_model_01.json'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_05_01():
    filepath = TEST_DIR + '/test_model_01.json'
    with open(filepath, 'r') as fh:
        input_data = json.load(fh)

        pdata = system.load(input_data)
        foc.solve(pdata)
        foc.print_results(pdata)

        assert foc.h2_improvement(pdata) < 1.0


def test_01_06():
    filepath = TEST_DIR + '/test_model_01_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)


def test_01_06_01():
    filepath = TEST_DIR + '/test_model_01_01_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_07():
    filepath = TEST_DIR + '/test_model_02_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_08():
    filepath = TEST_DIR + '/test_model_03_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_08():
    filepath = TEST_DIR + '/test_model_04_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_09():
    filepath = TEST_DIR + '/test_model_05_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_10():
    filepath = TEST_DIR + '/test_model_06_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


def test_01_11():
    filepath = TEST_DIR + '/test_model_07_for_FO.mat'
    pdata = system.load(filepath)
    foc.solve(pdata)
    foc.print_results(pdata)

    assert foc.h2_improvement(pdata) < 1.0


if __name__ == "__main__":
        test_01_01()

