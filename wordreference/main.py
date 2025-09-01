import sys

from wordreference.wordreference import *
from wordreference.cli import *

def main():
    args = get_args()
    brief_mode = args.brief

    if args.filename:
        output_stream = open(args.filename, 'w', encoding='utf-8')
        colors = NoColors()
    else:
        colors = Colors()
        output_stream = sys.stdout

    for word in args.words:
        dictionary = get_dictionary(word)

        error = dictionary.get('error')
        if error:
            print(f'{colors.BRIGHT_RED}在 WordReference 英-汉词典中，没有发现 \'{word}\' 的翻译{colors.RESET}', file=output_stream)
            return

        uk_pronunciation = dictionary['pronunciation'].get('uk', '')
        us_pronunciation = dictionary['pronunciation'].get('us', '')
        sections = dictionary.get('sections', [])
        meanings = dictionary.get('meanings', [])
        print(f'{colors.BRIGHT_YELLOW}{word}{colors.RESET}{colors.YELLOW}{' UK ' + uk_pronunciation if uk_pronunciation else ''}{' US ' + us_pronunciation if us_pronunciation else ''}{colors.RESET}', file=output_stream)

        for index in range(len(sections)):
            print(f'{colors.BRIGHT_RED}{sections[index]}{colors.RESET}', file=output_stream)
            for meaning in meanings[index]:
                source = meaning.get('source', '')
                part_of_speech = meaning.get('part_of_speech', '')
                synonym = meaning.get('synonym', '')
                translation = meaning.get('translation', '')
                example = meaning.get('example', '')
                example_translation = meaning.get('example_translation', '')
                print(f'{colors.BRIGHT_CYAN}{source}{colors.RESET} {colors.BRIGHT_BLUE}{part_of_speech}{colors.RESET} {synonym} {translation}', file=output_stream)
                if example and not brief_mode:
                    print(f'{colors.DARK_GRAY}{example}{colors.RESET}', file=output_stream)
                if example_translation and not brief_mode:
                    print(f'{colors.DARK_GRAY}{example_translation}{colors.RESET}', file=output_stream)

        print('', file=output_stream)

if __name__ == "__main__":
    main()
