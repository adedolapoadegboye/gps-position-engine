from utils import SPEED_OF_LIGHT

def format_pseudorange(pr_dict):
    """
    Formats raw pseudorange data and computes pseudorange for each satellite.

    The DF394 field is a bitmask in MSB-first order, where the leftmost bit represents SVID 1,
    the next bit SVID 2, etc. The DF397, DF398, and DF400 fields are provided in the order of
    the set bits in DF394. For instance, if DF394 converted to a bit string is:
        101001011010000110010000100000000000
    then the first set bit (bit 1) corresponds to SVID 1, the second set bit (bit 3) to SVID 3,
    the third set bit (say SVID 6) to the next index, and so forth.

    Args:
        pr_dict (dict): Dictionary containing raw MSM4 pseudorange data keyed by DF fields.

    Returns:
        dict: Formatted pseudorange data with computed values keyed by the actual SVID.
    """
    formatted_pr = {}

    # Retrieve DF394 bitmask from the dictionary.
    svid_bitmask = pr_dict.get('DF394', 0)
    # Convert the bitmask to a binary string. This string is MSB-first:
    bitstring = bin(svid_bitmask)[2:]
    # If needed, pad the bitstring to a fixed length (e.g., 64 bits) with leading zeros:
    bitstring = bitstring.zfill(64)

    # Build the list of SVIDs by iterating over the bitstring from left (MSB) to right.
    svid_list = []
    for i, bit in enumerate(bitstring, start=1):
        if bit == '1':
            svid_list.append(i)

    # The pseudorange fields (DF397, DF398, DF400) are indexed by the order
    # in which satellites appear in the bitmask.
    for idx, svid in enumerate(svid_list, start=1):
        index_str = f"{idx:02d}"  # zero-padded index: '01', '02', etc.
        nms_key = f"DF397_{index_str}"
        rough_range_key = f"DF398_{index_str}"
        # fine_range_key = f"DF400_{index_str}" # Removing fine ranges to reduce complexity

        nms = pr_dict.get(nms_key)
        rough_range = pr_dict.get(rough_range_key)
        # fine_range = pr_dict.get(fine_range_key)

        #if nms is not None and rough_range is not None and fine_range is not None:
        if nms is not None and rough_range is not None:
            pseudorange = (SPEED_OF_LIGHT / 1000) * (
                nms + (rough_range / 1024)
            )
            #pseudorange = (SPEED_OF_LIGHT / 1000) * (
            #    nms + (rough_range / 1024) + ((2 ** -24) * fine_range)
            #)
            formatted_pr[svid] = pseudorange

    return formatted_pr
