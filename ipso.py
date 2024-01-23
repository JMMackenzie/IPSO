"""
A simple codebase for computing Innate Pairwise SERP Ordering (IPSO).

"""
from enum import Enum

class IPSOType(Enum):
    """
    Enumeration to handle the four IPSO cases.
    """
    EQUAL = 1
    """ The SERPS are equal """

    LESSER = 2,
    """ SERP A <= SERP B """

    GREATER = 3,
    """ SERP A >= SERP B """

    NONSEP = 4,
    """ SERP A <=?=> SERP B """

def pad_list_with_zeros(my_list, k):
    """
    Pad my_list to length k with zeros
    """
    return my_list[:k] + [0]*(k - len(my_list))

def ipso_compare(serp_a: list, serp_b: list, k: int) -> IPSOType:
    """
    Given two SERP lists, A and B, and a depth k, compute IPSO
    and return the given result.
    """

    # 1. Check the SERPs are of suitable length
    serp_a = pad_list_with_zeros(serp_a, k)
    serp_b = pad_list_with_zeros(serp_b, k)

    # 2. Prepare some variables
    accumulator = 0
    been_negative = False
    been_positive = False
    negative_first = True
    transition_1 = k
    transition_2 = k
    status = IPSOType.EQUAL

    # 3. Walk the SERPs
    for idx in range(k):
        # Accumulate the current judgment on each SERP
        accumulator += serp_a[idx]
        accumulator -= serp_b[idx]

        # Now checks and balances to see if we have disrupted order
        if accumulator < 0 and not been_negative:
            been_negative = True
            # Have we already had SERP_A > SERP_B?
            if not been_positive:
                # No, so this is the first transition point
                transition_1 = idx
                negative_first = True
            else:
                # Yes, this is the second transition point
                transition_2 = idx

        # Same for the positive side
        if accumulator > 0 and not been_positive:
            been_positive = True
            if not been_negative:
                transition_1 = idx
                negative_first = False
            else:
                transition_2 = idx

        # Compute the status of the two SERPs at this point
        if been_negative and been_positive:
            status = IPSOType.NONSEP
        elif been_negative:
            status = IPSOType.LESSER
        elif been_positive:
            status = IPSOType.GREATER
        else:
            status = IPSOType.EQUAL

    return status


"""
Example Usage: See Figure 4 in the paper.
"""

serp_a = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0]
serp_b = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]

for mk in range(1, 11):
    print ("Comparing A and B at k =", mk)
    print ("A =", serp_a[0:mk], ", B =", serp_b[0:mk])
    print(ipso_compare(serp_a, serp_b, mk))
    print ("---")
