"""Parser module to parse gear config.json."""

import logging
import pandas as pd

from flywheel_gear_toolkit import GearToolkitContext
from pandas import DataFrame

log = logging.getLogger(__name__)


def load_inputs(
    gear_context: GearToolkitContext,
) -> tuple[bool, DataFrame | None, DataFrame | None, DataFrame | None]:
    """Read provided input csv files and return dataframes.

    The user provides new labels for subjects, sessions, and acquisitions in the input csv files.
    Not all input csv files are required. If any are missing, the corresponding dataframe will be None.

    Returns:
         inputs_provided [bool]: true if any input csv file is provided
         acq_df  [dataframe]: acquisition spreadsheet
         ses_df  [dataframe]: session spreadsheet
         sub_df [dataframe]: subject spreadsheet
    """
    acq = gear_context.get_input_path("acquisitions")
    ses = gear_context.get_input_path("sessions")
    sub = gear_context.get_input_path("subjects")

    if acq or ses or sub:
        if acq:
            acq_df = pd.read_csv(acq)
            log.info(f"Loaded {acq}")
        else:
            acq_df = None
            log.info("Acquisition spreadsheet not provided")
        if ses:
            ses_df = pd.read_csv(ses)
            log.info(f"Loaded {ses}")
        else:
            ses_df = None
            log.info("Session spreadsheet not provided")
        if sub:
            sub_df = pd.read_csv(sub)
            log.info(f"Loaded {sub}")
        else:
            sub_df = None
            log.info("Subject spreadsheet not provided")
        inputs_provided = True

    else:
        acq_df = None
        ses_df = None
        sub_df = None
        inputs_provided = False

    return inputs_provided, acq_df, ses_df, sub_df
