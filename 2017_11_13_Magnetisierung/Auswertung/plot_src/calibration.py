"""
Functions to return the magnetic field/ magnetization of a sample
as a function of the SQUID voltage.
"""

U_BASE_ONLY = 0.456


# TODO: propbably wrong
def magnetic_field(squid_voltage, orientation='perpendicular'):
    """
    Return the magnetic field (unit: Gauss) at the SQUID as a function
    of the SQUID voltage (unit: Volt).
    """
    if orientation not in ('perpendicular', 'parallel'):
        raise Exception('No valid orientation')

    if orientation == 'parallel':
        return 0.802 * (squid_voltage - U_BASE_ONLY)

    return 0.783 * (squid_voltage - U_BASE_ONLY)
    # return 2.28 * (squid_voltage - U_0)


# TODO: propbably wrong
def magnetization(squid_voltage, orientation='perpendicular'):
    """
    Return the magnetization (unit: Ampere/Meter) at the SQUID as a
    function of the SQUID voltage (unit: Volt).
    """
    if orientation not in ('perpendicular', 'parallel'):
        raise Exception('No valid orientation')

    if orientation == 'parallel':
        return 487346.93877551 * squid_voltage

    return 476171.48554337 * squid_voltage
