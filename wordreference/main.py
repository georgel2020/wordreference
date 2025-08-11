from wordreference import *

def main():
    sections, meanings = get_dictionary('test')

    for section in range(len(meanings)):
        print(sections[section])
        for index in range(len(meanings[section])):
            print(meanings[section][index])

if __name__ == "__main__":
    main()