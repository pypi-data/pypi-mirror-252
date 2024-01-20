"""Complete Blood Count Metrics."""


def mcv(hct: float, rbc: float) -> float:
    """Calculate Mean Corpuscular Volume (MCV).

    :param hct: Hematocrit as a decimal (e.g., 0.425 = 42.5%).
    :param rbc: Red Blood Cell count (cells per microliter, /µL).
    :return: MCV in femtoliters (fL).
    """
    return hct * 10e8 / rbc


def mch(hb: float, rbc: float) -> float:
    """Calculate Mean Corpuscular Hemoglobin (MCH).

    :param hb: Hemoglobin level (in grams per deciliter, g/dL).
    :param rbc: Red Blood Cell count (cells per microliter, /µL).
    :return: MCH in picograms (pg).
    """
    return hb * 10e6 / rbc


def mchc(hb: float, hct: float) -> float:
    """Calculate Mean Corpuscular Hemoglobin Concentration (MCHC).

    :param hb: Hemoglobin level (in grams per deciliter, g/dL).
    :param hct: Hematocrit as a decimal (e.g., 0.425 = 42.5%).
    :return: MCHC in grams per deciliter (g/dL).
    """
    return hb / hct


def nlr(absolute_anc: float, absolute_alc: float) -> float:
    """Calculate Neutrophil to Lymphocyte Ratio (NLR).

    :param absolute_anc: Absolute Neutrophil Count (cells per microliter, /µL).
    :param absolute_alc: Absolute Lymphocyte Count (cells per microliter, /µL).
    :return: NLR (dimensionless).
    """
    return absolute_anc / absolute_alc


def anc(wbc: float, nphi: float, bands: float) -> float:
    """Calculate Absolute Neutrophil Count (ANC).

    :param wbc: White Blood Cell count (cells per microliter, /µL).
    :param nphi: Proportion of mature neutrophils as a decimal.
    :param bands: Proportion of immature neutrophile as a decimal.
    :return: ANC (cells per microliter, /µL).
    """
    return (nphi + bands) * wbc


def alc(wbc: float, lym: float) -> float:
    """Calculate Absolute Lymphocyte Count (ALC).

    :param wbc: White Blood Cell count (cells per microliter, /µL).
    :param lym: Proportion of lymphocytes in total WBC count as a decimal.
    :return: ALC (cells per microliter, /µL).
    """
    return wbc * lym
