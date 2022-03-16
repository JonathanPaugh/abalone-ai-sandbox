"""
Defines a tween animation for hex coordinates.
"""

from lib.anims.tween import TweenAnim
from core.hex import Hex

class HexTweenAnim(TweenAnim):
    """
    A tween animation for hex coordinates.
    Inputs `src` and `dest` Hex instances and outputs a `cell`, handling
    interpolation out of the box.
    """

    def __init__(self, src, dest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._src = src
        self._dest = dest
        self._cell = src

    def __repr__(self):
        return f"HexTweenAnim(target={self.target}, cell={self._cell})"

    @property
    def cell(self):
        """
        Gets the animation's current hex position.
        :return: a Hex
        """
        return self._cell

    def update(self):
        """
        Updates the animation.
        :return: a Hex denoting the animation's current hex position
        """
        pos = super().update()

        if self.done:
            return self._dest

        self._cell = Hex.lerp(self._src, self._dest, pos)
        return self._cell
