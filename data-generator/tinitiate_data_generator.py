import csv,json
from xml.dom import minidom
import random
from decimal import Decimal
from faker import Faker
import string 
import datetime 
import time
import pandas as pd

class Tinitiate_DataGen():

    # Class vars
    # #####################
    RECORD_COUNT = 1
    fake = Faker()
    response=[]
    gid=None
    person_details = {}

    ranger = {"random_dist":10,"start":-1,"end":-1,"current":-1,"interval":-1,"interval_ctr":0}

    def ranger_data(self,p_count,p_start,p_end):
        if self.ranger["current"] == -1:
            interval = (p_end-p_start)/p_count
            self.ranger["start"] = p_start
            self.ranger["end"] = p_end
            self.ranger["current"] = p_start
        
        self.ranger["current"] = self.ranger["current"] + 1
        return self.ranger["current"]


    # def __init__(self):
    #    self.gen_person_details()
    
    def create_json_file(self,response):
        with open('data.json', 'w') as fp: 
            json.dump(response, fp, indent=4,default=str) 
            
    def create_csv_file(self,response):
        df = pd.DataFrame(response)  
        df.to_csv('data.csv',index=False) 

    def gen_person_details(self):
        gender = 'M' if random.randint(0,1) == 0 else 'F'
        first = self.fake.first_name_male() if gender=='M' else self.fake.first_name_female()
        last = self.fake.last_name()
        full = first +' '+last 
        email = self.fake.email()
        phone_num = self.fake.phone_number()
        ssn = self.fake.ssn()
        address = self.fake.address()
        self.person_details = { 'gender':gender
                               ,'first_name':first
                               ,'last_name':first
                               ,'full_name':full
                               ,'email':email
                               ,'phone_num':phone_num
                               ,'ssn':ssn
                               ,'address':address}

    # Random Date
    def gen_date(self,p_startyear=None,p_format=None):
        l_startyear = 1980
        l_format="%m/%d/%Y"
        if p_startyear:
            l_startyear=p_startyear
        if p_format:
            l_format = p_format
        sd=self.fake.date_between_dates(date_start=datetime.datetime.strptime(str(l_startyear)+"-01-01", "%Y-%m-%d"), date_end=datetime.datetime.now())
        return sd.strftime(l_format)

    def get_int(self,p_precision=None):
        if p_precision:
            return random.randint(int('1'+'0'*(p_precision-1)),int('9'*p_precision))
        else:
            return random.randint(0,10)

    def get_int_seq(self,start_seq):
        global gid
        if self.gid:
            pass
        else:
            self.gid=start_seq-1
        self.gid+=1
        return self.gid

    def get_random_decimal(start, end, precision):
        factor = 10 ** precision
        scaled_start = start * factor
        scaled_end = end * factor
        random_scaled = random.randint(scaled_start, scaled_end)
        return random_scaled / factor

    def get_decimal(self,p_precision=None):
        if p_precision:
            return str(self.get_int(int(str(p_precision)[0:str(p_precision).find('.')]))) +'.'+ str(self.get_int(int(str(p_precision)[int(str(p_precision).find('.'))+1:])))

    def random_datetime(self,p_startyear=None):
        l_startyear=1980
        if p_startyear:
            l_startyear=p_startyear
        return datetime.datetime.strptime(str(l_startyear)+"-01-01", "%Y-%m-%d") + datetime.timedelta(
            seconds=random.randint(0, int((datetime.datetime.now() - datetime.datetime.strptime(str(l_startyear)+"-01-01", "%Y-%m-%d")).total_seconds())),
        )

    def random_timestamp(self):
        return random_datetime().strftime("%H:%M:%S:")+str(random.randint(100000,999999))

    def get_int_1_to_max(self,p_max=10):
        return random.randint(1,p_max)

    def get_loan_amount(self,p_precision=None):
        if p_precision ==None:
            p_precision=2
        return round(random.uniform(10000.00,30000.00),p_precision)

    def create_data(self,col_info): #, output_format=None, output_style=None):
        header=[]
        data=[]
        m = globals()['Tinitiate_DataGen']()

        for c in range(self.RECORD_COUNT):
            row={}
            self.gen_person_details()
            for column in col_info:
                func = getattr(m, column['field_descriptor'][0])

                if column['field_descriptor'][0].lower() == 'gen_person_details': # in ['first_name','last_name','gender','full_name','email','phone_num','ssn','address']:
                #    # row[column['col']]=gen_name_gender_email()[column['field_descriptor'][0]]
                    row[column['col']] = self.person_details[column['field_descriptor'][1]]
                elif column['field_descriptor'][1]:
                    a= func(column['field_descriptor'][1])
                    row[column['col']]=a
                else:
                    # a= self.column['field_descriptor'][0]()
                    a = func()
                    row[column['col']]=a
            data.append(row)
        return data


if __name__ == "__main__":
    
    dataset = Tinitiate_DataGen()
    dataset.RECORD_COUNT = 100000

    """
    gen_map_array = [
         {'col':'customer_id','field_descriptor':['get_int_seq',1]}
        ,{'col':'customer_name','field_descriptor':['gen_person_details','full_name']}
        ,{'col':'invoice_date','field_descriptor':['gen_date',2022]}
        ,{'col':'invoice_id','field_descriptor':['get_int_seq',1]}
        ,{'col':'discount_percent','field_descriptor':['get_int_1_to_max',9]}
        ]

    """
    gen_map_array = [
         {'col':'invoice_item_id','field_descriptor':['get_int_seq',1]}
        ,{'col':'invoice_id','field_descriptor':['get_int_1_to_max',10000]}
        ,{'col':'product_id','field_descriptor':['get_int_1_to_max',25]}
        ,{'col':'quantity','field_descriptor':['get_int_1_to_max',15]}
        ]

    data = dataset.create_data(gen_map_array)
    # print(type(data))
    # print(json.dumps(data,indent=4))
    # create_json_file(data)
    dataset.create_csv_file(data)