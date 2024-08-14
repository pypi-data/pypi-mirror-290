### Step 6: Add Tests

# Add some basic tests in `tests/test_info.py`:

# ```python
import unittest
from sysinfor.info import get_system_info

class TestSystemInfo(unittest.TestCase):

    def test_system_info(self):
        info = get_system_info()
        self.assertIn("Kernel", info)
        self.assertIn("Release", info)

if __name__ == "__main__":
    unittest.main()