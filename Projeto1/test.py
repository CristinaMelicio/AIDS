import unittest
from solver import main

class TestSolver(unittest.TestCase):

    def t(self,testname,type):
        output = str(main([1, type, "testes/"+testname+".txt"]))
        cost = float(output.split("\n")[-1])
        with open("testes/"+testname+".out", 'r')  as f:
            expected = f.readlines()
            expected_cost = float(expected[-1])
        self.assertEqual(cost, expected_cost)

    def test_simple1_uniformed(self):
        "simple1.txt [uniformedSearch]"
        self.t("simple1","-u")

    def test_simple1_informed(self):
        "simple1.txt [informedSearch]"
        self.t("simple1","-i")

    def test_trivial1_uniformed(self):
        "trivial1.txt [uniformedSearch]"
        self.t("trivial1","-u")

    def test_trivial1_informed(self):
        "trivial1.txt [informedSearch]"
        self.t("trivial1","-i")

    def test_trivial2_uniformed(self):
        "trivial2.txt [uniformedSearch]"
        self.t("trivial2","-u")

    def test_trivial2_informed(self):
        "trivial2.txt [informedSearch]"
        self.t("trivial2", "-i")

    def test_lbc_uniformed(self):
        "lbc.txt [uniformedSearch]"
        self.t("lbc","-u")

    def test_lbc_informed(self):
        "lbc.txt [informedSearch]"
        self.t("lbc", "-u")

    def test_mir_uniformed(self):
        "mir.txt [uniformedSearch]"
        self.t("mir","-u")

    def test_mir_informed(self):
        "mir.txt [informedSearch]"
        self.t("mir","-i")

    def test_t0_uniformed(self):
        "t0.txt [uniformedSearch]"
        self.t("t0","-u")

    def test_t0_informed(self):
        "t0.txt [informedSearch]"
        self.t("t0","-i")

    def test_t1_uniformed(self):
        "t1.txt [uniformedSearch]"
        self.t("t1","-u")

    def test_t1_informed(self):
        "t1.txt [informedSearch]"
        self.t("t1","-i")

    def test_t2_uniformed(self):
        "t2.txt [uniformedSearch]"
        self.t("t2","-u")

    def test_t2_informed(self):
        "t2.txt [informedSearch]"
        self.t("t2","-i")

    def test_t3_uniformed(self):
        "t3.txt [uniformedSearch]"
        self.t("t3","-u")

    def test_t3_informed(self):
        "t3.txt [informedSearch]"
        self.t("t3","-i")

    def test_t4_uniformed(self):
        "t4.txt [uniformedSearch]"
        self.t("t4","-u")

    def test_t4_informed(self):
        "t4.txt [informedSearch]"
        self.t("t4","-i")

    def test_t5_uniformed(self):
        "t5.txt [uniformedSearch]"
        self.t("t5","-u")

    def test_t5_informed(self):
        "t5.txt [uniformedSearch]"
        self.t("t5","-i")


if __name__ == '__main__':

     unittest.main(verbosity=3)