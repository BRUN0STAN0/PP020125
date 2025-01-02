import os


class Virgilio:
    def __init__(self, directory: str):
        self.directory = directory

    def __file_path_exist(self, canto_number: int):
        file_path = os.path.join(self.directory, f"Canto_{canto_number}.txt")
        file_path_exist = os.path.exists(file_path)
        if not file_path_exist:
            raise FileNotFoundError(f"Il canto numero {canto_number} non esiste.")
        return file_path

    def read_canto_lines(self, canto_number: int):

        file_path = self.__file_path_exist(canto_number)
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read()
        return lines

    def count_verses(self, canto_number: int):
        return


def main():
    """This function allows you to call and execute the main program in an external module."""
    directory_path = "canti"
    reader = Virgilio(directory_path)

    while True:
        canto_to_read = input("\nPerfavore, fornisci un valido numero di Canto.\n\nCanto Numero: ")
        try:
            int(canto_to_read)
            canto = reader.read_canto_lines(canto_to_read)
            print(f"\n{canto}")
            break
        except Exception as err:
            print(f"{type(err).__name__}: {err}")


# Main Program start automatically when started from the source file.
if __name__ == "__main__":
    main()
