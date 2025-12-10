import io
import base64
import qrcode
from PIL import Image, ImageDraw, ImageFont


class ImageService:

    def generate_stamped_document(self,
                                  original_b64: str,
                                  verification_url: str,
                                  is_verified: bool = True) -> str:

        img_data = base64.b64decode(original_b64)
        base_image = Image.open(io.BytesIO(img_data)).convert("RGBA")
        width, height = base_image.size

        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(verification_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white").convert("RGBA")

        qr_size = int(width * 0.15)
        qr_img = qr_img.resize((qr_size, qr_size))

        stamp_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(stamp_layer)

        if is_verified:
            stamp_text = "e-HASTAAKSHAR VERIFIED"
            draw.text((width - 300, height - 100), stamp_text, fill=(0, 255, 0, 128))

        padding = 50
        qr_position = (width - qr_size - padding, height - qr_size - padding)

        base_image.paste(qr_img, qr_position, mask=qr_img)

        final_image = Image.alpha_composite(base_image, stamp_layer)

        buffered = io.BytesIO()
        final_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


image_processor = ImageService()