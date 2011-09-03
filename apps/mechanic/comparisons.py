import re

from mechanic.literals import COMPARISON_ICONTAINS, COMPARISON_CONTAINS, \
    COMPARISON_EQUALS, COMPARISON_IEQUALS
    
    
def insensitive_string_compare(s1, s2):
    """ Method that takes two strings and returns True or False, based
        on if they are equal, regardless of case."""
    try:
        return s1.lower() == s2.lower()
    except AttributeError:
        print 'Please only pass strings into this method.'
        print 'You passed a %s and %s' % (s1.__class__, s2.__class__)


def comparison_contains(s1, s2, negated=False):
    if negated:
        return not re.search(s1, s2, 0)
    else:
        return re.search(s1, s2, 0)


def comparison_icontains(s1, s2, negated=False):
    if negated:
        return not re.search(s1, s2, re.I)
    else:
        return re.search(s1, s2, re.I)
               
                
def comparison_equals(s1, s2, negated=False):
    if negated:
        return not s1 == s2
    else:
        return s1 == s2
           
           
def comparison_iequals(s1, s2, negated=False):
    if negated:
        return not insensitive_string_compare(s1, s2)
    else:
        return insensitive_string_compare(s1, s2)
        

COMPARISON_FUNCTIONS = {
    COMPARISON_ICONTAINS: comparison_icontains,
    COMPARISON_CONTAINS: comparison_contains,
    COMPARISON_EQUALS: comparison_equals,
    COMPARISON_IEQUALS: comparison_iequals,
}
