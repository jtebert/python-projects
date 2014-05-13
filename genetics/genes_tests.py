import unittest
from genes import *

a = Nucleotide("A")
c = Nucleotide("C")
t = Nucleotide("T")
g = Nucleotide("G")
n = Nucleotide("")

enz_a_t = Restriction_enzyme([a,t], 1)
enz__at = Restriction_enzyme([a,t], 0)

class _tests(unittest.TestCase):
    
    def test_find_sub_list(self):
        self.assertEqual(find_sub_list(['a','t'],['c','a','t']), 1)
        self.assertEqual(find_sub_list(['c'],['c','a','t']), 0)
        self.assertEqual(find_sub_list([c],[c,a,t]), 0)
        self.assertEqual(find_sub_list([a,t],[c,a,t]), 1)
        self.assertEqual(find_sub_list([a,t],[c,c,c,a,t]), 3)
        self.assertEqual(find_sub_list([a,t],[a,t,c,c,c,a,t]), 0)

class Nucleotide_tests(unittest.TestCase):
    
    def test_is_complementary(self):
        self.assertTrue(a.is_complementary(t))
        self.assertTrue(g.is_complementary(c))
        self.assertFalse(c.is_complementary(t))
        self.assertTrue(n.is_complementary(t))
        self.assertTrue(a.is_complementary(n))
        
    def test_is_empty(self):
        self.assertFalse(a.is_empty())
        self.assertTrue(n.is_empty())
        
    def test_pair(self):
        self.assertEqual(a.pair(), t)
        self.assertEqual(g.pair(), c)
        self.assertEqual(n.pair(), n)
        self.assertNotEqual(a.pair(), n)
        self.assertNotEqual(n.pair(), t)
        self.assertNotEqual(a.pair(), g)
        
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
        self.cat = Single_strand('cat')
        self.at = Single_strand('at')
        self.atat = Single_strand('atat')
    
    def test_split(self):
        self.assertEqual(self.actg.split(0), [Single_strand(''), self.actg])
        self.assertEqual(self.actg.split(4), [self.actg, Single_strand('')])
        self.assertEqual(self.actg.split(2), \
            [Single_strand('ac'), Single_strand('tg')])
    
    def test_reverse_strand(self):
        self.assertEqual(self.ca.reverse_strand(), self.ac)
        self.assertEqual(self.actg.reverse_strand(), self.gtca)
        self.assertNotEqual(self.actg.reverse_strand(), self.cagt)
        self.assertNotEqual(self.actg.reverse_strand(), self.ca)
    
    def test_is_complementary(self):
        self.assertTrue(self.actg.is_complementary(self.cagt))
        self.assertFalse(self.actg.is_complementary(self.ca))
        self.assertFalse(self.actg.is_complementary(self.gtca))
        self.assertFalse(self.actg.is_complementary(self.tgac))
        
    def test_is_palindromic(self):
        self.assertFalse(self.actg.is_palindromic())
        self.assertFalse(Single_strand('aat').is_palindromic())
        self.assertTrue(Single_strand('aatt').is_palindromic())
        self.assertFalse(self.nnac.is_palindromic())
        
    def test_remove_empties(self):
        self.assertEqual(self.actg.remove_empties(), self.actg)
        self.assertEqual(self.nnac.remove_empties(), self.ac)
        self.assertEqual(self.actgn.remove_empties(), self.actg)
        
    def test_ligate(self):
        self.assertEqual(self.actg.ligate(self.ac), self.actgac)
        self.assertEqual(self.actg.ligate(self.nnac), self.actgac)
        self.assertEqual(self.actgn.ligate(self.ac), self.actgac)
        
    def test_restrict(self):
        self.assertEqual(self.actg.restrict(enz_a_t), [self.actg])
        self.assertEqual(self.cat.restrict(enz_a_t), \
            [Single_strand('ca'), Single_strand('t')])
        self.assertEqual(self.at.restrict(enz_a_t), \
            [Single_strand('a'), Single_strand('t')])
        #self.assertEqual(self.at.restrict(enz__at), [self.at])
        self.assertEqual(self.atat.restrict(enz_a_t), \
            [Single_strand('a'), Single_strand('ta'), Single_strand('t')])
        #self.assertEqual(self.atat.restrict(enz__at), [self.at, self.at])
        
    
class Double_strand_test(unittest.TestCase):
    
    def setUp(self):
        self.actg = Double_strand('actg')
        self.ca = Double_strand('ca')
        self.actg_cagt = Double_strand('actg', 'cagt')
        self.ca_nn = Double_strand('ca', '  ')
        self.cca_ngg = Double_strand('cca', ' gg')
        self.na_tt = Double_strand(Single_strand([n,a]), 'tt')
        
    def test_split(self):
        self.assertEqual(self.actg.split(0), [Double_strand(''), self.actg])
        self.assertEqual(self.actg.split(4), [self.actg, Double_strand('')])
        self.assertEqual(self.actg.split(2), \
            [Double_strand('ac'), Double_strand('tg')])
    
    def test_strand53(self):
        self.assertEqual(self.actg.strand53(), Single_strand('actg'))
        self.assertEqual(self.ca.strand53(), Single_strand('ca'))
        self.assertEqual(self.actg.strand53(), self.actg_cagt.strand53())
    
    def test_strand35(self):
        self.assertEqual(self.actg.strand35(), Single_strand('cagt'))
        self.assertEqual(self.ca.strand35(), Single_strand('tg'))
        self.assertEqual(self.actg.strand35(), self.actg_cagt.strand35())
        
    def test_anneal(self):
        self.assertEqual(self.actg.anneal(), \
            [Single_strand('actg'), Single_strand('cagt')])
        self.assertEqual(self.ca.anneal(), \
            [Single_strand('ca'), Single_strand('tg')])
        self.assertEqual(self.ca_nn.anneal(), \
            [Single_strand('ca'), Single_strand('  ')])
        self.assertEqual(self.na_tt.anneal(), \
            [Single_strand([n,a]), Single_strand('tt')])
            
    def test_rotate(self):
        self.assertEqual(self.actg.rotate(), Double_strand('cagt'))
        self.assertEqual(self.ca.rotate(), Double_strand('tg'))
        self.assertEqual(self.cca_ngg.rotate(), \
            Double_strand(' gg', 'cca'))
            
    def test_overhang_5(self):
        self.assertEqual(self.actg.overhang_5(), [Double_strand(""), self.actg])
        self.assertEqual(self.na_tt.overhang_5(), \
            [Double_strand(' ',"t"), Double_strand('a')])
        self.assertEqual(self.ca_nn.overhang_5(), [self.ca_nn, Double_strand('')])
        
    def test_overhang_3(self):
        self.assertEqual(self.actg.overhang_3(), [self.actg, Double_strand("")])
        self.assertEqual(self.ca_nn.overhang_3(), [Double_strand(''), self.ca_nn])
        self.assertEqual(self.na_tt.overhang_3(), [self.na_tt, Double_strand("")])
        self.assertEqual(self.cca_ngg.overhang_3(),
             [Double_strand('cc'), Double_strand('a',' ')])
    
    def test_ligate(self):
        self.assertFalse(self.actg.ligate(self.ca_nn))
        self.assertFalse(self.ca_nn.ligate(self.na_tt))
        self.assertEqual(self.actg.ligate(self.ca), Double_strand('actgca'))
        self.assertEqual(self.ca_nn.ligate(Double_strand('  ', 'tg')), \
            Double_strand('ca'))
        atn_cat = Double_strand(Single_strand([a,t,n]), 'cat')
        gcc_ggn = Double_strand('gcc', 'gg ')
        self.assertEqual(atn_cat.ligate(gcc_ggn), Double_strand('atgcc'))
    
    Double_strand(Single_strand([n,n,n,c,a,t,g,a,t,a,a]), \
                  Single_strand([n,n,a,t,c,a,t,g,t,t,a])).draw_ladder()
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()
