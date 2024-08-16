import Aligner
from unittest import TestCase, main, expectedFailure


class Tests(TestCase):

    def test1(self):
        s1 = list("VTTFSYGVOC")
        s2 = list("VTTYFSGVOC")
        weight_char1_s1 = [1] * len(s1)
        weight_char1_s2 = [1] * len(s2)
        
        weights1 =[10 if x== ord('Y')else 1 for x in s1]
        weights2 =[10 if x== ord('Y')else 1 for x in s2]
        
        aligner = Aligner.AlignerWrapper()
        Weighted_score, Weighted_aln1, Weighted_aln2 = aligner.align_C(s1, s2, weights1, weights2, True)
        print(Weighted_score)
        print(Weighted_aln1)
        print(Weighted_aln2)

if __name__ == '__main__':
    main()
