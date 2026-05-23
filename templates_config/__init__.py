from .rob2_pt import ROB2
from .robins_i_pt import ROBINS_I
from .robins_e_pt import ROBINS_E
from .nos_cohort_pt import NOS_COHORT
from .nos_case_control_pt import NOS_CASE_CONTROL
from .nos_cross_sectional_pt import NOS_CROSS_SECTIONAL
from .downs_black_pt import DOWNS_BLACK
from .jbi_case_report_pt import JBI_CASE_REPORT
from .jbi_case_series_pt import JBI_CASE_SERIES
from .jbi_cross_sectional_pt import JBI_CROSS_SECTIONAL

INSTRUMENTS = {
    "rob2": ROB2,
    "robins-i": ROBINS_I,
    "robins-e": ROBINS_E,
    "nos-cohort": NOS_COHORT,
    "nos-cc": NOS_CASE_CONTROL,
    "nos-xs": NOS_CROSS_SECTIONAL,
    "db": DOWNS_BLACK,
    "jbi-cr": JBI_CASE_REPORT,
    "jbi-cs": JBI_CASE_SERIES,
    "jbi-xs": JBI_CROSS_SECTIONAL
}
