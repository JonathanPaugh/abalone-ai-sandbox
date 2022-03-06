class FileHandler:
    @staticmethod
    def write_file(filepath: str, data: str):
        with open(filepath, mode="w") as file:
            file.write(data)

    @staticmethod
    def read_file(filepath: str) -> str:
        with open(filepath) as file:
            data = file.read()

        return data