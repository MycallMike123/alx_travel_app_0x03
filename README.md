# README.md (excerpt)

## Payment Integration via Chapa

1. Create a Chapa account at https://developer.chapa.co/ and get your secret key.
2. Set environment variables:
   ```bash
   export CHAPA_SECRET_KEY="your_chapa_secret_key"
   export PAYMENT_CALLBACK_URL="https://your-domain.com/api/payments/verify/"
   export PAYMENT_RETURN_URL="https://your-domain.com/bookings/confirmation/"
    ```
3. Apply migrations:
    ```bash
    python manage.py makemigrations listings
    python manage.py migrate
    ```

4. Initiate payment:
    ```bash
    POST /api/payments/initiate/  {
        "booking": "<booking_uuid>",
        "amount": 100.00,
        "currency": "USD"
    }
    ```

5. Verify payment:
    ```bash
    POST /api/payments/verify/  {
        "transaction_id": "<chapa_tx_id>"
    }
    ```
