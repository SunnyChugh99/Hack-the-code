from fosforml.model_manager.snowflakesession import get_session
session = get_session()

from sklearn.ensemble._forest import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd

m_dataset = load_iris() 
feature_names = m_dataset.feature_names
u_features = [col.replace(" ","_").replace("(","").replace(")","") for col in feature_names]
m_df = pd.DataFrame(m_dataset.data,columns=u_features)
m_df["Target"] = m_dataset.target


x_train,x_test,y_train,y_test = train_test_split(m_df.iloc[:,:-1],m_df['Target'])
model = RandomForestClassifier()
model.fit(x_train,y_train)

y_pred = pd.DataFrame(model.predict(x_test),columns=["Predicted"])


from fosforml import register_model
register_model(
  model_obj=model,
  session=session,
  x_train=x_train,
  y_train=y_train,
  x_test=x_test,
  y_test=y_test,
  y_pred=y_pred,
    dataset_name = "iris",
    dataset_source = "iris",
  name="SklearnMulitClassModel",
  description="This is a test sklearn model",
  flavour="sklearn",
  model_type="classification",
  conda_dependencies=["scikit-learn==1.3.2"],
    source="NOTEBOOK"
)


from sklearn.ensemble._forest import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pandas as pd

m_dataset = load_breast_cancer() 
feature_names = m_dataset.feature_names
u_features = [feature.replace(" ","_") for feature in feature_names]
m_df = pd.DataFrame(m_dataset.data,columns=u_features)
m_df["Target"] = m_dataset.target


x_train,x_test,y_train,y_test = train_test_split(m_df.iloc[:,:-1],m_df['Target'])
model = RandomForestClassifier()
model.fit(x_train,y_train)

y_pred = pd.DataFrame(model.predict(x_test),columns=["Predicted"])


from fosforml import register_model
register_model(
  model_obj=model,
  session=session,
  x_train=x_train,
  y_train=y_train,
  x_test=x_test,
  y_test=y_test,
  y_pred=y_pred,
  name="SklearnBinaryModel",
  description="This is a test sklearn model",
  flavour="sklearn",
  model_type="classification",
  conda_dependencies=["scikit-learn==1.3.2"]
)
