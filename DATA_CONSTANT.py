COLS_RAW= ['timestamp','id','open', 'high', 'low', 'close', 'volume', 'adj_close']
COLS_DATA=['open', 'high', 'low', 'close', 'volume', 'adj_close']
IDX_DATE=0
COL_TARGET='open'
COL_ADJ='adj_close'
COLS_TRAIN_EXCLUDE=['open', 'high', 'low', 'close', 'volume', 'adj_close','y']
FIELD_OUTPUT_CSV=('timestamp','id','open', 'high', 'low', 'close', 'volume', 'adj_close','y','y_pred')
X='timestamp'
ML_MODEL_LIST = ['rfr','gbr']