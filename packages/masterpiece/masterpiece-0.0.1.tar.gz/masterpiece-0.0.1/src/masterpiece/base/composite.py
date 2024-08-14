from typing import List
from .masterpiece import MasterPiece


class Composite(MasterPiece):
    """Class implementing hierarchy. Objects of this class can consist of children.

    This class can be used for grouping masterpieces into larger entities.

    Example:
    ::

        motion_sensors = Composite("motionsensors")
        motion_sensors.add(ShellyMotionSensor("downstairs"))
        motion_sensors.add(ShellyMotionSensor("upstairs"))
    """

    def __init__(self, name: str = "group") -> None:
        super().__init__(name)
        self.children: List[MasterPiece] = []
        self.role: str = "union"

    def add(self, h: MasterPiece) -> None:
        """Add new automation object as children. The object to be inserted
        must be derived from MasterPiece base class.

        Args:
            h (T): object to be inserted.
        """
        self.children.append(h)

    def to_dict(self):
        data = super().to_dict()
        data["_group"] = {
            "role": self.role,
            "children": [child.to_dict() for child in self.children],
        }
        return data

    def from_dict(self, data):
        """Recursively deserialize the group from a dictionary, including its
        children.

        Args:
            data (dict): data to deserialize from.
        """
        super().from_dict(data)
        for key, value in data.get("_group", {}).items():
            if key == "children":
                for child_dict in value:
                    child = MasterPiece.instantiate(child_dict["_class"])
                    self.add(child)
                    child.from_dict(child_dict)
            else:
                setattr(self, key, value)

    def print(self, prefix="", is_last=True):
        """Print the hierarchy of the node using ├─, └─, and │.

        Example:
        ::

            parent = Composite("parent")
            child = MasterPiece("child")
            parent.add(child)
            parent.print()

            # expected output:
            # parent
            #  └─ child

        Args:
            prefix (str, optional): Defaults to "".
            is_last (bool, optional): Defaults to True.
        """
        super().print(prefix, is_last)

        # Prepare the new prefix for the child nodes
        if prefix:
            prefix += "    " if is_last else "│   "
        else:
            prefix = "    " if is_last else "│   "

        # Recursively print all the children
        for i, child in enumerate(self.children):
            is_last_child = i == len(self.children) - 1
            child.print(prefix, is_last_child)

    # @override
    def run(self) -> None:
        """
        Dispatches first the call to all children and then to the super class.
        It is up to the sub classes to implement the actual functionality
        for this method.
        """

        for s in self.children:
            s.run()
        super().run()

    # @override
    def shutdown(self) -> None:
        """
        Dispatches first the call to all children and then to the super class.
        It is up to the sub classes to implement the actual functionality
        for this method.
        """

        for s in self.children:
            s.shutdown()
        super().shutdown()
