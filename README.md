# Cold-Chain Expiry Accelerator

A web-based inventory management system for temperature-sensitive products with dynamic shelf-life adjustment based on storage conditions.

## Features

- **Product Management**: Add, edit, delete, and view products
- **Batch Management**: Track multiple batches per product
- **Temperature Logging**: Record storage temperatures with automatic shelf-life adjustment
- **Dynamic Expiration**: Automatically recalculate expiration dates based on temperature violations
- **Dashboard**: Visual overview of inventory status
- **Reports**: Generate and export inventory reports

## Technology Stack

- **Backend**: Python 3.x, Flask, SQLAlchemy
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create MySQL database:
   ```sql
   CREATE DATABASE cold_chain_db;
   ```

5. Copy `.env.example` to `.env` and configure your database credentials

6. Initialize the database:
   ```bash
   python init_db.py
   ```

7. Run the application:
   ```bash
   python app.py
   ```

8. Access the application at `http://localhost:5000`

## Project Structure

```
cold-chain-expiry-accelerator/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── models/                 # Database models
├── routes/                 # Route handlers
├── services/               # Business logic
├── utils/                  # Utility functions
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
└── requirements.txt        # Python dependencies
```

## Database Schema

- **Products**: Store product information including temperature thresholds
- **Batches**: Track individual product batches with expiration dates
- **Temperature_Logs**: Record temperature checks and adjustments

## Usage

1. **Add Products**: Define products with their temperature requirements
2. **Create Batches**: Add batches with manufacturing and expiration dates
3. **Log Temperatures**: Record storage temperatures during inspections
4. **Monitor Dashboard**: View real-time inventory status
5. **Check Expiring Products**: Review products nearing expiration
6. **Generate Reports**: Export inventory data

## Business Rules

- When logged temperature exceeds maximum safe temperature:
  - Penalty days = (temperature difference) × 0.5
  - Adjusted expiration date is reduced by penalty days
  - Original expiration date remains unchanged for reference

## License

MIT License
