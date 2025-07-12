// server.js
const express = require('express');
const Stripe = require('stripe');
const cors = require('cors');

const app = express();
const stripe = Stripe('sk_test_51PYWS0RrMhyZ8aXWVMHPDRM7O0dVOUag74NA5wh8ICWoLOsiFZob93BwLxUen9SjSUNJU6eWC95I0NNAiXDc0MvF00NRsKKBp7'); // replace with your secret test key

app.use(cors());
app.use(express.json());

app.post('/create-checkout-session', async (req, res) => {
    try {
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card', 'upi', 'google_pay'],
            line_items: [
                {
                    price_data: {
                        currency: 'inr',
                        product_data: {
                            name: 'Sample Product',
                        },
                        unit_amount: 5000, // ₹50
                    },
                    quantity: 1,
                },
            ],
            mode: 'payment',
            success_url: 'https://yourdomain.com/success',
            cancel_url: 'https://yourdomain.com/cancel',
        });

        res.json({ id: session.id });
    } catch (error) {
        console.error('Stripe error:', error);
        res.status(500).json({ error: error.message });
    }
});

app.listen(4242, () => console.log('Server running on http://localhost:4242'));



