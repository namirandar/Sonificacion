import numpy as np
import pandas as pd

# Clase para convertir longitudes de onda a notas MIDI
class WavelengthToMIDIConverter:
    def __init__(self, csv_file_path, output_csv_path):
        # Realiza la conversión automáticamente
        self.midi_notes = self.convert_wavelengths_to_midi(csv_file_path)
        self.save_midi_notes_to_csv(output_csv_path)

    def wavelength_to_frequency(self, wavelength):
        speed_of_light = 3e8
        frequency = speed_of_light / (wavelength * 1e-9)
        return frequency

    def frequency_to_midi(self, frequency):
        if frequency <= 0:
            return None
        midi_note = 69 + 12 * np.log2(frequency / 880)
        return round(midi_note)

    def convert_wavelengths_to_midi(self, csv_file_path):
        data = pd.read_csv(csv_file_path)
        midi_notes = []

        for index, row in data.iterrows():
            blue_wavelength = row['Blue Wavelength (nm)']
            green_wavelength = row['Green Wavelength (nm)']
            red_wavelength = row['Red Wavelength (nm)']

            blue_midi = self.wavelength_to_midi(blue_wavelength, "blue")
            green_midi = self.wavelength_to_midi(green_wavelength, "green")
            red_midi = self.wavelength_to_midi(red_wavelength, "red")

            midi_notes.append({
                'ID': row['ID'],
                'X': row['X'],
                'Y': row['Y'],
                'Blue MIDI': blue_midi,
                'Green MIDI': green_midi,
                'Red MIDI': red_midi
            })
        return midi_notes

    def wavelength_to_midi(self, wavelength, color):
        if color == "blue":
            frequency = self.map_wavelength_to_frequency(wavelength, 400, 900, 60, 16000)
        elif color == "green":
            frequency = self.map_wavelength_to_frequency(wavelength, 800, 1400, 60, 16000)
        elif color == "red":
            frequency = self.map_wavelength_to_frequency(wavelength, 1000, 25000, 60, 16000)
        else:
            return None
        return self.frequency_to_midi(frequency)
        
    def map_wavelength_to_frequency(self, wavelength, min_wavelength, max_wavelength, min_freq, max_freq):
        return np.interp(wavelength, [min_wavelength, max_wavelength], [min_freq, max_freq])

    def save_midi_notes_to_csv(self, output_file_path):
        midi_df = pd.DataFrame(self.midi_notes)
        midi_df.to_csv(output_file_path, index=False)
        print(f"Conversión completa. Notas MIDI guardadas en '{output_file_path}'.")