from unittest import TestCase

class TestSimpylReader(TestCase):
    def test_read_json(self):
        from simpyl import reader
        self.assertIsNotNone(reader.read_sample_json())
