"""First run of gear with no inputs, gathers labels for subjects, sessions, and acquisitions."""

import logging

import flywheel
import pandas as pd

log = logging.getLogger(__name__)


def get_container_labels(client, destination):
    """Get unique labels for all subjects, sessions, and acquisitions in the container.

    This is done using a single Data View which is more efficient than iterating through all acquisitions,
    sessions, and subjects. This prevents time-out errors in large projects.

    Args:
        client (flywheel.Client): A flywheel client.
        destination (flywheel.Analysis): Where results will be stored

    Returns:
        sub [dataframe]: unique subject labels
        ses [dataframe]: unique session labels
        acq [dataframe]: unique acquisition labels
    """

    dest_project_id = destination.parents["project"]
    dest_parent_id = destination.parent["id"]

    if destination.parent["type"] == "project":
        filter = None
    elif destination.parent["type"] == "subject":
        filter = f"subject.id={dest_parent_id}"

    builder = flywheel.ViewBuilder(
        label="relabel-container-acquisitions",
        columns=["acquisition.label"],
        container="acquisition",
        match="all",
        process_files=False,
        include_ids=False,
        sort=False,
        filter=filter,
    )

    sdk_dataview = builder.build()
    sdk_dataview.parent = dest_project_id
    labels_df = client.read_view_dataframe(sdk_dataview, dest_project_id)

    sub = pd.DataFrame(labels_df["subject.label"].unique(), columns=["subject.label"])
    ses = pd.DataFrame(labels_df["session.label"].unique(), columns=["session.label"])
    acq = pd.DataFrame(
        labels_df["acquisition.label"].unique(), columns=["acquisition.label"]
    )

    return sub, ses, acq


def save_csv_with_empty_column(df, new_col_label, output_dir, filename):
    """Save a dataframe to a csv file with an empty column for user input.

    Logs the file name and location.

    Args:
        df [dataframe]: the dataframe to be saved
        new_col_label [str]: the label for the new column
        output_dir [str]: the directory where the file will be saved
        filename [str]: the name of the file
    """

    df[new_col_label] = pd.Series("")
    output_file = f"{output_dir}/{filename}"
    df.to_csv(output_file, index=False)
    log.info(f"Saved {output_file}")


def run_first_stage_no_inputs(context, destination):
    """Run the first stage of the gear with no inputs.

    Args:
        context (flywheel_gear_toolkit.GearToolkitContext): The gear context
        destination (flywheel.Analysis): Where results will be stored

    This stage gathers labels for subjects, sessions, and acquisitions and saves them to csv files.

    Returns:
        0 [int]: if it gets this far, all is well

    """

    sub, ses, acq = get_container_labels(context.client, destination)

    save_csv_with_empty_column(
        sub, "new subject.label", context.output_dir, "subjects.csv"
    )
    save_csv_with_empty_column(
        ses, "new session.label", context.output_dir, "sessions.csv"
    )
    save_csv_with_empty_column(
        acq, "new acquisition.label", context.output_dir, "acquisitions.csv"
    )

    return 0  # all is well
