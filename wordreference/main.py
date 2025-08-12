from wordreference.wordreference import *
from wordreference.cli import *

def main():
    args = get_args()
    brief_mode = args.brief

    for word in args.words:
        dictionary = get_dictionary(word)

        error = dictionary.get('error')
        if error:
            print(f'{Colors.BRIGHT_RED}在 WordReference 英-汉词典中，没有发现 \'{args.word}\' 的翻译{Colors.RESET}')
            return

        uk_pronunciation = dictionary['pronunciation'].get('uk', '')
        us_pronunciation = dictionary['pronunciation'].get('us', '')
        sections = dictionary.get('sections', [])
        meanings = dictionary.get('meanings', [])
        print(f'{Colors.BRIGHT_YELLOW}{word}{Colors.RESET}{Colors.YELLOW}{' UK ' + uk_pronunciation if uk_pronunciation else ''}{' US ' + us_pronunciation if us_pronunciation else ''}{Colors.RESET}')

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
                if example and not brief_mode:
                    print(f'{Colors.DARK_GRAY}{example}{Colors.RESET}')
                if example_translation and not brief_mode:
                    print(f'{Colors.DARK_GRAY}{example_translation}{Colors.RESET}')

if __name__ == "__main__":
    main()