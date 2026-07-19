import sys
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

def main():
    if len(sys.argv) < 2:
        print("error: path file", file=sys.stderr)
        sys.exit(1)
        
    gcs_input_path = sys.argv[1]

    # A1
    spark = SparkSession.builder \
        .appName("ws5-regression") \
        .getOrCreate()

    # A2
    df = spark.read.csv(gcs_input_path, header=True, inferSchema=True)
    df.show(5)

    # A3
    assembler = VectorAssembler(
        inputCols=["total_bill", "size"], 
        outputCol="features"
    )

    # A4
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    # A5
    lr = LinearRegression(featuresCol="features", labelCol="tip")
    pipeline = Pipeline(stages=[assembler, lr])
    pipeline_model = pipeline.fit(train_df)

    # A6
    predictions_df = pipeline_model.transform(test_df)

    # A7
    evaluator = RegressionEvaluator(labelCol="tip", predictionCol="prediction")
    
    evaluator.setMetricName("rmse")
    rmse = evaluator.evaluate(predictions_df)
    
    evaluator.setMetricName("r2")
    r2 = evaluator.evaluate(predictions_df)

    # A8
    lr_model = pipeline_model.stages[-1]
    
    print("\n" + "="*40)
    print("JOB LOG OUTPUT")
    print("="*40)
    print(f"Coefficients: {lr_model.coefficients}")
    print(f"Intercept: {lr_model.intercept}")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")
    print("="*40 + "\n")

    spark.stop()

if __name__ == "__main__":
    main()
