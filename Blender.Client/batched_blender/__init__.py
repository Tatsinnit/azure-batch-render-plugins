﻿
bl_info = {
    "name": "BatchLabs Blender Plugin",
    "author": "Microsoft Corporation <bigcompute@microsoft.com>",
    "version": (0, 1, 0),
    "blender": (2, 7, 9),
    "location": "Render Properties",
    "description": "Render your Blender scene externally with Azure Batch and BatchLabs.",
    "category": "Render"
}

import importlib
import os
import bpy

_APP_DIR = os.path.dirname(__file__)

from batched_blender.props.props_shared import BatchPreferences
from batched_blender.shared import BatchSettings
from batched_blender.draw import *

@bpy.app.handlers.persistent
def start_session(self):
    """
    Instantiate the Batch Apps session and register all the property
    classes to the Blender context.
    This is handled in an event to allow it to run under the full
    Blender context rather than the limited loading scope.

    Once the session has started (or reported an error), this function
    is removed from the event handlers.
    """
    try:
        session = BatchSettings()

        def get_session(self):
            return session

        bpy.types.Scene.batch_session = property(get_session)

    except Exception as e:
        print("Batch Addon failed to load.")
        print("Error: {0}".format(e))
        bpy.types.Scene.batch_error = e

    finally:
        bpy.app.handlers.scene_update_post.remove(start_session)


def register():
    """
    Register module and applicable classes.
    This method also sets some Batch globals. In particular, the
    python module Requests that is packaged with blender does not allow
    for certificates to be verified, so we have to either turn this off,
    or replace the included Requests module (recommended).

    Here we also register the User Preferences for the Addon, so it can
    be configured in the Blender User Preferences window.
    """
    bpy.app.handlers.scene_update_post.append(start_session)
    bpy.utils.register_class(BatchPreferences)
    bpy.utils.register_module(__name__)


def unregister():
    """
    Unregister the addon if deselected from the User Preferences window.
    """
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
