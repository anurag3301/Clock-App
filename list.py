import pickle
alarm_data = {
    "alarm1": [0, 0, 'AM', False],
    "alarm2": [0, 0, 'AM', False],
    "alarm3": [0, 0, 'AM', False],
    "alarm4": [0, 0, 'AM', False],
    "alarm5": [0, 0, 'AM', False],
}

pickle_out = open("alarm_data.pickle", "wb")
pickle.dump(alarm_data, pickle_out)
pickle_out.close()

pickle_in = open("alarm_data.pickle", "rb")
alarm_data = pickle.load(pickle_in)
pickle_in.close()
print(alarm_data)
print(type(alarm_data))