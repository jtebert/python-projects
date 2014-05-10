from abc import ABCMeta, abstractmethod
import operator
import unittest

def andmap(b,L):
    return reduce(operator.and_, [b(x) for x in L])

def ormap(b,L):
    return reduce(operator.or_, [b(x) for x in L])

# TODO : Define a DNAmol, Genome
# TODO : Allow non-complementary double strand creation (perhaps with warning?)
# TODO : Ligation with different rotations

class Restriction_enzyme(object):
    """Abstract class representing DNA restriction enzymes"""
    __metaclass__ = ABCMeta
    
    def __eq__(self, other):
        """Override equals method"""
        if isinstance(other, Restriction_enzyme):
            return self.rec_site == other.rec_site and \
                 self.cut_site == other.cut_site
        else:
            return False
    
    @property
    def rec_site(self):
        """The DNA sequence requised to cut (5' -> 3' direction)
           Must be palindromic (pair with itself on the other strand
           List<Nucleotide>"""
        raise NotImplementedError("Need to implement rec_site field")
    
    @property
    def cut_site(self):
        """The part of rec_site from the beginning to the location to cut
           List<Nucleotide>"""
        raise NotImplementedError("Need to implement cut_site field")
        
    @abstractmethod
    def foo(self):
        """Dummy example method"""
        raise NotImplementedError("Need to implement foo method")

class Nucleotide:
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
        ValueError("Invalid input to create DNA molecule: " + str(type(strand))) 
        
class Single_strand:
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
        return self.bases.__str__()
    
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
        """Cut the strand into pieces if it has the rec_site
           Restriction_enzyme -> Single_strand or List<DNAmol>"""
        # TODO : Write this
        
class Double_strand:
    """Represents a double-stranded DNA molecule with a list of tuples"""
    
    def __init__(self, strand1, strand2 = None):
        """Create a double strand of DNA from a string or list
           String OR Single_strand OR List<Nucleotide> -> Double_strand"""
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
        return self.base_pairs.__str__()
        
    def strand53(self):
        """Get the 5'->3' strand out of the double strand
           -> Single_strand"""
        strands = zip(*self.base_pairs);
        new_strand = list(strands[0])
        return Single_strand(new_strand)
        
    def strand35(self):
        """Get the 3'->5' strand out of the double strand
           Reverses it so that it ends up in the 5'->3' direction
           -> Single_strand"""
        strands = zip(*self.base_pairs);
        new_strand = list(strands[1])
        return Single_strand(new_strand).reverse_strand()
        
    def anneal(self):
        """Split the Double_strand into 2 Single_strands
           List : [5'->3' strand, 3' ->5' strand] (but both in 5'->3' order)
           -> Genome"""
        return [self.strand53(), self.strand35()]
        
    def flip(self):
        """Rotate the Double_strand 180 deg (still 5'->3' but change which
           strand is on top
           -> Double_strand"""
        new_strands = self.anneal()
        return Double_strand(new_strands[1], new_strands[0])
        
    def overhang_3(self):
        """Return the 3' overhang at the end of the double strand
           -> Single_strand"""
       # TODO : I don't know what the goal of this even is anymore. Which end?
        
    def ligate(self, ds):
        """Turn 2 fragments into 1, if ends match, or return false
           Assumes both strands are in the 5'->3' direction
           Currently set up so to only ligate ds to end of self (no flipping)
           (There are 3 other combinations)
           Double_strand -> Double_strand OR false"""
        # TODO : Allow non-complementary (letters but not connecting)
        # Might be good to make use of appending single strands and checking if complementary
        # Try combining at both ends
        split_self = self.anneal()
        split_ds = ds.anneal()
        new53 = split_self[0].ligate(split_ds[0])
        #print "53: " + str(new53)
        new35 = split_ds[1].ligate(split_self[1])
        #print "35: " + str(new35)
        if new53.is_complementary(new35):
            # create new double strand
            return Double_strand(new53, new35)
        else:
            return False
            
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
            



