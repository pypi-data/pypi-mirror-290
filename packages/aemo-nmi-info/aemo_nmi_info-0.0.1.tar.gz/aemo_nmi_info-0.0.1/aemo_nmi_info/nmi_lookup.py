
def nmi_lookup(nmi):
    # Define the NMI ranges and their corresponding state and participant ID
    nmi_ranges = [
        ('NGGG', '7001', 'ACT', 'ACTEWP'),
        ('NAAA', '4001', 'NSW', 'CNRGYP'),
        ('NBBB', '4508', 'NSW', 'CNRGYP'),
        ('NCCC', '4102', 'NSW', 'ENERGYAP'),
        ('NDDD', '4204', 'NSW', 'CNRGYP'),
        ('NEEE', '4310', 'NSW', 'INTEGP'),
        ('NFFF', '4407', 'NSW', 'CNRGYP'),
        ('NTTT', '4608', 'NSW', 'TRANSGP'),
        ('25', '25', 'NSW', 'PWCLNSP'),
        ('QAAA', '', 'QLD', 'ERGONETP'),
        ('QB', '31', 'QLD', 'ENERGEXP'),
        ('QCCC', '', 'QLD', 'ERGONETP'),
        ('QDDD', '', 'QLD', 'ERGONETP'),
        ('QEEE', '', 'QLD', 'ERGONETP'),
        ('QFFF', '', 'QLD', 'ERGONETP'),
        ('QGGG', '', 'QLD', 'ERGONETP'),
        ('30', '30', 'QLD', 'ERGONETP'),
        ('SAAA', '2001', 'SA', 'UMPLP'),
        ('SASM', '2001', 'SA', 'UMPLP'),
        ('T', '8000', 'TAS', 'AURORAP'),
        ('T', '8590', 'TAS', 'AURORAP'),
        ('VAAA', '6102', 'VIC', 'CITIPP'),
        ('VBBB', '6305', 'VIC', 'EASTERN'),
        ('VCCC', '6203', 'VIC', 'POWCP'),
        ('VDDD', '6001', 'VIC', 'SOLARISP'),
        ('VEEE', '6407', 'VIC', 'UNITED'),
        ('WAAA', '8001', 'WA', 'MISC'),
        ('80', '8021', 'WA', 'MISC'),
        ('52', '52', 'GAS', 'NSW Gas NMIs (& ACT)'),
        ('53', '53', 'GAS', 'Vic Gas NMIs'),
        ('54', '54', 'GAS', 'Qld Gas NMIs'),
        ('55', '55', 'GAS', 'SA Gas NMIs'),
        ('56', '56', 'GAS', 'WA Gas NMIs'),
        ('57', '57', 'GAS', 'Tas Gas NMIs'),
        ('NJJJ', '', 'NT', 'MISC'),
        ('NKKK', '7102', 'NT', 'MISC'),
        ('71', '7105', 'NT', 'MISC'),
        ('88', '8801', 'MISC', 'Embedded Network Managers - Child NMIs'),
        ('9', '9', 'MISC', 'AEMO Reserved block 2')
    ]

    # Check if the NMI is valid (10 or 11 characters long)
    if len(nmi) not in [10, 11]:
        return None, None

    # Try to match the NMI with the defined ranges
    for prefix, numeric_prefix, state, participant_id in nmi_ranges:
        if nmi.startswith(prefix):
            return state, participant_id
        elif numeric_prefix and nmi.startswith(numeric_prefix):
            return state, participant_id

    # If no match is found
    return None, None
