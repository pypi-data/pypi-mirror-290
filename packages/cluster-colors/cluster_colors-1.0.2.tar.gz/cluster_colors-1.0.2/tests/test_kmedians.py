"""Test methods in KMedSupercluster

:author: Shay Hill
:created: 2023-03-14
"""

# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false

from typing import Annotated

import numpy as np
import numpy.typing as npt
import pytest

from cluster_colors.kmedians import KMedSupercluster
from cluster_colors.vector_stacker import stack_vectors

ColorsArray = Annotated[npt.NDArray[np.float_], (-1, 3)]

@pytest.fixture(
    scope="function",
    params=[np.random.randint(0, 255, (100, 4), dtype=np.uint8) for _ in range(10)],
)
def colors(request) -> ColorsArray:
    return stack_vectors(request.param)

class TestKMedians:
    def test_get_rsorted_clusters(self, colors: ColorsArray):
        """Test that the clusters are sorted by the number of colors in them"""
        clusters = KMedSupercluster.from_stacked_vectors(colors)
        clusters.split_to_delta_e(100/3)
        color_clusters = clusters.get_rsorted_clusters()

    def test_get_rsorted_exemplars(self, colors: ColorsArray):
        """Test that the clusters are sorted by the number of colors in them"""
        clusters = KMedSupercluster.from_stacked_vectors(colors)
        clusters.split_to_delta_e(100/3)
        colors = clusters.get_rsorted_exemplars()
