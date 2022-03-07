class FileHandler:
    """
    This class contained the functions to write and read files.
    """
    @staticmethod
    def write_file(filepath: str, data: str):
        """
        Writes to a file.
        :param filepath: a string containing file path name
        :param data: a string containing data to be written
        :return: none
        """
        with open(filepath, mode="w") as file:
            file.write(data)

    @staticmethod
    def read_file(filepath: str) -> str:
        """
        Reads a file.
        :param filepath:  a string containing file path name
        :return: a string containing the data in the file
        """
        with open(filepath) as file:
            data = file.read()

        return data
