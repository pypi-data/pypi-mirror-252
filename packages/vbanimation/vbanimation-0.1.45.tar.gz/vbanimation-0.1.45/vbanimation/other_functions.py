def chunk_words(s, n):
    words = s.split()
    return [' '.join(words[i:i+n]) for i in range(0, len(words), n)]

