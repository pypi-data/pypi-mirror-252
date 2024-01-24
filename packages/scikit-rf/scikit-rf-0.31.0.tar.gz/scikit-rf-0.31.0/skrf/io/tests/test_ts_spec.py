import skrf as rf
import numpy as np
from pathlib import Path
import pytest

test_data = Path(__file__).parent / "ts" 

s_mag = np.array(
        [[[0.6 , 0.4 , 0.42, 0.53],
        [0.4 , 0.6 , 0.53, 0.42],
        [0.42, 0.53, 0.6 , 0.4 ],
        [0.53, 0.42, 0.4 , 0.6 ]]])
    
s_deg = np.array(
    [[[161.24, -42.2 , -66.58, -79.34],
    [-42.2 , 161.2 , -79.34, -66.58],
    [-66.58, -79.34, 161.24, -42.2 ],
    [-79.34, -66.58, -42.2 , 161.24]]])

s = s_mag * np.exp(1j*s_deg*np.pi/180)
ex_5_6 = rf.Network(s=s, z0=[50, 75, 0.01, 0.01], f=5e9, f_unit="Hz")

@pytest.mark.parametrize("fname", 
    [
        test_data / "ex_5.ts",
        test_data / "ex_6.ts",
    ]
)
def test_ts_example_5_6(fname):
    ts = rf.Network(fname)
    assert ex_5_6 == ts

def test_ts_example_17():
    s_mag = np.array([
        [[0.95, 0.04],
        [3.57, 0.66]],

       [[0.6 , 0.14],
        [1.3 , 0.56]]])
    
    s_deg = np.array([
        [[ -26.,   76.],
        [ 157.,  -14.]],

       [[-144.,   40.],
        [  40.,  -85.]]])
    
    s = s_mag * np.exp(1j*s_deg * np.pi / 180)

    z0 = [[50, 25], [50, 25]]

    ref = rf.Network(f=[2,22], f_unit="GHz", s=s, z0=z0)
    ts = rf.Network(test_data / "ex_17.ts")

    assert ref == ts
    assert ts.noisy

    ts.z0 = 50
    snp = rf.Network(test_data / "ex_18.s2p")
    assert ts == snp
    assert np.allclose(ts.noise, snp.noise)
     
def test_ts_example_16():
    ts = rf.Network(test_data / "ex_16.ts")