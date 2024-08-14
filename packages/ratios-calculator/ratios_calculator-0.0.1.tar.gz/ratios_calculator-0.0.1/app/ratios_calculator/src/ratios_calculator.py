#######New Dataframe
#######Graphs for each year



import numpy as np 
import pandas as pd 
import re
import os

# ###TESLA###
# balance_sheet_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Tesla/Tesla_balance_sheet.xlsx" 
# income_statement_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Tesla/Tesla_Income_Statement.xlsx"
# price_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Tesla/Tesla_PriceHistory.xlsx" 

# ###APPLE###
# balance_sheet_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Apple/Apple_balance_sheet.xlsx"
# income_statement_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Apple/Apple_Income_Statement.xlsx"
# price_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Apple/Apple_PriceHistory.xlsx"

# ###BABA###
# balance_sheet_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/BABA/BABA_balance_sheet.xlsx"
# income_statement_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/BABA/BABA_Income_Statement.xlsx"
# price_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/BABA/BABA_PriceHistory.xlsx"

# ###GOOGLE###
# balance_sheet_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Google/Google_balance_sheet.xlsx"
# income_statement_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Google/Google_income_statement.xlsx"
# price_file_name = "/Users/billjiang/Desktop/EQUATE/EQUATE_Data_Analyze/Google/Google_PriceHistory.xlsx"

balance_sheet_file_name = input("Enter the balance sheet file path (xlsx): ")
if not os.path.exists(balance_sheet_file_name):
        print("File does not exist.")
        exit()
income_statement_file_name = input("Enter the income statement file path (xlsx): ")
if not os.path.exists(balance_sheet_file_name):
        print("File does not exist.")
        exit()
price_file_name = input("Enter the stock price history file path (xlsx): ")
if not os.path.exists(balance_sheet_file_name):
        print("File does not exist.")
        exit()

df_price = pd.read_excel(price_file_name, skiprows = 15)
df_balance_sheet = pd.read_excel(balance_sheet_file_name)
df_income_statement = pd.read_excel(income_statement_file_name)
is_copy = df_income_statement.copy()
# print(df_income_statement.iloc[:,0])

def unit_conversion(df_balance_sheet, df_income_statement):
    is_unit = df_income_statement.iloc[-1, 0].split()[3].lower()
    bs_unit = df_balance_sheet.iloc[-1, 0].split()[3].lower()

    conversion_factors = {
        'thousands': 1,
        'millions': 1e3,
        'billions': 1e6,
        'trillions': 1e9
    }

    # Ensure factor defaults to 1 if units do not match expected values
    factor = conversion_factors.get(is_unit, 1) / conversion_factors.get(bs_unit, 1) if is_unit in conversion_factors and bs_unit in conversion_factors else 1
    # print(factor)

    skip_keywords = ['EPS', 'Shares Outstanding']

    def convert_row(row):
        # Check if the first cell in the row contains any skip keywords
        if any(keyword in str(row.iloc[0]) for keyword in skip_keywords):
            return row  # Return the row unchanged if it should be skipped
        else:
            # Apply conversion factor to numeric values in the row
            return row.apply(lambda x: x * factor if isinstance(x, (int, float)) else x)
    
    # Apply the convert_row function to each row in the DataFrame
    df_income_statement_converted = df_income_statement.apply(convert_row, axis=1)
    return df_income_statement_converted



df_income_statement = unit_conversion(df_balance_sheet, df_income_statement)

# print(df_income_statement.iloc[46:55, 1])

def fetch_line_data(df, line_title):
    """Reads the data of specific category on balance sheet
    Args: 
        df: balance sheet data
        line_title: title of the category
    
    Returns:
        A list of the data of the desired balance sheet category
    """
    # return df[df.iloc[:, 0].str.contains(re.escape(line_title), na=False, case=False, regex=True)]
    line_data = df[df.iloc[:, 0].str.contains(re.escape(line_title), na=False, case=False, regex=True)]
    if not line_data.empty:
        return line_data.iloc[0, 1:].tolist()
    else:
        return "N/A"

def get_years(data):
    """
    Tries to identify a row containing years formatted as 'MONTH 'YY' and returns them sorted from most recent to least recent.

    Args:
        balance_sheet_file_name: The balance sheet Excel file data which has been already read.

    Returns:
        A sorted list of years on the balance sheet, from most recent to least recent.
    """
    year_pattern = "[A-Z]{3} '\\d{2}"
    for index, row in data.iterrows():
        if row.astype(str).str.contains(year_pattern, regex=True, na=False).any():
            years = [2000 + int(cell.split("'")[1]) for cell in row[1:] if pd.notna(cell)]
            return sorted(set(years), reverse=True)  

    raise ValueError("No row with valid years found in the balance sheet.")

def get_year_and_month(data):
    year_pattern = "[A-Z]{3} '\\d{2}"
    for index, row in data.iterrows():
        if row.astype(str).str.contains(year_pattern, regex=True, na=False).any():
            years = [cell for cell in row[1:] if pd.notna(cell)]
    return years


def align_columns(df_balance_sheet, df_income_statement):
    """
    Aligns the columns of income statement to match those of the balance sheet based on year columns identified.

    Args:
        df_balance_sheet (pd.DataFrame): DataFrame of the balance sheet.
        df_income_statement (pd.DataFrame): DataFrame of the income statement.

    Returns:
        pd.DataFrame: Modified income statement with aligned columns.
    """
    # Identify year columns in both DataFrames
    bs_years = get_years(df_balance_sheet)
    is_years = get_years(df_income_statement)

    # Convert to sets for easy comparison
    set_bs_years = set(bs_years)
    set_is_years = set(is_years)

    # Find year columns in the income statement not in the balance sheet
    years_to_drop = list(set_is_years - set_bs_years)

    year_pattern = "[A-Z]{3} '\\d{2}"
    converted_years = {str(year % 100) for year in years_to_drop}
    columns_to_drop = []
    for index, row in df_income_statement.iterrows():
        if row.astype(str).str.contains(year_pattern, regex=True, na=False).any():
            years = [cell for cell in row if pd.notna(cell) and str(cell).split("'")[1] in converted_years]
    columns_to_drop.extend(years)

    mask = df_income_statement.isin(columns_to_drop).any()
    # Drop these columns
    df_income_statement.drop(columns=df_income_statement.columns[mask], inplace=True)
    
    return df_income_statement

def get_price_for_year_end(data): 
    """Gets the price of the stock at the last day of each year, and puts them in a dictionary.

    Args:
        data: Company stock price data (price_data from above).

    Returns:
        A dictionary with year as key and stock price at end of year as value. 
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    last_day_each_year = data.resample('YE').last()
    last_day_each_year.reset_index(inplace=True)
    last_day_each_year['Year'] = last_day_each_year['Date'].dt.strftime('%Y')
    print(last_day_each_year[['Date', 'Price']])
    price_dict = last_day_each_year.set_index('Year')['Price'].to_dict()
    return price_dict


def get_price_for_date(date, data):
    month, year_suffix = date.split()
    year_suffix = year_suffix.replace("'", "")
    full_year = f"20{year_suffix}"
    full_date_str = f"01 {month} {full_year}"
    date = pd.to_datetime(full_date_str, format='%d %b %Y').strftime('%B %Y')  # Note the uppercase 'Y' for four-digit years
    month_year_filter = data['Date'].dt.strftime('%B %Y')== date
    filtered_data = data[month_year_filter]
    mean_price = np.mean(filtered_data['Price'])
    return mean_price

def ratios_of_each_year(numerator_term, denominator_term, ratio_name, df_balance_sheet):
    ratio_name_dic = {}
    years_list = get_year_and_month(df_balance_sheet)
    for index in range (len(years_list)):
        if not isinstance(numerator_term, list) or not isinstance(denominator_term, list):
            ratio_name_dic[f'{ratio_name}{years_list[index]}'] = "N/A"
        else:
            ratio_name_dic[f'{ratio_name}{years_list[index]}'] = round(numerator_term[index]/denominator_term[index], 3) if denominator_term[index] != 0 else "N/A"
    return ratio_name_dic



def perform_financial_analysis(df_balance_sheet, df_income_statement, df_price):
    """Determines data based on the focus of analysis provided by user input.
    
    Args:
        df (pd.DataFrame): DataFrame containing balance sheet data.
    
    Returns:
        tuple: A tuple containing lists of data for assets and liabilities based on the analysis focus.
    """

    matched_income_statement = align_columns(df_balance_sheet, df_income_statement)
    most_recent_year = get_year_and_month(df_balance_sheet)[0]
    previous_years = str(get_years(df_balance_sheet)[-1]) + "-" + str(get_years(df_balance_sheet)[1])
    
    # LIQUIDITY
    total_current_assets = fetch_line_data(df_balance_sheet, 'Total Current Assets')
    total_current_liabilities = fetch_line_data(df_balance_sheet, 'Total Current Liabilities')
    inventories = fetch_line_data(df_balance_sheet, 'Inventories')
    Cash_and_Equivalents = fetch_line_data(df_balance_sheet, 'Cash & Short-Term Investments')

    dict_liq_current = ratios_of_each_year(total_current_assets, total_current_liabilities, 'Current Ratio', df_balance_sheet)
    dict_liq_quick = ratios_of_each_year((np.array(total_current_assets) - np.array(inventories)).tolist(), total_current_liabilities, 'Quick Ratio', df_balance_sheet)
    dict_liq_cash = ratios_of_each_year(Cash_and_Equivalents, total_current_liabilities, 'Cash Ratio', df_balance_sheet)

    dict_liq = {**dict_liq_current, **dict_liq_quick, **dict_liq_cash}
        
    # Current_Ratio_of_Most_Recent_Year = total_current_assets[0]/total_current_liabilities[0] if total_current_liabilities[0] != 0 else "N/A"
    # Avg_Current_Ratio_of_Previous_Years = np.mean(total_current_assets[1:])/np.mean(total_current_liabilities[1:]) if np.mean(total_current_liabilities[1:]) != 0 else "N/A"
    # Quick_Ratio_of_Most_Recent_Year = (total_current_assets[0] - inventories[0])/total_current_liabilities[0] if total_current_liabilities[0] != 0 else "N/A"
    # Avg_Quick_Ratio_of_Previous_Years = (np.mean(total_current_assets[1:])-np.mean(inventories[1:]))/np.mean(total_current_liabilities[1:]) if np.mean(total_current_liabilities[1:]) != 0 else "N/A"
    # Cash_Ratio_of_Most_Recent_Year = Cash_and_Equivalents[0]/total_current_liabilities[0] if total_current_liabilities[0] != 0 else "N/A"
    # Cash_Ratio_of_Previous_Years = (np.mean(Cash_and_Equivalents[1:]))/np.mean(total_current_liabilities[1:]) if np.mean(total_current_liabilities[1:]) != 0 else "N/A"
    
    # dict_liq = {}
    # dict_liq[f'Current Ratio{most_recent_year}'] = round(Current_Ratio_of_Most_Recent_Year, 3) if Current_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_liq[f'Avg Current Ratio{previous_years}'] = round(Avg_Current_Ratio_of_Previous_Years, 3) if Avg_Current_Ratio_of_Previous_Years != "N/A" else "N/A"
    # dict_liq[f'Quick Ratio{most_recent_year}'] = round(Quick_Ratio_of_Most_Recent_Year, 3) if Quick_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_liq[f'Avg Quick Ratio{previous_years}'] = round(Avg_Quick_Ratio_of_Previous_Years, 3) if Avg_Quick_Ratio_of_Previous_Years != "N/A" else "N/A"
    # dict_liq[f'Cash Ratio{most_recent_year}'] = round(Cash_Ratio_of_Most_Recent_Year, 3) if Cash_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_liq[f'Cash Ratio{previous_years}'] = round(Cash_Ratio_of_Previous_Years, 3) if Cash_Ratio_of_Previous_Years != "N/A" else "N/A"

    # liquidity_weigths = {'Current_Ratio': 0.4, 'Quick_Ratio': 0.3, 'Cash_Ratio': 0.3}
    # Liquidity_Strength_Score_Most_Recent_Year = round(dict_liq[f'Current Ratio{most_recent_year}'] * liquidity_weigths['Current_Ratio'] + dict_liq[f'Quick Ratio{most_recent_year}'] * liquidity_weigths['Quick_Ratio'] + dict_liq[f'Cash Ratio{most_recent_year}'] * liquidity_weigths['Cash_Ratio'], 3) if all(val != "N/A" for val in [dict_liq[f'Current Ratio{most_recent_year}'], dict_liq[f'Quick Ratio{most_recent_year}'], dict_liq[f'Cash Ratio{most_recent_year}']]) else "N/A"
    # Liquidity_Strength_Score_Most_Prev_Years = round(dict_liq[f'Avg Current Ratio{previous_years}'] * liquidity_weigths['Current_Ratio'] + dict_liq[f'Avg Quick Ratio{previous_years}'] * liquidity_weigths['Quick_Ratio'] + dict_liq[f'Cash Ratio{previous_years}'] * liquidity_weigths['Cash_Ratio'], 3) if all(val != "N/A" for val in [dict_liq[f'Avg Current Ratio{previous_years}'], dict_liq[f'Avg Quick Ratio{previous_years}'], dict_liq[f'Cash Ratio{previous_years}']]) else "N/A"
    # dict_liq[f'Liquidity Strength Score {most_recent_year}'] = Liquidity_Strength_Score_Most_Recent_Year
    # dict_liq[f'Liquidity Strength Score {previous_years}'] = Liquidity_Strength_Score_Most_Prev_Years
    # print(dict_liq)


    # SOLVENCY
    total_liabilities = fetch_line_data(df_balance_sheet, 'Total Liabilities')
    total_shareholders_equity = fetch_line_data(df_balance_sheet, "Total Shareholders' Equity")
    # Debt_to_Equity_Ratio_of_Most_Recent_Year = total_liabilities[0]/total_shareholders_equity[0] if total_shareholders_equity[0] != 0 else "N/A"
    # Debt_to_Equity_Ratio_of_Previous_Years = np.mean(total_liabilities[1:]) / np.mean(total_shareholders_equity[1:]) if np.mean(total_shareholders_equity[1:]) != 0 else "N/A"
    operating_income = fetch_line_data(matched_income_statement, 'EBIT (Operating Income)')
    interest_expense = fetch_line_data(matched_income_statement, 'Interest Expense')
    # Interest_Coverage_Ratio_of_Most_Recent_Year = operating_income[0]/interest_expense[0] if interest_expense[0] != 0 else "N/A"
    # Interest_Coverage_Ratio_of_Previous_Years = np.mean(operating_income[1:]) / np.mean(interest_expense[1:]) if np.mean(interest_expense[1:]) != 0 else "N/A"

    # dict_solv = {}
    # dict_solv[f'Debt to Equity Ratio{most_recent_year}'] = round(Debt_to_Equity_Ratio_of_Most_Recent_Year, 3) if Debt_to_Equity_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_solv[f'Debt to Equity Ratio{previous_years}'] = round(Debt_to_Equity_Ratio_of_Previous_Years, 3) if Debt_to_Equity_Ratio_of_Previous_Years != "N/A" else "N/A"
    # dict_solv[f'Interest Coverage Ratio{most_recent_year}'] = round(Interest_Coverage_Ratio_of_Most_Recent_Year, 3) if Interest_Coverage_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_solv[f'Interest Coverage Ratio{previous_years}'] = round(Interest_Coverage_Ratio_of_Previous_Years, 3) if Interest_Coverage_Ratio_of_Previous_Years != "N/A" else "N/A"

    dict_solv_Debt_to_Equity = ratios_of_each_year(total_liabilities, total_shareholders_equity, 'Debt to Equity Ratio', df_balance_sheet)
    dict_solv_Interest_Coverage = ratios_of_each_year(operating_income, interest_expense, 'Interest Coverage Ratio', df_balance_sheet)

    dict_solv = {**dict_solv_Debt_to_Equity, **dict_solv_Interest_Coverage}
    # solvency_weights = {'Debt_to_Equity_Ratio': 0.5, 'Interest_Coverage_Ratio': 0.5}
    # Solvency_Score_Most_Recent_Year = dict_solv[f'Debt to Equity Ratio{most_recent_year}'] * solvency_weights['Debt_to_Equity_Ratio'] + dict_solv[f'Interest Coverage Ratio{most_recent_year}'] * solvency_weights['Interest_Coverage_Ratio'] if all(val != "N/A" for val in [dict_solv[f'Debt to Equity Ratio{most_recent_year}'], dict_solv[f'Interest Coverage Ratio{most_recent_year}']]) else "N/A"
    # Solvency_Score_Previous_Years = dict_solv[f'Debt to Equity Ratio{previous_years}'] * solvency_weights['Debt_to_Equity_Ratio'] + dict_solv[f'Interest Coverage Ratio{previous_years}'] * solvency_weights['Interest_Coverage_Ratio'] if all(val != "N/A" for val in [dict_solv[f'Debt to Equity Ratio{previous_years}'], dict_solv[f'Interest Coverage Ratio{previous_years}']]) else "N/A"
    # dict_solv[f'Solvency Score {most_recent_year}'] = round(Solvency_Score_Most_Recent_Year, 3) if Solvency_Score_Most_Recent_Year != "N/A" else "N/A"
    # dict_solv[f'Solvency Score {previous_years}'] = round(Solvency_Score_Previous_Years, 3) if Solvency_Score_Previous_Years != "N/A" else "N/A"


    # EFFICIENCY
    fixed_assets = fetch_line_data(df_balance_sheet, 'Fixed Assets')
    sales = fetch_line_data(matched_income_statement, 'Sales')
    total_assets = fetch_line_data(df_balance_sheet, 'Total Assets')
    # Asset_Turnover_Ratio_of_Most_Recent_Year = sales[0]/total_assets[0] if total_assets[0] != 0 else "N/A"
    # Asset_Turnover_Ratio_of_Previous_Years = np.mean(sales[1:])/np.mean(total_assets[1:]) if np.mean(total_assets[1:]) != 0 else "N/A"
    cost_of_goods = fetch_line_data(matched_income_statement, 'Cost of Goods Sold (COGS) incl. D&A')
    average_inventories = fetch_line_data(df_balance_sheet, 'Inventories')
    # Inventory_Turnover_Ratio_of_Most_Recent_Year = cost_of_goods[0]/average_inventories[0] if average_inventories[0] != 0 else "N/A"
    # Inventory_Turnover_Ratio_of_Previous_Years = np.mean(cost_of_goods[1:])/np.mean(average_inventories[1:]) if np.mean(average_inventories[1:]) != 0 else "N/A"
    dict_eff_Asset_Turnover = ratios_of_each_year(sales, total_assets, 'Asset Turnover Ratio', df_balance_sheet)
    dict_eff_Inventory_Turnover = ratios_of_each_year(cost_of_goods, average_inventories, 'Inventory Turnover Ratio', df_balance_sheet)
    dict_eff_Fixed_Asset_Turnover = ratios_of_each_year(sales, fixed_assets, 'Fixed Asset Turnover Ratio', df_balance_sheet)

    dict_eff = {**dict_eff_Asset_Turnover, **dict_eff_Inventory_Turnover, **dict_eff_Fixed_Asset_Turnover}
    
    # dict_eff = {}
    # dict_eff[f'Asset Turnover Ratio{most_recent_year}'] = round(Asset_Turnover_Ratio_of_Most_Recent_Year, 3) if Asset_Turnover_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_eff[f'Asset Turnover Ratio{previous_years}'] = round(Asset_Turnover_Ratio_of_Previous_Years, 3) if Asset_Turnover_Ratio_of_Previous_Years != "N/A" else "N/A"
    # dict_eff[f'Inventory Turnover Ratio{most_recent_year}'] = round(Inventory_Turnover_Ratio_of_Most_Recent_Year, 3) if Inventory_Turnover_Ratio_of_Most_Recent_Year != "N/A" else "N/A"
    # dict_eff[f'Inventory Turnover Ratio{previous_years}'] = round(Inventory_Turnover_Ratio_of_Previous_Years, 3) if Inventory_Turnover_Ratio_of_Previous_Years != "N/A" else "N/A"

    # efficiency_weights = {'Asset_Turnover': 0.5, 'Inventory_Turnover': 0.5}
    # Efficiency_Score_Most_Recent_Year = dict_eff[f'Asset Turnover Ratio{most_recent_year}'] * efficiency_weights['Asset_Turnover'] + dict_eff[f'Inventory Turnover Ratio{most_recent_year}'] * efficiency_weights['Inventory_Turnover'] if all(val != "N/A" for val in [dict_eff[f'Asset Turnover Ratio{most_recent_year}'], dict_eff[f'Inventory Turnover Ratio{most_recent_year}']]) else "N/A"
    # Efficiency_Score_Previous_Years = dict_eff[f'Asset Turnover Ratio{previous_years}'] * efficiency_weights['Asset_Turnover'] + dict_eff[f'Inventory Turnover Ratio{previous_years}'] * efficiency_weights['Inventory_Turnover'] if all(val != "N/A" for val in [dict_eff[f'Asset Turnover Ratio{previous_years}'], dict_eff[f'Inventory Turnover Ratio{previous_years}']]) else "N/A"
    # dict_eff[f'Efficiency Score {most_recent_year}'] = round(Efficiency_Score_Most_Recent_Year, 3) if Efficiency_Score_Most_Recent_Year != "N/A" else "N/A"
    # dict_eff[f'Efficiency Score {previous_years}'] = round(Efficiency_Score_Previous_Years, 3) if Efficiency_Score_Previous_Years != "N/A" else "N/A"


    # PROFITABILITY
    net_income = fetch_line_data(matched_income_statement, 'Net Income')
    comprehensive_income = fetch_line_data(df_income_statement, 'Comprehensive Income - Hedging Gain/Loss')
    ebitda = fetch_line_data(df_income_statement, 'EBITDA')
    net_sales = fetch_line_data(matched_income_statement, 'Net Sales')
    gross_profit = fetch_line_data(matched_income_statement, 'Gross Profit')
    operating_profit = fetch_line_data(matched_income_statement, 'Operating Profit')
    total_liabilities = fetch_line_data(df_balance_sheet, 'Total Liabilities')

    # Return_on_Assets_Most_Recent_Year = net_income[0] / total_assets[0] if total_assets[0] != 0 and net_income[0] != "N/A" else "N/A"
    # Return_on_Asset_Previous_Years = np.mean(net_income[1:])/np.mean(total_assets[1:]) if np.mean(total_assets[1:]) != 0 else "N/A"
    # Return_on_Equity_Most_Recent_Year = net_income[0] / total_shareholders_equity[0] if total_shareholders_equity[0] != 0 and net_income != "N/A" else "N/A"
    # Return_on_Equity_Most_Previous_Years = np.mean(net_income[1:])/np.mean(total_shareholders_equity[1:]) if np.mean(total_shareholders_equity[1:]) != 0 and net_income != "N/A" else "N/A"
    # Comprehensive_ROA_rec = comprehensive_income[0] / total_assets[0] if total_assets[0] != 0 and comprehensive_income != "N/A" else "N/A"
    # Comprehensive_ROA_prev = np.mean(comprehensive_income[1:])/np.mean(total_assets[1:]) if np.mean(total_assets[1:]) != 0 and comprehensive_income != "N/A" else "N/A"
    # Comprehensive_ROE_rec = comprehensive_income[0] / total_shareholders_equity[0] if total_shareholders_equity[0] != 0 and comprehensive_income != "N/A" else "N/A"
    # Comprehensive_ROE_prev = np.mean(comprehensive_income[1:]) / np.mean(total_shareholders_equity[1:]) if np.mean(total_shareholders_equity[1:]) != 0 and comprehensive_income != "N/A" else "N/A"
    # Gross_Profit_Margin = gross_profit[0] / sales[0] if sales[0] != 0 and gross_profit != "N/A" else "N/A"
    # Operating_Profit_Margin = operating_profit[0] / sales[0] if sales[0] != 0 and operating_profit != "N/A" and sales != "N/A" else "N/A"
    # EBITDA_Margin = ebitda[0] / sales[0] if sales[0] != 0 and ebitda != "N/A" and sales != "N/A" else "N/A"
    # Net_Profit_Margin = net_income[0] / sales[0] if sales[0] != 0 and net_income != "N/A" and sales != "N/A" else "N/A"
    # # Asset_Turnover = sales[0] / total_assets[0] if total_assets[0] != 0 and sales != "N/A" else "N/A"
    # # Fixed_Asset_Turnover = sales[0] / fixed_assets[0] if fixed_assets[0] != 0 and sales != "N/A" and fixed_assets != "N/A" else "N/A"
    # Return_on_Invested_Capital = operating_profit[0] / (total_liabilities[0] + total_shareholders_equity[0]) if (total_liabilities[0] + total_shareholders_equity[0]) != 0 and operating_profit != "N/A" else "N/A"


    dict_prof_ROA = ratios_of_each_year(net_income, total_assets, 'Return on Assets ROA', df_balance_sheet)
    dict_prof_ROE = ratios_of_each_year(net_income, total_shareholders_equity, 'Return on Equity ROE', df_balance_sheet)
    dict_prof_Comprehensive_ROA_rec = ratios_of_each_year(comprehensive_income, total_assets, 'Comprehensive - ROA', df_balance_sheet)
    dict_prof_Comprehensive_ROE_rec = ratios_of_each_year(comprehensive_income, total_shareholders_equity, 'Comprehensive - ROE', df_balance_sheet)
    dict_prof_Gross_Profit_Margin = ratios_of_each_year(gross_profit, sales, 'Gross Profit Margin', df_balance_sheet)
    dict_prof_Operating_Profit_Margin = ratios_of_each_year(operating_profit, sales, 'Operating Profit Margin', df_balance_sheet)
    dict_prof_EBITDA_Margin = ratios_of_each_year(ebitda, sales, 'EBITDA Margin', df_balance_sheet)
    dict_prof_Net_Profit_Margin = ratios_of_each_year(net_income, sales, 'Net Profit Margin', df_balance_sheet)
    dict_prof_Return_on_Invested_Capital = ratios_of_each_year(operating_profit, np.array(total_liabilities) + np.array(total_shareholders_equity).tolist(), 'Return on Invested Capital', df_balance_sheet)
    

    dict_prof = {**dict_prof_ROA, **dict_prof_ROE, **dict_prof_Comprehensive_ROA_rec, **dict_prof_Comprehensive_ROE_rec, **dict_prof_Gross_Profit_Margin, **dict_prof_Operating_Profit_Margin, **dict_prof_EBITDA_Margin, **dict_prof_Net_Profit_Margin, **dict_prof_Return_on_Invested_Capital}


    # dict_prof = {}
    # dict_prof[f'Return on Assets ROA {most_recent_year}'] = round(Return_on_Assets_Most_Recent_Year, 3) if Return_on_Assets_Most_Recent_Year != "N/A" else "N/A"
    # dict_prof[f'Return on Assets ROA {previous_years}'] = round(Return_on_Asset_Previous_Years, 3) if Return_on_Asset_Previous_Years != "N/A" else "N/A"
    # dict_prof[f'Return on Equity ROE {most_recent_year}'] = round(Return_on_Equity_Most_Recent_Year, 3) if Return_on_Equity_Most_Recent_Year != "N/A" else "N/A"
    # dict_prof[f'Return on Equity ROE {previous_years}'] = round(Return_on_Equity_Most_Previous_Years, 3) if Return_on_Equity_Most_Previous_Years != "N/A" else "N/A"
    # dict_prof[f'Comprehensive - ROA {most_recent_year}'] = round(Comprehensive_ROA_rec, 3) if Comprehensive_ROA_rec != "N/A" else "N/A"
    # dict_prof[f'Comprehensive - ROA {previous_years}'] = round(Comprehensive_ROA_prev, 3) if Comprehensive_ROA_prev != "N/A" else "N/A"
    # dict_prof[f'Comprehensive - ROE {most_recent_year}'] = round(Comprehensive_ROE_rec, 3) if Comprehensive_ROE_rec != "N/A" else "N/A"
    # dict_prof[f'Comprehensive - ROE {previous_years}'] = round(Comprehensive_ROE_prev, 3) if Comprehensive_ROE_prev != "N/A" else "N/A"
    # dict_prof[f'Gross Profit Margin {most_recent_year}'] = round(Gross_Profit_Margin, 3) if Gross_Profit_Margin != "N/A" else "N/A"
    # dict_prof[f'Operating Profit Margin {most_recent_year}'] = round(Operating_Profit_Margin, 3) if Operating_Profit_Margin != "N/A" else "N/A"
    # dict_prof[f'EBITDA Margin {most_recent_year}'] = round(EBITDA_Margin, 3) if EBITDA_Margin != "N/A" else "N/A"
    # dict_prof[f'Net Profit Margin {most_recent_year}'] = round(Net_Profit_Margin, 3) if Net_Profit_Margin != "N/A" else "N/A"
    # dict_prof[f'Asset Turnover {most_recent_year}'] = round(Asset_Turnover, 3) if Asset_Turnover != "N/A" else "N/A"
    # dict_prof[f'Fixed Asset Turnover {most_recent_year}'] = round(Fixed_Asset_Turnover, 3) if Fixed_Asset_Turnover != "N/A" else "N/A"
    # dict_prof[f'Return on Invested Capital {most_recent_year}'] = round(Return_on_Invested_Capital, 3) if Return_on_Invested_Capital != "N/A" else "N/A"

    
    # profitability_weights = {'ROA': 0.5, 'ROE': 0.5}
    # Profitability_Score_Most_Recent_Year = dict_prof[f'Return on Assets ROA {most_recent_year}'] * profitability_weights['ROA'] + dict_prof[f'Return on Equity ROE {most_recent_year}'] * profitability_weights['ROE'] if all(val != "N/A" for val in [dict_prof[f'Return on Assets ROA {most_recent_year}'], dict_prof[f'Return on Equity ROE {most_recent_year}']]) else "N/A"
    # Profitability_Score_Previous_Years = dict_prof[f'Return on Assets ROA {previous_years}'] * profitability_weights['ROA'] + dict_prof[f'Return on Equity ROE {previous_years}'] * profitability_weights['ROE'] if all(val != "N/A" for val in [dict_prof[f'Return on Assets ROA {previous_years}'], dict_prof[f'Return on Equity ROE {previous_years}']]) else "N/A"
    # dict_prof[f'Profitability Score {most_recent_year}'] = round(Profitability_Score_Most_Recent_Year, 3) if Profitability_Score_Most_Recent_Year != "N/A" else "N/A"
    # dict_prof[f'Profitability Score {previous_years}'] = round(Profitability_Score_Previous_Years, 3) if Profitability_Score_Previous_Years != "N/A" else "N/A"


    # Market Performance Context
    # PE Ratio
    dict_MP = {}
    years = get_year_and_month(df_balance_sheet)
    EPS_diluted = fetch_line_data(matched_income_statement, 'EPS (diluted)')
    EPS_basic = fetch_line_data(matched_income_statement, "EPS (basic)")
    stock_prices_of_years = [get_price_for_date(year, df_price) for year in years]
    dict_MP_P_E_Ratio = ratios_of_each_year(stock_prices_of_years, EPS_basic, 'Price to Earnings Ratio (P/E)', df_balance_sheet)
    dict_MP_Reverse_P_E = ratios_of_each_year(EPS_diluted, stock_prices_of_years, 'Reverse PE Ratio', df_balance_sheet)
    dict_MP_P_d_E_Ratio = ratios_of_each_year(stock_prices_of_years, EPS_diluted, 'Price to Diluted Earnings Ratio', df_balance_sheet)
    dict_MP_Reverse_P_d_E_Ratio = ratios_of_each_year(EPS_diluted, stock_prices_of_years, 'Reverse Diluted PE Ratio', df_balance_sheet)
    # print(EPS_basic)
    # print(EPS_diluted)
    # print(stock_prices_of_years)




    # for index in range(len(years)):
    #     stock_price_of_year = get_price_for_date(years[index], df_price)
    #     P_E_Ratio = stock_price_of_year/EPS_basic[index] if EPS_basic[index] != 0 else "N/A"
    #     P_d_E_Ratio = stock_price_of_year/EPS_diluted[index] if EPS_diluted[index] != 0 else "N/A"
    #     dict_MP[f'Price to Earnings Ratio (P/E) {years[index]}'] = round(P_E_Ratio, 3) if P_E_Ratio != "N/A" else "N/A"
    #     dict_MP[f'Reverse PE Ratio {years[index]}'] = round(1/P_E_Ratio, 3) if P_E_Ratio != "N/A" else "N/A"
    #     dict_MP[f'Price to Diluted Earnings Ratio {years[index]}'] = round(P_d_E_Ratio, 3) if P_d_E_Ratio != "N/A" else "N/A"
    #     dict_MP[f'Reverse Diluted PE Ratio {years[index]}'] = round(1/P_d_E_Ratio, 3) if P_d_E_Ratio != "N/A" else "N/A"
    
    # Market Book Ratio
    Book_Value_per_Share = fetch_line_data(df_balance_sheet, 'Book Value per Share')
    dict_MP_M_B_Ratio = ratios_of_each_year(stock_prices_of_years, Book_Value_per_Share, 'Market to Book Ratio', df_balance_sheet)
    
    
    dict_MP = {**dict_MP_P_E_Ratio, **dict_MP_Reverse_P_E, **dict_MP_P_d_E_Ratio, **dict_MP_Reverse_P_d_E_Ratio, **dict_MP_M_B_Ratio}


    # for index in range(len(years)):
    #     stock_price_of_year = get_price_for_date(years[index], df_price)
    #     M_B_Ratio = stock_price_of_year/Book_Value_per_Share[index] if Book_Value_per_Share[index] != 0 else "N/A"
    #     dict_MP[f'Market to Book Ratio {years[index]}'] = round(M_B_Ratio, 3) if M_B_Ratio != "N/A" else "N/A"

    
    # LEVERAGE
    # Debt_ratio_of_most_recent = total_liabilities[0]/total_assets[0] if total_assets[0] != 0 else "N/A"
    # Debt_ratio_prev_yrs = np.mean(total_liabilities[1:])/np.mean(total_assets[1:]) if np.mean(total_assets[1:]) != 0 else "N/A"
    Minority_Interest = fetch_line_data(df_balance_sheet, "Minority Interest Under Canadian GAAP")
    # Alt_debt_ratio_most_recent = (total_liabilities[0] + Minority_Interest[0])/total_assets[0] if Minority_Interest != "N/A" and total_assets[0] != 0 else "N/A"
    # Alt_debt_ratio_prev = (np.mean(total_liabilities[1:]) + np.mean(Minority_Interest[1:]))/np.mean(total_assets[1:]) if Minority_Interest != "N/A" and np.mean(total_assets[1:]) != 0 else "N/A"

    # Equity_ratio_most_rec = total_shareholders_equity[0]/total_assets[0] if total_assets[0] != 0 else "N/A"
    # Equity_ratio_prev_yrs = np.mean(total_shareholders_equity[1:])/np.mean(total_assets[1:]) if np.mean(total_assets[1:]) != 0 else "N/A"
    
    dict_lev_Debt_ratio = ratios_of_each_year(total_liabilities, total_assets, 'Debt Ratio', df_balance_sheet)
    dict_lev_Alt_debt_ratio = ratios_of_each_year(total_liabilities, Minority_Interest, 'Alternative Debt Ratio', df_balance_sheet)
    dict_lev_Equity_ratio = ratios_of_each_year(total_shareholders_equity, total_assets, 'Equity Ratio', df_balance_sheet)

    dict_lev = {**dict_lev_Debt_ratio, **dict_lev_Alt_debt_ratio, **dict_lev_Equity_ratio}

    # dict_lev = {}
    # dict_lev[f'Debt Ratio{most_recent_year}'] = round(Debt_ratio_of_most_recent, 3) if Debt_ratio_of_most_recent != "N/A" else "N/A"
    # dict_lev[f'Debt Ratio{previous_years}'] = round(Debt_ratio_prev_yrs, 3) if Debt_ratio_prev_yrs != "N/A" else "N/A"
    # dict_lev[f'Alternative Debt Ratio{most_recent_year}'] = round(Alt_debt_ratio_most_recent, 3) if Alt_debt_ratio_most_recent != "N/A" else "N/A"
    # dict_lev[f'Alternative Debt Ratio{previous_years}'] = round(Alt_debt_ratio_prev, 3) if Alt_debt_ratio_prev != "N/A" else "N/A"
    # dict_lev[f'Equity Ratio{most_recent_year}'] = round(Equity_ratio_most_rec, 3) if Equity_ratio_most_rec != "N/A" else "N/A"
    # dict_lev[f'Equity Ratio{previous_years}'] = round(Equity_ratio_prev_yrs, 3) if Equity_ratio_prev_yrs != "N/A" else "N/A"

    # COVERAGE
    EBIT = fetch_line_data(matched_income_statement, 'EBIT (Operating Income)')
    interest_expense = fetch_line_data(matched_income_statement, 'Interest Expense')
    depreciation_amortization = fetch_line_data(matched_income_statement, 'Depreciation & Amortization Expense')
    CMLTD = fetch_line_data(df_balance_sheet, 'ST Debt & Curr. Portion LT Debt')
    operating_cash_flow = fetch_line_data(matched_income_statement, 'Operating Cash Flow')

    # interest_coverage_most_recent = EBIT[0] / interest_expense[0] if interest_expense[0] != 0 else "N/A"
    # interest_coverage_prev_yrs = np.mean(EBIT[1:]) / np.mean(interest_expense[1:]) if np.mean(interest_expense[1:]) != 0 else "N/A"

    # fixed_charge_coverage_most_recent = EBIT[0] / (interest_expense[0] + CMLTD[0]) if (interest_expense[0] + CMLTD[0]) != 0 else "N/A"
    # fixed_charge_coverage_prev_yrs = np.mean(EBIT[1:]) / (np.mean(interest_expense[1:]) + np.mean(CMLTD[1:])) if (np.mean(interest_expense[1:]) + np.mean(CMLTD[1:])) != 0 else "N/A"

    # cash_flow_coverage_most_recent = (net_income[0] + depreciation_amortization[0]) / CMLTD[0] if CMLTD[0] != 0 else "N/A"
    # cash_flow_coverage_prev_yrs = (np.mean(net_income[1:]) + np.mean(depreciation_amortization[1:])) / np.mean(CMLTD[1:]) if np.mean(CMLTD[1:]) != 0 else "N/A"

    # operating_cash_flow_ratio_most_recent = operating_cash_flow[0] / total_current_liabilities[0] if total_current_liabilities[0] != 0 and operating_cash_flow != "N/A" else "N/A"
    # operating_cash_flow_ratio_prev_yrs = np.mean(operating_cash_flow[1:]) / np.mean(total_current_liabilities[1:]) if np.mean(total_current_liabilities[1:]) != 0 and operating_cash_flow != "N/A" else "N/A"


    dict_cov_interest_coverage = ratios_of_each_year(EBIT, interest_expense, 'Interest Coverage Ratio', df_balance_sheet)
    dict_cov_fixed_charge_covereage = ratios_of_each_year(EBIT, (np.array(interest_expense) + np.array(CMLTD)).tolist(), 'Fixed-Charge Coverage Ratio', df_balance_sheet)
    dict_cov_cash_flow_coverage = ratios_of_each_year((np.array(net_income) + np.array(depreciation_amortization)).tolist(), CMLTD, 'Cash Flow Coverage Ratio', df_balance_sheet)
    dict_cov_operating_cash_flow = ratios_of_each_year(operating_cash_flow, total_current_liabilities, 'Operating Cash Flow Ratio', df_balance_sheet)

    dict_cov = {**dict_cov_interest_coverage, **dict_cov_fixed_charge_covereage, **dict_cov_cash_flow_coverage, **dict_cov_operating_cash_flow}


    # dict_cov = {}
    # dict_cov[f'Interest Coverage Ratio{most_recent_year}'] = round(interest_coverage_most_recent, 3) if interest_coverage_most_recent != "N/A" else "N/A"
    # dict_cov[f'Interest Coverage Ratio{previous_years}'] = round(interest_coverage_prev_yrs, 3) if interest_coverage_prev_yrs != "N/A" else "N/A"
    # dict_cov[f'Fixed-Charge Coverage Ratio{most_recent_year}'] = round(fixed_charge_coverage_most_recent, 3) if fixed_charge_coverage_most_recent != "N/A" else "N/A"
    # dict_cov[f'Fixed-Charge Coverage Ratio{previous_years}'] = round(fixed_charge_coverage_prev_yrs, 3) if fixed_charge_coverage_prev_yrs != "N/A" else "N/A"
    # dict_cov[f'Cash Flow Coverage Ratio{most_recent_year}'] = round(cash_flow_coverage_most_recent, 3) if cash_flow_coverage_most_recent != "N/A" else "N/A"
    # dict_cov[f'Cash Flow Coverage Ratio{previous_years}'] = round(cash_flow_coverage_prev_yrs, 3) if cash_flow_coverage_prev_yrs != "N/A" else "N/A"
    # dict_cov[f'Operating Cash Flow Ratio{most_recent_year}'] = round(operating_cash_flow_ratio_most_recent, 3) if operating_cash_flow_ratio_most_recent != "N/A" else "N/A"
    # dict_cov[f'Operating Cash Flow Ratio{previous_years}'] = round(operating_cash_flow_ratio_prev_yrs, 3) if operating_cash_flow_ratio_prev_yrs != "N/A" else "N/A"


    # Creating DataFrames
    liquidity_df = pd.DataFrame(list(dict_liq.items()), columns=['Metric', 'Value'])

    liquidity_df['Focus'] = 'Liquidity'

    solvency_df = pd.DataFrame(list(dict_solv.items()), columns=['Metric', 'Value'])
    solvency_df['Focus'] = 'Solvency'

    efficiency_df = pd.DataFrame(list(dict_eff.items()), columns=['Metric', 'Value'])
    efficiency_df['Focus'] = 'Efficiency'

    profitability_df = pd.DataFrame(list(dict_prof.items()), columns=['Metric', 'Value'])
    profitability_df['Focus'] = 'Profitability'

    market_performance_df = pd.DataFrame(list(dict_MP.items()), columns=['Metric', 'Value'])
    market_performance_df['Focus'] = 'Market Performance'

    leverage_df = pd.DataFrame(list(dict_lev.items()), columns=['Metric', 'Value'])
    leverage_df['Focus'] = 'Leverage'

    coverage_df = pd.DataFrame(list(dict_cov.items()), columns=['Metric', 'Value'])
    coverage_df['Focus'] = 'Coverage'

    df_combined = pd.concat([liquidity_df, solvency_df, efficiency_df, profitability_df, market_performance_df, leverage_df, coverage_df], ignore_index=True)
    
    # The focus is only displayed next to the first term
    # df_combined['Focus'] = df_combined['Focus'].where(df_combined['Focus'] != df_combined['Focus'].shift(), "")
    
    df_combined = df_combined[['Focus', 'Metric', 'Value']]

    # Display the Entire DataFrame
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.width', None)  
    pd.set_option('display.max_colwidth', None)  


############# NEW DATAFRAME ##############
    year_pattern = re.compile(r"[A-Z]{3} '\d{2}")
    year_range_pattern = re.compile(r"\d{4}-\d{4}")


    def extract_time_period(metric):
        # Find all matches of the year pattern
        match = year_pattern.findall(metric)
        if match:
            # If a match is found, return the last occurrence
            return match[-1]
        # If no match is found, return 'Unknown' or a default value
        elif any(year_range_pattern.findall(metric)):
            return year_range_pattern.search(metric).group()
        return 'Unknown'
    
    def clean_metric_name(metric):
        metric = year_pattern.sub('', metric)
        # Remove any year range like "2014-2022" from the metric name
        metric = year_range_pattern.sub('', metric)
        # Strip any remaining leading or trailing whitespace
        return metric.strip()

    df_combined['Time'] = df_combined['Metric'].apply(extract_time_period)
    df_combined['Metric'] = df_combined['Metric'].apply(clean_metric_name)  

    df_combined['Metric'] = df_combined['Focus'] + "_" + df_combined['Metric']
    df_combined.drop(columns='Focus', inplace=True)  # Drop the original 'Focus' column as it's now part of 'Metric'
    print(df_combined)

    # Pivot the table to form a DataFrame with a multi-level column index
    result_df = df_combined.pivot_table(
        index='Time',
        columns='Metric',
        values='Value',
        aggfunc='first'
    )

    # Optionally, you can create a more explicit multi-level column header
    result_df.columns = pd.MultiIndex.from_tuples(
        [(col.split('_')[0], col.split('_')[1]) for col in result_df.columns], names=['Focus', 'Metric']
    )

    result_df.reset_index(inplace=True)  # Ensure 'Time' is a column for the operations
    result_df['Time'] = pd.to_datetime(result_df['Time'].str.replace("'", ""), format='%b %y')
    result_df.sort_values('Time', ascending=False, inplace=True)
    result_df['Time'] = result_df['Time'].dt.strftime('%b \'%y')

    # print(result_df['Time'])

    # Save to CSV
    result_df.to_csv('ratios.csv', index=False)

    # Display the DataFrame
    # print(result_df)  
    # ratio_names = result_df.columns.get_level_values(1).unique().tolist()
    ratio_names = [' - '.join(col) if isinstance(col, tuple) else col for col in result_df.columns][1:]
    # print(ratio_names)

    # Now, ratio_names contains all the unique ratio names

    # Return the DataFrame for further use
    return result_df



df_ratios = perform_financial_analysis(df_balance_sheet, df_income_statement, df_price)
print(df_ratios)


