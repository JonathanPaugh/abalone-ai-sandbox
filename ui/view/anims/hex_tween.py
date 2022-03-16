from ui.view.anims.tween import TweenAnim
from core.hex import Hex

class HexTweenAnim(TweenAnim):

    def __init__(self, src, dest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._src = src
        self._dest = dest
        self._cell = src

    def __repr__(self):
        return f"HexTweenAnim(target={self.target}, cell={self._cell})"

    @property
    def cell(self):
        return self._cell

    def update(self):
        pos = super().update()

        if self.done:
            return self._dest

        self._cell = Hex.lerp(self._src, self._dest, pos)
        return self._cell
