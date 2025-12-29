def input_string():
    user = input("Enter a string: ")
    return user

def count_words(s):
    words = s.split()
    return len(words)

def word_count(s):
    words = s.split()
    dict_words = {}
    for word in words:
        word = word.lower()
        if word in dict_words:
            dict_words[word] += 1
        else:
            dict_words[word] = 1
    
    for word,count in dict_words.items():
        print(f"'{word}': {count}")

def characters_count(s):
    return len(s)

def count_characters(s):
    dict_chars = {}
    for char in s:
        
        if not char.isalnum():
            continue  # skip spaces, 

        if (char in dict_chars):
            dict_chars[char] += 1
        else:
            dict_chars[char] = 1
    
    for char,count in dict_chars.items():
        print(f"'{char}': {count}")

def main():
    user_string = input_string()
    print(f"Total words: {count_words(user_string)}")
    print("Word frequencies:")
    word_count(user_string)
    print(f"Total characters: {characters_count(user_string)}")
    print("Character frequencies:")
    count_characters(user_string)

if __name__ == "__main__":
    main()