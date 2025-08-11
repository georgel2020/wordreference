import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Get word meaning from WordReference')
    parser.add_argument('word', help='word to get Chinese meaning')
    return parser.parse_args()