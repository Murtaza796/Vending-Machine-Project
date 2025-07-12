# gpaycodetest.py
import qrcode
import os
import cv2
import webbrowser
import time
from pyzbar.pyzbar import decode
from multiprocessing import Process
from flask import Flask, render_template, request, jsonify
import stripe

# ---------------------- FLASK SERVER SETUP ----------------------


def run_flask_app():
    app = Flask(__name__)
    balance = {}

    stripe.api_key = 'sk_test_51PYWS0RrMhyZ8aXWVMHPDRM7O0dVOUag74NA5wh8ICWoLOsiFZob93BwLxUen9SjSUNJU6eWC95I0NNAiXDc0MvF00NRsKKBp7'

    @app.route("/")
    def index():
        return "<h1>Scan the QR to Pay</h1>"

    @app.route("/pay")
    def pay():
        machine_id = request.args.get("machine_id")
        amount = int(request.args.get("amount", 0))
        balance[machine_id] = amount
        return render_template("pay.html", machine_id=machine_id, amount=amount)

    @app.route('/payment')
    def payment():
        chips = request.args.get("chips", 0)
        juice = request.args.get("juice", 0)
        biscuit = request.args.get("biscuit", 0)
        chocolate = request.args.get("chocolate", 0)
        return render_template('payment.html', chips=chips, juice=juice, biscuit=biscuit, chocolate=chocolate)

    @app.route("/create-checkout-session", methods=["POST"])
    def create_checkout_session():
        try:
            data = request.get_json()
            amount = int(data.get('amount', 0))
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {'name': 'Smart Vending Machine Items'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:5000/payment?chips=20&juice=40&biscuit=10&chocolate=15',
                cancel_url='http://localhost:5000/pay?machine_id=123&amount=0',
            )
            return jsonify({'id': session.id})
        except Exception as e:
            return jsonify(error=str(e)), 500

    @app.route("/verify")
    def verify():
        machine_id = request.args.get("machine_id")
        if balance.get(machine_id, 0) > 0:
            balance[machine_id] = 0
            return render_template("verify.html", success=True)
        else:
            return render_template("verify.html", success=False)

    app.run(debug=False, use_reloader=False)

# ---------------------- MAIN PROGRAM ----------------------


if __name__ == "__main__":
    # Start Flask server in background
    flask_process = Process(target=run_flask_app)
    flask_process.start()

    # Give the server time to start
    time.sleep(2)

    # Create QR code
    amount = 0
    os.makedirs("qr_codes", exist_ok=True)
    url = f"http://localhost:5000/pay?machine_id=123&amount={amount}"
    img = qrcode.make(url)
    img.save("qr_codes/machine_qr.png")
    print("QR code saved successfully in qr_codes/machine_qr.png")

    # Start QR Scanner
    cap = cv2.VideoCapture(0)
    print("Launching QR scanner (simulating GPay)...")
    print("Press 'q' to quit scanning after QR is detected.\n")

    qr_data_found = None
    while True:
        success, frame = cap.read()
        for qr in decode(frame):
            qr_data = qr.data.decode('utf-8')
            print(f"\nQR Code Detected: {qr_data}")
            cv2.putText(frame, qr_data, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            qr_data_found = qr_data
        cv2.imshow("Simulated GPay QR Scanner", frame)
        if cv2.waitKey(1) == ord('q') or qr_data_found:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Open payment page
    if qr_data_found:
        webbrowser.open(qr_data_found)

    # Optional: stop Flask process when done
    # flask_process.terminate()
