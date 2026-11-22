setup:
	python -m pip install -r requirements.txt

pipeline:
	python load_data.py
	python Analysis.py

dashboard:
	python -m streamlit run app.py