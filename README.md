# alx_travel_app_0x02 for learning purpose
# ALX Travel App – Chapa Payment Integration API

This project demonstrates how to integrate the [Chapa](https://chapa.co/) payment gateway into the `alx_travel_app` Django REST Framework application. It allows users to initiate and verify payments for travel bookings using Chapa’s secure API.

---

## Features

- **Initiate Payment:** Start a payment process and get a checkout URL from Chapa.
- **Verify Payment:** Confirm the status of a payment after user completes the process.
- **Payment Model:** Stores transaction details and status in the database.
- **Secure:** Uses Chapa secret key and callback URL for secure transactions.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/alx_travel_app.git
cd alx_travel_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Chapa Settings

Add the following to your `settings.py`:

```python
CHAPA_SECRET_KEY = "your_chapa_secret_key"
CHAPA_INITIALIZE_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_CALLBACK_URL = "https://yourdomain.com/api/payment-callback/"
```

Replace with your actual Chapa credentials and callback URL.

### 4. Add `listings` to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...
    'listings',
    'rest_framework',
]
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## API Endpoints

### 1. Initiate Payment

**POST** `/api/initiate_payment/`

**Request Body:**
```json
{
  "amount": "100.00",
  "booking_reference": "ABC123"
}
```

**Response:**
```json
{
  "checkout_url": "https://checkout.chapa.co/..."
}
```

### 2. Verify Payment

**POST** `/api/verify-payment/`

**Request Body:**
```json
{
  "transaction_reference": "the-tx-ref-from-initiate"
}
```

**Response (Success):**
```json
{
  "message": "Payment verified successfully",
  "data": { ... }
}
```

**Response (Failure):**
```json
{
  "message": "Payment verification failed",
  "data": { ... }
}
```

---

## How It Works

1. **User initiates a payment** via `/api/initiate_payment/`.
2. **App sends payment data** to Chapa and receives a `checkout_url`.
3. **User completes payment** on Chapa’s site.
4. **App verifies payment** via `/api/verify-payment/` using the transaction reference.
5. **Payment status is updated** in the database.

---

## Developer Notes

- Make sure your Chapa secret key is kept safe and never exposed publicly.
- The `Payment` model stores all transaction details and can be extended as needed.
- Use Django admin to view and manage payments.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](LICENSE)


