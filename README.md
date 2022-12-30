# Setup the environment under project root directory
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
2. Put these four pickles into the pickles folder: clean_test, data7_0, test_data, default_comments
3. Change env variable in file configuration/AppConfiguration.py to test
4. Run the following command

```
streamlit run main.py --server.maxUploadSize 2000
```

# Screenshots
### Data Management
![Screen Shot 2022-12-16 at 3 08 50 PM](https://user-images.githubusercontent.com/61313159/208180875-5e8d79d3-d5ec-425f-813e-d9b42e41ccbe.png)
### Dashboard
![Screen Shot 2022-12-16 at 3 11 19 PM](https://user-images.githubusercontent.com/61313159/208181319-31d1d911-f6ab-4ca5-9109-f28d3c7df4c8.png)
### Models
![Screen Shot 2022-12-16 at 3 12 48 PM](https://user-images.githubusercontent.com/61313159/208181518-adfc2878-fadd-46d9-9e01-48faff8791bb.png)
### NLP
![Screen Shot 2022-12-16 at 3 13 24 PM](https://user-images.githubusercontent.com/61313159/208181604-44c2f9bd-03b4-4f99-bcc4-ce4694d98164.png)
