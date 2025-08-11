from wordreference.wordreference import *
from wordreference.cli import *

def main():
    args = get_args()
    sections, meanings = get_dictionary(args.word)

    for section in range(len(meanings)):
        print(sections[section])
        for index in range(len(meanings[section])):
            print(meanings[section][index])

if __name__ == "__main__":
    main()