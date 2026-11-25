"""
Script ekstraksi sprite pixel-perfect dari concept art PhaseShift.
Memisahkan karakter murni dari label teks dan judul.
"""
from PIL import Image
import numpy as np
import os

def extract_sprites():
    src_path = "C:/PhaseShift/assets/characters_concept.jpg"
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img, dtype=np.float32)

    # Background color di sekitar (36, 39, 44)
    bg_color = np.array([36.0, 39.0, 44.0])
    diff = np.linalg.norm(arr[:, :, :3] - bg_color, axis=2)

    # Alpha mask halus
    alpha = np.clip((diff - 25.0) / (45.0 - 25.0) * 255.0, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha
    clean_img = Image.fromarray(arr.astype(np.uint8), mode="RGBA")

    # Ignis sprites: Y murni 55 s/d 240 (menghindari teks IGNIS di atas & teks label di bawah)
    ignis_boxes = [
        ("idle", (63, 55, 136, 240)),
        ("walk", (204, 55, 313, 240)),
        ("jump", (387, 55, 463, 240)),
        ("dash", (499, 55, 662, 240)),
        ("heat_stance", (694, 55, 848, 240)),
        ("fall", (886, 55, 981, 240)),
    ]

    # Cryo sprites: Y murni 340 s/d 505 (menghindari teks CRYO di atas & teks label di bawah)
    cryo_boxes = [
        ("idle", (56, 340, 142, 505)),
        ("walk", (192, 340, 337, 505)),
        ("jump", (388, 340, 473, 505)),
        ("dash", (545, 340, 674, 505)),
        ("frost_cast", (703, 340, 855, 505)),
        ("fall", (895, 340, 981, 505)),
    ]

    os.makedirs("C:/PhaseShift/assets/sprites/ignis", exist_ok=True)
    for name, box in ignis_boxes:
        crop = clean_img.crop(box)
        bbox = crop.getbbox()
        if bbox:
            crop = crop.crop(bbox)
        out_path = f"C:/PhaseShift/assets/sprites/ignis/{name}.png"
        crop.save(out_path)
        print(f"Ignis [{name:11s}]: {crop.size} -> {out_path}")

    os.makedirs("C:/PhaseShift/assets/sprites/cryo", exist_ok=True)
    for name, box in cryo_boxes:
        crop = clean_img.crop(box)
        bbox = crop.getbbox()
        if bbox:
            crop = crop.crop(bbox)
        out_path = f"C:/PhaseShift/assets/sprites/cryo/{name}.png"
        crop.save(out_path)
        print(f"Cryo  [{name:11s}]: {crop.size} -> {out_path}")

    print("Pixel-perfect sprite extraction successfully completed!")

if __name__ == "__main__":
    extract_sprites()
