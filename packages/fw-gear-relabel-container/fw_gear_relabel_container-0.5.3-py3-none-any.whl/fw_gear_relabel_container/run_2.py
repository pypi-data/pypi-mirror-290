"""Second run of gear with inputs and doing renaming"""

import logging
import re

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def make_file_name_safe(input_basename, regex, replace_str=""):
    """Remove non-safe characters from a filename and return a filename with
        these characters replaced with replace_str.

    :param input_basename: the input basename of the file to be replaced
    :type input_basename: str
    :param replace_str: the string with which to replace the unsafe characters
    :type   replace_str: str
    :param regex: The regex to substitute against
    :type   regex: compiled regex object, ex. re.compile('[A-Z]')
    :return: output_basename, a safe
    :rtype: str
    """

    # Replace non-alphanumeric (or underscore) characters with replace_str
    safe_output_basename = re.sub(regex, replace_str, input_basename)

    if safe_output_basename.startswith("."):
        safe_output_basename = safe_output_basename[1:]

    log.debug('"' + input_basename + '" -> "' + safe_output_basename + '"')

    return safe_output_basename


def handle_acquisitions(acq_df, fw, run_level, hierarchy, dry_run=False):
    """Change acquisition labels for each new label provided.

    Args:
        acq_df (pd.DataFrame): dataframe of acquisitions
        fw (flywheel.Client): A flywheel client
        run_level (str): the level at which the gear is running: 'project' or 'subject'
        hierarchy (dict): ids for the group, project, subject, session, and acquisition
        dry_run (bool, optional): If True, do not make any changes just show what would have been. Defaults to False.
    """
    base_find = f"parents.{run_level}={hierarchy[run_level]}"
    # Acquisitions
    for index, row in acq_df.iterrows():
        # Since len(rows) != len(project.acquisitions), need to find all acquisitions
        #   in the project for each row in the acquisition dataframe.
        # That is, multiple acquisitions may have the same label.  All need to be changed.
        # If names are numeric, the value has to be wrapped in double quotes

        find_string = f"{base_find},label=\"{row['acquisition.label']}\""
        acquisitions_for_row = fw.acquisitions.iter_find(find_string)

        for acquisition in acquisitions_for_row:
            if row.get(
                "new acquisition.label"
            ):  # then a new acquisition label was provided
                new_acq_name = row["new acquisition.label"]
            else:
                new_acq_name = row["acquisition.label"]
            # Warn for bad labels
            if (
                make_file_name_safe(row["new acquisition.label"], "")
                != row["new acquisition.label"]
            ):
                log.warning(
                    f"New acquisition label f{row['new acquisition.label']} may not be BIDS compliant"
                )

            if new_acq_name == row["acquisition.label"]:
                log.info(
                    f"Acquisition {row['acquisition.label']} did not change, not updating"
                )

            else:
                if dry_run:
                    log.info(
                        f"Dry Run: NOT updating acquisition label from {acquisition.label} to {new_acq_name}"
                    )
                else:
                    log.info(
                        f"updating acquisition label from {acquisition.label} to {new_acq_name}"
                    )
                    acquisition.update({"label": new_acq_name})


def handle_sessions(ses_df, fw, run_level, hierarchy, dry_run=False):
    """Change session labels for each new label provided.

    Args:
        ses_df (pd.DataFrame): dataframe of sessions
        fw (flywheel.Client): A flywheel client
        run_level (str): the level at which the gear is running: 'project' or 'subject'
        hierarchy (dict): ids for the group, project, subject, session, and acquisition
        dry_run (bool, optional): If True, do not make any changes just show what would have been. Defaults to False.
    """

    base_find = f"parents.{run_level}={hierarchy[run_level]}"

    for index, row in ses_df.iterrows():
        find_string = f"{base_find},label=\"{row['session.label']}\""
        sessions_for_row = fw.sessions.iter_find(find_string)
        for session in sessions_for_row:
            if row.get("new session.label"):  # then a new session label was provided
                new_ses_name = row["new session.label"]
            else:
                new_ses_name = row["session.label"]

            # Warn for bad labels
            if row["new session.label"] != make_file_name_safe(
                row["new session.label"], ""
            ):
                log.warning(
                    f"New session label f{row['new session.label']} may not be BIDS compliant"
                )

            if row["session.label"] == new_ses_name:
                log.info(f"Session {row['session.label']} did not change, not updating")
            else:
                if dry_run:
                    log.info(
                        f"Dry Run: NOT updating session label from {session.label} to {new_ses_name}"
                    )
                else:
                    log.info(
                        f"updating session label from {session.label} to {new_ses_name}"
                    )
                    session.update({"label": new_ses_name})


def handle_subjects(subj_df, fw, run_level, hierarchy, dry_run=False):
    """Change subject labels for each new label provided.

    Args:
        subj_df (pd.DataFrame): dataframe of subjects
        fw (flywheel.Client): A flywheel client
        run_level (str): the level at which the gear is running: 'project' or 'subject'
        hierarchy (dict): ids for the group, project, subject, session, and acquisition
        dry_run (bool, optional): If True, do not make any changes just show what would have been. Defaults to False.
    """

    if run_level == "subject":
        log.info("Running at subject level, not adjusting subjects.")
        return

    base_find = f"parents.{run_level}={hierarchy[run_level]}"
    for index, row in subj_df.iterrows():
        find_string = f"{base_find},label=\"{row['subject.label']}\""
        subjects_for_row = fw.subjects.iter_find(find_string)
        for subject in subjects_for_row:
            if row.get("new subject.label"):
                new_subj_name = row["new subject.label"]
            else:
                new_subj_name = row["subject.label"]

            # Warn for bad labels
            if row["new subject.label"] != make_file_name_safe(
                row["new subject.label"], ""
            ):
                log.warning(
                    f"New subject label f{row['new subject.label']} may not be BIDS compliant"
                )

            if row["subject.label"] == new_subj_name:
                log.info(f"Subject {row['subject.label']} did not change, not updating")
            else:
                if dry_run:
                    log.info(
                        f"Dry Run: NOT updating subject {subject.label} with new label, code of {new_subj_name}"
                    )
                else:
                    log.info(
                        f"updating new subject {subject.label} with new label, code of {new_subj_name}"
                    )
                    subject.update({"label": new_subj_name, "code": new_subj_name})


def run_second_stage_with_inputs(
    client, run_level, hierarchy, acq_df, ses_df, sub_df, dry_run
):
    """Since input csv files were provided, update labels where new ones were given.

    Args:
        client (flywheel.Client): A flywheel client
        run_level (str): the level at which the gear is running: 'project' or 'subject'
        hierarchy (dict): ids for the group, project, subject, session, and acquisition
        acq_df (pd.DataFrame): dataframe of acquisitions
        ses_df (pd.DataFrame): dataframe of sessions
        sub_df (pd.DataFrame): dataframe of subjects
        dry_run (bool): If True, do not make any changes just show what would have been.

    Returns:
        int: 0 if all is well, 1 if there is an error
    """

    # Clear df's, if no new labels have been provided
    num_empty_dfs = 0
    for df in [acq_df, ses_df, sub_df]:
        if isinstance(df, pd.DataFrame):
            col_new_name = [col for col in df.columns if col.startswith("new ")][0]
            df.replace("", np.nan, inplace=True)
            df.dropna(subset=col_new_name, inplace=True)
            if df.empty:
                log.info(f"No new labels provided for {df.columns[0]}")
                num_empty_dfs += 1
        else:  # it is not a dataframe (probably None) so count it as empty
            num_empty_dfs += 1

    if num_empty_dfs == 3:
        log.warning(
            "No new labels provided for acquisitions, sessions or subjects, exiting"
        )
        return 1

    if isinstance(acq_df, pd.DataFrame) and not acq_df.empty:
        handle_acquisitions(acq_df, client, run_level, hierarchy, dry_run)

    if isinstance(ses_df, pd.DataFrame) and not ses_df.empty:
        handle_sessions(ses_df, client, run_level, hierarchy, dry_run)

    if isinstance(sub_df, pd.DataFrame) and not sub_df.empty:
        handle_subjects(sub_df, client, run_level, hierarchy, dry_run)

    return 0  # all is well
