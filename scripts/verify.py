import mido

# Verificar los puertos de salida disponibles
for port_name in mido.get_output_names():
    print(port_name)