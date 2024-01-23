from typing import Dict, List, Tuple

import numpy as np
import torch


class Bbox:
    def __init__(self, *, x1: int, y1: int, x2: int, y2: int):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def scale(self, factor: float):
        return Bbox(
            x1=int(self.x1 * factor),
            y1=int(self.y1 * factor),
            x2=int(self.x2 * factor),
            y2=int(self.y2 * factor))

    def move(self, *, dx: int, dy: int):
        return Bbox(
            x1=self.x1 + dx,
            y1=self.y1 + dy,
            x2=self.x2 + dx,
            y2=self.y2 + dy)

    @property
    def area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    @property
    def tensor(self):
        return torch.tensor([self.x1, self.y1, self.x2, self.y2])

    @property
    def dict(self):
        return {
            'xmin': self.x1,
            'ymin': self.y1,
            'xmax': self.x2,
            'ymax': self.y2}

    def __str__(self):
        return str(self.dict)

    @staticmethod
    def from_dict(bb: Dict):
        return Bbox(
            x1=bb['xmin'],
            y1=bb['ymin'],
            x2=bb['xmax'],
            y2=bb['ymax'])

    @staticmethod
    def from_tensor(bb: torch.Tensor):
        x1, y1, x2, y2 = bb.tolist()
        return Bbox(x1=x1, y1=y1, x2=x2, y2=y2)

    @staticmethod
    def from_xyxy(bb: List[int]):
        x1, y1, x2, y2 = bb
        return Bbox(x1=x1, y1=y1, x2=x2, y2=y2)

    @staticmethod
    def from_xywh(bb: List[float]):
        x, y, w, h = bb
        return Bbox(x1=int(x), y1=int(y), x2=int(x + w), y2=int(y + h))

    @staticmethod
    def from_xyxyxyxy(bb: np.ndarray):
        assert bb.shape == (4, 2), f'Expected (4, 2), got {bb.shape}'
        x1, y1 = bb.min(axis=0)
        x2, y2 = bb.max(axis=0)

        return Bbox(x1=x1, y1=y1, x2=x2, y2=y2)

    @staticmethod
    def from_yolo(bb: List[float], img_size: Tuple[int, int]):
        assert len(bb) == 4, f'Expected 4 values, got {bb}'
        width, height = img_size
        cx, cy, w, h = bb
        return Bbox(
            x1=int((cx - w / 2) * width),
            y1=int((cy - h / 2) * height),
            x2=int((cx + w / 2) * width),
            y2=int((cy + h / 2) * height))
