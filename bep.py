from collections import defaultdict
from collections import Counter


def learn_bpe(corpus, num_merges=3):
    vocab = defaultdict(int)

    for sentence in corpus.split(' '):
        words = sentence.strip().split()
        for word in words:
            chars = ['<'] + list(word) + ['>']
            for i in range(len(chars) - 1):
                pair = (chars[i], chars[i+1])
                vocab[pair] += 1
    
    merges = []
    for _ in range(num_merges):
        if not vocab:
            break        
        most_frequent = max(vocab, key = lambda x: vocab[x])
        merges.append(most_frequent)

        new_char = ''.join(most_frequent)
        new_vocab = defaultdict(int)
        for pair in vocab:
            count = vocab[pair]
            if pair == most_frequent:
                continue
            new_pair = list(pair)

            if pair == most_frequent[0] and new_pair[1] == most_frequent[1]:
                new_pair[0] == new_char
                new_pair.pop(1)
            new_vocab[tuple(new_pair)] += count
        old_vocab = vocab
        vocab = new_vocab
    return merges
    # return vocab #try it later 
print(learn_bpe('Hello There'))

merges = []
