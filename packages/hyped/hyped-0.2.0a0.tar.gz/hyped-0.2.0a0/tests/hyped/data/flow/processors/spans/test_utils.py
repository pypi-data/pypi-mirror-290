from contextlib import nullcontext
from itertools import compress

import numpy as np
import pytest

from hyped.data.flow.processors.spans.utils import (
    ResolveOverlapsStrategy,
    compute_spans_overlap_matrix,
    resolve_overlaps,
)


def test_compute_spans_overlap_matrix():
    # test spans
    src_spans = [(0, 4), (5, 8), (15, 21)]
    tgt_spans = [(0, 4), (3, 7)]
    # expected overlap mask
    expected_mask = np.asarray([[True, True], [False, True], [False, False]])
    # test
    assert (
        compute_spans_overlap_matrix(src_spans, tgt_spans) == expected_mask
    ).all()


class TestResolveOverlaps:
    def resolve(self, spans, strategy):
        mask = resolve_overlaps(spans, strategy)
        return list(compress(spans, mask))

    @pytest.mark.parametrize(
        "spans, expected_err",
        [[[(2, 4), (5, 9)], None], [[(2, 7), (5, 9)], ValueError]],
    )
    def test_raise(self, spans, expected_err):
        with nullcontext() if expected_err is None else pytest.raises(
            expected_err
        ):
            self.resolve(spans, ResolveOverlapsStrategy.RAISE)

    @pytest.mark.parametrize(
        "spans, expected_spans",
        [
            [
                [(2, 4), (5, 9)],
                [(2, 4), (5, 9)],
            ],
            [
                [(2, 5), (5, 9)],
                [(2, 5), (5, 9)],
            ],
            [
                [(2, 6), (5, 9)],
                [(2, 6)],
            ],
            [
                [(5, 9), (2, 6)],
                [(5, 9)],
            ],
            [
                [(2, 6), (5, 9), (10, 13)],
                [(2, 6), (10, 13)],
            ],
            [
                [(2, 6), (10, 13), (5, 9)],
                [(2, 6), (10, 13)],
            ],
            [
                [(2, 6), (5, 9), (10, 13), (12, 17)],
                [(2, 6), (10, 13)],
            ],
            [
                [(2, 6), (7, 9), (10, 13), (1, 17)],
                [(2, 6), (7, 9), (10, 13)],
            ],
        ],
    )
    def test_keep_first(self, spans, expected_spans):
        assert (
            self.resolve(spans, ResolveOverlapsStrategy.KEEP_FIRST)
            == expected_spans
        )

    @pytest.mark.parametrize(
        "spans, expected_spans",
        [
            [
                [(2, 4), (5, 9)],
                [(2, 4), (5, 9)],
            ],
            [
                [(2, 5), (5, 9)],
                [(2, 5), (5, 9)],
            ],
            [
                [(2, 6), (5, 9)],
                [(5, 9)],
            ],
            [
                [(5, 9), (2, 6)],
                [(2, 6)],
            ],
            [
                [(2, 6), (5, 9), (10, 13)],
                [(5, 9), (10, 13)],
            ],
            [
                [(2, 6), (10, 13), (5, 9)],
                [(10, 13), (5, 9)],
            ],
            [
                [(2, 6), (5, 9), (10, 13), (12, 17)],
                [(5, 9), (12, 17)],
            ],
            [
                [(2, 6), (7, 9), (10, 13), (1, 17)],
                [(1, 17)],
            ],
        ],
    )
    def test_keep_last(self, spans, expected_spans):
        assert (
            self.resolve(spans, ResolveOverlapsStrategy.KEEP_LAST)
            == expected_spans
        )

    @pytest.mark.parametrize(
        "spans, expected_spans",
        [
            [
                [(2, 4), (5, 9)],
                [(2, 4), (5, 9)],
            ],
            [
                [(2, 5), (5, 9)],
                [(2, 5), (5, 9)],
            ],
            [
                [(2, 6), (3, 9)],
                [(3, 9)],
            ],
            [
                [(3, 9), (2, 6)],
                [(3, 9)],
            ],
            [
                [(2, 6), (3, 9), (10, 13)],
                [(3, 9), (10, 13)],
            ],
            [
                [(2, 6), (10, 13), (3, 9)],
                [(10, 13), (3, 9)],
            ],
            [
                [(2, 6), (3, 9), (10, 13), (12, 17)],
                [(3, 9), (12, 17)],
            ],
            [
                [(2, 6), (7, 9), (10, 13), (1, 17)],
                [(1, 17)],
            ],
        ],
    )
    def test_keep_largest(self, spans, expected_spans):
        assert (
            self.resolve(spans, ResolveOverlapsStrategy.KEEP_LARGEST)
            == expected_spans
        )

    @pytest.mark.parametrize(
        "spans, expected_spans",
        [
            [
                [(2, 4), (5, 9)],
                [(2, 4), (5, 9)],
            ],
            [
                [(2, 5), (5, 9)],
                [(2, 5), (5, 9)],
            ],
            [
                [(2, 6), (3, 9)],
                [(2, 6)],
            ],
            [
                [(3, 9), (2, 6)],
                [(2, 6)],
            ],
            [
                [(2, 6), (3, 9), (10, 13)],
                [(2, 6), (10, 13)],
            ],
            [
                [(2, 6), (10, 13), (3, 9)],
                [(2, 6), (10, 13)],
            ],
            [
                [(2, 6), (3, 9), (10, 13), (12, 17)],
                [(2, 6), (10, 13)],
            ],
            [
                [(2, 6), (7, 9), (10, 13), (1, 17)],
                [(2, 6), (7, 9), (10, 13)],
            ],
        ],
    )
    def test_keep_smallest(self, spans, expected_spans):
        assert (
            self.resolve(spans, ResolveOverlapsStrategy.KEEP_SMALLEST)
            == expected_spans
        )
