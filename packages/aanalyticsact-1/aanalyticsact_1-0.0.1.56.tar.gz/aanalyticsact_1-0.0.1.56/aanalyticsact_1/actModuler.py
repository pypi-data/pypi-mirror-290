# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com
# Updated by Youngkwang Cho 
# Inquiry : youngkwang.Cho@concentrix.com 
# encoding, create_engine(),apply & map, limit function 


import aanalytics2 as api2
import aanalyticsactauth as auth
import json
from datetime import datetime, timedelta
from copy import deepcopy
from sqlalchemy import create_engine
import os
import re

from sqlalchemy import pool   ###YK
from sqlalchemy.pool import NullPool ###YK
import pandas as pd ###YK


# initator
def dataInitiator():
    api2.importConfigFile(os.path.join(auth.auth, 'aanalyticsact_auth.json'))
    logger = api2.Login()
    logger.connector.config

def dataReportSuites():
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header
    rsids = ags.getReportSuites()
    print(rsids)

# data retrieving function
def dataretriever_data(jsonFile):
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header
    myreport = ags.getReport(jsonFile, limit=1000000, n_results='inf')
    return myreport['data']


def dataretriever_data_breakdown(jsonFile):
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header
    myreport1 = ags.getReport(jsonFile, limit=1000000, n_results='inf',item_id=True)
    data_report = myreport1['data']

    return data_report


def exportToCSV(dataSet, fileName):
    dataSet.to_csv(fileName, sep=',', index=False)


def returnRsID(jsonFile):
    with open(jsonFile, 'r', encoding='UTF-8') as bla:
        json_data = json.loads(bla.read())
    json_data.pop("capacityMetadata")
    rsID = json_data['rsid']

    return rsID


def EndDateCalculation(startDate, endDate):
    startDate = str(startDate)
    endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
    endDate += timedelta(days=1)
    endDate = str(endDate)

    return startDate, endDate


def timeChanger(time_obj, start):
    if start == True:
        return str('T' + time_obj + ':00.000/')
    else:
        time_obj = datetime.strptime(time_obj, "%H:%M")
        time_obj += timedelta(minutes=1)
        return str('T' + str(time_obj.strftime("%H:%M"))+ ':00.000')
    

def jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour):

    startDate = EndDateCalculation(startDate, endDate)[0]
    endDate = EndDateCalculation(startDate, endDate)[1]

    with open(jsonFile, 'r', encoding='UTF-8') as bla:
        json_data = json.load(bla)
    json_data.pop("capacityMetadata")

    globalFilterElement = json_data['globalFilters']
    if start_hour == "00:00" and end_hour == "00:00":
        tobeDate = str(startDate + "T00:00:00.000/" + endDate + "T00:00:00.000")
    else :
        tobeDate = str(startDate + timeChanger(start_hour, True) + endDate + timeChanger(end_hour, False))
        
    for i in range(len(globalFilterElement)):
        globalFilterElement[i]['dateRange'] = tobeDate

    json_data['globalFilters'] = globalFilterElement
    
    return json_data

def addStartEndDateColumn(startDate, endDate, rowNum):
    startDateList = []
    endDateList = []

    for i in range(rowNum):
        startDateList.append(startDate)
        endDateList.append(endDate)

    return startDateList, endDateList

def checkSiteCode(dimension):
    if (dimension == "variables/prop1" or dimension == "variables/evar1" or dimension == "variables/entryprop1"):
        return True

    else:
        return False

# 1st Level data Caller
def refinedFrame(startDate, endDate, period, jsonFile, epp, if_site_code, site_code_rs, start_hour, end_hour):
    dataInitiator()
    dateChange = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)
    dataFrame = dataretriever_data(dateChange)

    if dateChange['rsid'] != "sssamsung4mstglobal":
        columnList = []
        for i in range(dataFrame.shape[1]):
            columnList.append(i)

        dataFrame.columns = columnList

        if site_code_rs == True:
            dataFrame = dataFrame.drop(0,axis =1)

        if dateChange['rsid'] == "sssamsungnewus":
            dataFrame.insert(0, "site_code", "us", True)

        else:
            rsName = dateChange['rsid'].split('4')
            if "epp" in rsName[-1]:
                dataFrame.insert(0, "site_code", rsName[-1].replace('epp', ''), True)
                epp = "Y"
            else:
                dataFrame.insert(0, "site_code", rsName[-1], True)

    if (if_site_code == True or site_code_rs == True):
        dataFrame.insert(1, "period", period, True)
        if start_hour == "00:00" and end_hour == "00:00":
            dataFrame.insert(2, "start_date", startDate, True)
            dataFrame.insert(3, "end_date", endDate, True)
        else :
            dataFrame.insert(2, "start_date", "{0} {1}".format(startDate, start_hour), True)
            dataFrame.insert(3, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)     
        dataFrame.insert(4, "is_epp", epp, True)
    else:
        if dateChange['rsid'] == "sssamsung4mstglobal":
            dataFrame.insert(0, "site_code", "MST", True)
        dataFrame.insert(2, "period", period, True)
        if start_hour == "00:00" and end_hour == "00:00":
            dataFrame.insert(3, "start_date", startDate, True)
            dataFrame.insert(4, "end_date", endDate, True)        
        else :
            dataFrame.insert(3, "start_date", "{0} {1}".format(startDate, start_hour), True)
            dataFrame.insert(4, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)
        dataFrame.insert(5, "is_epp", epp, True)

    return dataFrame  
# updated 220527. smb site code added
# updated 221202. my bday! :D smb site code added (10.31 open)
# updated 240813 app site code added (636 site code)
def filterSiteCode(dataframe, site_code):
    if site_code != "":
        return dataframe.loc[dataframe['site_code'].isin(site_code)]
    else :
       return dataframe.loc[dataframe['site_code'].isin(["ae","ae-app","ae-epp","ae-epp-app","ae-smb","ae-smb-app","ae_ar","ae_ar-app","ae_ar-epp","ae_ar-epp-app","ae_ar-smb","ae_ar-smb-app","africa_en","africa_en-app","africa_en-epp","africa_en-epp-app","africa_en-smb","africa_en-smb-app","africa_fr","africa_fr-app","africa_fr-epp","africa_fr-epp-app","africa_fr-smb","africa_fr-smb-app","africa_pt","africa_pt-app","africa_pt-epp","africa_pt-epp-app","africa_pt-smb","africa_pt-smb-app","al","al-app","al-epp","al-epp-app","al-smb","al-smb-app","ar","ar-app","ar-epp","ar-epp-app","ar-smb","ar-smb-app","at","at-app","at-epp","at-epp-app","at-smb","at-smb-app","au","au-app","au-epp","au-epp-app","au-smb","au-smb-app","az","az-app","az-epp","az-epp-app","az-smb","az-smb-app","ba","ba-app","ba-epp","ba-epp-app","ba-smb","ba-smb-app","bd","bd-app","bd-epp","bd-epp-app","bd-smb","bd-smb-app","be","be-app","be-epp","be-epp-app","be-smb","be-smb-app","be_fr","be_fr-app","be_fr-epp","be_fr-epp-app","be_fr-smb","be_fr-smb-app","bg","bg-app","bg-epp","bg-epp-app","bg-smb","bg-smb-app","bh","bh-app","bh-epp","bh-epp-app","bh-smb","bh-smb-app","bh_ar","bh_ar-app","bh_ar-epp","bh_ar-epp-app","bh_ar-smb","bh_ar-smb-app","br","br-app","br-epp","br-epp-app","br-smb","br-smb-app","ca","ca-app","ca-epp","ca-epp-app","ca-smb","ca-smb-app","ca_fr","ca_fr-app","ca_fr-epp","ca_fr-epp-app","ca_fr-smb","ca_fr-smb-app","ch","ch-app","ch-epp","ch-epp-app","ch-smb","ch-smb-app","ch_fr","ch_fr-app","ch_fr-epp","ch_fr-epp-app","ch_fr-smb","ch_fr-smb-app","cl","cl-app","cl-epp","cl-epp-app","cl-smb","cl-smb-app","cn","cn-app","cn-epp","cn-epp-app","cn-smb","cn-smb-app","co","co-app","co-epp","co-epp-app","co-smb","co-smb-app","cz","cz-app","cz-epp","cz-epp-app","cz-smb","cz-smb-app","de","de-app","de-epp","de-epp-app","de-smb","de-smb-app","dk","dk-app","dk-epp","dk-epp-app","dk-smb","dk-smb-app","ee","ee-app","ee-epp","ee-epp-app","ee-smb","ee-smb-app","eg","eg-app","eg-epp","eg-epp-app","eg-smb","eg-smb-app","eg_en","eg_en-app","eg_en-epp","eg_en-epp-app","eg_en-smb","eg_en-smb-app","es","es-app","es-epp","es-epp-app","es-smb","es-smb-app","fi","fi-app","fi-epp","fi-epp-app","fi-smb","fi-smb-app","fr","fr-app","fr-epp","fr-epp-app","fr-smb","fr-smb-app","ge","ge-app","ge-epp","ge-epp-app","ge-smb","ge-smb-app","gr","gr-app","gr-epp","gr-epp-app","gr-smb","gr-smb-app","hk","hk-app","hk-epp","hk-epp-app","hk-smb","hk-smb-app","hk_en","hk_en-app","hk_en-epp","hk_en-epp-app","hk_en-smb","hk_en-smb-app","hr","hr-app","hr-epp","hr-epp-app","hr-smb","hr-smb-app","hu","hu-app","hu-epp","hu-epp-app","hu-smb","hu-smb-app","id","id-app","id-epp","id-epp-app","id-smb","id-smb-app","ie","ie-app","ie-epp","ie-epp-app","ie-smb","ie-smb-app","il","il-app","il-epp","il-epp-app","il-smb","il-smb-app","in","in-app","in-epp","in-epp-app","in-smb","in-smb-app","iq_ar","iq_ar-app","iq_ar-epp","iq_ar-epp-app","iq_ar-smb","iq_ar-smb-app","iq_ku","iq_ku-app","iq_ku-epp","iq_ku-epp-app","iq_ku-smb","iq_ku-smb-app","iran","iran-app","iran-epp","iran-epp-app","iran-smb","iran-smb-app","it","it-app","it-epp","it-epp-app","it-smb","it-smb-app","jo","jo-app","jo-epp","jo-epp-app","jo-smb","jo-smb-app","jo_ar","jo_ar-app","jo_ar-epp","jo_ar-epp-app","jo_ar-smb","jo_ar-smb-app","jp","jp-app","jp-epp","jp-epp-app","jp-smb","jp-smb-app","kw","kw-app","kw-epp","kw-epp-app","kw-smb","kw-smb-app","kw_ar","kw_ar-app","kw_ar-epp","kw_ar-epp-app","kw_ar-smb","kw_ar-smb-app","kz_kz","kz_kz-app","kz_kz-epp","kz_kz-epp-app","kz_kz-smb","kz_kz-smb-app","kz_ru","kz_ru-app","kz_ru-epp","kz_ru-epp-app","kz_ru-smb","kz_ru-smb-app","latin","latin-app","latin-epp","latin-epp-app","latin-smb","latin-smb-app","latin_en","latin_en-app","latin_en-epp","latin_en-epp-app","latin_en-smb","latin_en-smb-app","lb","lb-app","lb-epp","lb-epp-app","lb-smb","lb-smb-app","levant","levant-app","levant-epp","levant-epp-app","levant-smb","levant-smb-app","levant_ar","levant_ar-app","levant_ar-epp","levant_ar-epp-app","levant_ar-smb","levant_ar-smb-app","lt","lt-app","lt-epp","lt-epp-app","lt-smb","lt-smb-app","lv","lv-app","lv-epp","lv-epp-app","lv-smb","lv-smb-app","ma","ma-app","ma-epp","ma-epp-app","ma-smb","ma-smb-app","mk","mk-app","mk-epp","mk-epp-app","mk-smb","mk-smb-app","mm","mm-app","mm-epp","mm-epp-app","mm-smb","mm-smb-app","mn","mn-app","mn-epp","mn-epp-app","mn-smb","mn-smb-app","mo","mo-app","mo-epp","mo-epp-app","mo-smb","mo-smb-app","mx","mx-app","mx-epp","mx-epp-app","mx-smb","mx-smb-app","my","my-app","my-epp","my-epp-app","my-smb","my-smb-app","n_africa","n_africa-app","n_africa-epp","n_africa-epp-app","n_africa-smb","n_africa-smb-app","nl","nl-app","nl-epp","nl-epp-app","nl-smb","nl-smb-app","no","no-app","no-epp","no-epp-app","no-smb","no-smb-app","nz","nz-app","nz-epp","nz-epp-app","nz-smb","nz-smb-app","om","om-app","om-epp","om-epp-app","om-smb","om-smb-app","om_ar","om_ar-app","om_ar-epp","om_ar-epp-app","om_ar-smb","om_ar-smb-app","pa","pa-app","pa-epp","pa-epp-app","pa-smb","pa-smb-app","pe","pe-app","pe-epp","pe-epp-app","pe-smb","pe-smb-app","ph","ph-app","ph-epp","ph-epp-app","ph-smb","ph-smb-app","pk","pk-app","pk-epp","pk-epp-app","pk-smb","pk-smb-app","pl","pl-app","pl-epp","pl-epp-app","pl-smb","pl-smb-app","ps","ps-app","ps-epp","ps-epp-app","ps-smb","ps-smb-app","pt","pt-app","pt-epp","pt-epp-app","pt-smb","pt-smb-app","py","py-app","py-epp","py-epp-app","py-smb","py-smb-app","qa","qa-app","qa-epp","qa-epp-app","qa-smb","qa-smb-app","qa_ar","qa_ar-app","qa_ar-epp","qa_ar-epp-app","qa_ar-smb","qa_ar-smb-app","ro","ro-app","ro-epp","ro-epp-app","ro-smb","ro-smb-app","rs","rs-app","rs-epp","rs-epp-app","rs-smb","rs-smb-app","ru","ru-app","ru-epp","ru-epp-app","ru-smb","ru-smb-app","sa","sa-app","sa-epp","sa-epp-app","sa-smb","sa-smb-app","sa_en","sa_en-app","sa_en-epp","sa_en-epp-app","sa_en-smb","sa_en-smb-app","se","se-app","se-epp","se-epp-app","se-smb","se-smb-app","sec","sec-app","sec-epp","sec-epp-app","sec-smb","sec-smb-app","sg","sg-app","sg-epp","sg-epp-app","sg-smb","sg-smb-app","si","si-app","si-epp","si-epp-app","si-smb","si-smb-app","sk","sk-app","sk-epp","sk-epp-app","sk-smb","sk-smb-app","th","th-app","th-epp","th-epp-app","th-smb","th-smb-app","tr","tr-app","tr-epp","tr-epp-app","tr-smb","tr-smb-app","tw","tw-app","tw-epp","tw-epp-app","tw-smb","tw-smb-app","ua","ua-app","ua-epp","ua-epp-app","ua-smb","ua-smb-app","uk","uk-app","uk-epp","uk-epp-app","uk-smb","uk-smb-app","uy","uy-app","uy-epp","uy-epp-app","uy-smb","uy-smb-app","uz_ru","uz_ru-app","uz_ru-epp","uz_ru-epp-app","uz_ru-smb","uz_ru-smb-app","uz_uz","uz_uz-app","uz_uz-epp","uz_uz-epp-app","uz_uz-smb","uz_uz-smb-app","ve","ve-app","ve-epp","ve-epp-app","ve-smb","ve-smb-app","vn","vn-app","vn-epp","vn-epp-app","vn-smb","vn-smb-app","za","za-app","za-epp","za-epp-app","za-smb","za-smb-app"])] 


# updated 210907. added site_code_rs for us integration(us has no site code)
# updated 240813 extra1 added
def jsonToDb(startDate, endDate, period, jsonLocation, tbColumn, dbTableName, epp, if_site_code, site_code_rs, limit, extra, extra1, start_hour, end_hour, site_code):
    df = refinedFrame(startDate, endDate, period, jsonLocation, epp, if_site_code, site_code_rs, start_hour, end_hour)
    df.columns = tbColumn
    if extra != "":
        df.insert(5, "extra", extra, True)
    if extra1 != "":
        df.insert(6, "extra1", extra1, True)
    if limit == 0:
        df = df
    else:
        df = df.head(limit)

    if if_site_code == True:
        if returnRsID(jsonLocation) == "sssamsung4mstglobal":
            df = filterSiteCode(df, site_code)
 
    stackTodb(df, dbTableName)

def create_connection_pool():   ###YK
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/act?charset=utf8mb4'
    pool_size = 20  
    max_overflow = 10  
    return create_engine(db_connection_str, encoding='utf-8', poolclass=pool.QueuePool, pool_size=pool_size, max_overflow=max_overflow)

def stackTodb(dataFrame, dbTableName):  ###YK
    print(dataFrame)
    # UNICODE 전처리
    dataFrame = unicodeCompile_df(dataFrame)
    db_connection = create_connection_pool()
    with db_connection.connect() as conn:
        dataFrame.to_sql(name=dbTableName, con=conn, if_exists='append', index=False)
    db_connection.dispose()
    print("finished")
   
""" MST breakdown """

# breakdown itemID
def ChangeItemID(itemID, breakdownJson):
    temp_breakdownJson = deepcopy(breakdownJson)
    before_temp = temp_breakdownJson['metricContainer']['metricFilters']

    # change date > call using itemID iteration
    after_temp = deepcopy(before_temp)
    for i in range(len(after_temp)):
        if "itemId" in after_temp[i]:
            after_temp[i]["itemId"] = itemID
        else:
            continue

    temp_breakdownJson['metricContainer']['metricFilters'] = after_temp

    return temp_breakdownJson


def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF-8') as bla:
        json_data = json.loads(bla.read())
    json_data.pop("capacityMetadata")
    return json_data
        

def returnItemID(startDate, endDate, jsonItemID, start_hour, end_hour, site_code):
    jsonFile = deepcopy(jsonItemID)
    itemIDjson = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)

    dataInitiator()

    itemIDdf = dataretriever_data_breakdown(itemIDjson)

    columnList = list(map(str, range(itemIDdf.shape[1])))   

    columnList[0] = 'site_code'
    columnList[-1] = 'item_id'

    itemIDdf.columns = columnList

    if (itemIDjson["dimension"] == "variables/prop1" or itemIDjson["dimension"] == "variables/evar1" or itemIDjson["dimension"] == "variables/entryprop1"):
        itemIDdfFiltered = filterSiteCode(itemIDdf, site_code)
        itemIDlist = itemIDdfFiltered[['site_code', 'item_id']].values.tolist()        

    else:
        itemIDlist = itemIDdf[['site_code', 'item_id']].values.tolist()

    return itemIDlist

def returnItemID_rs(jsonItemID):
    dataInitiator()

    itemIDdf = dataretriever_data_breakdown(jsonItemID)

    columnList = list(map(str, range(itemIDdf.shape[1])))   

    columnList[0] = 'site_code'
    columnList[-1] = 'item_id'

    itemIDdf.columns = columnList
    itemIDlist = itemIDdf[['site_code', 'item_id']].values.tolist()

    return itemIDlist

#emoji eliminator
def unicodeCompile_df(df):
    only_BMP_pattern = re.compile("["
                                  u"\U00010000-\U0010FFFF"  # out of BMP characters 
                                  "]+", flags=re.UNICODE)

    def remove_non_bmp(text):
        if isinstance(text, str):
            return only_BMP_pattern.sub(r'', text) # only BMP characters
        else:
            return text  # 문자열이 아닌 경우 그대로 반환

    return df.apply(lambda col: col.map(remove_non_bmp))#df.apply(remove_non_bmp)

# Save as dictionary format return in tuple
def ReturnJsonchanged(startDate, endDate, jsonFile, jsonFilebreakdown, start_hour, end_hour, site_code):
    itemIDList = returnItemID(startDate, endDate, jsonFile, start_hour, end_hour, site_code)

    itemIDdict = {}
    for i in range(len(itemIDList)):
        jsonbreakdown = jsonDateChange(startDate, endDate, jsonFilebreakdown, start_hour, end_hour)
        itemIDdict[itemIDList[i][0]] = ChangeItemID(itemIDList[i][1], jsonbreakdown)
    
    itemIDdict = list(zip(itemIDdict.keys(), itemIDdict.values()))
    
    return itemIDdict

def StackbreakValue(startDate, endDate, period, jsonFile, jsonFilebreakdown, tbColumn, dbTableName, epp, limit, extra, extra1, start_hour, end_hour, site_code):
    if returnRsID(jsonFile) == "sssamsung4mstglobal":
        itemIDdict = ReturnJsonchanged(startDate, endDate, jsonFile, jsonFilebreakdown, start_hour, end_hour, site_code)

        # iterable = list(map(int, range(len(itemIDdict))))

        # pool = multiprocessing.Pool(4)
        # func = partial(mstbreakDown, itemIDdict, startDate, endDate, period, tbColumn, dbTableName, epp, limit)
        # pool.map(func, iterable)
        # pool.close()
        # pool.join()

        for i in range(len(itemIDdict)):
            dataFrame = dataretriever_data(itemIDdict[i][1])

            if limit == 0:
                dataFrame2 = dataFrame
            else:
                dataFrame2 = dataFrame.head(limit)

            dataFrame2.insert(0, "site_code", itemIDdict[i][0], True)
            dataFrame2.insert(2, "period", period, True)
            if start_hour == "00:00" and end_hour == "00:00":
                dataFrame2.insert(3, "start_date", startDate, True)
                dataFrame2.insert(4, "end_date", endDate, True)
            else :
                dataFrame2.insert(3, "start_date", "{0} {1}".format(startDate, start_hour), True)
                dataFrame2.insert(4, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)
            dataFrame2.insert(5, "is_us_epp", epp, True)

            dataFrame2.columns = tbColumn
            if extra != "":
                dataFrame2.insert(6, "extra", extra, True)
            if extra1 != "":
                dataFrame2.insert(7, "extra1", extra1, True)
            stackTodb(dataFrame2, dbTableName)

    else:
        dataInitiator()
        dateChange = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)
        dataFrame = dataretriever_data(dateChange)

        dataFrame.columns = list(map(int, range(dataFrame.shape[1])))
        
        if limit == 0:
            dataFrame2 = dataFrame
        else:
            dataFrame2 = dataFrame.head(limit)

        if returnRsID(jsonFile) == "sssamsungnewus":
            dataFrame2.insert(0, "site_code", "us", True)
        else:
            rsName = dateChange['rsid'].split('4')
            dataFrame2.insert(0, "site_code", rsName[-1], True)   

        dataFrame2.insert(2, "period", period, True)
        if start_hour == "00:00" and end_hour == "00:00":
            dataFrame2.insert(3, "start_date", startDate, True)
            dataFrame2.insert(4, "end_date", endDate, True)
        else :
            dataFrame2.insert(3, "start_date", "{0} {1}".format(startDate, start_hour), True)
            dataFrame2.insert(4, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)
        dataFrame2.insert(5, "is_us_epp", epp, True)

        dataFrame2.columns = tbColumn
        if extra != "":
           dataFrame2.insert(6, "extra", extra, True)
        if extra1 != "":
           dataFrame2.insert(7, "extra1", extra1, True)

        stackTodb(dataFrame2, dbTableName)

"""Return after RS Name changed"""

def rsIDchange(jsonFile, rsID):
    temp_simple = deepcopy(jsonFile)
    temp_simple['rsid'] = rsID

    return temp_simple

def refineRsIDChange(startDate, endDate, jsonFile, rsList, period, tbColumn, epp, limit, extra, extra1, start_hour, end_hour):
    datechanged = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)
    rschanged = rsIDchange(datechanged, rsList[1])

    dataInitiator()
    dataFrame1 = dataretriever_data(rschanged)
    if limit == 0 :
        dataFrame=dataFrame1
    else :
        dataFrame=dataFrame1.head(limit)

    columnList = []
    for i in range(dataFrame.shape[1]):
        columnList.append(i)

    dataFrame.columns = columnList

    dataFrame.insert(0, "site_code", rsList[0], True)
    dataFrame.insert(2, "period", period, True)
    if start_hour == "00:00" and end_hour == "00:00":
        dataFrame.insert(3, "start_date", startDate, True)
        dataFrame.insert(4, "end_date", endDate, True)
    else :
        dataFrame.insert(3, "start_date", "{0} {1}".format(startDate, start_hour), True)
        dataFrame.insert(4, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)

    if epp == True:
        dataFrame.insert(5, "is_epp", "Y", True)
    else:
        dataFrame.insert(5, "is_epp", "N", True)

    if (rsList[1] == "sssamsungnewus" or rsList[1] == "sssamsung4sec"):
        dataFrame.insert(6, "is_epp_integ", "Y", True)
    else:
        dataFrame.insert(6, "is_epp_integ", "N", True)
            
    dataFrame.columns = tbColumn
    if extra != "":
        dataFrame.insert(7, "extra", extra, True)
    if extra1 != "":
        dataFrame.insert(8, "extra1", extra1, True)
    return dataFrame

def secondCaller1(startDate, endDate, jsonFile, jsonFilebreakdown, rsList, limit, period, tbColumn, dbTableName, epp, extra="", extra1="", start_hour="00:00", end_hour="00:00"):
    dateChanged_json = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)
    dateChanged_bd_json = jsonDateChange(startDate, endDate, jsonFilebreakdown, start_hour, end_hour)
    
    rsChanged_json = rsIDchange(dateChanged_json, rsList[1])
    rsChanged_json_bd = rsIDchange(dateChanged_bd_json, rsList[1])

    itemIDList = returnItemID_rs(rsChanged_json)

    itemIDdict = {}
    for i in range(len(itemIDList)):
        itemIDdict[itemIDList[i][0]] = ChangeItemID(itemIDList[i][1], rsChanged_json_bd)
    
    itemIDdict = list(zip(itemIDdict.keys(), itemIDdict.values()))

    for i in range(len(itemIDdict)):
        dataFrame = dataretriever_data(itemIDdict[i][1])
        
        if limit == 0:
            dataFrame2 = dataFrame
        else:
            dataFrame2 = dataFrame.head(limit)

        dataFrame2.insert(0, "site_code", rsList[0], True)
        dataFrame2.insert(1, "dimension", itemIDdict[i][0], True)
        dataFrame2.insert(3, "period", period, True)
        if start_hour == "00:00" and end_hour == "00:00":
            dataFrame2.insert(4, "start_date", startDate, True)
            dataFrame2.insert(5, "end_date", endDate, True)
        else :
            dataFrame2.insert(4, "start_date", "{0} {1}".format(startDate, start_hour), True)
            dataFrame2.insert(5, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)
        dataFrame2.insert(6, "epp", epp, True)
        
        if extra != "":
            dataFrame2.insert(7, "extra", extra, True)
        if extra1 != "":
            dataFrame2.insert(8, "extra1", extra1, True)
        dataFrame2.columns = tbColumn
        stackTodb(dataFrame2, dbTableName)

def secondCaller(startDate, endDate, jsonFile, jsonFilebreakdown, rsList, period, tbColumn, dbTableName, epp, limit1, limit2, extra="", extra1="", start_hour="00:00", end_hour="00:00"):
    dateChanged_json = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)
    dateChanged_bd_json = jsonDateChange(startDate, endDate, jsonFilebreakdown, start_hour, end_hour)
    
    rsChanged_json = rsIDchange(dateChanged_json, rsList[1])
    rsChanged_json_bd = rsIDchange(dateChanged_bd_json, rsList[1])

    itemIDList = returnItemID_rs(rsChanged_json)
    itemIDdict = {}
    for i in range(len(itemIDList)):
        itemIDdict[itemIDList[i][0]] = ChangeItemID(itemIDList[i][1], rsChanged_json_bd)
    
    itemIDdict = list(zip(itemIDdict.keys(), itemIDdict.values()))

    if limit1==0:
        lenItemID = len(itemIDdict)
    else :
        lenItemID = limit1

    for i in range(lenItemID):
        dataFrame = dataretriever_data(itemIDdict[i][1])
        
        if limit2 == 0:
            dataFrame2 = dataFrame
        else:
            dataFrame2 = dataFrame.head(limit2)

        dataFrame2.insert(0, "site_code", rsList[0], True)
        dataFrame2.insert(1, "dimension", itemIDdict[i][0], True)
        dataFrame2.insert(3, "period", period, True)
        if start_hour == "00:00" and end_hour == "00:00":
            dataFrame2.insert(4, "start_date", startDate, True)
            dataFrame2.insert(5, "end_date", endDate, True)
        else :
            dataFrame2.insert(4, "start_date", "{0} {1}".format(startDate, start_hour), True)
            dataFrame2.insert(5, "end_date", "{0} {1}".format(EndDateCalculation("0", endDate)[1], end_hour), True)
        dataFrame2.insert(6, "epp", epp, True)
        
        if extra != "":
            dataFrame2.insert(7, "extra", extra, True)
        if extra1 != "":
            dataFrame2.insert(8, "extra1", extra1, True)
        dataFrame2.columns = tbColumn
        stackTodb(dataFrame2, dbTableName)

def refineRsIDChangeRB(startDate, endDate, jsonFile, rsList, period, tbColumn, epp, limit, Biz_type, Device_type, Division, Category, site_code_ae, start_hour, end_hour):
    datechanged = jsonDateChange(startDate, endDate, jsonFile, start_hour, end_hour)
    rschanged = rsIDchange(datechanged, rsList[1])

    dataInitiator()
    dataFrame1 = dataretriever_data(rschanged)
    if limit == 0 :
        dataFrame=dataFrame1
    else :
        dataFrame=dataFrame1.head(limit)

    columnList = []
    for i in range(dataFrame.shape[1]):
        columnList.append(i)

    dataFrame.columns = columnList

    if site_code_ae != "" :
        dataFrame.insert(0, "site_code", site_code_ae, True)
    else :
        dataFrame.insert(0, "site_code", rsList[0], True)

    dataFrame.insert(1, "RS ID", rsList[1], True)
    
    dataFrame.insert(2, "Biz_type", Biz_type, True)
    dataFrame.insert(3, "Division", Division, True)
    dataFrame.insert(4, "Category", Category,True)
    dataFrame.insert(5, "Device_type", Device_type, True)
    dataFrame.insert(6, "Date", startDate, True)
    dataFrame.columns = tbColumn
    return dataFrame
