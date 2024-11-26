from fosforml.model_manager.snowflakesession import get_session, get_connection_params
session = get_session()
connection_params = get_connection_params()

from sklearn.ensemble._forest import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd

m_dataset = load_iris() 
feature_names = m_dataset.feature_names
u_features = [col.replace(" ","_").replace("(","").replace(")","") for col in feature_names]
m_df = pd.DataFrame(m_dataset.data,columns=u_features)
m_df["Target"] = m_dataset.target


x_train,x_test,y_train,y_test = train_test_split(m_df.iloc[:,:-1],m_df['Target'])
model = DecisionTreeClassifier()
model.fit(x_train,y_train)

y_pred = pd.DataFrame(model.predict(x_test),columns=["Predicted"])
y_prob = pd.DataFrame(model.predict_proba(x_test),columns=['a','b','c'])


from fosforml import register_model

register_model(
  model_obj=model,
  session=session,
  x_train=x_train,
  y_train=y_train,
  x_test=x_test,
  y_test=y_test,
  y_pred=y_pred,
  y_prob=y_prob,
  source="Notebook",
  dataset_name="HR_CHURN",
  dataset_source="InMemory",
  name="MyModel",
  description="This is a sklearn model",
  flavour="sklearn",
  model_type="classification",
  conda_dependencies=["scikit-learn==1.3.2"]
)


# dev -n insight exec -it runtestdebugi-115339-job-ds6kt bash
