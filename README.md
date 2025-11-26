# 📊 Sales Forecasting Automation with Watsonx.ai


## 🚀 What is this project?

This project leverages **IBM watsonx.ai AutoAI** to build, train, and deploy a **Sales Forecasting model** using historical sales data. The model predicts future sales trends automatically, allowing businesses to plan and optimize resources more efficiently.

---

## 💡 Why do we need Sales Forecasting?

Sales forecasting is crucial for businesses to:

- Optimize inventory and reduce overstock or stockouts 📦  
- Plan budgets and allocate resources efficiently 💰  
- Identify trends and seasonality to maximize revenue 📈  
- Improve strategic decision-making across departments 🏢  

By automating this process with AI, we save time and reduce human error while generating more accurate predictions.

---

## 🏗 Our Architecture

<img src="https://github.com/user-attachments/assets/f3192e15-a1ee-4957-836d-24fd030f9284" 
     width="500px" 
     style="display: block; margin: 20px auto;" />

1. **Data Preparation**: Historical sales data is collected in Excel and preprocessed (dates converted, missing values handled).  
2. **Model Training**: We use **Watsonx.ai AutoAI** to train multiple models and select the best-performing Random Forest Regressor.  
3. **Deployment**: The model is deployed in a **Watsonx.ai deployment space**, exposed via a public endpoint.  
4. **Scoring Pipeline**: Input data is sent to the endpoint via Python (`requests`) and predictions are returned.  
5. **Output & Analysis**: Forecasted sales are saved back to Excel for visualization and business insights.  


---

## ⚡ Key Highlights & Important Decisions

- ✅ **Switched to Public Endpoint for Scoring**  
  Instead of using the `APIClient` (which caused `invalid_cloud_scenario_url` errors), we opted for direct HTTP requests with the IAM token — simpler and more reliable.

- ✅ **Handled Excel Data Efficiently**  
  Added support for `.xlsx` files with `openpyxl` and implemented preprocessing to automatically convert dates to strings and fill missing values.

- ✅ **Prepared Model Input Dynamically**  
  Ensured that the fields and values sent to the deployment endpoint always match the model’s expectations, preventing misaligned data errors.

- ✅ **Batch Scoring Support**  
  Structured the payload to handle multiple rows at once, making the pipeline more efficient for larger datasets.

- ✅ **Environment-based Secrets Management**  
  Used `.env` files to securely store API keys and deployment URLs, avoiding hardcoding sensitive information.



---

## ⚙️ Areas Needing More Focus

- 🔍 **Input validation**: Some edge-case inputs may still break the pipeline.  
- 📊 **Advanced feature engineering**: Adding more features could improve predictions.  
- ⏱ **Real-time scoring optimization**: Currently, batch scoring works best.  
- 🔄 **Deployment scaling**: Handling multiple simultaneous requests may require attention.  

---
