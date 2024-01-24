"""
Presubmission script to export vrscene files.

To write your own presubmission script, use this as a jumping off point and
consult the Conductor Max reference documentation.
https://docs.conductortech.com/reference/max/#pre-submission-script
"""

import os

from ciopath.gpath_list import PathList
from ciopath.gpath import Path
from pymxs import runtime as rt
from ciomax.scripts import export_utils

from contextlib import contextmanager


@contextmanager
def maintain_save_state():
    required = rt.getSaveRequired()
    yield
    rt.setSaveRequired(required)


@contextmanager
def preserve_state():
    """
    Remember and reset all the properties we change.
    """
    rend_time_type = rt.rendTimeType
    rend_pickup_frames = rt.rendPickupFrames
    rend_nth_frame = rt.rendNThFrame
    try:
        yield
    finally:
        rt.rendTimeType = rend_time_type
        rt.rendPickupFrames = rend_pickup_frames
        rt.rendNThFrame = rend_nth_frame


def main(dialog, *args):
    """
    Export assets needed for a vray render.

    Return an object containing the list of generated assets.
    """
    prefix = args[0]

    vray_scene = export_vrscene(dialog, prefix)
    amendment_paths = [vray_scene]

    for new_file in amendment_paths:
        found = export_utils.wait_for_file(new_file)
        if not found:
            raise ValueError(f"File not found: {new_file}")
        else:
            print(f"File found: {new_file}")

    # amendments() function isn't used as it's a guess.
    # We need the real vray_scene filename for the submission.
    return {"upload_paths": amendment_paths, "environment": amendments_env(dialog)}


def amendments(dialog, *args):
    """
    Return payload amendments only.

    Payload amendments consist of a vrscene filename(s), and asset search paths. Scene filename is a guess andis here only to indicate presence in the pteview tab. 
    """
    prefix = os.path.splitext(args[0])[0]

    vray_scene = "{}.vrscene".format(prefix)  # Guess

    return {"upload_paths": [vray_scene], "environment": amendments_env(dialog)}


def amendments_env(dialog):
    """
    Return env amendments.

    Result consist of a list of search paths.
    """
    result = []
    assets_list = dialog.configuration_tab.section(
        "ExtraAssetsSection"
    ).collect_assets()
    seen = set()
    for asset in assets_list:
        seen.add(os.path.dirname(asset.fslash(with_drive=False)))
    for directory in seen:
        result.append(
            {"name": "VRAY_ASSETS_PATH", "value": directory, "merge_policy": "append"}
        )
    return result


def export_vrscene(dialog, vrscene_prefix):
    render_scope = dialog.render_scope
    valid_renderers = ["VrayGPURenderScope", "VraySWRenderScope"]

    if not render_scope.__class__.__name__ in valid_renderers:
        raise TypeError(
            "If you want to export Vray files, please set the current renderer to one of: {}".format(
                valid_renderers
            )
        )

    main_sequence = dialog.configuration_tab.section("FramesSection").main_sequence

    camera_name = dialog.configuration_tab.section(
        "GeneralSection"
    ).camera_component.combobox.currentText()
    print("Set the current view to look through camera: {}", format(camera_name))

    rt.viewport.setCamera(rt.getNodeByName(camera_name))

    print("Ensure directory is available for vrscene_file")
    _ensure_directory_for(vrscene_prefix)

    print("Closing render setup window if open...")
    if rt.renderSceneDialog.isOpen():
        rt.renderSceneDialog.close()

    with preserve_state():
        print("Setting render time type to use a specified sequence...")
        rt.rendTimeType = 4

        print("Setting the frame range...")
        rt.rendPickupFrames = "{}-{}".format(main_sequence.start, main_sequence.end)

        print("Setting the by frame to 1...")
        rt.rendNThFrame = 1

        print("Exporting vrscene files")
        error = 0

        # If incrBaseFrame is introduced here, more complex logic will be needed to determine
        # the file names. incrBaseFrame will output one vrayscene file per frame.
        vray_scene = "{}.vrscene".format(vrscene_prefix)

        with maintain_save_state():
            error = rt.vrayExportRTScene(
                vray_scene, startFrame=main_sequence.start, endFrame=main_sequence.end
            )

        # It's possible the vray scene was exported without the extension
        if not os.path.exists(vray_scene):
            raise ValueError(
                "Vray scene export failed. Unnable to find {}. Check %temp%/vraylog.txt".format(
                    vray_scene
                )
            )

        if error:
            print(
                "Scene was exported, but there were errors during export. Check %temp%/vraylog.txt"
            )

        # return list of extra dependencies
        print("Completed vrscene export..")

    return vray_scene

def _ensure_directory_for(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
