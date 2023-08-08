class Grandparent:
    grandparent_attribute = "I'm from Grandparent class"

    def spoketh(self, speak):
        print('what did you say!')


class Parent(Grandparent):
    parent_attribute = "I'm from Parent class"

    def spoken(self, speak):
        print(f'{speak} sounds too expensive')


class Grandchild(Parent):
    grandchild_attribute = "I'm from Grandchild class"

    def said(self, speak):
        print(f'{speak} sounds lame')


def find_unique_attributes(obj):
    cls = type(obj)
    unique_attributes = set(cls.__dict__.keys())
    for base in cls.__bases__:
        unique_attributes -= set(base.__dict__.keys())
    return unique_attributes


grandchild = Grandchild()
unique_attrs = find_unique_attributes(grandchild)

print(unique_attrs)  # Should print {'grandchild_attribute'}
