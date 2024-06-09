# calo-assessment-task

## Implementation Details
- This project processes transaction logs to generate reports on subscriber balances, identifying discrepancies and overdrafts.
### Data Collection
- Data was collected from two sources: transaction logs and error logs.
- Transaction logs contain information about credit and debit transactions, including user IDs, balances, amounts, and timestamps.
- Error logs contain details about errors encountered during transaction processing.
- Both sets of data were stored in CSV format.

### Data Preprocessing
- The transaction and error data were loaded into pandas DataFrames.
- Relevant columns, such as user IDs, balances, amounts, and timestamps, were selected for analysis.
- Data standardization was applied using StandardScaler to ensure consistent scaling across features.

### Anomaly Detection
- Anomaly detection was performed using the Isolation Forest algorithm.
- Isolation Forest is well-suited for detecting anomalies in high-dimensional datasets and works by isolating anomalies in sparse regions of the feature space.
- A contamination parameter of 0.01 was chosen to indicate the expected proportion of anomalies in the dataset.

### Automated Reconciliation
- Automated reconciliation involves matching transactions with expected balances and identifying discrepancies.
- This process reduces manual effort and ensures financial stability.
- Future improvements could include implementing automated workflows for flagging and investigating discrepancies, generating reconciliation reports, and integrating with accounting systems.

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
