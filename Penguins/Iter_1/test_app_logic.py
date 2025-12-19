import unittest

from app import (
    filter_data,
    describe_data,
    unique_data,
    ColumnNotFoundError,
    MissingArgumentError,
    InvalidNumberError,
    NotNumericColumnError,
)


class TestFilterData(unittest.TestCase):
    def setUp(self):
        self.data = [
            ["Adelie", "181", "39.1", "18.1", "3750", "Torgersen", "F"],
            ["Chinstrap", "195", "50.0", "19.8", "3800", "Biscoe", "M"],
            ["Adelie", "190", "40.5", "17.5", "4000", "Dream", "F"],
            ["Gentoo", "217", "50.3", "19.0", "5000", "Biscoe", "M"],
        ]

    def test_filter_string_column(self):
        res = filter_data(["filter", "species", "Adelie"], self.data)
        self.assertEqual(len(res), 2)
        self.assertTrue(all(row[0] == "Adelie" for row in res))

    def test_filter_numeric_column(self):
        res = filter_data(["filter", "body_mass_g", "4500"], self.data)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0], "Gentoo")

    def test_filter_invalid_numeric_value(self):
        with self.assertRaises(InvalidNumberError):
            filter_data(["filter", "body_mass_g", "not_a_number"], self.data)

    def test_filter_missing_args(self):
        with self.assertRaises(MissingArgumentError):
            filter_data(["filter"], self.data)

    def test_filter_unknown_column(self):
        with self.assertRaises(ColumnNotFoundError):
            filter_data(["filter", "unknown_col", "x"], self.data)


class TestDescribeData(unittest.TestCase):
    def setUp(self):
        self.data = [
            ["A", "10", "0", "0", "100", "I", "M"],
            ["B", "11", "0", "0", "200", "I", "F"],
            ["C", "12", "0", "0", "300", "I", "M"],
        ]

    def test_describe_valid(self):
        minimum, maximum, average = describe_data(["describe", "body_mass_g"], self.data)
        self.assertEqual(minimum, 100.0)
        self.assertEqual(maximum, 300.0)
        self.assertAlmostEqual(average, 200.0)

    def test_describe_non_numeric_column(self):
        with self.assertRaises(NotNumericColumnError):
            describe_data(["describe", "species"], self.data)

    def test_describe_missing_column(self):
        with self.assertRaises(ColumnNotFoundError):
            describe_data(["describe", "nope"], self.data)

    def test_describe_missing_arg(self):
        with self.assertRaises(MissingArgumentError):
            describe_data(["describe"], self.data)

    def test_describe_no_numeric_values(self):
        data = [
            ["A", "x", "0", "0", "NA", "I", "M"],
            ["B", "y", "0", "0", "NA", "I", "F"],
        ]
        res = describe_data(["describe", "body_mass_g"], data)
        self.assertIsNone(res)


class TestUniqueData(unittest.TestCase):
    def setUp(self):
        self.data = [
            ["Adelie", "181", "...", "...", "100", "I", "F"],
            ["Adelie", "182", "...", "...", "150", "I", "M"],
            ["Gentoo", "200", "...", "...", "250", "I", "M"],
        ]

    def test_unique_counts(self):
        res = unique_data(["unique", "species"], self.data)
        self.assertEqual(res, {"Adelie": 2, "Gentoo": 1})

    def test_unique_missing_arg(self):
        with self.assertRaises(MissingArgumentError):
            unique_data(["unique"], self.data)

    def test_unique_unknown_column(self):
        with self.assertRaises(ColumnNotFoundError):
            unique_data(["unique", "unknown"], self.data)


if __name__ == "__main__":
    unittest.main()
