"""Example module tests."""
import os

from plab2.example import find_waldo


class TestExample:
    """Test class for example module."""

    def test_find_waldo(self):
        """Tests that find_waldo method can find waldo."""
        people = ['Bruce', 'Waldo', 'Jack', 'John']
        waldo_position = find_waldo(people)  # Should be at position 1
        assert isinstance(waldo_position, int)  # Check if output data type is correct
        assert waldo_position == 1  # Check if output is correct
