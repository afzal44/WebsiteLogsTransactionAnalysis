# calo-assessment-task

## Implementation Details
- This project processes transaction logs to generate reports on subscriber balances, identifying discrepancies and overdrafts.

## Technology Choices
- Python was chosen as the primary programming language due to its extensive libraries for data analysis and machine learning.
- pandas was used for data manipulation and preprocessing.
- scikit-learn was used for implementing the Isolation Forest algorithm for anomaly detection.
- StandardScaler from scikit-learn was used for data standardization.

## Future Improvements
- Integration with real-time data streams for continuous monitoring and detection of anomalies.
- Implementation of advanced anomaly detection techniques, such as deep learning-based methods, for improved accuracy.
- Development of a user-friendly dashboard for visualizing anomalies and reconciliation results.
- Incorporation of feedback mechanisms to improve the accuracy and effectiveness of the automated system over time.
- Enhance log parsing to handle more complex log structures.
- Implement more robust error handling and logging.
- Integrate with a database for better data management.
- Add support for more output formats (e.g., CSV, PDF).

## Step-by-Step Solution
### Step 1: Parse and Load Log Data

We'll use Python to parse the log data and extract the transaction details.

### Step 2: Identify Overdrafts

We'll filter transactions where the new balance is negative.

### Step 3: Identify Discrepancies

We'll compare the subscription balance and payment balance from the errors dataset.

### Step 4: Generate Reports

We'll generate an Excel file containing the parsed transactions, overdrafts, and discrepancies.

### Step 5: Dockerize the Solution

We'll create a Dockerfile to containerize the solution.
## Project Structure

- `app/main.py`: Main script for parsing logs and generating reports.
- `app/requirements.txt`: Python dependencies.
- `app/Dockerfile`: Docker configuration.
- `logs/`: Sample log files directory.
- `reports/`: Directory for generated reports.

## Usage

1. Ensure Docker is installed on your machine.
2. Build the Docker image:
   ```sh
   docker build -t calo_balance_sync .
   ```
3. Run the Docker container:
   ```sh
   docker run -v $(pwd)/logs:/app/logs -v $(pwd)/reports:/app/reports calo_balance_sync
   ```
4. The reports will be generated in the `reports` directory.


