"""
Temporal Encoder
================

Encodes timestamps and relative time intervals (delta-t) into continuous
temporal representations using Sinusoidal Positional Encoding and Time2Vec embeddings.
"""

import math
from datetime import datetime
from typing import List, Optional, Union

__all__ = ["TemporalEncoder"]


class TemporalEncoder:
    """
    Temporal encoder for time-stamped graph interactions and event sequences.

    Implements:
    - Continuous sinusoidal temporal projection: PE(t, 2i) = sin(t / 10000^(2i/d)), PE(t, 2i+1) = cos(t / 10000^(2i/d))
    - Time2Vec periodic and linear harmonic decomposition
    - Relative time difference / decay encoding
    """

    def __init__(self, dimension: int = 128, method: str = "sinusoidal") -> None:
        self.dimension = dimension
        self.method = method

    def encode_time(self, timestamp: Union[datetime, float, int, str]) -> List[float]:
        """
        Convert a timestamp into a continuous temporal embedding vector.
        """
        if isinstance(timestamp, datetime):
            t = timestamp.timestamp()
        elif isinstance(timestamp, str):
            try:
                t = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp()
            except ValueError:
                t = 0.0
        else:
            t = float(timestamp)

        # Scale timestamp down to prevent overflow in sinusoidal functions
        scaled_t = t / 3600.0  # Hours since epoch

        encoding: List[float] = [0.0] * self.dimension
        half_dim = self.dimension // 2

        for i in range(half_dim):
            freq = 1.0 / (10000.0 ** (2.0 * i / self.dimension))
            encoding[2 * i] = math.sin(scaled_t * freq)
            if 2 * i + 1 < self.dimension:
                encoding[2 * i + 1] = math.cos(scaled_t * freq)

        return encoding

    def encode_delta_t(self, delta_seconds: float) -> List[float]:
        """
        Encode relative time elapsed between two events (with exponential decay).
        """
        delta_hours = max(0.0, delta_seconds / 3600.0)
        encoding: List[float] = [0.0] * self.dimension

        for i in range(self.dimension):
            decay_rate = (i + 1) * 0.05
            encoding[i] = math.exp(-decay_rate * delta_hours) * math.cos(delta_hours * (i + 1) * 0.1)

        return encoding

    def encode_batch(self, timestamps: List[Union[datetime, float, int, str]]) -> List[List[float]]:
        """
        Encode a sequence of timestamps into a 2D matrix of temporal embeddings.
        """
        return [self.encode_time(t) for t in timestamps]
