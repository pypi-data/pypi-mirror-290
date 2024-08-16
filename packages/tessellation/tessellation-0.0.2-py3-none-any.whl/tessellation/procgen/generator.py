"""Base class for tesselation generators."""

from abc import ABC

import numpy as np


class Generator(ABC):
    """Base class for tesselation generators."""

    def generate(self, *args, **kwargs) -> np.ndarray:
        """Generate a new tesselation."""
        raise NotImplementedError

    @staticmethod
    def tessellate(mask: np.ndarray, n_shapes: int = 5) -> np.ndarray:
        """Tessellate the mask n_shapes times."""
        side_len = mask.shape[0]
        side_len_full_image = side_len * n_shapes
        tessellation = np.zeros((side_len_full_image, side_len_full_image), dtype=int)

        color = 0
        for i in range(n_shapes):
            for j in range(n_shapes):
                y_start = i * side_len
                y_end = y_start + side_len

                x_start = j * side_len
                x_end = x_start + side_len

                if color == 0:
                    color_mask = np.logical_not(mask)
                    color = 1
                else:
                    color_mask = mask
                    color = 0

                tessellation[y_start:y_end, x_start:x_end] = color_mask

        return tessellation
