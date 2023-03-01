import gspread

gc = gspread.service_account(filename='googleApi.json')

sh = gc.open('openrent-result').sheet1

sh.update('A1', 'Test update')

sh.append_row(['first','second', 'third'])
#
sh.append_row(['1','2', '3'])