import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime

# CSV Extract Function
def extract_from_csv(file_to_process): 
    dataframe = pd.read_csv(file_to_process) 
    return dataframe

# JSON Extract Function
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe

# XML Extract Function
def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel'])
    tree = ET.parse(file_to_process) 
    root = tree.getroot() 
    for person in root: 
        car_model = person.find("car_model").text 
        year_of_manufacture = int(person.find("year_of_manufacture").text)
        price = float(person.find("price").text) 
        fuel = person.find("fuel").text 
        dataframe = dataframe.append({"car_model":car_model, "year_of_manufacture":year_of_manufacture, "price":price, "fuel":fuel}, ignore_index=True) 
        return dataframe

def extract():
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel']) 
    #for csv files
    for csvfile in glob.glob("datasource/*.csv"):
        extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
    #for json files
    for jsonfile in glob.glob("datasource/*.json"):
        extracted_data = extracted_data.append(extract_from_json(jsonfile), ignore_index=True)
    #for xml files
    for xmlfile in glob.glob("datasource/*.xml"):
        extracted_data = extracted_data.append(extract_from_xml(xmlfile), ignore_index=True)
    return extracted_data


# transform
def transform(data):
    data['price'] = round(data.price, 2)
    return data

# Load function:
def load(targetfile,data_to_load):
    data_to_load.to_csv(targetfile)
    
def log(message):
    timestamp_format = '%H:%M:%S-%h-%d-%Y'
    #Hour-Minute-Second-MonthName-Day-Year
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("dealership_logfile.txt","a") as f: f.write(timestamp + ',' + message + 'n')
    
log("ETL Job Started")

log("Extract phase Started")
extracted_data = extract() 
log("Extract phase Ended")

log("Transform phase Started")
transformed_data = transform(extracted_data)
log("Transform phase Ended")

log("Load phase Started")
load('targetfile',transformed_data)
log("Load phase Ended")


log("ETL Job Ended")
