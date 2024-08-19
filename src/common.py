# -----------------------------------------------------------
# AUTHOR --------> Francisco Contreras
# OFFICE --------> Senior VFX Compositor, Software Developer
# WEBSITE -------> https://vinavfx.com
# -----------------------------------------------------------
import os
import nuke  # type: ignore
from ..settings import COMFYUI_DIR
from ..nuke_util.nuke_util import get_nuke_path
from .connection import GET

state_dir = '{}/comfyui_state'.format(get_nuke_path())
if not os.path.isdir(state_dir):
    os.mkdir(state_dir)

if not getattr(nuke, 'comfyui_running', False):
    nuke.comfyui_running = False

image_inputs = ['image', 'frames', 'pixels', 'images']
mask_inputs = ['mask', 'attn_mask', 'mask_optional']
updated_inputs = False


def update_images_and_mask_inputs():
    global image_inputs, mask_inputs, updated_inputs

    if updated_inputs:
        return

    updated_inputs = True

    info = GET('object_info')
    if not info:
        return

    for _, data in info.items():
        input_data = data['input']
        required = input_data.get('required', {})
        optional = input_data.get('optional', {})

        for name, value in list(required.items()) + list(optional.items()):
            if value[0] == 'IMAGE':
                if not name in image_inputs:
                    image_inputs.append(name)

            elif value[0] == 'MASK':
                if not name in mask_inputs:
                    mask_inputs.append(name)


def get_available_name(prefix, directory):
    prefix += '_'
    taken_names = set(os.listdir(directory))

    for i in range(10000):
        potential_name = '{}{:04d}'.format(prefix, i)
        if potential_name not in taken_names:
            return potential_name

    return prefix


def get_comfyui_dir():
    if os.path.isdir(os.path.join(COMFYUI_DIR, 'comfy')):
        return COMFYUI_DIR

    nuke.message('Directory "{}" does not exist'.format(COMFYUI_DIR))

    return ''
