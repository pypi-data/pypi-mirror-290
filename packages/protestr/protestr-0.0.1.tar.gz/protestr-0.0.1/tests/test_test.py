import unittest
from protestr import provide, resolve
from protestr.specs import between, sequence, either, subset
import json


class TestTest(unittest.TestCase):
    @provide(
        # anything
        int, float, complex, str,

        # specify keyword args
        bounded_int=between(-20, 20),
        bounded_real=between(-20.0, 20.0)
    )
    def test_anything(
        intgr, real, complx, word,

        # match keyword args
        bounded_int,
        bounded_real
    ):
        pass

    @provide(
        # any number of any things
        people=sequence(
            each={
                # limit possibilities
                "first name": either("John", "Jane", "Joe"),
                "last name": either("Doe", "Smith"),
                "hobbies": subset(
                    ("cycling", "swimming", "testing with protestr"),
                    n=2
                ),

                # generate both keys and values
                "metadata": {
                    "password": str,
                    str: str
                }
            },

            # describe the sequence size
            n=between(1, 5),

            # optionally, cast to some sequence type
            type=list
        )
    )
    def test_more(people):
        # also, resolve manually if you need to
        indent = resolve(either(2, 4))
        print(f"people={json.dumps(people, indent=indent)}")
#       [
#           {
#               "first name": "Joe",
#               "last name": "Doe",
#               "hobbies": [
#                   "cycling",
#                   "testing with protestr"
#               ],
#               "metadata": {
#                   "password": "nFvgELbMptWisGdIDgQ",
#                   "EzUnRmbjxBTzQDFLjXyXCngaIz": "sOQZTiGXzXapAwoztrdCKSQwmCaTYaK"
#               }
#           },
#           {
#               "first name": "Jane",
#               "last name": "Smith",
#               "hobbies": [
#                   "swimming",
#                   "testing with protestr"
#               ],
#               "metadata": {
#                   "password": "qczkMMUzgEshkpMfPkbhmSQTgb",
#                   "spMfiBZauonqASJeuWNcYaXTkNvACqIaRiXOkrXqhpBWMtBui": "MJwtFAnlIRpjJOFKVxDqVL"
#               }
#           }
#       ]

    # protestr also supports all things callable, so you can write your
    # own fixtures and provide those in your tests

    # write your own fixture
    @provide(lat=between(-90, 90), lon=between(-180, 180))
    def location(lat, lon):
        return lat, lon

    # then provide the new fixture all the same
    @provide(location)
    def test_loc(loc):
        pass


if __name__ == "__main__":
    unittest.main()
