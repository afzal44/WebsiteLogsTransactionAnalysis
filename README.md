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
Step 1: Parsing and Loading Data
# Convert json data to DataFrame

# Extract required fields and normalize nested metadata

# Identify overdrafts
def identify_overdrafts(df):
    overdrafts = df[df['newBalance'] < 0]
    return overdrafts

# Identify trends and anomalies (example implementation)
def identify_anomalies(df):
    anomalies = df[df['amount'] > 1000]  # Example condition
    return anomalies

overdrafts_df = identify_overdrafts(transactions_df)
anomalies_df = identify_anomalies(transactions_df)

# Identify discrepancies between subscriptionBalance and paymentBalance
def identify_discrepancies(errors_df):
    discrepancies = errors_df[errors_df['subscriptionBalance'] != errors_df['paymentBalance']]
    return discrepancies

discrepancies_df = identify_discrepancies(errors_df)
Step 3: Generating Reports

# Save reports to Excel
with pd.ExcelWriter('reports/balance_reports.xlsx') as writer:
    transactions_df.to_excel(writer, sheet_name='All Transactions', index=False)
    overdrafts_df.to_excel(writer, sheet_name='Overdrafts', index=False)
    anomalies_df.to_excel(writer, sheet_name='Anomalies', index=False)
    discrepancies_df.to_excel(writer, sheet_name='Discrepancies', index=False)

print("Reports generated successfully.")
Step 4: Dockerizing the Solution

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
Run the Docker container:
docker run -v $(pwd)/logs:/app/logs -v $(pwd)/reports:/app/reports calo_balance_sync

The reports will be generated in the reports directory.
Implementation Details
Parsing and Loading Data: Extracted transactions from log files and loaded error data.
Data Transformation: Processed transaction data, identified overdrafts, discrepancies, and anomalies.
Generating Reports: Created Excel reports for easy viewing.
Dockerizing the Solution: Packaged the solution in a Docker container for platform independence.
Future Improvements
Enhance log parsing to handle more complex log structures.
Implement more robust error handling and logging.
Integrate with a database for better data management.
Add support for more output formats (e.g., CSV, PDF).

### Complete Code


# Identify overdrafts
def identify_overdrafts(df):
    overdrafts = df[df['newBalance'] < 0]
    return overdrafts

# Identify trends and anomalies (example implementation)
def identify_anomalies(df):
    anomalies = df[df['amount'] > 1000]  # Example condition
    return anomalies

overdrafts_df = identify_overdrafts(transactions_df)
anomalies_df = identify_anomalies(transactions_df)

# Identify discrepancies between subscriptionBalance and paymentBalance
def identify_discrepancies(errors_df):
    discrepancies = errors_df[errors_df['subscriptionBalance'] != errors_df['paymentBalance']]
    return discrepancies

discrepancies_df = identify_discrepancies(errors_df)

# Save reports to Excel

