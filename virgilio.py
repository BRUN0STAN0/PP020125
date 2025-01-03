import os
import traceback


class Virgilio:
    def __init__(self, directory: str):
        self.directory: str = self.__validate_directory__(directory)

        # TIP: Si potrebbero usare queste ulteriori variabili, per migliorare la velocità del codice, evitando di ciclare in continuazione.
        # self.selected_canto: int | None = None
        # self.selected_verse: int | None = None
        # self.selected_verses: List[str] | None = None

    # Controlla se esiste la directory
    def __validate_directory__(self, directory: str):
        if not os.path.isdir(directory):
            raise NotADirectoryError("Please, give a valid directory.")
        return directory

    # Ritorna la lista di tutti i nomi dei canti presenti nella cartella [Canto_1.txt,Canto_2.txt,Canto_3.txt,...]
    def __get_file_names__(self):
        files = os.listdir(self.directory)
        if not files:
            raise FileNotFoundError("The directory given is empty")
        file_names: list[str] = []
        for file in files:
            file_names.append(file)
        return files

    # Ritorna la lista di tutti i numeri dei canti presenti nella cartella [1,2,3,4,5...]
    def __get_canti_numbers__(self):
        canti = self.__get_file_names__()
        canti_numbers: list[int] = []
        for canto in canti:
            canto_number = int(canto.split("_")[1].split(".")[0])
            canti_numbers.append(canto_number)
        return sorted(canti_numbers)

    # Controlla se il numero "8" esiste come canto disponibile nella cartella
    def __validate_canto_number__(self, canto_number: int):
        canti_numbers = self.__get_canti_numbers__()
        if canto_number not in canti_numbers:
            raise FileNotFoundError(f"Il canto numero {canto_number} non esiste.")
        return canto_number

    # Trova la parola in un canto
    def __find_word_in_canto__(self, canto_number: int, word: str):
        canto = self.read_canto_lines(canto_number)
        recurrence_word: int = 0
        for lines in canto:
            if word in lines:
                recurrence_word += 1
        return recurrence_word

    def __format_lines__(self, lines: list[str]):
        return "".join(lines)

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

    # 1. Dato un numero, legge un intero canto restituitendo una stringa formattata.

    def read_canto_lines(self, canto_number: int):
        directory = self.directory
        canto_num = self.__validate_canto_number__(canto_number)
        file_name = f"Canto_{canto_num}.txt"
        file_path = os.path.join(directory, file_name)
        lines = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file.readlines():
                lines.append(line.strip())
        return lines

    # 2. Conta quanti versi ha un canto.
    def count_verses(self, canto_number: int):
        list_verses = self.read_canto_lines(canto_number)
        number_of_verses = len(list_verses)
        return number_of_verses

    # 3. Conta quante terzine ci sono nel canto
    def count_tercets(self, canto_number: int):
        number_of_tercets = self.count_verses(canto_number) // 3
        return number_of_tercets

    # 4. Conta quante ricorrenza ha la parola nel canto
    def count_word(self, canto_number: int, word: str):
        recurrencies = int(self.__find_word_in_canto__(canto_number, word))
        return recurrencies

    # 5. Trova il primo verso con la parola cercata
    def get_verse_with_word(self, canto_number: int, word: str):
        canto = self.read_canto_lines(canto_number)
        for line in canto:
            if word in line:
                return line
        if not line:
            raise NameError("La parola non esiste in questo canto.")

    # 6. Trova tutti i versi con la parola cercata
    def get_verses_with_word(self, canto_number: int, word: str):
        canto = self.read_canto_lines(canto_number)
        verse_list = []
        for line in canto:
            if word in line:
                verse_list.append(f"{line}")
        if not verse_list:
            raise NameError("La parola non esiste in questo canto.")
        verses_with_word = self.__format_lines__(verse_list)
        return verses_with_word

    # 7. Ottieni il verso piu lungo da un canto.
    def get_longest_verse(self, canto_number: int):
        canto = self.read_canto_lines(canto_number)
        longest_verse = max(canto, key=len)
        return longest_verse

    # 8. Ottieni il canto con piu versi dell'interno inferno, restituendo un dict['canto_number': int, 'canto_len': int]
    def get_longest_canto(self):
        canti_available = self.__get_canti_numbers__()
        longest_canto: dict[str, None | int] = {"canto_number": None, "canto_len": 0}
        for canto_number in canti_available:
            canto_lines = self.read_canto_lines(canto_number)
            canto_len = len(canto_lines)
            if canto_len > longest_canto["canto_len"]:
                longest_canto["canto_number"] = canto_number
                longest_canto["canto_len"] = canto_len
        return longest_canto

    # 9. Conta le ricorrenze di una lista di parole utilizzata nel canto - Restituisce un dict["bello":str, 5:in-t]  Case sensitive
    def count_words(self, canto_number: int, words: list[str]):
        count_words: dict[str, int] = {}
        for word in words:
            recurrencies = self.count_word(canto_number, word)
            count_words[word] = recurrencies
        return count_words

    # 10. Leggi tutti i versi dell'Inferno, in ordine dal primo a l'ultimo. List(str)
    def get_hell_verses(self):
        canti_numbers = self.__get_canti_numbers__()
        hell_verses: list[str] = []
        for canto_number in canti_numbers:
            canto = self.read_canto_lines(canto_number)
            hell_verses.extend(canto)
        return hell_verses

    # 11. Conta tutti i versi dell'Inferno
    def count_hell_verses(self):
        count_hell_verses = len(self.get_hell_verses())
        return count_hell_verses

    # 12. Conta con un float la lunghezza media di tutti i versi dei canti dell'inferno
    def get_hell_verse_mean_len(self):
        return ""


def main():
    """This function allows you to call and execute the main program in an external module."""
    directory_path = "canti"
    reader = Virgilio(directory_path)

    while True:
        canto_to_read = input("\nPerfavore, fornisci un valido numero di Canto.\n\nCanto Numero: ")
        try:
            canto_to_read = int(canto_to_read)

            print("\nExercise 1")
            # Exercise 1
            canto = reader.read_canto_lines(canto_to_read)
            print(f"\n{canto}")

            print("\nExercise 2")
            # Exercise 2
            verses_of_canto = reader.count_verses(canto_to_read)
            print(f"Versi del canto: {verses_of_canto}")

            print("\nExercise 3")
            # Exercise 3
            tercets_of_canto = reader.count_tercets(canto_to_read)
            print(f"Terzine del canto: {tercets_of_canto}")

            print("\nExercise 4")
            # Exercise 4
            word = input("Fornisci una parola, per contare l'utilizzo: ")
            recurrence_word = reader.count_word(canto_to_read, word)
            print(f"Numero di utilizzo della parola '{word}' nel {canto_to_read}: {recurrence_word}")

            print("\nExercise 5")
            # Exercise 5
            verse_with_word = reader.get_verse_with_word(canto_to_read, word)
            print(f"Primo utilizzo della parola '{word}': {verse_with_word}")

            print("\nExercise 6")
            # Exercise 6
            verses_with_word = reader.get_verses_with_word(canto_to_read, word)
            print(f"Tutti gli utilizzi della parola '{word}: {verses_with_word}")

            print("\nExercise 7")
            # Exercise 7
            longest_verse = reader.get_longest_verse(canto_to_read)
            print(f"Verso piu lungo del canto: {longest_verse}")

            print("\nExercise 8")
            # Exercise 8
            longest_canto = reader.get_longest_canto()
            print(f"Il canto piu lungo è il {longest_canto["canto_number"]} con una lunghezza pari a {longest_canto["canto_len"]}")

            print("\nExercise 9")
            # Exercise 9
            count_words = reader.count_words(canto_to_read, ["amore", "e", "spazio"])
            for key, value in count_words.items():
                print(f"La parola {key} è comparsa {value}")

            print("\nExercise 10")
            # Exercise 10
            hell_verses = reader.get_hell_verses()
            for canto in hell_verses:
                print(canto)

            print("\nExercise 11")
            # Exercise 11
            count_hell_verses = reader.count_hell_verses()
            print(count_hell_verses)

            break
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            for frame in traceback.extract_tb(err.__traceback__):
                print(f" linea {frame.lineno}, nella funzione {frame.name}")


# Main Program start automatically when started from the source file.
if __name__ == "__main__":
    main()
