def retfive():
    return 5


def itertest(lst):
    for x in lst:
        print(x)
        retfive()


def retnone():
    print('this will return nothing')


def testlist(lst):
    i = 0
    while i < len(lst):
        print(lst[i])
        if i == 3:
            i = i + 3
        else:
            i = i + 1


from dataclasses import dataclass


@dataclass
class DocStatus:
    ok = True


def testnums(x):
    for num in x:
        try:
            good = num <= 6
            if not good:
                raise RuntimeError('bad number, runtime error')
            print(f'{num} is good')

        except RuntimeError:
            print('except RuntimeError')


def ret_none():
    print('this is returning none...')
    return


print('wowee')

l1 = [1, 2, 3]
l1.append(4)
print(l1)

 # add a list of numbers
 def 