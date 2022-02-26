import enum

class BoardLayout(enum.Enum):
  Standard = 0
  German = 1
  Belgian = 2

  @classmethod
  def from_string(cls, string):
    return {
      "Standard": cls.Standard,
      "German Daisy": cls.German,
      "Belgian Daisy": cls.Belgian
    }[string]
