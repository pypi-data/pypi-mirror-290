### Step 6: Add Tests

# Add some basic tests in `tests/test_info.py`:

# ```python
import unittest
from sysinfor import getsysinfo

class TestSystemInfo(unittest.TestCase):

    def test_system_info(self):
        info = getsysinfo()
        self.assertIn("Kernel", info)
        self.assertIn("Release", info)

if __name__ == "__main__":
    unittest.main()