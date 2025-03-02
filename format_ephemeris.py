def format_ephemeris(eph_dict):
    """
    Formats raw ephemeris data into a structured dictionary.

    Args:
        eph_dict (dict): Dictionary containing raw ephemeris data keyed by satellite PRN.

    Returns:
        dict: Formatted ephemeris data with labeled parameters.
    """
    formatted_eph = {}

    for sv, eph_ in eph_dict.items():
        formatted_eph[sv] = {
            'msgid': eph_.get('DF002', None),
            'svid': eph_.get('DF009', None),
            'GPSWeek': eph_.get('DF076', None),
            'GPSSVAcc': eph_.get('DF077', None),
            'GPSCodeL2': eph_.get('DF078', None),
            'idot': eph_.get('DF079', None),
            'iode': eph_.get('DF071', None),
            'toc': eph_.get('DF081', None),
            'af2': eph_.get('DF082', None),
            'af1': eph_.get('DF083', None),
            'af0': eph_.get('DF084', None),
            'iodc': eph_.get('DF085', None),
            'crs': eph_.get('DF086', None),
            'dn': eph_.get('DF087', None),
            'm0': eph_.get('DF088', None),
            'cuc': eph_.get('DF089', None),
            'e': eph_.get('DF090', None),
            'cus': eph_.get('DF091', None),
            'sqrtA': eph_.get('DF092', None),
            'toe': eph_.get('DF093', None),
            'cic': eph_.get('DF094', None),
            'omg0': eph_.get('DF095', None),
            'cis': eph_.get('DF096', None),
            'i0': eph_.get('DF097', None),
            'crc': eph_.get('DF098', None),
            'w': eph_.get('DF099', None),
            'omgdot': eph_.get('DF100', None),
            'tgd': eph_.get('DF101', None),
            'svhealth': eph_.get('DF102', None),
            'l2pdataflag': eph_.get('DF103', None),
            'fitinterval': eph_.get('DF137', None)
        }

    return formatted_eph
