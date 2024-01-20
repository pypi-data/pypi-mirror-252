schema = "symbol TEXT,strategy TEXT, credit TEXT, status TEXT, exp_date TEXT,\
        spread REAL, open_price REAL,breakeven_l REAL, breakeven_h REAL,\
        max_profit REAL, max_loss REAL,pnl REAL, win_prob REAL, last_win_prob REAL,\
        trade_date TEXT,earning_date TEXT,trade_stock_price REAL,\
        margin REAL,quantity REAL, last_quote_date TEXT,\
        last_stock_price REAL,exp_stock_price REAL,\
        last_price REAL,exp_price REAL,pl REAL,gain REAL,\
        stop_price REAL,stop_date TEXT,stop_reason TEXT,\
        uuid TEXT,legs_desc TEXT,\
        target_low REAL, target_high REAL,open_cash REAL, open_margin REAL, close_cash REAL, close_margin REAL,\
        cash_position REAL, margin_position REAL,\
        ib_orderId INTEGER, ib_clientId INTEGER,ib_status TEXT\
        ib_filled INTEGER, ib_remaining INTEGER, ib_lastFillPrice REAL,\
        primary key(uuid)"
##NNUALIZED_RETURN = 'annualized_return' 

class position_summary_col_name():
    SYMBOL            = 'symbol'
    CREDIT            = 'credit'
    STRATEGY          = 'strategy' 
    SPREAD            = 'spread' 
    EXP_DATE          = 'exp_date'
    OPEN_PRICE        = 'open_price'
    LAST_PRICE        = 'last_price'        
    EXP_PRICE         = 'exp_price'
    PL                = 'pl'
    GAIN              = 'gain'  
    BREAKEVEN_L       = 'breakeven_l'
    BREAKEVEN_H       = 'breakeven_h'        
    MAX_PROFIT        = 'max_profit'  
    MAX_LOSS          = 'max_loss'
    PNL               = 'pnl'         
    WIN_PROB          = 'win_prob'
    LAST_WIN_PROB     = 'last_win_prob'         
    TRADE_DATE        = 'trade_date'           
    LAST_QUOTE_DATE   = 'last_quote_date'
    EARNING_DATE      = 'earning_date'        
    TRADE_STOCK_PRICE = 'trade_stock_price'
    LAST_STOCK_PRICE  = 'last_stock_price'
    EXP_STOCK_PRICE   = 'exp_stock_price'        
    MARGIN            = 'margin'        
    QUANTITY          = 'quantity'
    STATUS            = 'status'
    STOP_PRICE        = 'stop_price'    
    STOP_DATE         = 'stop_date'
    STOP_REASON       = 'stop_reason'    
    UUID              = 'uuid'              
    LEGS              = 'legs_desc'
    TARGET_LOW        = 'target_low'
    TARGET_HIGH       = 'target_high'
    OPEN_CASH         = 'open_cash'
    OPEN_MARGIN       = 'open_margin'
    CLOSE_CASH        = 'close_cash'
    CLOSE_MARGIN      = 'close_margin'
    CASH_POSITION     = 'cash_position'
    MARGIN_POSITION   = 'margin_position'
    MAX_RISK          = 'max_risk'    
    OPEN_INTEREST     = 'openInterest'

    IB_STATUS       = 'ib_status'
    IB_ORDER_ID     = 'ib_orderId' 

    IB_FILLED         = 'ib_filled'
    IB_REMAINING      = 'ib_remaining'
    IB_LAST_FILL_PRICE= 'ib_lastFillPrice'
 
    IB_CLIENT_ID      = 'ib_clientId'

'''
String alterTableQuery = "ALTER TABLE " + TABLE_NAME + " ADD COLUMN ";
List<String> newColumns = ..// Your new columns

db.beginTransaction();
for (String column : newColumns){
    db.execSQL(alterTableQuery + column +  " VARCHAR");
}
db.setTransactionSuccessful();
db.endTransaction();
'''

        