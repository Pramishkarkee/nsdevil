# Attendance System Documentation

## Overview

The Attendance System is designed to manage and track student attendance in academic classes. It provides functionalities to record attendance and visualize data. This system is built using Django and Django REST Framework (DRF), with features including a web-based interface, API endpoints, and data visualization.

## Features
- **Attendance Recording**: Track attendance for students in various classes.
- **Data Visualization**: Display attendance data using graphs.

## Installation

### Prerequisites

- Python 3.10
- Django==5.0.6
- Django REST Framework 3.x
- Other dependencies listed in `requirements.txt`

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone git@github.com:Pramishkarkee/nsdevil.git
   cd nsdevil
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver or make serve
   ```

## Usage

### Web Interface

1. **Access the Admin Interface**

   Go to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

2. **Manage Students and Classes**

   Navigate to the Student and AcademicClass sections to add or update records.

3. **Record Attendance**

   Use the Attendance section to mark attendance for students.

### API Endpoints

#### **Weekly Report**

- **Endpoint**: `/api/v1/dashboard/?time_period=Week & academic_class=041e9b36-aed7-4f85-adba-364ca8943742`
- **Method**: `GET`
- **Description**: Retrieve a weekly attendance report.

#### **Monthly Report**

- **Endpoint**: `/api/v1/dashboard/?time_period=Monthely & academic_class=041e9b36-aed7-4f85-adba-364ca8943742`
- **Method**: `GET`
- **Description**: Retrieve a monthly attendance report.

## Data Visualization

### **Charts and Graphs**

The system uses Chart.js for visualizing attendance data. The charts include:

- **Weekly Attendance Chart**: Shows attendance counts per week.
- **Monthly Attendance Chart**: Displays attendance counts per month.

### **Integration**

To integrate the visualizations, include Chart.js in your HTML templates and pass data from Django views to the frontend.

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  var ctx = document.getElementById('attendanceChart').getContext('2d');
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
      datasets: [{
        label: 'Attendance Count',
        data: [10, 20, 15, 25],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
</script>
```




## Contact

For any questions or issues, please contact [karkipramish18@gmail.com].
