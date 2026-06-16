import unittest
from voynich_analysis.naibbe.encoder import NaibbeEncoder
from voynich_analysis.naibbe.signatures import (
    compute_sig1,
    compute_sig2,
    compute_sig3,
    compute_sig4
)

class TestNaibbe(unittest.TestCase):
    def test_encoder_normalization(self):
        encoder = NaibbeEncoder(seed=42)
        self.assertEqual(encoder.normalize("hello world"), "hellouorld")

    def test_encoder_respacing(self):
        encoder = NaibbeEncoder(seed=42)
        normalized = "hellouorld"
        tokens = encoder.respace(normalized)
        self.assertGreater(len(tokens), 0)
        self.assertEqual("".join(tokens), normalized)

    def test_encoder_encoding(self):
        encoder = NaibbeEncoder(seed=42)
        ciphertext = encoder.encode("Test document encoding", unambiguous=True)
        self.assertTrue(isinstance(ciphertext, str))
        self.assertGreater(len(ciphertext.split()), 0)
        self.assertTrue(all(token.startswith("<") and token.endswith(">") for token in ciphertext.split()))

    def test_signatures(self):
        words = ["<ol>", "<chedy>", "<daiin>", "<shedy>", "<qokaiin>"]
        s1 = compute_sig1(words)
        self.assertTrue(0.0 <= s1 <= 1.0)
        
        s2 = compute_sig2(words)
        self.assertIn("extreme_start", s2)
        self.assertIn("extreme_end", s2)
        self.assertIn("present", s2)
        
        s3 = compute_sig3(words)
        self.assertTrue(isinstance(s3, float))
        
        s4 = compute_sig4(words)
        self.assertIn("start_r2", s4)
        self.assertIn("end_cv", s4)

if __name__ == '__main__':
    unittest.main()
