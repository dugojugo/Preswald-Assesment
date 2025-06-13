import preswald
import pandas as pd
import plotly.express as px
from preswald import (
    connect,
    get_df,
    plotly,
    slider,
    table,
    text,
    query,
    Workflow,
    sidebar
)

connect()

sidebar(
    defaultopen=True,
    logo="https://upload.wikimedia.org/wikipedia/commons/5/58/Dollar_in_classic_solid_style.svg",
    name="Viresh Bhurke"
)

df = get_df("financial_fraud_dataset")

sql = """SELECT amount, merchant_category,customer_age,device_type FROM financial_fraud_dataset 
WHERE device_type = 'tablet' AND is_fraud = 1;"""

filtered_df = query(sql,"financial_fraud_dataset")

text("# My Data Analysis App")

text("## Financial Fraud Dataset For tablets")
table(filtered_df, title="Filtered Data")

text("## Financial Fraud Scatter Plot")

fig = px.scatter(df, 
                 x="customer_age", 
                 y="amount", 
                 color="merchant_category",
                 title="Amount vs. Customer Age by Merchant Category",
                 labels={
                     "customer_age": "Customer Age",
                     "amount": "Transaction Amount",
                     "merchant_category": "Merchant Category"
                 })

plotly(fig)

text("## Financial Fraud Box Plot")


fig_1 = px.box(filtered_df, 
             x='merchant_category', 
             y='amount',
             title='Transaction Amounts by Merchant Category (Tablet Users)',labels={'amount': 'Transaction Amount', 'merchant_category': 'Category'},)
             
plotly(fig_1)

### IIT DATA CLEANING
text("# IIT Admissions Dashboard")
text("## Unclean IIT Addmisions Data")
dff = get_df("iit")
table(dff, title="Unclean IIT Addmisions Data")
text("## Clean IIT Addmisions Data")
workflow = Workflow()

@workflow.atom()
def load_data():
    df = get_df("iit")
    return df

@workflow.atom(dependencies=["load_data"])
def clean_data(load_data):
    df = load_data.copy()
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
    required_cols = ['year', 'program_name', 'category']
    df.dropna(subset=required_cols, inplace=True)
    return df

@workflow.atom(dependencies=["clean_data"])
def show_table(clean_data):
    return table(clean_data, title="Cleaned IIT Admissions Data")
    
#@workflow.atom(dependencies=["clean_data"])
#def show_chart(clean_data):
 #   avg_ranks = clean_data.groupby("category")["closing_rank"].mean().reset_index()
    
  #  fig = px.bar(avg_ranks, x="category", y="closing_rank", title="Average Closing Rank by Category", labels={"closing_rank": "Avg. Closing Rank", "category": "Category"})
    
   # return plotly(fig)

workflow.execute()







