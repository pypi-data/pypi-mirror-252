## OOPyGUI

OOPyGUI is an object-oriented wrapper for DearPyGUI (https://github.com/hoffstadt/DearPyGui).

Using DearPyGUI, GUI elements can be added with functions of form add_<item_name>(<params>). They return the element's ID, through which the element's attributes and behavior can be changed, again, via DearPyGUI functions, e.g. ``set_item_height(item, height)``, where ``item`` is a parameter for the element's ID. Dynamic behavior, such as on-click event, is implemented via callbacks.

OOPyGUI provides classes for the respective GUI elements, with attributes and functions wrapping the respective DearPyGUI functions. Thus, you can operate GUI elements in an object-oriented manner. 