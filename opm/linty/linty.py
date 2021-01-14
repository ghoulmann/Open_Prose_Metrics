from proselint.tools import lint
'''
handle proselint
'''
def lint_text(text):
    #print(type(text))
    lint_results = []
    suggestions = lint(str(text))
    for s in suggestions:
        #print(type(s))
        excerpt = " ..." + str(text[s[4]-15:s[5]+15]) + "..."
        while "\n\n" in excerpt:
            excerpt = excerpt.replace("\n\n", "  ")
        while "  " in excerpt:
            excerpt = excerpt.replace("  ", " ")
        lint_results.append((s[0], s[1][:-1], excerpt))
    return lint_results
