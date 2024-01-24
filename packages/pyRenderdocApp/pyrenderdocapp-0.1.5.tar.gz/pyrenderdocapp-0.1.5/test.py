#  Copyright (c) 2023-2024 Thomas Mathieson.
#  Distributed under the terms of the MIT license.

from pyRenderdocApp import load_render_doc
from pyRenderdocApp.renderdoc_enums import RENDERDOC_CaptureOption, RENDERDOC_OverlayBits

rd = load_render_doc()
print(rd.get_api_version())
print(rd.get_num_captures())
print(rd.get_capture_option_u32(RENDERDOC_CaptureOption.eRENDERDOC_Option_AllowFullscreen))
print(rd.get_capture_file_path_template())
rd.set_capture_file_path_template("C:\\Temp\\pyRenderdocApp")
print(rd.get_capture_file_path_template())
rd.set_capture_file_path_template(None)
print(rd.get_capture_file_path_template())
rd.start_frame_capture(None, None)
rd.mask_overlay_bits(RENDERDOC_OverlayBits.eRENDERDOC_Overlay_None,
                     RENDERDOC_OverlayBits.eRENDERDOC_Overlay_CaptureList)
print(rd.get_overlay_bits())
# print(rd.launch_replay_ui(False, None))
