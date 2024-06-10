from flask import Flask, render_template, send_file, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main import parse_logs_recursively
import os
import platform

app = Flask(__name__)

# Define the path to the logs
# path = r"C:\Users\afjal\OneDrive\Desktop\big Data Engineer\calo_balance_sync\logs"
if os.name == 'nt':
    print("This is a Windows system (identified using os.name).")
    path = r"C:\Users\afjal\OneDrive\Desktop\big Data Engineer\calo_balance_sync\logs"
    xlsx_file = r'C:\Users\afjal\OneDrive\Desktop\big Data Engineer\calo_balance_sync\reports\transactions.xlsx'
elif os.name == 'posix':
    print("This is a Unix-like system (identified using os.name).")
    path = r"logs"
    xlsx_file = 'reports/transactions.xlsx'
# Parse logs
transactions, errors = parse_logs_recursively(path)

# Create directories for storing images
IMG_DIR = 'static/img'
os.makedirs(IMG_DIR, exist_ok=True)

# Create DataFrames
t_df = pd.DataFrame(transactions)
error_df = pd.DataFrame(errors)

# Convert timestamp columns to datetime
t_df['timestamp'] = pd.to_datetime(t_df['timestamp'])
error_df['timestamp'] = pd.to_datetime(error_df['timestamp'])

# Normalize transaction JSON data
tn_df = pd.json_normalize(t_df['transaction'])

# Add normalized transaction data and timestamp to a new DataFrame
tf = pd.concat([tn_df, t_df['timestamp']], axis=1)

# Calculate statistics
tf['month'] = tf['timestamp'].dt.to_period('M')
tf['year'] = tf['timestamp'].dt.to_period('Y')
user_average_transaction_amount_per_m = tf.groupby(['userId', 'month']).agg({'amount': 'mean'}).reset_index()
user_average_transaction_amount_per_yr = tf.groupby(['userId', 'year']).agg({'amount': 'mean'}).reset_index()

# Detecting Overdrafts and Anomalies
overdraft_users = error_df[error_df['paymentBalance'] < 0].copy()
overdraft_users['date'] = overdraft_users['timestamp'].dt.date

# Check for anomalies in the transaction data
large_transactions = tf[tf['amount'] > 2000].copy()
large_transactions['date'] = large_transactions['timestamp'].dt.date

# Look for irregular patterns in transaction frequency
transaction_frequency_stats = tn_df['userId'].value_counts()
abnormal_frequency_users = transaction_frequency_stats[(transaction_frequency_stats < 10) | (transaction_frequency_stats > 100)]
abnormal_frequency_users_df = abnormal_frequency_users.reset_index()
abnormal_frequency_users_df.columns = ['User ID', 'Transaction Count']

# Impute missing transaction types
tf['type'] = tf.apply(lambda x: "CREDIT" if x["newBalance"] - (x['amount'] - x["vat"]) > 0 else 'DEBIT', axis=1)
type_counts_imputed = tf["type"].value_counts()

def save_plot(plot_func, filename):
    filepath = os.path.join(IMG_DIR, filename)
    plot_func(filepath)
    return filepath

def plot_transaction_types(filepath):
    plt.figure(figsize=(8, 8))
    plt.pie(type_counts_imputed, labels=type_counts_imputed.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#99ff99'])
    plt.title('Distribution of Transaction Types (Imputed)')
    plt.axis('equal')
    plt.savefig(filepath, format='png')
    plt.close()

def plot_balance_changes(filepath):
    daily_balance = tf.groupby(tf['timestamp'].dt.date)['amount'].sum()
    plt.figure(figsize=(10, 6))
    plt.plot(daily_balance.index, daily_balance.values, marker='o', linestyle='-')
    plt.title('Changes in Balance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.grid(True)
    plt.savefig(filepath, format='png')
    plt.close()

def plot_transaction_amount_histogram(filepath):
    plt.figure(figsize=(10, 6))
    plt.hist(tf['amount'], bins=20, color='blue', edgecolor='black')
    plt.title('Distribution of Transaction Amounts')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(filepath, format='png')
    plt.close()

def plot_user_activity_over_time(filepath):
    user_activity = tf.groupby(tf['timestamp'].dt.to_period('M'))['userId'].nunique()
    plt.figure(figsize=(10, 6))
    user_activity.plot(kind='bar', color='green')
    plt.title('User Activity Over Time')
    plt.xlabel('Month')
    plt.ylabel('Number of Active Users')
    plt.grid(True)
    plt.savefig(filepath, format='png')
    plt.close()

def plot_monthly_transaction_volume(filepath):
    monthly_transaction_volume = tf.groupby(tf['month'])['userId'].count()
    plt.figure(figsize=(10, 6))
    monthly_transaction_volume.plot(kind='line', marker='o', linestyle='-')
    plt.title('Monthly Transaction Volume')
    plt.xlabel('Month')
    plt.ylabel('Number of Transactions')
    plt.grid(True)
    plt.savefig(filepath, format='png')
    plt.close()

def plot_transaction_activity_heatmap(filepath):
    tf['hour'] = tf['timestamp'].dt.hour
    tf['day_of_week'] = tf['timestamp'].dt.dayofweek
    heatmap_data = tf.pivot_table(index='hour', columns='day_of_week', values='userId', aggfunc='count', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d')
    plt.title('Transaction Activity Heatmap')
    plt.xlabel('Day of Week')
    plt.ylabel('Hour of Day')
    plt.savefig(filepath, format='png')
    plt.close()

# Save plots
save_plot(plot_transaction_types, 'transaction_types_imputed.png')
save_plot(plot_balance_changes, 'balance_changes.png')
save_plot(plot_transaction_amount_histogram, 'transaction_amount_histogram.png')
save_plot(plot_user_activity_over_time, 'user_activity_over_time.png')
save_plot(plot_monthly_transaction_volume, 'monthly_transaction_volume.png')
save_plot(plot_transaction_activity_heatmap, 'transaction_activity_heatmap.png')

@app.route('/')
def index():
    try:
        transaction_types_imputed_pie_chart_url = url_for('static', filename=f'img/transaction_types_imputed.png')
        balance_changes_plot_url = url_for('static', filename=f'img/balance_changes.png')
        transaction_amount_histogram_url = url_for('static', filename=f'img/transaction_amount_histogram.png')
        user_activity_over_time_url = url_for('static', filename=f'img/user_activity_over_time.png')
        monthly_transaction_volume_url = url_for('static', filename=f'img/monthly_transaction_volume.png')
        transaction_activity_heatmap_url = url_for('static', filename=f'img/transaction_activity_heatmap.png')
        
        return render_template(
            'index.html',
            balance_changes_plot_url=balance_changes_plot_url,
            transaction_types_imputed_pie_chart_url=transaction_types_imputed_pie_chart_url,
            transaction_amount_histogram_url=transaction_amount_histogram_url,
            user_activity_over_time_url=user_activity_over_time_url,
            monthly_transaction_volume_url=monthly_transaction_volume_url,
            transaction_activity_heatmap_url=transaction_activity_heatmap_url,
            user_average_transaction_amount_per_m=user_average_transaction_amount_per_m.head(10).to_html(index=False),
            user_average_transaction_amount_per_yr=user_average_transaction_amount_per_yr.head(10).to_html(index=False),
            overdraft_users=overdraft_users[['userId', 'subscriptionBalance', 'paymentBalance', 'date']].head(10).to_html(index=False),
            large_transactions=large_transactions[['userId', 'currency', 'amount', 'vat', 'oldBalance', 'type', 'date']].head(10).to_html(index=False),
            abnormal_frequency_users=abnormal_frequency_users_df.head(10).to_html(index=False, header=["User ID", "Transaction Count"])
        )
    except Exception as e:
        return str(e)

@app.route('/generate_report')
def generate_report():
    try:
        writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
        
        user_average_transaction_amount_per_m.to_excel(writer, sheet_name='Avg Txn Amount per Month', index=False)
        user_average_transaction_amount_per_yr.to_excel(writer, sheet_name='Avg Txn Amount per Year', index=False)
        overdraft_users[['userId', 'subscriptionBalance', 'paymentBalance', 'date']].to_excel(writer, sheet_name='Overdrafted Users', index=False)
        large_transactions[['userId', 'currency', 'amount', 'vat', 'oldBalance', 'type', 'date']].to_excel(writer, sheet_name='Anomaly in Txn Amt(<1000)', index=False)
        abnormal_frequency_users_df.to_excel(writer, sheet_name='Anomaly Txn Frequency', index=False, header=["User ID", "Transaction Count"])
        
        workbook = writer.book
        worksheet_balance = workbook.add_worksheet('Changes in Balance Over Time')
        worksheet_balance.insert_image('A1', "static/img/balance_changes.png")

        worksheet_imputed_pie_chart = workbook.add_worksheet('Transaction Types Pie Chart')
        worksheet_imputed_pie_chart.insert_image('A1', "static/img/transaction_types_imputed.png")
        
        worksheet_histogram = workbook.add_worksheet('Transaction Amount Histogram')
        worksheet_histogram.insert_image('A1', "static/img/transaction_amount_histogram.png")
        
        worksheet_activity_over_time = workbook.add_worksheet('User Activity Over Time')
        worksheet_activity_over_time.insert_image('A1', "static/img/user_activity_over_time.png")
        
        worksheet_monthly_volume = workbook.add_worksheet('Monthly Transaction Volume')
        worksheet_monthly_volume.insert_image('A1', "static/img/monthly_transaction_volume.png")
        
        worksheet_heatmap = workbook.add_worksheet('Transaction Activity Heatmap')
        worksheet_heatmap.insert_image('A1', "static/img/transaction_activity_heatmap.png")
        
        writer.close()
        print(f"xlsx_file: {xlsx_file}")
        return send_file(xlsx_file, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)
