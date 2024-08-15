# We're just going to bring these to the front
# This is Tynan guessing what


# start delvewheel patch
def _delvewheel_patch_1_7_4():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'osrt.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_7_4()
del _delvewheel_patch_1_7_4
# end delvewheel patch

from osrt.model.osrt import OSRT
from osrt.model.threshold_guess import get_thresholds
