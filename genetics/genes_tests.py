import unittest
from genes import *

a = Nucleotide("A")
c = Nucleotide("C")
t = Nucleotide("T")
g = Nucleotide("G")
n = Nucleotide("")

class Nucleotide_tests(unittest.TestCase):
    
    def test_is_complementary(self):
        self.setUp();
        self.failUnless(a.is_complementary(t))
        self.failUnless(g.is_complementary(c))
        self.failIf(c.is_complementary(t))
        self.failUnless(n.is_complementary(t))
        self.failUnless(a.is_complementary(n))
        
    def test_is_empty(self):
        self.failIf(a.is_empty())
        self.failUnless(n.is_empty())
        
    def test_pair(self):
        self.failUnless(a.pair() == t)
        self.failUnless(g.pair() == c)
        self.failUnless(n.pair() == n)
        self.failIf(a.pair() == n)
        self.failIf(n.pair() == t)
        self.failIf(a.pair() == g)
        
class Single_strand_tests(unittest.TestCase):

    def setUp(self):
        self.actg = Single_strand('actg')
        self.cagt = Single_strand('cagt')
        self.ca = Single_strand('ca')
        self.ac = Single_strand('ac')
        self.gtca = Single_strand('gtca')
        self.tgac = Single_strand('tgac')
        self.nnac = Single_strand('  ac')
        self.actgn = Single_strand('actg ')
        self.actgac = Single_strand('actgac')
    
    def test_reverse_strand(self):
        self.failUnless(self.ca.reverse_strand() == self.ac)
        self.failUnless(self.actg.reverse_strand() == self.gtca)
        self.failIf(self.actg.reverse_strand() == self.cagt)
        self.failIf(self.actg.reverse_strand() == self.ca)
    
    def test_is_complementary(self):
        self.failUnless(self.actg.is_complementary(self.cagt))
        self.failIf(self.actg.is_complementary(self.ca))
        self.failIf(self.actg.is_complementary(self.gtca))
        self.failIf(self.actg.is_complementary(self.tgac))
        
    def test_remove_empties(self):
        self.failUnless(self.actg.remove_empties() == self.actg)
        self.failUnless(self.nnac.remove_empties() == self.ac)
        self.failUnless(self.actgn.remove_empties() == self.actg)
        
    def test_ligate(self):
        self.failUnless(self.actg.ligate(self.ac) == self.actgac)
        self.failUnless(self.actg.ligate(self.nnac) == self.actgac)
        self.failUnless(self.actgn.ligate(self.ac) == self.actgac)
        
    # TODO : Write tests once the method is written
    # def test_restrict(self):
    
class Double_strand_test(unittest.TestCase):
    
    def setUp(self):
        self.actg = Double_strand('actg')
        self.ca = Double_strand('ca')
        self.actg_cagt = Double_strand('actg', 'cagt')
        self.ca_nn = Double_strand('ca', '  ')
        self.cca_ngg = Double_strand('cca', ' gg')
        self.na_tt = Double_strand(Single_strand([n,a]), 'tt')
        
    def test_strand53(self):
        self.failUnless(self.actg.strand53() == Single_strand('actg'))
        self.failUnless(self.ca.strand53() == Single_strand('ca'))
        self.failUnless(self.actg.strand53() == self.actg_cagt.strand53())
    
    def test_strand35(self):
        self.failUnless(self.actg.strand35() == Single_strand('cagt'))
        self.failUnless(self.ca.strand35() == Single_strand('tg'))
        self.failUnless(self.actg.strand35() == self.actg_cagt.strand35())
        
    def test_anneal(self):
        self.failUnless(self.actg.anneal() == \
            [Single_strand('actg'), Single_strand('cagt')])
        self.failUnless(self.ca.anneal() == \
            [Single_strand('ca'), Single_strand('tg')])
        self.failUnless(self.ca_nn.anneal() == \
            [Single_strand('ca'), Single_strand('  ')])
        self.failUnless(self.na_tt.anneal() == \
            [Single_strand([n,a]), Single_strand('tt')])
            
    def test_flip(self):
        self.failUnless(self.actg.flip() == Double_strand('cagt'))
        self.failUnless(self.ca.flip() == Double_strand('tg'))
        self.failUnless(self.cca_ngg.flip() == \
            Double_strand(' gg', 'cca'))
        self.actg.draw_ladder()
        self.cca_ngg.draw_ladder()
        self.ca_nn.draw_ladder()
    
    def test_ligate(self):
        #self.failIf(self.actg.ligate(self.ca))
        #self.failIf(self.ca_nn.ligate(self.na_tt))
        self.failUnless(self.actg.ligate(self.ca) == Double_strand('actgca'))
        self.failUnless(self.ca_nn.ligate(Double_strand('  ', 'tg')) \
            == Double_strand('ca'))
        atn_cat = Double_strand(Single_strand([a,t,n]), 'cat')
        gcc_ggn = Double_strand('gcc', 'gg ')
        self.failUnless(atn_cat.ligate(gcc_ggn) == Double_strand('atgcc'))
    
    Double_strand(Single_strand([n,n,n,c,a,t,g,a,t,a,a]), \
                  Single_strand([n,n,a,t,c,a,t,g,t,t,a])).draw_ladder()
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()
