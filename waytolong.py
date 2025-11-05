words = list()
for i in range(int(input())):
    words.append(input())
def solution():
    for word in words:
        first_char,last_char=word[0],word[-1]
        if len(word)<=4:
            print(word)
        else:
            count=0
            for _ in range(len(word[1:-1])):
                count+=1
            print(first_char+str(count)+last_char)
solution()