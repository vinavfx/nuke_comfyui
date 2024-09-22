# -----------------------------------------------------------
# AUTHOR --------> Francisco Contreras
# OFFICE --------> Senior VFX Compositor, Software Developer
# WEBSITE -------> https://vinavfx.com
# -----------------------------------------------------------
import nuke  # type: ignore


def init_menu():
    nuke.addOnCreate(on_create)
    nuke.addKnobChanged(knob_changed)


last_node = None


def knob_changed():
    knob = nuke.thisKnob()
    if knob and not knob.name() == 'selected':
        return

    node = nuke.thisNode()

    if not node.isSelected():
        return

    update_menu(node)


def on_create():
    node = nuke.thisNode()
    update_menu(node)


def update_menu(node):
    global last_node

    if node == last_node:
        return

    last_node = node

    menu = nuke.menu('Properties')

    if not node.knob('data'):
        menu.clearMenu()
        print(node.name(), 'reset menu')
        return

    print(node.name(), 'node with menu')

    menu.addCommand('Open Properties', convert_knob_to_input)
    menu.clearMenu()

    knob_to_input_menu = menu.addMenu('Convert Knob to Input')
    input_to_knob_menu = menu.addMenu('Convert Input to Knob')

    knob_to_input_menu.addCommand('knobs...', convert_knob_to_input)
    input_to_knob_menu.addCommand('inputs...', convert_input_to_knob)


def convert_knob_to_input():
    print('knob')


def convert_input_to_knob():
    print('input')
