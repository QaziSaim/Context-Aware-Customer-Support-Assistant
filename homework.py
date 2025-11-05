results = list()
for _ in range(int(input('Enter The Number of instruction: '))):
    V = 0
    D = -1
    s1_input = int(input('enter s1 char: '))
    s1 = list(input('Enter S1 String: '))
    s2_input = int(input('enter s1 char: '))
    s2 = list(input('Enter S2 String: '))
    s3 = input('Enter The DV char: ').upper()
    if len(s3)==len(s2):
        for i in range(len(s3)):
            print(i)
            print(s2[i])
            if s3[i]=='V':
                s1.insert(1,s2[i])
            elif s3[i]=='D':
                s1.append(s2[i])
                s2.pop(i)
            print('output')
            print(s1)
    results.append("".join(s1))
for record in results:
    print(record)

