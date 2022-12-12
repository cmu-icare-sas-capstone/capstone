import pickle

with open("./model/dnn_model.pkl", 'rb') as file:
    dnn_model = pickle.load(file)
