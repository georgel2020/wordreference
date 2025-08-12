from wordreference.wordreference import *
from wordreference.cli import *

def main():
    args = get_args()

    uk_pronunciation, us_pronunciation, sections, meanings = get_dictionary(args.word)

    print(f'{Colors.BRIGHT_CYAN}{args.word}{Colors.RESET}{Colors.CYAN}{' UK ' + uk_pronunciation if uk_pronunciation else ''}{' US ' + us_pronunciation if us_pronunciation else ''}{Colors.RESET}')

    for index in range(len(sections)):
        print(f'{Colors.BRIGHT_RED}{sections[index]}{Colors.RESET}')
        for meaning in meanings[index]:
            source = meaning.get('source', '')
            part_of_speech = meaning.get('part_of_speech', '')
            synonym = meaning.get('synonym', '')
            translation = meaning.get('translation', '')
            example = meaning.get('example', '')
            example_translation = meaning.get('example_translation', '')
            print(f'{Colors.BRIGHT_CYAN}{source}{Colors.RESET} {Colors.BRIGHT_BLUE}{part_of_speech}{Colors.RESET} {synonym} {translation}')
            if example:
                print(f'{Colors.DARK_GRAY}{example}{Colors.RESET}')
            if example_translation:
                print(f'{Colors.DARK_GRAY}{example_translation}{Colors.RESET}')

if __name__ == "__main__":
    main()