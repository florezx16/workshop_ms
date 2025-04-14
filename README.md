# 🛠️ workshop_ms – Workshop Management System

**workshop_ms** is a lightweight and easy-to-use system designed for small workshop owners and similar businesses to help them manage and control the key information of their daily operations.

Whether you want to track service orders, inventory movements, or keep supplier/customer records organized — this system helps you do it all from a single, clean interface.

---

## ✨ Key Features

- 📁 Centralized management of customers and suppliers
- 🧾 Service order lifecycle tracking: creation → diagnostics → repair → completed
- 📦 Full inventory control with movement history
- 📊 Dashboard with real-time widgets and business insights
- 🖨️ Exportable reports for service orders and inventory activity

---

## 🧩 Main Modules

### 📇 Assets
Store essential data about your **customers** and **suppliers**. Customers can be linked to service orders; suppliers are related to inventory codes.

### 🧾 Inventory Code Management
Create and manage all the product types or parts you want to track. These codes are used to build your actual inventory.

### 📦 Inventory & Movements
After defining inventory codes, you can load your **stock levels** and visualize how inventory gets **consumed or moved** across the system.

### 🔧 Service Orders
The heart of the app. Each service order moves through **up to 4 states**:
1. Created  
2. Diagnosed  
3. Repaired  
4. Completed/Cancelled  

You can upload related images at each stage, consume inventory parts, and **generate a final summary report** for each order.

---

## 📊 Dashboard Overview

- 👨‍🔧 Service orders in diagnosis or repair status
- ✅ Completed/cancelled orders from the last 90 days
- 🔄 Most recent inventory movements

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.9+
- pip

### 📥 Installation

```bash
git clone https://github.com/your-username/workshop_ms.git
cd workshop_ms
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🤝 Contributions

### Contributions are welcome and appreciated!

If you'd like to suggest an improvement, fix a bug, or add a feature:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request and describe your changes.

Please open an issue first to discuss major changes or ideas.


## 📝 License

This project is open-source and distributed under the **BSD 3-Clause License**.

Feel free to use, modify, and distribute it for personal or commercial purposes — just remember to give proper credit when applicable.
