from abc import ABCMeta, abstractmethod
import operator
import random

def andmap(b,L):
    return reduce(operator.and_, [b(x) for x in L])

def ormap(b,L):
    return reduce(operator.or_, [b(x) for x in L])

# TODO : Define a DNAmol, Genome
# TODO : Allow non-complementary double strand creation (perhaps with warning?)
# TODO : Ligation with different rotations

def find_sub_list(sl,l):
    sll=len(sl)
    if sll > len(l): return False
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            return ind
        else:
            return False

def process_strand(strand):
    """Get a list of Nucleotides from various input types and verify correctness
       of input.
       String OR List<Nucleotide> OR Single_strand -> List<Nucleotide>"""
    if isinstance(strand, str):
        strand = list(strand)
        return map(lambda b: Nucleotide(b), strand)
    elif isinstance(strand, Single_strand):
        return strand.bases
    elif isinstance(strand, list) and \
        len(filter(lambda b: not isinstance(b, Nucleotide), strand))==0:
        return strand
    else:
        raise ValueError("Invalid input to create DNA molecule: " + str(type(strand))) 

class Restriction_enzyme(object):
    """Represents a restriction enzyme to cut DNA"""
    
    def __init__(self, recog_site, cut_site):
        """Constructor for restriciton enzyme
           List<Nucleotide> int -> Restriction_enzyme"""
        self.recog_site = recog_site
        self.cut_site = cut_site
    
    def __eq__(self, other):
        """Override equals method"""
        if isinstance(other, Restriction_enzyme):
            return self.recog_site == other.recog_site and \
                 self.cut_site == other.cut_site
        else:
            return False
            
    def __len__(self):
        return len(self.recog_site)
    
    def __str__(self):
        """Override string method"""
        out = '<'
        for i in range(len(self)):
            if i == self.cut_site:
                out += "|"
            out = out + str(self.recog_site[i])
        return out + '>'

class Nucleotide(object):
    """Concrete class representing A, C, T, or G base"""
    
    base_matches = {'A':'T', 'T':'A', 'C':'G', 'G':'C', '':''}
    valid_bases = base_matches.keys()

    def __init__(self, base):
        base = base.upper()
        if base in self.valid_bases:
            self.base = base
        elif base == " ":
            self.base = ""
        else:
            raise ValueError('Invalid base.  Must be one of A, C, T, G, or " "')
            
    def __eq__(self, other):
        """Override equals method"""
        if isinstance(other, Nucleotide):
            return self.base == other.base
        else:
            return False
    
    def __str__(self):
        """Override string method"""
        return self.base
        
    def __repr__(self):
        """Override string method"""
        return self.base
            
    def is_complementary(self, base):
        """Does the given base pair with this base?
           Nucleotide -> Boolean"""
        if base.is_empty() or self.is_empty():
            return True
        else:
            return self.base_matches[self.base] == base.base
    
    def is_empty(self):
        """Is the base empty?
           -> Boolean"""
        return len(self.base) == 0
        
    def pair(self):
        """Returns the complementary base
           -> Nucleotide"""
        return Nucleotide(self.base_matches[self.base])
        
class Single_strand(object):
    """Represents a single stranded DNA molecule"""
    
    def __init__(self, bases):
        """String OR List<Nucleotide> -> Single_strand"""
        self.bases = process_strand(bases)
            
    def __eq__(self, other):
        """Override equals method"""
        if isinstance(other, Single_strand):
            return self.bases == other.bases
        else:
            return False
    
    def __str__(self):
        """Override string method"""
        out = '['
        for b in self.bases: out += str(b)
        return out + ']'
        
    def __repr__(self):
        return str(self)
        
    def __len__(self):
        return len(self.bases)
        
    def split(self, ind):
        """Split the DNA into two single strands (with blunt ends) before the
           given ind.  0 <= ind <= size(self)
           int -> List<Single_strand>"""
        fragments = []
        fragments.append(Single_strand(self.bases[0:ind]))
        fragments.append(Single_strand(self.bases[ind:len(self)]))
        return fragments
    
    def reverse_strand(self):
        """Reverse the strand into 3' -> 5' order (for annealing purposes)
           -> Single_strand"""
        new_bases = self.bases[::-1]
        return Single_strand(new_bases)
    
    def is_complementary(self, ss):
        """Do all of the bases on the strands pair?
           Single_strand -> Boolean"""
        # TODO : Some way to handle if they match with an offset
        if len(self.bases) == 0 and len(ss.bases) == 0:
            return True
        elif len(self.bases) != len(ss.bases):
            return False
        else:
            pairs = zip(self.bases, ss.reverse_strand().bases)
            return andmap(lambda p: p[0].is_complementary(p[1]), pairs)
            
    def is_palindromic(self):
        """Is the sequence palindromic? (second half self-complimentary)
        -> Boolean"""
        paired = Double_strand(self)
        match_strands = paired.anneal()
        return match_strands[0] == match_strands[1]
    
    def remove_empties(self):
        """Remove empty bases from the strand
           -> SingleStrand"""
        return Single_strand(filter(lambda b: not b.is_empty(), self.bases))
    
    def ligate(self, ss):
        """Append the two single strands, including getting rid of empties
           Adds ss to the 3' end of self
           Single_strand -> Single_strand"""
        self_clean_bases = self.remove_empties().bases
        ss_clean_bases = ss.remove_empties().bases
        self_clean_bases.extend(ss_clean_bases)
        return Single_strand(self_clean_bases)
        
    def restrict(self, enzyme):
        """Cut the strand into pieces if it has the recog_site
           Restriction_enzyme -> Single_strand or List<DNAmol>"""
        recog_ind = find_sub_list(enzyme.recog_site, self.bases)
        print self
        print type(recog_ind)
        if not recog_ind is False:
            temp_segments = self.split(recog_ind + enzyme.cut_site)
            print temp_segments
            all_segments = [temp_segments[0]]
            other_segments = temp_segments[1].restrict(enzyme)
            all_segments.extend(other_segments)
            return all_segments
        else:
            return [self]
        
class Double_strand(object):
    """Represents a double-stranded DNA molecule with a list of tuples"""
    
    def __init__(self, strand1, strand2 = None):
        """Create a double strand of DNA from a string or list
           String OR Single_strand OR List<Nucleotide> -> Double_strand"""
        if isinstance(strand1, list) and \
            len(filter(lambda b: not isinstance(b, tuple), strand1))==0:
            self.base_pairs = strand1
        else:
            strand1 = process_strand(strand1)
            if strand2 is None:
                strand2 = map(lambda b: b.pair(), strand1)
                strand2.reverse()
            else:
                strand2 = process_strand(strand2)
            if Single_strand(strand1).is_complementary(Single_strand(strand2)):
                strand2.reverse()
                base_pairs = zip(strand1, strand2)
                self.base_pairs = base_pairs
            else:
                raise ValueError("Input strands are not complementary")
        
    def __eq__(self, other):
        """Override equals method"""
        if isinstance(other, Double_strand):
            return self.base_pairs == other.base_pairs
        else:
            return False
    
    def __str__(self):
        """Override the string method"""
        out = '['
        for b in self.base_pairs:
            out = out + str(b[0]) + str(b[1]) + " "
        return out[0:-1] + ']'
        
    def __repr__(self):
        return str(self)
        
    def __len__(self):
        return len(self.base_pairs)
    
    @staticmethod
    def random_dna(n):
        """Generate a string of n random base pairs of DNA.
           No empty bases, blunt ends"""
        bases = ['a','c','t','g']
        rand_inds = [random.randint(0,len(bases)-1) for _ in range(n)]
        rand_bases = map(lambda i: bases[i], rand_inds)
        str_bases = "".join(rand_bases)
        return Double_strand(str_bases)
    
    def split(self, ind):
        """Split the DNA into two double strands (with blunt ends) before the
           given ind.  0 <= ind <= size(self)
           int -> List<DoubleStrand>"""
        fragments = []
        fragments.append(Double_strand(self.base_pairs[0:ind]))
        fragments.append(Double_strand(self.base_pairs[ind:len(self)]))
        return fragments
    
    def strand53(self):
        """Get the 5'->3' strand out of the double strand
           -> Single_strand"""
        strands = zip(*self.base_pairs);
        if len(strands) == 0: strands = [[],[]]
        new_strand = list(strands[0])
        return Single_strand(new_strand)
        
    def strand35(self):
        """Get the 3'->5' strand out of the double strand
           Reverses it so that it ends up in the 5'->3' direction
           -> Single_strand"""
        strands = zip(*self.base_pairs)
        if len(strands) == 0: strands = [[],[]]
        new_strand = list(strands[1])
        return Single_strand(new_strand).reverse_strand()
        
    def anneal(self):
        """Split the Double_strand into 2 Single_strands
           List : [5'->3' strand, 3' ->5' strand] (but both in 5'->3' order)
           -> Genome"""
        return [self.strand53(), self.strand35()]
        
    def rotate(self):
        """Rotate the Double_strand 180 deg (still 5'->3' but change which
           strand is on top
           -> Double_strand"""
        new_strands = self.anneal()
        return Double_strand(new_strands[1], new_strands[0])
        
    def overhang_5(self):
        """Return list of the overhang at the start of the double strand (5'
           end of leading strand) and paired portion
           -> List<Double_strand>"""
        nonempty_inds = [i for i, b in enumerate(self.base_pairs) if \
            (not b[0].is_empty() and not b[1].is_empty())]
        if len(nonempty_inds) == 0:
            split_ind = len(self)
        else:
            split_ind = nonempty_inds[0]
        split_strands = self.split(split_ind)
        return split_strands
    
    def overhang_3(self):
        """Return list of the paired portion and the overhang at the end of 
           the double strand (3' end of the leading strand, in 5'->3' direction)
           -> DoubleStrand"""
        nonempty_inds = [i for i, b in enumerate(self.base_pairs) if \
            (not b[0].is_empty() and not b[1].is_empty())]
        if len(nonempty_inds) == 0:
            split_ind = 0
        else:
            split_ind = nonempty_inds[-1] + 1
        split_strands = self.split(split_ind)
        return split_strands
        
        tail = []
        bases = self.base_pairs[::-1]
        i = 0;
        while i < len(bases) and \
            (bases[i][0].is_empty() or bases[i][1].is_empty()):
            tail.append(bases[i])
            i += 1
        tail.reverse()
        if len(tail) == 0:
            tail_strands = [[],[]]
        else:
            tail_strands = map(lambda s: list(s), zip(*tail))
        return Double_strand(tail_strands[0], tail_strands[1])
        
    def ligate(self, ds):
        """Turn 2 fragments into 1, if ends match, or return false
           Assumes both strands are in the 5'->3' direction
           Currently set up so to only ligate ds to end of self (no rotation)
           (There are 3 other combinations)
           Double_strand -> Double_strand OR false"""
        # Get overhang_3 of self
        self_overhang_3 = self.overhang_3()
        self_body = self_overhang_3[0]
        self_tail3 = self_overhang_3[1]
        # Get overhang_5 of ds
        ds_overhang_5 = ds.overhang_5()
        ds_tail5 = ds_overhang_5[0]
        ds_body = ds_overhang_5[1]
        # Anneal and ligate ds_tail to end of self_tail
        self_tail3 = self_tail3.anneal()
        ds_tail5 = ds_tail5.anneal()
        overlap_53 = self_tail3[0].ligate(ds_tail5[0])
        overlap_35 = self_tail3[1].ligate(ds_tail5[1])
        # Remove empties
        overlap_53 = overlap_53.remove_empties()
        overlap_35 = overlap_35.remove_empties()
        # Check if 2 strands are complementary
        if overlap_53.is_complementary(overlap_35):
            # Combine if they are (into DS)
            overlap = Double_strand(overlap_53, overlap_35)
            # stick together all 3 pieces
            new_body = []
            new_body.extend(self_body.base_pairs)
            new_body.extend(overlap.base_pairs)
            new_body.extend(ds_body.base_pairs)
            return Double_strand(new_body)
        else:
            return False
    
    def restrict(self, enzyme):
        """Cut the double stranded DNA at all restriction sites and produce a
           list of the fragments (may have sticky ends)
           Restriction_enzyme -> List<Double_strand>"""
        # Find restriction site on leading strand
        # Figure out range that needs to be considered 
            
    def draw_ladder(self):
        """Draw an ASCII art DNA ladder"""
        print ""
        for pair in self.base_pairs:
            if pair[0].is_empty():
                rungL = "   "
                ladderL = " "
            else:
                rungL = str(pair[0]) + "--"
                ladderL = "|"
            if pair[1].is_empty():
                rungR = "   "
                ladderR = " "
            else:
                rungR = "--" + str(pair[1])
                ladderR = "|"
            print "\t" + ladderL + "    " + ladderR
            print "\t" + rungL + rungR
        print "\t" + ladderL + "    " + ladderR
            

#Double_strand.random_dna(10000).draw_ladder()

