import pandas as pd
from datetime import datetime

BOT_REPORT_SHEETS = ["summary_destination", "summary_description", "data"]
LOAD_FACTOR_SHEETS = ['Sheet1', 'Sheet2']
LOAD_FACTOR_COLUMNS = ['ROUTE#', 'DATE', 'TAIL', 'ROUTING', 'CONF', 'WAIT', 'STBY', 'NOSH', 'CURT', 'BORD', 'CAP', '%']
WAYBILLS_COLUMNS = ['Waybills To Ship Report', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3',
                    'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8',
                    'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11']


def extract_waybills_to_ship_file(filename):
    if report_check(filename=filename, column_name_check=WAYBILLS_COLUMNS, sheet_name=["Sheet1"]):
        waybill_data = pd.read_excel(filename).to_dict('records')
        awb_data = []
        found_index = 0

        check_duplicates = []

        for index, awb_value in enumerate(waybill_data):
            if index == 0 or "Sub Total" in awb_value["Waybills To Ship Report"] or index == len(waybill_data) - 1:
                continue
            elif "WPG" in awb_value["Waybills To Ship Report"]:
                destination = awb_value["Waybills To Ship Report"].replace(" ", "").split("=")[1]
                awb_data.append({
                    "index_number": index,
                    "destination": destination,
                    "awb_details": []
                })
                found_index = index
            elif ("YTH" in awb_value["Waybills To Ship Report"] or "YXL" in awb_value["Waybills To Ship Report"]
                  or "=" in awb_value["Waybills To Ship Report"]):
                continue
            else:
                if str(awb_value["Unnamed: 10"]) != "nan":
                    (hours, priority) = str(awb_value["Unnamed: 10"]).split(" ")

                    if hours == "NA":
                        hours = 999

                else:
                    hours = 999
                    priority = 999

                awb = awb_value["Unnamed: 1"].replace(awb_value["Unnamed: 1"][0:4], "")

                for details in awb_data:
                    if found_index == details.get("index_number") and awb_value["Unnamed: 1"] not in check_duplicates:
                        past_date = datetime.strptime(awb_value["Waybills To Ship Report"], '%Y-%m-%d %H:%M')
                        days_on_hand = datetime.now() - past_date

                        details["awb_details"].append({
                            "awb": awb,
                            "piece_rcd": awb_value["Unnamed: 2"],
                            "weight_rcd": awb_value["Unnamed: 3"],
                            "piece_count_on_hand": awb_value["Unnamed: 4"],
                            "weight_on_hand": awb_value["Unnamed: 5"],
                            "consignee": awb_value["Unnamed: 6"],
                            "goods_desc": awb_value["Unnamed: 7"],
                            "hours_remaining": int(hours),
                            "priority": int(priority),
                            "date_received": awb_value["Waybills To Ship Report"],
                            "days_on_hand": int(days_on_hand.days) + 2,
                        })
                        check_duplicates.append(awb_value["Unnamed: 1"])
                        break

        return True, awb_data

    return False, None


def sheet_checker(filename, sheet_to_check):
    sheet_names = pd.ExcelFile(filename).sheet_names
    if sorted(sheet_names) != sorted(sheet_to_check):
        return False
    return True


def report_check(filename, column_name_check: list, sheet_name: list):
    if sheet_checker(filename, sheet_name):
        excel_sheet = pd.read_excel(filename)
        column_names = list(excel_sheet.columns)
        converted_column_names = [column.replace("\xa0", "") for column in column_names]

        if sorted(column_name_check) != sorted(converted_column_names):
            return False
        return True

    return False
