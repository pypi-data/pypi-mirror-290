# tests/test_converter.py

import unittest
from audio_to_text.converter import AudioToTextConverter

class TestAudioToTextConverter(unittest.TestCase):
    def setUp(self):
        self.converter = AudioToTextConverter()

    def test_convert(self):
        text = self.converter.convert("path_to_test_audio.wav")
        self.assertIsInstance(text, str)

if __name__ == '__main__':
    unittest.main()

