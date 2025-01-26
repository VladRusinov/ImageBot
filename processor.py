import numpy as np
from PIL import Image


class ImageProcessor:
    def __init__(self, img):
        self.image = self.convert_image_to_array(img)
        self.grayscale_image = None
        self.result_image = None

    def convert_image_to_array(self, img):
        return np.array(Image.open(img))

    def convert_image_from_array(self):
        return Image.fromarray(self.result_image)

    def to_grayscale(self):
        if len(self.image.shape) == 3:  # Проверка на цветное изображение
            # Усреднение для преобразования в градации серого
            self.grayscale_image = np.mean(
                self.image[:, :, :3], axis=2
            ).astype(np.uint8)
        else:
            self.grayscale_image = self.image

    def apply_laplacian(self):
        laplacian_mask = np.array([[0, 1, 0],
                                   [1, -4, 1],
                                   [0, 1, 0]])
        padded_image = np.pad(
            self.grayscale_image, 1, mode='constant', constant_values=0
        )
        rows, cols = self.grayscale_image.shape
        result = np.zeros_like(self.grayscale_image)

        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                region = padded_image[i-1:i+2, j-1:j+2]
                result[i-1, j-1] = abs(np.sum(region * laplacian_mask))

        self.result_image = np.clip(result, 0, 255).astype(np.uint8)
