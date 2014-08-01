./convert.py --input="/home/exchangerate/ExchangeRate/ExchangeRate/output/" --output="/home/exchangerate/ExchangeRate/ExchangeRate/output/convert2mysql/" --commitType=daily

./dbCleanup.py --commitType=afterCurrency

./readResultsDB.py -f /home/exchangerate/ExchangeRate/ExchangeRate/html/ExchangeRate-data.DB.days-7.js -days=7

