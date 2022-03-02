import enum


class BoardLayout(enum.Enum):
    """
    BoardLayout specifies the different board layouts for the program.
    """

    Standard = 0
    German = 1
    Belgian = 2

    @classmethod
    def from_string(cls, string):
        """
        Returns a dictionary containing the string name and its enum value.
        :param string: a string
        :return: dictionary of layouts
        """
        return {
            "Standard": cls.Standard,
            "German Daisy": cls.German,
            "Belgian Daisy": cls.Belgian
        }[string]
