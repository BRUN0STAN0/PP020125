import os


class Virgilio:
    def __init__(self, directory: str):
        self.directory = directory

    def __file_path_exist__(self, canto_number: int):
        file_path = os.path.join(self.directory, f"Canto_{canto_number}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Il canto numero {canto_number} non esiste.")
        return file_path

    def __readlines_canto__(self, canto_number):
        file_path = self.__file_path_exist__(canto_number)
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return lines

    def read_canto_lines(self, canto_number: int):
        lines = self.__readlines_canto__(canto_number)
        formatted_lines = "".join(lines)
        return formatted_lines

    def count_verses(self, canto_number: int):
        list_verses = self.__readlines_canto__(canto_number)
        number_of_verses = len(list_verses)
        return number_of_verses

    def count_tercets(self, canto_number: int):
        number_of_verses = self.count_verses(canto_number)
        number_of_tercets = number_of_verses // 3
        return number_of_tercets

    def count_word(self, canto_number: int, word: str):
        canto = self.read_canto_lines(canto_number)
        recurrence_word = canto.count(word)
        return recurrence_word

    def get_verse_with_word(self, canto_number: int, word: str):
        if self.count_word(canto_number, word) == 0:
            return f"La parola '{word}' non viene mai utilizzata in questo Canto."
        canto = self.__readlines_canto__(canto_number)
        for line in canto:
            if word in line:
                verse = line
                break
        return verse

    def get_verses_with_word(self, canto_number: int, word: str):
        if self.count_word(canto_number, word) == 0:
            return f"La parola '{word}' non viene mai utilizzata in questo Canto."
        canto = self.__readlines_canto__(canto_number)
        verse_list = []
        for line in canto:
            if word in line:
                verse_list.append(f"{line}")
        verses = "".join(verse_list)
        return verses

    def get_longest_verse(self, canto_number: int):
        verses = self.__readlines_canto__(canto_number)
        return max(verses, key=len)


def main():
    """This function allows you to call and execute the main program in an external module."""
    directory_path = "canti"
    reader = Virgilio(directory_path)

    while True:
        canto_to_read = input("\nPerfavore, fornisci un valido numero di Canto.\n\nCanto Numero: ")
        try:
            int(canto_to_read)
            # Exercise 1
            canto = reader.read_canto_lines(canto_to_read)
            print(f"\n{canto} \n")

            # Exercise 2
            verses_of_canto = reader.count_verses(canto_to_read)
            print(f"Versi del canto: {verses_of_canto}")

            # Exercise 3
            tercets_of_canto = reader.count_tercets(canto_to_read)
            print(f"Terzine del canto: {tercets_of_canto}\n")

            # Exercise 4
            word = input("Fornisci una parola, per contare l'utilizzo: ")
            recurrence_word = reader.count_word(canto_to_read, word)
            print(f"\nNumero di utilizzo della parola '{word}' nel {canto_to_read}: {recurrence_word}\n")

            # Exercise 5
            verse_with_word = reader.get_verse_with_word(canto_to_read, word)
            print(f"Primo utilizzo della parola '{word}': {verse_with_word}")

            # Exercise 6
            verses_with_word = reader.get_verses_with_word(canto_to_read, word)
            print(f"Tutti gli utilizzi della parola '{word}: {verses_with_word}\n")

            # Exercise 6
            longest_verse = reader.get_longest_verse(canto_to_read)
            print(f"Verso piu lungo del canto: {longest_verse}\n")

            break
        except Exception as err:
            print(f"{type(err).__name__}: {err}")


# Main Program start automatically when started from the source file.
if __name__ == "__main__":
    main()
