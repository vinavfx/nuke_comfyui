# -----------------------------------------------------------
# AUTHOR --------> Francisco Contreras
# OFFICE --------> Senior VFX Compositor, Software Developer
# WEBSITE -------> https://vinavfx.com
# -----------------------------------------------------------
import nuke  # type: ignore


def init_menu():
    menu = nuke.menu('Properties')
    menu.addCommand('Swap Knobs and Inputs', swap)


def swap():
    # Here it need to get the correct node now, it doesn't work!
    node = nuke.thisNode()
    print(node.name())
    # Here the pyside menu is created
