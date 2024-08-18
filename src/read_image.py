# -----------------------------------------------------------
# AUTHOR --------> Francisco Contreras
# OFFICE --------> Senior VFX Compositor, Software Developer
# WEBSITE -------> https://vinavfx.com
# -----------------------------------------------------------
import os
import random
import nuke  # type: ignore

from ..nuke_util.nuke_util import get_input
from ..settings import COMFYUI_DIR
from ..nuke_util.media_util import get_name_no_padding


def update_filename_prefix(queue_prompt_node):
    output_node = get_input(queue_prompt_node, 0)
    if not output_node:
        return

    filename_prefix_knob = output_node.knob('filename_prefix_')
    if not filename_prefix_knob:
        return

    prefix = filename_prefix_knob.value().rsplit('_', 1)[0]
    rand = random.randint(10000, 99999)
    new_filename = '{}_{}'.format(prefix, rand)
    filename_prefix_knob.setValue(new_filename)


def create_read(queue_prompt_node):
    output_node = get_input(queue_prompt_node, 0)
    if not output_node:
        return

    filename_prefix_knob = output_node.knob('filename_prefix_')
    filepath_knob = output_node.knob('filepath_')

    if filename_prefix_knob:
        filename_prefix = filename_prefix_knob.value()
        sequence_output = os.path.join(COMFYUI_DIR, 'output')

    elif filepath_knob:
        filename = filepath_knob.value()
        filename_prefix = get_name_no_padding(filename)
        sequence_output = os.path.dirname(filename)

    else:
        return

    filenames = nuke.getFileNameList(sequence_output)
    filename = next((fn for fn in filenames if filename_prefix in fn), None)

    if not filename:
        return

    name = '{}Read'.format(queue_prompt_node.name())
    read = nuke.toNode(name)
    if not read:
        read = nuke.createNode('Read', inpanel=False)

    read.setName(name)
    read.knob('file').fromUserText(os.path.join(sequence_output, filename))
    read.setXYpos(queue_prompt_node.xpos(), queue_prompt_node.ypos() + 35)
    read.knob('tile_color').setValue(
        queue_prompt_node.knob('tile_color').value())


def save_image_backup():
    queue_prompt_node = nuke.thisNode()
    queue_prompt_node.parent().begin()

    read = nuke.toNode(queue_prompt_node.name() + 'Read')

    filename = '{} {}-{}'.format(read.knob('file').value(),
                                 read.knob('first').value(), read.knob('last').value())

    basename = get_name_no_padding(filename).replace(' ', '_')
    name = '{}Backup_{}'.format(queue_prompt_node.name(), basename)

    if not nuke.toNode(name):
        new_read = nuke.createNode('Read', inpanel=False)
        new_read.setName(name)
        new_read.knob('file').fromUserText(filename)

    xpos = read.xpos() + 50

    for n in nuke.allNodes():
        if not queue_prompt_node.name() + 'Backup_' in n.name():
            continue

        xpos += 100
        n.setXYpos(xpos, read.ypos())
