#Install library
#pip install qrcode[pil]
import qrcode
from PIL import Image
website_address = "https://www.gambilldataengineering.com/data-sphere"
logo = "D:/android.png"
# Create a QR code for a website
qr = qrcode.make(website_address)

# Save the QR code as an image file
qr.save("D:/GambillContact.png")

#QR code with custom image
# Step 1: Create a QR code
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code: higher numbers mean bigger size
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Allows for a higher error tolerance
    box_size=10,  # Size of the box where each pixel is drawn
    border=4,  # Thickness of the border
)

# Step 2: Add data to the QR code
qr.add_data(website_address)
qr.make(fit=True)

# Step 3: Create an image of the QR code
qr_code_image = qr.make_image(fill='black', back_color='white').convert('RGB')

# Step 4: Open your logo image and resize it
logo = Image.open(logo)

# Calculate the size based on the QR code size
qr_width, qr_height = qr_code_image.size
logo_size = int(qr_width / 4)  # Logo should be smaller than the QR code

# Resize the logo
logo = logo.resize((logo_size, logo_size))

# Step 5: Calculate position for the logo and paste it on the QR code
logo_position = (
    (qr_width - logo_size) // 2,  # X coordinate
    (qr_height - logo_size) // 2  # Y coordinate
)
qr_code_image.paste(logo, logo_position, mask=logo)  # Use mask for transparency

# Step 6: Save the final QR code with the logo
qr_code_image.save('D:/GDE_qr_code_with_logo.png')