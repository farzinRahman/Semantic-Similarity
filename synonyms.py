'''Semantic Similarity: 

Starter code provided by Michael Guerzhoy. The following functions implemented by Farzin: cosine_similarity(vec1, vec2), build_semantic_descriptors(sentences), build_semantic_descriptors_from_files(filenames), most_similar_word(word, choices, semantic_descriptors, similarity_fn), run_similarity_test(filename, semantic_descriptors, similarity_fn) functions 
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)



def cosine_similarity(vec1, vec2):
    ''' Return the cosine similarity between the sparse vectors vec1 and vec2 stored as dictionaries '''

    num = 0
    vec1sum = norm(vec1)
    vec2sum = norm(vec2)

    for word, number in vec1.items():
        if word in vec2:
            num += number * vec2[word]

    return num / (vec1sum * vec2sum)


def build_semantic_descriptors(sentences):
    ''' Given a list <sentences> containing lists of strings (words), return a dictionary such that for every word w that appears in at least one of the sentences, d[w] is itself a dictionary which represents the semantic descriptor of w. '''


    d = {}

    for sentence in sentences:
        for word in sentence:
            if word not in d:
                d[word] = {}

    for sentence in sentences:
        for i in range(len(sentence)):
            for j in range(len(sentence)):
                if sentence[j] != sentence[i]:
                    if sentence[j] not in d[sentence[i]]:
                        d[sentence[i]][sentence[j]] = 1
                    else:
                        d[sentence[i]][sentence[j]] += 1

    return d


def build_semantic_descriptors_from_files(filenames):
    ''' Given a list of <filenames> (strings containing file names), return a dictionary of the semantic descriptors of all the words in the files <filenames> with the files treated as a single text.
    Assume that only [".", "!", "?"] separate sentences, while these are the only punctuations present in the entire text: [",", "-", "--", ":", ";"]
    '''

    text = []

    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="UTF-8")
        text += f.read().lower().replace("!", ".").replace("?", ".").replace("\n", ".").split(".")


    for i in range(len(text)):
        text[i] = text[i].replace(",", " ").replace("-", " ").replace("--", " ").replace(":", " ").replace(";", " ").split()

    return build_semantic_descriptors(text)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    ''' Given a string <word>, a list of strings <choices>, a <semantic_descriptors> dictionary, and the <similarity_fn> function, return the choices[i] which has the largest semantic similarity to <word>.
    If the semantic similarity between two words cannot be computed, the value of semantic similarity = -1.
    In case of a tie between several choices[i], return the choices[i] at the smallest index.
    '''

    if word in semantic_descriptors:
        word_desc = semantic_descriptors[word]
    else:
        word_desc = {}

    choices_desc = {}
    for choice in choices:
        if choice in semantic_descriptors:
            choices_desc[choice] = semantic_descriptors[choice]
        else:
            choices_desc[choice] = {}


    similarity_value = {}
    for w, desc in choices_desc.items():
        if desc == {} or word_desc == {}:
            similarity_value[w] = -1
        else:
            similarity_value[w] = similarity_fn(desc, word_desc)


    cur_max = 0
    cur_leading = ''

    for word, value in similarity_value.items():
        cur_max = value
        cur_leading = word
        break

    for w, value in similarity_value.items():
        if value > cur_max:
            cur_max = value
            cur_leading = w


    return cur_leading


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''
    Given a <string> filename in the same format as test.txt, a <semantic_descriptor>, and a <similarity_fn>, return the percentage (float between 0.0 and 100.0) of questions on which the function most_similar_word() guesses the answer correctly
    '''

    f = open(filename, "r", encoding="UTF-8")
    text = f.read().split("\n")


    for i in range(len(text)):
        text[i] = text[i].split()

    # text[i][0] = word
    # text[i][1] = most_similar_word
    # text[i][2:] = choices

    exp_ans_count = 0
    cor_ans_count = 0

    for i in range(len(text)):
        cor_ans_count += 1
        exp_answer = most_similar_word(text[i][0], text[i][2:], semantic_descriptors, similarity_fn)

        if exp_answer == text[i][1]:
            exp_ans_count += 1


    return (exp_ans_count / cor_ans_count) * 100


if __name__ == '__main__':

    print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))
    print(cosine_similarity({"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}, {"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}))


    underground = [["i", "am", "a", "sick", "man"],
    ["i", "am", "a", "spiteful", "man"],
    ["i", "am", "an", "unattractive", "man"],
    ["i", "believe", "my", "liver", "is", "diseased"],
    ["however", "i", "know", "nothing", "at", "all", "about", "my", "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]

    print(build_semantic_descriptors(underground))
    print("============================")

    build_semantic_descriptors_from_files(["test.txt", "lt.txt"])
    print("============================")

    word = "alone"
    choices = ["thief", "talk", "clean", "lonely"]
    semantic_desc = build_semantic_descriptors_from_files(["test.txt"])
    print(most_similar_word(word, choices, semantic_desc, cosine_similarity))
    print("============================")

    import timeit

    print(timeit.timeit('build_semantic_descriptors_from_files(["wp.txt"])', globals = globals(), number=3))

    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])

    # print(sem_descriptors)

    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")

    # sem_descriptors2 = build_semantic_descriptors_from_files(["sw.txt"])
    # res2 = run_similarity_test("test.txt", sem_descriptors2, cosine_similarity)
    # print(res, "of the guesses were correct")
    #
    # sem_descriptors3 = build_semantic_descriptors_from_files(["lt.txt"])
    # res2 = run_similarity_test("test.txt", sem_descriptors3, cosine_similarity)
    # print(res, "of the guesses were correct")




