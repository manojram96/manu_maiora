
# PySpark ETL Process for Maiora Sales Data on Region A and B

---

## Prerequisites

1. **Python** (3.7 or later)
2. **PySpark** (3.x)
3. **Pandas** (1.x)
4. **SQLite** (with JDBC driver)
5. **Required Python libraries**:
   - pandas
   - json
   - pyspark

Install the required packages using:

```bash
pip install pandas pyspark
```

---

## Input Data Files

1. `order_region_a(in).csv` - Sales orders for Region A.
2. `order_region_b(in).csv` - Sales orders for Region B.

Both files should have a column named `PromotionDiscount` containing JSON data to be flattened.

---

## Steps in the ETL Process

### 1. **Reading Input Files**

The project reads two CSV files (Region A and Region B orders) using Pandas.

### 2. **Flattening JSON Fields**

The `PromotionDiscount` column, which contains JSON data, is flattened using `json.loads()` and `pandas.Series`. The resulting columns are appended to the original data.

### 3. **Dataframe Creation**

The flattened Pandas DataFrame is converted to a PySpark DataFrame. Each DataFrame is annotated with a `Region` column to identify the respective region.

### 4. **Combining DataFrames**

DataFrames from both regions are combined using the `union` operation.

### 5. **Calculating Metrics**

- **Total Sales**: Computed as `QuantityOrdered * ItemPrice`.
- **Net Sales**: Computed as `total_sales - Amount`.

### 6. **Data Cleaning**

- Duplicate records are removed based on `OrderId`.
- Records with `net_sales > 0` are filtered for further processing.

### 7. **Aggregation and Analysis**

SQL queries are executed on the transformed data to calculate:

- Total number of records.
- Total sales per region.
- Average sales per transaction per region.

### 8. **Storing Data in SQLite**

The cleaned and filtered DataFrame is stored in an SQLite database as a table named `transformed_sales`.

---

## SQLite Database Details

- **Database Path**: `/mnt/data/sales_data.db`
- **Table Name**: `transformed_sales`

---

## Execution Instructions

1. Set the paths for `order_region_a(in).csv` and `order_region_b(in).csv` in the script.
2. Ensure the SQLite JDBC driver is available.
3. Run the script using:

   ```bash
   spark-submit maiora.py
   ```

---

## Output

- **SQLite Database**: Contains the cleaned and transformed sales data.
- **Analysis Results**:
  - Total number of records.
  - Total sales per region.
  - Average sales per transaction per region.

---

## Key PySpark Functions Used

- `withColumn`: Adds new columns with transformations.
- `union`: Combines DataFrames.
- `dropDuplicates`: Removes duplicate rows.
- `filter`: Filters rows based on conditions.
- `sql`: Executes SQL queries on temporary views.
- `write.format("jdbc")`: Saves DataFrame to a database.
