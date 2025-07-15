# Vending-Machine-Project
A working project of how a vending machine works.
In order to execute this project:
 the "gpaycodetest.py" is the maim file which is supposed to be executed first, where we create our port on where the web browser is hosted, then it generates a qr code by itseld, and stores it to the "qrcodes" folder as an image, it also opens a webcam automatically on its own
 then, we take a picture of the scanner and show it to the webcam, which will scan and take you directly to the website,
 we can purchase our items and make payment on the same page.
 all the libraries required to run the "gpaycodetest.py" file are:
 | Library Name      | Purpose                                 | Install Command             |
| ----------------- | --------------------------------------- | --------------------------- |
| `qrcode`          | To generate QR codes                    | `pip install qrcode[pil]`   |
| `os`              | Built-in – used for file system ops     | ✅ No installation needed    |
| `cv2`             | OpenCV – to capture and read video      | `pip install opencv-python` |
| `webbrowser`      | Built-in – opens URLs in browser        | ✅ No installation needed    |
| `time`            | Built-in – to delay/sleep               | ✅ No installation needed    |
| `pyzbar`          | For decoding QR codes                   | `pip install pyzbar`        |
| `multiprocessing` | Built-in – to run Flask in a subprocess | ✅ No installation needed    |
| `flask`           | Web framework for backend               | `pip install flask`         |
| `stripe`          | For handling payments via Stripe        | `pip install stripe`        |

the order of folders and files stored:
your-project-folder/

│
├── gpaycodetest.py               # Main Python script to run everything
│
├── qr_codes/                     # Folder to store generated QR code images
│   └── machine_qr.png            # Generated QR code image
│
├── templates/                    # Flask HTML templates go here
│   ├── pay.html                  # Payment page with QR scan and amount
│   ├── payment.html              # After successful payment, item details shown
│   └── verify.html               # Shows success or failure of payment


