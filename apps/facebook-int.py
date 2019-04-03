import sys
def superDigit(n):
    if len(n) <=1:
        return int(n)
    res=0
    for num in n:
        res+=int(num)
    return superDigit(str(res))
if __name__ == "__main__":
    n, k = raw_input().strip().split(' ')
    n, k = [str(n), int(k)]
    cad = n*k
    result = superDigit(cad)
    print result
import fileinput
arr = list()
lines= raw_input().strip()
print(lines)
for line in range(int(lines)):
    print(line)
    arr.append(line)
    arr.append(line.replace('\n',''))
for digit in sorted(arr):
    print(int(digit))
import fileinput
def heap(lines):
    if lines <= 1:
        print lines
        return
    for line in range(int(lines)):
        arr.append(raw_input().strip())
    arr.append(lines)
    for digit in sorted(set(arr)):
        print(int(digit))
        pass
    return
if __name__ == "__main__":
    arr = list()
    lines = raw_input().strip()
    heap(lines)
