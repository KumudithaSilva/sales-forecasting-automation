import os
import pandas as pd
import requests
from dotenv import load_dotenv

def main():
    """
    -----------------------------------------------------------
    Sales Forecasting Script using IBM watsonx.ai Deployment API
    -----------------------------------------------------------
    Steps:
        1. Load secrets from .env (API key, Deployment URL, Excel file)
        2. Generate IAM token using API key
        3. Load Excel input data
        4. Preprocess data (convert dates, fill missing values)
        5. Send data to the deployed model endpoint
        6. Receive predictions and save output to Excel
    -----------------------------------------------------------
    """

    # -----------------------------------------------------------
    # 1. Load environment variables from .env file
    # -----------------------------------------------------------
    load_dotenv()
    API_KEY = os.getenv("WML_API_KEY")
    DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL") 
    EXCEL_FILE = os.getenv("EXCEL_FILE", "sales_data.xlsx") 

    if not API_KEY or not DEPLOYMENT_URL:
        raise ValueError("Missing environment variables. Check your .env file.")

    # -----------------------------------------------------------
    # 2. Get IAM access token for authentication
    # -----------------------------------------------------------
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    )
    token_response.raise_for_status()
    mltoken = token_response.json()["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mltoken}"
    }

    # -----------------------------------------------------------
    # 3. Load Excel input data
    # -----------------------------------------------------------
    df = pd.read_excel(EXCEL_FILE)

    # -----------------------------------------------------------
    # 4. Preprocess data
    # -----------------------------------------------------------
    # Convert date column to string to match model expectations
    if "Date" in df.columns:
        df["Date"] = df["Date"].astype(str)

    # Fill blank cells to avoid scoring errors
    df.fillna(0, inplace=True)

    # -----------------------------------------------------------
    # 5. Prepare payload for the model
    # -----------------------------------------------------------
    fields = df.columns.tolist()
    values = df.values.tolist()

    payload = {
        "input_data": [
            {
                "fields": fields,
                "values": values
            }
        ]
    }

    # -----------------------------------------------------------
    # 6. Call Watson ML deployment endpoint
    # -----------------------------------------------------------
    try:
        response = requests.post(DEPLOYMENT_URL, json=payload, headers=headers)
        response.raise_for_status()

        results = response.json()

        # Extract prediction results
        df["Sales"] = [item[0] for item in results["predictions"][0]["values"]]

        # Save final output with predictions
        df.to_excel("sales_forecasted.xlsx", index=False)

        print("Forecasting completed. Results saved to sales_forecasted.xlsx")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while scoring: {e}")

# -----------------------------------------------------------
# Script Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    main()
