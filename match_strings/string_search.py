
words = {
    "First words": [],
    "Second words": [],
}

def word_listing(word, key):
    i = 0

    while i < len(word):
        words[key].append(word[i])
        i += 1

    print "%s\n" % words[key]

print "Write some words"

word_listing(raw_input(), "First words")

print "Write words to compare to previous ones"

word_listing(raw_input(), "Second words")

if len(words["First words"]) > len(words["Second words"]):
    key_one = "First words"
    key_two = "Second words"
else:
    key_two = "First words"
    key_one = "Second words"

j = 0
matches = 0

while j < len(words[key_two]):
    if words[key_one][j] == words[key_two][j]:
        matches += 1
    j += 1

print "Matches: %r%s" % (matches * 100.0 / len(words[key_one]), " %")

