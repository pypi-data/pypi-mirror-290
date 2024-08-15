#!/usr/bin/env python3

import unittest

import torch

from linear_operator.test.utils import approx_equal
from linear_operator.utils.interpolation import left_interp, left_t_interp


class TestInterp(unittest.TestCase):
    def setUp(self):
        self.interp_indices = torch.tensor([[2, 3], [3, 4], [4, 5]], dtype=torch.long).repeat(3, 1)
        self.interp_values = torch.tensor([[1, 2], [0.5, 1], [1, 3]], dtype=torch.float).repeat(3, 1)
        self.interp_indices_2 = torch.tensor([[0, 1], [1, 2], [2, 3]], dtype=torch.long).repeat(3, 1)
        self.interp_values_2 = torch.tensor([[1, 2], [2, 0.5], [1, 3]], dtype=torch.float).repeat(3, 1)
        self.batch_interp_indices = torch.cat([self.interp_indices.unsqueeze(0), self.interp_indices_2.unsqueeze(0)], 0)
        self.batch_interp_values = torch.cat([self.interp_values.unsqueeze(0), self.interp_values_2.unsqueeze(0)], 0)
        self.interp_matrix = torch.tensor(
            [
                [0, 0, 1, 2, 0, 0],
                [0, 0, 0, 0.5, 1, 0],
                [0, 0, 0, 0, 1, 3],
                [0, 0, 1, 2, 0, 0],
                [0, 0, 0, 0.5, 1, 0],
                [0, 0, 0, 0, 1, 3],
                [0, 0, 1, 2, 0, 0],
                [0, 0, 0, 0.5, 1, 0],
                [0, 0, 0, 0, 1, 3],
            ],
            dtype=torch.float,
        )

        self.batch_interp_matrix = torch.tensor(
            [
                [
                    [0, 0, 1, 2, 0, 0],
                    [0, 0, 0, 0.5, 1, 0],
                    [0, 0, 0, 0, 1, 3],
                    [0, 0, 1, 2, 0, 0],
                    [0, 0, 0, 0.5, 1, 0],
                    [0, 0, 0, 0, 1, 3],
                    [0, 0, 1, 2, 0, 0],
                    [0, 0, 0, 0.5, 1, 0],
                    [0, 0, 0, 0, 1, 3],
                ],
                [
                    [1, 2, 0, 0, 0, 0],
                    [0, 2, 0.5, 0, 0, 0],
                    [0, 0, 1, 3, 0, 0],
                    [1, 2, 0, 0, 0, 0],
                    [0, 2, 0.5, 0, 0, 0],
                    [0, 0, 1, 3, 0, 0],
                    [1, 2, 0, 0, 0, 0],
                    [0, 2, 0.5, 0, 0, 0],
                    [0, 0, 1, 3, 0, 0],
                ],
            ],
            dtype=torch.float,
        )

    def test_left_interp_on_a_vector(self):
        vector = torch.randn(6)

        res = left_interp(self.interp_indices, self.interp_values, vector)
        actual = torch.matmul(self.interp_matrix, vector)
        self.assertTrue(approx_equal(res, actual))

    def test_left_t_interp_on_a_vector(self):
        vector = torch.randn(9)

        res = left_t_interp(self.interp_indices, self.interp_values, vector, 6)
        actual = torch.matmul(self.interp_matrix.mT, vector)
        self.assertTrue(approx_equal(res, actual))

    def test_batch_left_interp_on_a_vector(self):
        vector = torch.randn(6)

        actual = torch.matmul(self.batch_interp_matrix, vector.unsqueeze(-1).unsqueeze(0)).squeeze(-1)
        res = left_interp(self.batch_interp_indices, self.batch_interp_values, vector)
        self.assertTrue(approx_equal(res, actual))

    def test_batch_left_t_interp_on_a_vector(self):
        vector = torch.randn(9)

        actual = torch.matmul(self.batch_interp_matrix.mT, vector.unsqueeze(-1).unsqueeze(0)).squeeze(-1)
        res = left_t_interp(self.batch_interp_indices, self.batch_interp_values, vector, 6)
        self.assertTrue(approx_equal(res, actual))

    def test_left_interp_on_a_matrix(self):
        matrix = torch.randn(6, 3)

        res = left_interp(self.interp_indices, self.interp_values, matrix)
        actual = torch.matmul(self.interp_matrix, matrix)
        self.assertTrue(approx_equal(res, actual))

    def test_left_t_interp_on_a_matrix(self):
        matrix = torch.randn(9, 3)

        res = left_t_interp(self.interp_indices, self.interp_values, matrix, 6)
        actual = torch.matmul(self.interp_matrix.mT, matrix)
        self.assertTrue(approx_equal(res, actual))

    def test_batch_left_interp_on_a_matrix(self):
        batch_matrix = torch.randn(6, 3)

        res = left_interp(self.batch_interp_indices, self.batch_interp_values, batch_matrix)
        actual = torch.matmul(self.batch_interp_matrix, batch_matrix.unsqueeze(0))
        self.assertTrue(approx_equal(res, actual))

    def test_batch_left_t_interp_on_a_matrix(self):
        batch_matrix = torch.randn(9, 3)

        res = left_t_interp(self.batch_interp_indices, self.batch_interp_values, batch_matrix, 6)
        actual = torch.matmul(self.batch_interp_matrix.mT, batch_matrix.unsqueeze(0))
        self.assertTrue(approx_equal(res, actual))

    def test_batch_left_interp_on_a_batch_matrix(self):
        batch_matrix = torch.randn(2, 6, 3)

        res = left_interp(self.batch_interp_indices, self.batch_interp_values, batch_matrix)
        actual = torch.matmul(self.batch_interp_matrix, batch_matrix)
        self.assertTrue(approx_equal(res, actual))

    def test_batch_left_t_interp_on_a_batch_matrix(self):
        batch_matrix = torch.randn(2, 9, 3)

        res = left_t_interp(self.batch_interp_indices, self.batch_interp_values, batch_matrix, 6)
        actual = torch.matmul(self.batch_interp_matrix.mT, batch_matrix)
        self.assertTrue(approx_equal(res, actual))


if __name__ == "__main__":
    unittest.main()
