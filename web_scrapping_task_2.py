import pandas as pd 
import requests
from bs4 import BeautifulSoup

def get_debt_to_equity_ratio(ticker):
    print(f"Fetching data for {ticker}...")
    url= f"https://finance.yahoo.com/quote/{ticker}/key-statistics"

    headers = {"User-Agent":"Mozilla/5.0"}
    try:
        response = requests.get(url,headers=headers,timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"request error for {ticker}:{e}") 
        return None 
    soup = BeautifulSoup(response.text,"html.parser")

    try:
        rows = soup.find_all("tr")
        for row in rows:
            if "Total Debt/Equity" in row.text:
                print(f"Found Debt To Equity for {ticker}")
                return row.find_all("td")[1].text.strip()
            
    except Exception as e:
        print(f"error parsing data for {ticker}: {e}") 
    print(f"no Debt to Equity ratio found for {ticker}")
    return None



df = pd.read_csv("company_details.csv")
for index,row in df.iterrows():
    ticker = str(row["Ticker Symbol"])
    if pd.notna(ticker):
        df.at[index,"Debt-to-Equity Ratio"] = get_debt_to_equity_ratio(ticker)

df.to_csv("updated_company_details.csv",index = False)
print("Data fetch and saved successfully")                    