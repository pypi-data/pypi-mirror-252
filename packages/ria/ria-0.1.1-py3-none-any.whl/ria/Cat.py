"""
The `Cat` module provides a simple representation of a verbose cat.

Classes:
    - Cat: A class representing a cat.

Examples:

Creating and using a Cat instance::

    from cats import Cat

    my_cat = Cat(name="Whiskers", age=3, color="gray")
    my_cat.meow()  # Output: "Whiskers says meow"

"""


class Cat:
    """
    A class representing a cat.

    :ivar name: The name of the cat.
    :vartype name: str
    :ivar age: The age of the cat in years.
    :vartype age: int
    :ivar color: The color of the cat's fur.
    :vartype color: str
    """

    def __init__(self, name: str, age: int, color: str):
        """
        Initialize a new Cat instance.

        :param name: The name of the cat.
        :type name: str
        :param age: The age of the cat in years.
        :type age: int
        :param color: The color of the cat's fur.
        :type color: str
        """
        self.name = name
        self.age = age
        self.color = color

    def meow(self, times: int = 1) -> None:
        """
        Print out meows.

        :param times: The number of times the cat will meow. Default is 1.
        :type times: int

        :return: None
        """
        print(f"{self.name} says {'meow ' * times}")
