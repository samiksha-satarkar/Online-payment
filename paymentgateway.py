import qrcode
from tkinter import *
from tkinter import Frame, Label, Entry, Button, messagebox
from PIL import ImageTk, Image
import os
import re

# Function to validate UPI ID
def is_valid_upi_id(upi_id):
    # Basic UPI ID validation pattern
    pattern = r'^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$'
    return re.match(pattern, upi_id) is not None

# Function to validate amount
def is_valid_amount(amount):
    try:
        amt = float(amount)
        return amt > 0
    except ValueError:
        return False

# Function to generate QR codes
def generate_qr():
    upi_id = upi_entry.get().strip()
    amount = amount_entry.get().strip()

    # Validation
    if not upi_id or not amount:
        result_label.config(text="Please enter both UPI ID and Amount.", fg="red")
        return
    
    if not is_valid_upi_id(upi_id):
        result_label.config(text="Please enter a valid UPI ID (e.g., username@paytm)", fg="red")
        return
    
    if not is_valid_amount(amount):
        result_label.config(text="Please enter a valid amount (positive number).", fg="red")
        return

    try:
        # UPI URLs
        phonepe_url = f'upi://pay?pa={upi_id}&am={amount}&cu=INR&tn=Payment%20via%20PhonePe'
        paytm_url = f'upi://pay?pa={upi_id}&am={amount}&cu=INR&tn=Payment%20via%20Paytm'
        google_pay_url = f'upi://pay?pa={upi_id}&am={amount}&cu=INR&tn=Payment%20via%20Google%20Pay'

        # Generate QR codes
        phonepe_qr = qrcode.QRCode(version=1, box_size=10, border=5)
        phonepe_qr.add_data(phonepe_url)
        phonepe_qr.make(fit=True)
        phonepe_img = phonepe_qr.make_image(fill_color="black", back_color="white")

        paytm_qr = qrcode.QRCode(version=1, box_size=10, border=5)
        paytm_qr.add_data(paytm_url)
        paytm_qr.make(fit=True)
        paytm_img = paytm_qr.make_image(fill_color="black", back_color="white")

        google_pay_qr = qrcode.QRCode(version=1, box_size=10, border=5)
        google_pay_qr.add_data(google_pay_url)
        google_pay_qr.make(fit=True)
        gpay_img = google_pay_qr.make_image(fill_color="black", back_color="white")

        # Save QR codes
        phonepe_img.save("phonepe_qr.png")
        paytm_img.save("paytm_qr.png")
        gpay_img.save("google_pay_qr.png")

        # Display QR codes
        phonepe_display = ImageTk.PhotoImage(phonepe_img.resize((150, 150)))
        paytm_display = ImageTk.PhotoImage(paytm_img.resize((150, 150)))
        gpay_display = ImageTk.PhotoImage(gpay_img.resize((150, 150)))

        phonepe_label.config(image=phonepe_display)
        phonepe_label.image = phonepe_display

        paytm_label.config(image=paytm_display)
        paytm_label.image = paytm_display

        gpay_label.config(image=gpay_display)
        gpay_label.image = gpay_display

        # Show labels for each QR code
        phonepe_text.config(text="PhonePe")
        paytm_text.config(text="Paytm")
        gpay_text.config(text="Google Pay")

        result_label.config(text="QR Codes Generated Successfully!", fg="green")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")
        print(f"Error generating QR codes: {e}")

# GUI setup
root = Tk()
root.title("UPI Payment QR Generator")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Header
header_label = Label(root, text="UPI QR Code Generator", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
header_label.pack(pady=15)

# Input frame
input_frame = Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

Label(input_frame, text="UPI ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
upi_entry = Entry(input_frame, width=35, font=("Arial", 11))
upi_entry.grid(row=0, column=1, padx=10, pady=5)

Label(input_frame, text="Amount (₹):", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
amount_entry = Entry(input_frame, width=35, font=("Arial", 11))
amount_entry.grid(row=1, column=1, padx=10, pady=5)

# Example label
example_label = Label(root, text="Example: username@paytm, 9876543210@ybl", 
                     font=("Arial", 9), fg="gray", bg="#f0f0f0")
example_label.pack(pady=5)

# Generate button
generate_btn = Button(root, text="Generate QR Codes", command=generate_qr, 
                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                     width=20, height=2, cursor="hand2")
generate_btn.pack(pady=15)

# Result label
result_label = Label(root, text="", font=("Arial", 11), bg="#f0f0f0")
result_label.pack(pady=5)

# QR codes frame
qr_frame = Frame(root, bg="#f0f0f0")
qr_frame.pack(pady=20)

# QR code labels
phonepe_label = Label(qr_frame, bg="#f0f0f0")
phonepe_label.grid(row=0, column=0, padx=15)

paytm_label = Label(qr_frame, bg="#f0f0f0")
paytm_label.grid(row=0, column=1, padx=15)

gpay_label = Label(qr_frame, bg="#f0f0f0")
gpay_label.grid(row=0, column=2, padx=15)

# Text labels for QR codes
phonepe_text = Label(qr_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0")
phonepe_text.grid(row=1, column=0, pady=5)

paytm_text = Label(qr_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0")
paytm_text.grid(row=1, column=1, pady=5)

gpay_text = Label(qr_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0")
gpay_text.grid(row=1, column=2, pady=5)

# Instructions
instructions = Label(root, text="Scan the QR code with respective payment app to make payment", 
                    font=("Arial", 9), fg="gray", bg="#f0f0f0")
instructions.pack(side=BOTTOM, pady=10)

if __name__ == "__main__":
    print("UPI QR Generator started!")
    root.mainloop()