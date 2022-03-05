from os import system, name
from textwrap import wrap


class WordleHelper():
    __all_words: list
    __invalid_letters: list
    __valid_letters: list
    __known_letters: list
    __low_probability: list
    __mid_probability: list
    __high_probability: list
    __number_of_words: int

    def __init__(self) -> None:
        self.__all_words = self.__get_all_words()
        self.__invalid_letters = []
        self.__valid_letters = []
        self.__known_letters = self.__init_known_letters()
        self.__low_probability = []
        self.__mid_probability = []
        self.__high_probability = []

    def start(self) -> None:
        while True:
            self.__show_options()
            self.__get_choice()

    def __show_options(self) -> None:
        self.__clear_console()
        self.__show_results(self.__invalid_letters, "Invalid letters:")
        self.__show_results(self.__valid_letters, "Valid letters:")
        self.__show_known_letters()
        print("1. Add invalid letters")
        print("2. Remove invalid letters\n")
        print("3. Add valid letters")
        print("4. Remove valid letters\n")
        print("5. Add/Replace known letters\n")
        print("6. Show potential words")
        print("7. Reset lists\n")
        print("8. Exit\n")

    def __get_choice(self) -> None:
        choice = self.__input_int_range("Enter choice: ", 1, 8)
        match choice:
            case 1:
                self.__add_to_list(self.__invalid_letters, "invalid letters")
            case 2:
                self.__remove_from_list(self.__invalid_letters, "invalid letters")
            case 3:
                self.__add_to_list(self.__valid_letters, "valid letters")
            case 4:
                self.__remove_from_list(self.__valid_letters, "valid letters")
            case 5:
                self.__add_known_letters()
            case 6:
                self.__get_potential_words()
            case 7:
                self.__reset_lists()
            case 8:
                exit()

    def __clear_console(self) -> None:
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def __get_all_words(self) -> list:
        with open("wordle_words.txt") as file:
            words = file.read().splitlines()
            self.__number_of_words = len(words)
            return words

    def __init_known_letters(self) -> None:
        starting_knowns = []
        for index in range(1, 6):
            starting_knowns.append((index, "_"))
        return starting_knowns

    def __add_to_list(self, list_to_add: list, message: str) -> None:
        input_str = self.__input_letters_only(f"Enter {message} to add: ")
        list_to_add += list(input_str)

    def __remove_from_list(self, list_to_remove: list, message: str) -> None:
        input_str = self.__input_letters_only(f"Enter {message} to remove: ")
        for char in input_str:
            if char in list_to_remove:
                list_to_remove.remove(char)

    def __show_results(self, letters_list: list, message: str) -> None:
        print(message)
        if len(letters_list) != 0:
            for letter in letters_list:
                print(letter, end=" ")
        print("\n")

    def __get_potential_words(self) -> None:
        self.__clear_console()
        self.__low_probability.clear()
        for word in self.__all_words:
            temp = any(char in self.__invalid_letters for char in word)
            if temp == False:
                self.__low_probability.append(word)

        self.__mid_probability.clear()
        if len(self.__valid_letters) > 0:
            for word in self.__low_probability:
                temp = all([char in word for char in self.__valid_letters])
                if temp == True:
                    self.__mid_probability.append(word)

        self.__high_probability.clear()
        if len(self.__known_letters) > 0:
            for word in self.__mid_probability:
                score = 0
                for location, letter in self.__known_letters:
                    if word[location - 1] == letter:
                        score += 1
                if score == self.__amount_of_known_letters():
                    self.__high_probability.append(word)

        self.__show_potential_words()
        while True:
            answer = input("Press x to continue: \n")
            if answer == "x" or answer == "X":
                break

    def __add_known_letters(self) -> None:
        letters_locs = wrap(input("Enter known letters: "), 2)

        for group in letters_locs:
            if group[0].isdigit():
                location = int(group[0])
                letter = group[1]
            else:
                location = int(group[1])
                letter = group[0]
            self.__known_letters[location - 1] = (location, letter)

    def __show_known_letters(self) -> None:
        print("Known letters:")
        char_1 = char_2 = char_3 = char_4 = char_5 = '_'
        for location, letter in self.__known_letters:
            if location == 1:
                char_1 = letter
                continue
            if location == 2:
                char_2 = letter
                continue
            if location == 3:
                char_3 = letter
                continue
            if location == 4:
                char_4 = letter
                continue
            if location == 5:
                char_5 = letter
        print(f"{char_1} {char_2} {char_3} {char_4} {char_5}\n\n")

    def __amount_of_known_letters(self) -> int:
        amount = 0
        for _, letter in self.__known_letters:
            if letter != '_':
                amount += 1
        return amount

    def __show_potential_words(self) -> None:
        if len(self.__high_probability) > 0:
            print(f"Results: {self.__calculate_words(self.__high_probability)}")
            self.__show_results(self.__high_probability, "High probability:")
            return
        if len(self.__mid_probability) > 0:
            print(f"Results: {self.__calculate_words(self.__mid_probability)}")
            self.__show_results(self.__mid_probability, "Mid probability:")
            return
        if len(self.__low_probability) > 0:
            print(f"Results: {self.__calculate_words(self.__low_probability)}")
            self.__show_results(self.__low_probability, "Low probability:")
            return

    def __calculate_words(self, results: list) -> None:
        amount = f"{len(results)} potential words"
        percent = 100 - (len(results) / self.__number_of_words * 100)
        # percent_reduced = (len(results) / self.__number_of_words)
        # print(percent_reduced)
        return f"{amount} | {round(percent, 2)}% of words eliminated"
        # return ""

    def __reset_lists(self) -> None:
        self.__invalid_letters = []
        self.__valid_letters = []
        self.__known_letters = self.__init_known_letters()

    def __input_int_range(self, message: str, min: int, max: int) -> int:
        while True:
            input_str = input(message)
            if input_str.isdigit():
                value = int(input_str)
                if value >= min and value <= max:
                    return value
                else:
                    print(f"Value must be between {min} through {max}")
            else:
                print("Value can only be a number")

    def __input_letters_only(self, message: str) -> str:
        while True:
            input_str = input(message)
            if input_str.isalpha():
                return input_str
            else:
                print("Value can only contain letters from the alphabet")


if __name__ == "__main__":
    WordleHelper().start()