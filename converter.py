import sys
import json
import base64
import os
import math
from shutil import copyfile

if len(sys.argv) > 2:
    input_path = sys.argv[1]
    out_path = sys.argv[2]
    try:
        jsonFile = open(input_path,'r')
        values = json.load(jsonFile)
        assets= values["assets"]

        #create train and test dir in outpath
        train_dir = out_path + "/train"
        test_dir = out_path + "/test"

        #get training index
        training_index = math.ceil(75 * ( len(assets) /100 ))
        print("Training IndeX: ",training_index , " - ",len(assets))
        try:
            if not os.path.exists(out_path):
                os.mkdir(out_path)
            os.mkdir(train_dir)
            os.mkdir(test_dir)
        except OSError:
            print ("Creation of the directory %s failed" % out_path)

        
        for key,value in enumerate(assets):
            data = {}
            info = assets[value]["asset"]
            regions = assets[value]["regions"]
            imagePath = info["path"].replace("file:","")
            
            #Create each image jsonfile           

            data["version"] = "4.5.6"
            data["flags"] = {}
            data["shapes"] = []
            data["imagePath"] = info["name"]
            data["imageHeight"] = info["size"]["width"]
            data["imageWidth"] = info["size"]["height"]

            #set Region
            for region in regions:
                region_item = {}
                region_item["points"] = []
                region_item["label"] =   region["tags"][0] if len(region["tags"]) > 0 else ""
                region_item["group_id"] = None
                region_item["shape_type"] = "polygon"
                region_item["flags"] = {}

                for point in region["points"]:
                    item = [point["x"],point["y"]]
                    region_item["points"].append(item)
                
                data["shapes"].append(region_item)
            #image Data
            with open(imagePath, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                imageData = encoded_string.decode("utf-8")
                data["imageData"] = imageData
                
            #write json file
            fileName = ""
            if key < training_index:
                if os.path.exists(train_dir):
                    fileName = train_dir + "/" + info["name"].replace(".jpg",".json")
                    copyImageFileName = train_dir + "/" + info["name"]
                    copyfile(imagePath,copyImageFileName)
            else:
                if os.path.exists(test_dir):
                    fileName = test_dir + "/" + info["name"].replace(".jpg",".json") 
                    copyImageFileName = test_dir + "/" + info["name"]
                    copyfile(imagePath,copyImageFileName)                   
            
            # Serializing json  
            json_object = json.dumps(data, indent = 4) 
            with open(fileName, "w") as outfile: 
                outfile.write(json_object) 
            print("Write To ",fileName)

        jsonFile.close()
    except IOError:
        print("Error occured when opeing file or json parse error.")

else:
    print("Set Input and Output Path.")
