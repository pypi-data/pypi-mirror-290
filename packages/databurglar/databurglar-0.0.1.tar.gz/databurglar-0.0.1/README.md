# qa - SqlAlchemy Plugin for Data Collection

<p>
  <b>SOMETHING</b> happened at <b>SOMETIME</b> and we would like to <b>COLLECT</b> it.
</p>

<hr />

### Init
```python
from qa.models import setup_data_collection, setup_surveys

engine: Engine = ...

## setup tables to collect data based on a `UserEvent`
setup_data_collection(
    engine,
    UserEvent
)

## setup tables to build dynamic data collection forms/surveys
setup_surveys(engine)
```

### Queries

### Commands

### Local Project Setup
```
  python3 -m venv env
  .\env\Scripts\activate
  pip install -r requirements.txt
```
