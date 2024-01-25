# pyspark-test

[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Unit Test](https://github.com/debugger24/pyspark-test/workflows/Unit%20Test/badge.svg?branch=main)](https://github.com/debugger24/pyspark-test/actions?query=workflow%3A%22Unit+Test%22)
[![PyPI version](https://badge.fury.io/py/pyspark-val.svg)](https://badge.fury.io/py/pyspark-val)
[![Downloads](https://pepy.tech/badge/pyspark-val)](https://pepy.tech/project/pyspark-val)

PySpark validation & testing tooling.

# Installation

```
pip install pyspark-val
```

# Usage

```py
assert_pyspark_df_equal(left_df, actual_df)
```

## Additional Arguments

* `check_dtype` : To compare the data types of spark dataframe. Default true
* `check_column_names` : To compare column names. Default false. Not required of we are checking data types.
* `check_columns_in_order` : To check the columns should be in order or not. Default to false
* `order_by` : Column names with which dataframe must be sorted before comparing. Default None.

# Example

```py
import datetime

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

from pyspark_test import assert_pyspark_df_equal

sc = SparkContext.getOrCreate(conf=conf)
spark_session = SparkSession(sc)

df_1 = spark_session.createDataFrame(
    data=[
        [datetime.date(2020, 1, 1), 'demo', 1.123, 10],
        [None, None, None, None],
    ],
    schema=StructType(
        [
            StructField('col_a', DateType(), True),
            StructField('col_b', StringType(), True),
            StructField('col_c', DoubleType(), True),
            StructField('col_d', LongType(), True),
        ]
    ),
)

df_2 = spark_session.createDataFrame(
    data=[
        [datetime.date(2020, 1, 1), 'demo', 1.123, 10],
        [None, None, None, None],
    ],
    schema=StructType(
        [
            StructField('col_a', DateType(), True),
            StructField('col_b', StringType(), True),
            StructField('col_c', DoubleType(), True),
            StructField('col_d', LongType(), True),
        ]
    ),
)

assert_pyspark_df_equal(df_1, df_2)
```
