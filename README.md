# Employee Attrition Prediction

Predict employee attrition using machine learning and visualize key factors that contribute to employee retention or turnover. This project is built with **Python**, **Flask**, and **Random Forest Classifier**.

---

## 📂 Project Structure

```
Employee-Attrition-Prediction/
│
├── Data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│
├── templates/
│   ├── index.html        # Input form page
│   └── result.html       # Result & visualization page
│
├── app.py                # Flask backend
├── train_model.py        # Model training & saving
├── model.pkl             # Saved Random Forest model
├── requirements.txt      # Python dependencies
└── README.md             # Project overview
```

---

## ⚡ Features

- Predict whether an employee is likely to leave the company.
- Input 8 important parameters:
  - Age
  - Monthly Income
  - Job Role
  - OverTime
  - Distance From Home
  - Job Satisfaction
  - Work Life Balance
  - Total Working Years
- Display probability of attrition using a **donut chart**.
- Visualize **feature importance** with a bar chart.
- Highlight **top 3 factors** influencing attrition with clear explanations.
- Clean and professional dashboard for HR analytics.

---

## 🛠 Technologies Used

- Python 3.x
- Flask
- pandas, scikit-learn, joblib
- Bootstrap 5
- Chart.js for interactive charts

---

## 🚀 How to Run

1. **Clone the repository**

```bash
git clone https://github.com/your-username/Employee-Attrition-Prediction.git
cd Employee-Attrition-Prediction
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Train the model** (optional, if `model.pkl` is already available)

```bash
python train_model.py
```

4. **Run the Flask app**

```bash
python app.py
```

5. **Open in browser**

Go to `http://127.0.0.1:5000` to access the input form.

---

## 🖼 Screenshots

**1. Input Form Page**

![Input Form](screenshots/home.png)

**2. Prediction Result Page**

![Prediction Result](screenshots/result.png)

---

## 📈 Model Details

- **Algorithm:** Random Forest Classifier
- **Selected Features:** 8 important attributes
- **Saved Model:** `model.pkl`
- **Visualization:** Feature importance, top influencing factors, and probability donut chart.

---

## 📌 Notes

- Ensure the CSV dataset is in the `Data/` folder.
- Make sure the names of job roles and other categorical values match those used during training.
- Charts are responsive and designed to be visually appealing for HR dashboards.
