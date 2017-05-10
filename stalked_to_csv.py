import os
import json
import sys
from subprocess import check_call

data_path = "/home/agu/tinder_stalker/data/"

csv_lines = ["user_id,gender,age,lat,lon,timestamp\n"]

_, _, filenames = next(os.walk(data_path))
for filename in filenames:
	if filename[-3:] == "txt":
		with open(data_path + filename, "r") as f:
			file_str = f.read()

		users_dict = json.loads(file_str.replace("'", '"'))
		date_str = filename[0:4] + "-" + filename[4:6] + "-" + filename[6:8] + " " + filename[9:11] + ":00"

		for user_id, data in users_dict.items():
			csv_lines.append("%s,%s,%d,%s,%s,%s\n" % (user_id, data["gender"], data["age"], str(data["lat"]), str(data["lon"]), date_str))

dataset_name = sys.argv[1]

with open("/home/agu/tinder_stalker/datasets/" + dataset_name + ".csv", "w") as f:
	f.writelines(csv_lines)

tar_cmd = "tar czf %s.tar.gz %s.csv" % (dataset_name, dataset_name)
check_call(tar_cmd.split(), cwd="/home/agu/tinder_stalker/datasets")
remove_cmd = "rm /home/agu/tinder_stalker/datasets/" + dataset_name + ".csv"
check_call(remove_cmd.split())