"""
LP01 Mode detector
==================

"""

# %%
# Importing the package: PyMieSim
from PyMieSim.single.detector import LPMode

detector = LPMode(
    mode_number="LP01",
    sampling=300,
    NA=0.3,
    gamma_offset=0,
    phi_offset=40,
    coupling_mode='Point'
)

figure = detector.plot()

_ = figure.show()

# -
