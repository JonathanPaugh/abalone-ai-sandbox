"""
Defines a generic tween animation.
"""

from lib.anims import Anim

class TweenAnim(Anim):
    """
    A generic tween animation.
    A tween animation has a position (a float between 0 and 1) that may be
    transformed using an easing function and interpolated to obtain precise
    source and destination positions in n-dimensional space.
    """

    def __init__(self, *args, easing=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._easing = easing
        self._pos = 0

    @property
    def pos(self):
        """
        Gets the animation's current position.
        :return: a float
        """
        return self._pos

    def update(self):
        """
        Updates the animation.
        :return: a float denoting the animation's position
        """
        time = super().update()

        if self.done:
            self._pos = 1
            return 1

        self._pos = max(0, time / self.duration)
        if self._easing:
            self._pos = self._easing(self._pos)

        return self._pos
