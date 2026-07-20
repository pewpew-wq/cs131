import pandas as pd
import time
import glob

print("trying to load all raw daily Backblaze CSVs into local memory using Pandas...")
start_time = time.time()

try:

    all_files = glob.glob(r"C:\Users\puiyi\cs131\project\raw_2026_q1\data_Q1_2026\*.csv")
    

    df_list = [pd.read_csv(f) for f in all_files]
    full_df = pd.concat(df_list, ignore_index=True)
    
    print(f"success: Loaded {len(full_df)} rows in {time.time() - start_time:.2f} seconds.")
except MemoryError as e:
    print(f"CRASH DETECTED: Local system ran out of RAM! MemoryError: {e}")
except Exception as e:
    print(f"Process terminated or crashed: {e}")
