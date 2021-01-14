# -*- coding: utf-8 -*-

import language_check

def main(full_text):
    tool = language_check.LanguageTool('en-US')
    text = full_text
    matches = tool.check(text)
    return len(matches), matches

if __name__ == "__main__":
    main(full_text)
