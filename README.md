# Calo Logs Transaction Analysis

## Implementation Details

### Overview

The Calo Logs Transaction Analysis project aims to provide insights into subscriber transaction data captured by the Calo system. It involves parsing transaction logs, identifying trends, detecting anomalies, and presenting the findings through a web interface.

### Technologies Used

- Python: The primary programming language used for data analysis, plotting, and web development.
- Flask: A lightweight web framework for Python used to create the web application.
- Pandas: A powerful data manipulation library in Python used for processing and analyzing transaction data.
- Matplotlib & Seaborn: Python libraries used for data visualization, including creating plots and charts.
- HTML/CSS: Used for structuring and styling the web interface.
- Jinja2: A templating engine for Python used with Flask to generate HTML content dynamically.
Implementation Choices
- Flask: Chosen for its simplicity and flexibility, Flask allows for rapid development of web applications and integrates seamlessly with Python.
- Matplotlib & Seaborn: These libraries provide comprehensive tools for creating various types of plots, enabling effective visualization of transaction data.
- Pandas: Ideal for data manipulation and analysis tasks, Pandas simplifies tasks such as grouping, filtering, and aggregating transaction data.
- HTML/CSS: Used to create a user-friendly web interface for viewing transaction analysis results.

### Future Improvements

- Enhance log parsing to handle more complex log structures.
- Implement more robust error handling and logging.
- Integrate with a database for better data management.
- User Authentication: Implement user authentication to restrict access to sensitive transaction data.
- Integration with real-time data streams for continuous monitoring and detection of anomalies.
- Development of a user-friendly dashboard for visualizing anomalies and reconciliation results.
- Interactive Visualization: Enhance the web interface with interactive plots and charts for better data exploration.
- Real-Time Data Updates: Implement mechanisms to update transaction data and analysis results in real-time.
- Optimization: Optimize data processing and visualization algorithms to improve performance, especially for large datasets.
- Alerting System: Integrate an alerting system to notify administrators of potential anomalies or issues in transaction data.
- Data Export Options: Provide options to export transaction analysis results in different formats such as CSV or Excel.
- Incorporation of feedback mechanisms to improve the accuracy and effectiveness of the automated system over time.
- Implementation of advanced anomaly detection techniques, such as deep learning-based methods, for improved accuracy.


## Step-by-Step Solution

### Step 1: Understand the Logs and Data Structure

- Parse the logs to extract relevant information such as transaction details, user balances, and error messages.
- Identify key events like balance updates and discrepancies.
- We'll use Python to parse the log data and extract the transaction details.

### Step 2: Identify Overdrafts

- Filter transactions where the new balance is negative.

### Step 3: Identify Discrepancies

- Compare the subscription balance and payment balance from the errors dataset.

### Step 4: Generate Reports

- Use Python for parsing logs and generating reports.
- Export the reports to Excel for easy viewing by non-technical users.
- Generate an Excel file containing the parsed transactions, overdrafts, and discrepancies.

### Step 5: Dockerize the Solution

- Create a Dockerfile to containerize the solution.
  
## Project Structure

- `app/main.py`: Main script for parsing logs and generating reports.
- `app/requirements.txt`: Python dependencies.
- `app/Dockerfile`: Docker configuration.
- `logs/`: Sample log files directory.
- `reports/`: Directory for generated reports.

## Usage

1. Ensure Docker is installed on your machine.
2. Ensure Git in installed in you machine
3. Git clone.

   ```sh
   git clone https://github.com/afzal44/calo-assessment-task.git
   cd calo-assessment-task
   docker build -t calo_balance_sync .
   docker run -v $(pwd)/logs:/app/logs -v $(pwd)/reports:/app/reports -p 5000:5000 calo_balance_sync
   ```

