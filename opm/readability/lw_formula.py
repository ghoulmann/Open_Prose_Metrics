from readability.utils import count_syllables

def linsear_write_formula(text):
    
    
    easy_word = 0
    difficult_word = 0
    word_tokens = text.split(" ")[10:109]
    #stokens.reverse()
    
    
    for word in word_tokens:
        if count_syllables(word) < 3:
            easy_word += 1
        else:
            difficult_word += 3
    sample = " ".join(word_tokens)
    sentences = sample.count(".")
    number = float(((easy_word) + (difficult_word)) / sentences+1)
    
    if number <= 20:
        number -= 2
    print(sentences, easy_word, difficult_word)
    return number / 2