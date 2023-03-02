import gspread
import random



def get_todo_list_length():
    records = sh.get_all_records()
    todo_list = []

    for i in range(2, len(records)):
        if records[i]['let-agreed'] == '':
            todo_list.append(records[i])

    print(len(todo_list))
    # def get_update_list(self):
    #     records = sh.get_all_records()
    #     # get not rent out list
    #     for i in range(2, len(records)):
    #         if records[i]['let-agreed'] == '':
    #             self.to_update_list.append(records[i])
    #
    # def update_record(self, response):
    #     if len(self.to_update_list) == 0:
    #         return
    #
    #     next_todo_url = self.to_update_list.pop()
    #     yield scrapy.Request(next_todo_url, callback=self.update_record, dont_filter=True)


def updateRecord():


    records = sh.get_all_records()
    todo_list = []

    for i in range(2, len(records)):
        if records[i]['let-agreed'] == '':
            todo_list.append(records[i])

    print(len(todo_list))

    todo_list = random.sample(todo_list, int(len(todo_list)/4))
    print(len(todo_list))

    for i in range(0, len(todo_list)):
        todo_list[i]



if __name__ == '__main__':
    gc = gspread.service_account(filename='googleApi.json')
    sh = gc.open('openrent-p').sheet1
    updateRecord()
