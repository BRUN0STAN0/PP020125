import os
import json


class CantoNotFoundError(Exception):
    """ Custom Exception raised when a requested canto number is out of range"""

    def __init__(self, message="canto_number must be between 1 and 34"):
        self.message = message
        super().__init__(f"{message}")


class Virgilio:

    def __init__(self, directory: str):
        self.directory: str = self.__validate_directory__(directory)

        # TIP: Si potrebbero usare queste ulteriori variabili, per migliorare la velocità del codice, evitando di ciclare in continuazione.
        # self.selected_canto: int | None = None
        # self.selected_verse: int | None = None
        # self.selected_verses: List[str] | None = None

    # EX-17. Controlla se esiste la directory
    def __validate_directory__(self, directory: str):
        """Checks if the provided directory exists and is valid."""
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Error while opening file_path. You must to enter a valid directory.")
        return directory

    # Ritorna la lista di tutti i numeri dei canti presenti nella cartella [1,2,3,4,5...]
    def __get_canti_numbers__(self):
        """Retrieves and sorts the numbers of available canti in the directory."""
        canti = os.listdir(self.directory)
        if not canti:
            raise FileNotFoundError("The directory given is empty")
        canti_numbers: list[int] = []
        for canto in canti:
            if canto.startswith("Canto_"):
                canto_number = int(canto.split("_")[1].split(".")[0])
                canti_numbers.append(canto_number)
        return sorted(canti_numbers)

    # Controlla se il numero "8" esiste come canto disponibile nella cartella
    def __validate_canto_number__(self, canto_number: int):
        """Ensures the provided canto number exists among the available files."""
        canti_numbers = self.__get_canti_numbers__()
        # EX-16. verifichi se canto_number ha un valore incompatibile col numero dei Canti (che va da 1 a 34)
        if canto_number not in canti_numbers:
            raise CantoNotFoundError()
        return canto_number

    # Trova la parola in un canto
    def __find_word_in_canto__(self, canto_number: int, word: str):
        """Counts how many times a word appears in the specified canto"""
        canto = self.read_canto_lines(canto_number)
        recurrence_word: int = 0
        for lines in canto:
            if word in lines:
                recurrence_word += 1
        return recurrence_word

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

    # EX-1. Dato un numero, legge un intero canto restituitendo una stringa formattata.
    def read_canto_lines(self, canto_number: int, strip_lines: bool = False, num_lines: int = None):
        """Reads the lines of a specified canto, optionally stripping whitespace or limiting the number of lines."""
        # EX-15. Verifica se canto_number è un int
        try:
            canto_number = int(canto_number)
        except Exception as err:
            raise TypeError(f"canto_number must be an integer. '{err}' is not valid")

        directory = self.directory
        canto_num = self.__validate_canto_number__(canto_number)
        file_name = f"Canto_{canto_num}.txt"
        file_path = os.path.join(directory, file_name)
        lines = []
        with open(file_path, "r", encoding="utf-8") as file:
            for index, line in enumerate(file.readlines()):
                # 14. Nel caso in cui num_lines venga valorizzato, il metodo legge solo un numero di righe pari ad esso,
                if num_lines is not None and index >= num_lines:
                    break

                # EX-13 - Strip lines
                if strip_lines is True:
                    line = line.strip() + "\n"  # Rimuovo e pulisco l'inizio e la fine di ogni versetto, ma ci riaggiungo un a capo.
                lines.append(line)
        return lines

    # EX-2. Conta quanti versi ha un canto.
    def count_verses(self, canto_number: int):
        """Calculates the total number of verses in the specified canto"""
        list_verses = self.read_canto_lines(canto_number)
        number_of_verses = len(list_verses)
        return number_of_verses

    # EX-3. Conta quante terzine ci sono nel canto
    def count_tercets(self, canto_number: int):
        """Determines the number of tercets (groups of three lines) in the canto."""
        number_of_tercets = self.count_verses(canto_number) // 3
        return number_of_tercets

    # EX-4. Conta quante ricorrenza ha la parola nel canto
    def count_word(self, canto_number: int, word: str):
        """Finds how many times a specific word appears in a canto."""
        recurrencies = int(self.__find_word_in_canto__(canto_number, word))
        return recurrencies

    # EX-5. Trova il primo verso con la parola cercata
    def get_verse_with_word(self, canto_number: int, word: str):
        """Identifies the first verse in the canto that contains the specified word."""
        canto = self.read_canto_lines(canto_number)
        for line in canto:
            if word in line:
                if line:
                    return line
            raise NameError("La parola non esiste in questo canto.")

    # EX-6. Trova tutti i versi con la parola cercata

    def get_verses_with_word(self, canto_number: int, word: str):
        """Collects all verses containing a specific word from the canto."""
        canto = self.read_canto_lines(canto_number)
        verse_list = []
        for line in canto:
            if word in line:
                verse_list.append(f"{line}")
        if not verse_list:
            raise NameError("La parola non esiste in questo canto.")
        return "".join(verse_list)

    # EX-7. Ottieni il verso piu lungo da un canto.
    def get_longest_verse(self, canto_number: int):
        """Determines the longest verse from the specified canto."""
        canto = self.read_canto_lines(canto_number)
        longest_verse = max(canto, key=len)
        return longest_verse

    # EX-8. Ottieni il canto con piu versi dell'interno inferno, restituendo un dict['canto_number': int, 'canto_len': int]
    def get_longest_canto(self):
        """Identifies the canto with the highest number of verses among all available."""
        canti_available = self.__get_canti_numbers__()
        longest_canto: dict[str, None | int] = {"canto_number": None, "canto_len": 0}
        for canto_number in canti_available:
            canto_lines = self.read_canto_lines(canto_number)
            canto_len = len(canto_lines)
            if canto_len > longest_canto["canto_len"]:
                longest_canto["canto_number"] = canto_number
                longest_canto["canto_len"] = canto_len
        return longest_canto

    # EX-9. Conta le ricorrenze di una lista di parole utilizzata nel canto - Restituisce un dict["bello":str, 5:in-t]  Case sensitive
    def count_words(self, canto_number: int, words: list[str]):
        """Computes the frequency of multiple words in a specified canto and saves the results to a JSON file."""
        count_words: dict[str, int] = {}
        for word in words:
            recurrencies = self.count_word(canto_number, word)
            count_words[word] = recurrencies

        # EX-18. Serializzazione del risultato in un file JSON
        json_file_path = os.path.join(self.directory, "word_counts.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(count_words, json_file, ensure_ascii=False, indent=4)
        return count_words

    # EX-10. Leggi tutti i versi dell'Inferno, in ordine dal primo a l'ultimo. List(str)
    def get_hell_verses(self):
        """Gathers all verses from all available canti in sequential order."""
        canti_numbers = self.__get_canti_numbers__()
        hell_verses: list[str] = []
        for canto_number in canti_numbers:
            canto = self.read_canto_lines(canto_number)
            hell_verses.extend(canto)
        return hell_verses

    # EX-11. Conta tutti i versi dell'Inferno
    def count_hell_verses(self):
        """Calculates the total number of verses across all available canti."""
        count_hell_verses = len(self.get_hell_verses())
        return count_hell_verses

    # EX-12. Restituisce un float rappresentante la lunghezza media di tutti i versi dei canti dell'inferno
    def get_hell_verse_mean_len(self):
        """Computes the average length of all verses from the canti combined."""
        hell_verses = self.get_hell_verses()
        count_hell_verses = self.count_hell_verses()
        sum_length = 0
        for verse in hell_verses:
            sum_length += len(verse)

        mean_len = sum_length / count_hell_verses
        return mean_len


def main():
    """This function allows you to call and execute the main program in an external module."""

    exercise_titles = {
        1: "Leggi un canto",
        2: "Conta i versi di un canto",
        3: "Conta le terzine di un canto",
        4: "Conta l'utilizzo di una parola in un canto",
        5: "Trova il verso con una parola in un canto",
        6: "Trova tutti i versi con una parola in un canto",
        7: "Trova il verso più lungo in un canto",
        8: "Trova il canto più lungo dell'inferno",
        9: "Conta specifiche parole in un canto",
        10: "Trova i versi dell'inferno",
        11: "Conta i versi dell'inferno",
        12: "Lunghezza media dei versi dell'inferno",
        13: "Leggi un canto senza spazi inutili",
    }

    directory_path = "canti"
    reader = Virgilio(directory_path)
    while True:
        print("Menu:")
        for key, title in exercise_titles.items():
            print(f"{key}. {title}")
        print("0. Esci")
        try:
            exercise = int(input("\nSELEZIONA ESERCIZIO - Seleziona un esercizio (0 per uscire).\nEsercizio numero = "))
            if exercise == 0:
                print("Uscita dal programma.")
                break
            if exercise in exercise_titles:
                print(f"'{exercise}. {exercise_titles[exercise]}'\n")
            if exercise in [1, 2, 3, 4, 5, 6, 7, 9, 13]:
                canto_to_read = input("SELEZIONA CANTO - Inserisci quale canto vorresti leggere.\nCanto numero = ")
            if exercise == 0:
                print("Uscita dal programma.")
                break
            if exercise == 1:
                canto = reader.read_canto_lines(canto_to_read)
                print("".join(canto))
            elif exercise == 2:
                verses_of_canto = reader.count_verses(canto_to_read)
                print(f"Versi del canto: {verses_of_canto}")
            elif exercise == 3:
                tercets_of_canto = reader.count_tercets(canto_to_read)
                print(f"Terzine del canto: {tercets_of_canto}")
            elif exercise == 4:
                word = input("Fornisci una parola: ")
                recurrence_word = reader.count_word(canto_to_read, word)
                print(f"Numero di utilizzo della parola '{word}': {recurrence_word}")
            elif exercise == 5:
                word = input("Fornisci una parola: ")
                verse_with_word = reader.get_verse_with_word(canto_to_read, word)
                print(f"Primo utilizzo della parola '{word}': {verse_with_word}")
            elif exercise == 6:
                word = input("Fornisci una parola: ")
                verses_with_word = reader.get_verses_with_word(canto_to_read, word)
                print(f"Tutti gli utilizzi della parola '{word}': {verses_with_word}")
            elif exercise == 7:
                longest_verse = reader.get_longest_verse(canto_to_read)
                print(f"Verso più lungo: {longest_verse}")
            elif exercise == 8:
                longest_canto = reader.get_longest_canto()
                print(f"Il canto più lungo dell'inferno è il {longest_canto['canto_number']} con una lunghezza pari a {longest_canto['canto_len']} versi")
            elif exercise == 9:
                how_much_word = int(input("Quante parole vorresti cercare? "))
                words = []
                for index in range(1, how_much_word+1):
                    words.append(input(f"{index}. Give me a word = "))
                count_words = reader.count_words(canto_to_read, words)
                for key, value in count_words.items():
                    print(f"La parola {key} è comparsa {value} volte.")
            elif exercise == 10:
                hell_verses = reader.get_hell_verses()
                for canto in hell_verses:
                    print(canto.strip())
            elif exercise == 11:
                count_hell_verses = reader.count_hell_verses()
                print(f"Il totale dei versi contenuti nell'inferno è pari a {count_hell_verses}")
            elif exercise == 12:
                hell_verses_mean_len = reader.get_hell_verse_mean_len()
                print(f"La lunghezza media dei versi dell'inferno è pari a {hell_verses_mean_len:.2f}")
            elif exercise == 13:
                read_canto_lines_strip = reader.read_canto_lines(canto_to_read, True)
                print(''.join(read_canto_lines_strip))
            else:
                print("Scelta non valida. Perfavore, seleziona un'opzione dal menu.")
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
        input("\n---\nFINE - Premi Invio per continuare -> ")


# Main Program start automatically when started from the source file.
if __name__ == "__main__":
    main()
