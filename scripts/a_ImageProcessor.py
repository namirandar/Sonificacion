import numpy as np
import cv2
import pandas as pd

# Clase para manejar imágenes y análisis de canales
class ImageProcessor:
    def __init__(self, image_path, threshold, num_points, nir_wavelength_range, mir_wavelength_range, output_csv):
        # Inicializa la imagen
        self.image, self.image_normalized = self.load_image(image_path)
        self.blue_channel = self.image_normalized[:, :, 0]
        self.green_channel = self.image_normalized[:, :, 1]
        self.red_channel = self.image_normalized[:, :, 2]
        
        # Crea la máscara de luz y genera los puntos
        self.mask = self.create_light_mask(threshold)
        self.grid_points = self.generate_points_in_mask(self.mask, num_points)

        # Guarda los puntos en el archivo CSV
        self.save_points_to_csv(self.grid_points, nir_wavelength_range, mir_wavelength_range, output_csv)

        # Muestra la imagen con los puntos generados
        self.show_image_with_points(self.grid_points)

    def load_image(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        img_normalized = img.astype(np.float32) / 255.0
        return img, img_normalized

    def create_light_mask(self, threshold):
        avg_intensity = (self.blue_channel + self.green_channel + self.red_channel) / 3
        mask = avg_intensity > threshold
        return mask

    def generate_points_in_mask(self, mask, num_points):
        valid_points = np.column_stack(np.where(mask))
        np.random.shuffle(valid_points)
        selected_points = valid_points[:num_points]
        return [(int(x), int(y)) for y, x in selected_points]

    def show_image_with_points(self, grid_points):
        for point in grid_points:
            cv2.circle(self.image, point, 5, (0, 255, 0), -1)
        img_resized = cv2.resize(self.image, (1000, int(1000 * self.image.shape[0] / self.image.shape[1])))
        cv2.imshow('Imagen con Puntos Muestreados', img_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_points_to_csv(self, grid_points, nir_wavelength_range, mir_wavelength_range, output_file):
        data = []
        for idx, point in enumerate(grid_points):
            x, y = point
            blue_wavelength = self.calculate_wavelength(self.blue_channel[y, x], (400, 700))
            green_wavelength = self.calculate_wavelength(self.green_channel[y, x], nir_wavelength_range)
            red_wavelength = self.calculate_wavelength(self.red_channel[y, x], mir_wavelength_range)
            data.append({
                "ID": idx + 1,
                "X": x,
                "Y": y,
                "Blue Wavelength (nm)": blue_wavelength,
                "Green Wavelength (nm)": green_wavelength,
                "Red Wavelength (nm)": red_wavelength
            })

        # Convierte la lista de datos a un DataFrame y guárdalo como CSV
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8')

    def calculate_wavelength(self, channel, wavelength_range):
        channel_intensity = np.mean(channel)
        min_wavelength, max_wavelength = wavelength_range
        wavelength = min_wavelength + (channel_intensity * (max_wavelength - min_wavelength))
        return wavelength
