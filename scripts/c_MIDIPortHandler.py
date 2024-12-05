import mido
import time
import pandas as pd
import keyboard

# Clase para manejar puertos MIDI y envío de notas
class MIDIPortHandler:
    def __init__(self, csv_file, blue_delay, green_delay, red_delay):
        # Inicializa y abre los puertos MIDI
        print("Abriendo puertos MIDI...")
        self.blue_port = mido.open_output('loopMIDI Port 1')
        self.green_port = mido.open_output('loopMIDI Port 1 2')
        self.red_port = mido.open_output('loopMIDI Port 2 3')

        # Ejecuta el envío de notas al inicializar la clase
        print("Enviando notas MIDI desde el archivo...")
        self.send_midi_notes(csv_file, blue_delay, green_delay, red_delay)

        # Cierra los puertos MIDI al finalizar
        print("Cerrando puertos MIDI...")
        self.close_midi_ports()

    def print_output_ports(self):
        print("Puertos de salida disponibles:")
        print(mido.get_output_names())

    def send_midi_notes(self, csv_file, blue_delay, green_delay, red_delay):
        # Lee el archivo CSV con pandas
        midi_data = pd.read_csv(csv_file)

        # Itera sobre las filas del DataFrame
        for _, row in midi_data.iterrows():
            blue_midi_note = int(row['Blue MIDI'])
            green_midi_note = int(row['Green MIDI'])
            red_midi_note = int(row['Red MIDI'])

            # Crea mensajes MIDI para cada nota
            blue_msg = mido.Message('note_on', note=blue_midi_note, velocity=80)
            green_msg = mido.Message('note_on', note=green_midi_note, velocity=60)
            red_msg = mido.Message('note_on', note=red_midi_note, velocity=80)

            # Envía los mensajes MIDI a los puertos correspondientes
            self.blue_port.send(blue_msg)
            time.sleep(blue_delay)
            self.green_port.send(green_msg)
            time.sleep(green_delay)
            self.red_port.send(red_msg)
            time.sleep(red_delay)

            # Detener si se presiona la tecla "Esc"
            if keyboard.is_pressed('esc'):
                print("Detenido por el usuario.")
                break

    def close_midi_ports(self):
        self.blue_port.close()
        self.green_port.close()
        self.red_port.close()
        print("Puertos MIDI cerrados correctamente.")
