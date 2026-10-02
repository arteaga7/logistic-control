# logistic-control
A comparative between PySpark, Polars and Pandas commands for data analysis is presented.

## 🌎 Repository Structure
```
logistic-control/
│
├── .gitignore
├── venv/                       # Virtual enviroment
└── requirements.txt
└── Notebooks                   # Contains all Jupyter Notebooks
    └── nb.ipynb
```
## ✨ Details



## 🚀 How to run locally
1. Clone this repository:
```
git clone https://github.com/arteaga7/logistic-control.git
```
2. Set virtual environment and install dependencies.

For Windows:
```
uv venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\Activate.ps1
uv pip install --link-mode=copy -r requirements.txt
```

For Linux:
```
uv venv venv
source venv/bin/activate
uv pip install -r requirements.txt
```
3. Run "Notebooks/nb.ipynb".
