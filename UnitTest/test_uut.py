#  test_uut.py

# import imp  # Library to help us reload our UUT module, which is Deprecated
import importlib
from unittest import TestCase
from unittest.mock import patch

from UnitTest.app.uut import unit_to_be_tested
from app import uut  # Module with our thing to test


class TestUUT(TestCase):
    def setUp(self):
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            patch.stopall()  # Stops all patches started with start()
            importlib.reload(uut)  # Reload our UUT module which restores the original decorator

        self.addCleanup(
            kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        # Now patch the decorator where the decorator is being imported from
        patch('app.decorators.func_decor', lambda
            x: x).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        importlib.reload(uut)  # Reloads the uut.py module which applies our patched decorator

    def test_unit_to_be_tested(self):
        self.assertEqual(((1,), {}), unit_to_be_tested(1))
