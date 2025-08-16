from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def get_exif_data(image_path):
    """Extrae los metadatos EXIF de una imagen."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if not exif_data:
            return "No se encontraron metadatos EXIF."

        metadata = {}

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            
            # Manejar datos GPS de forma separada
            if tag == "GPSInfo":
                gps_data = {}
                for key in value:
                    sub_tag = GPSTAGS.get(key, key)
                    gps_data[sub_tag] = value[key]
                metadata["GPSInfo"] = gps_data
            else:
                metadata[tag] = value

        return metadata

    except Exception as e:
        return f"Error al leer la imagen: {e}"

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = "imagen.jpg"  # Cambia esto por la ruta de tu imagen
    exif = get_exif_data(ruta_imagen)

    if isinstance(exif, dict):
        for clave, valor in exif.items():
            print(f"{clave}: {valor}")
    else:
        print(exif)
