from sklearn.metrics import accuracy_score as acc
import pandas as pd
pred = pd.read_csv('/Users/danil/Library/CloudStorage/OneDrive-Personal/BELL/anomalies/data/1. cnc/data/merged/pred.csv')
y_true = list(np.repeat(0, 100)) + list(np.repeat(1, 125))

thresh = ThreshTuner(min_threshold = pred['Anomaly Score'].min(), max_threshold = pred['Anomaly Score'].max(), n_thresholds = 100, verbose = True)
thresh.fit(y_true, pred['Anomaly Score'], acc)
