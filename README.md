# Setup the environment
**Recommend do this in a separate environment to avoid conflicts**
```
bash setup.sh
```
Or run each commands of the bash file
```
pip install -r requirements.txt
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm
python -m spacy download en
```
# Run the Application
**In the root of the project directory**
```
streamlit run main.py --server.maxUploadSize 2000
```
Or 

Using the test environment with the following steps, this will load some default files

1. Under the root directory of the project create a data/pickles folder
2. Put these three pickles into the pickles folder: clean_test, data7_0, test_data, default_comments
3. Change env variable in file configuration/AppConfiguration.py to test
4. Run the following command
```
streamlit run main.py --server.maxUploadSize 2000
```