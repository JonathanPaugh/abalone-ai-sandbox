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
        Returns a BoardLayout from a string value.
        :param string: a string
        :return: a BoardLayout value
        """
        return {
            "Standard": cls.Standard,
            "German Daisy": cls.German,
            "Belgian Daisy": cls.Belgian
        }[string]
