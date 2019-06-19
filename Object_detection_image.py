

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys


# This is needed since the notebook is stored in the object_detection folder.
def detect(image_name):

	
	sys.path.append("..")
	# Import utilites
	# from utils import label_map_util
	# from utils import visualization_utils as vis_util

	# Name of the directory containing the object detection module we're using.
	MODEL_NAME = 'inference_graph'
	IMAGE_NAME = os.path.join('images',image_name)	
	
	THRESHOLD = 0.6
	# Grab path to current working directory
	CWD_PATH = os.getcwd()

	# Path to frozen detection graph .pb file, which contains the model that is used
	# for object detection.
	PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

	# Path to label map file
	PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

	# Path to image
	PATH_TO_IMAGE = os.path.join(CWD_PATH,image_name)

	# Number of classes the object detector can identify
	NUM_CLASSES = 1

	# Load the label map.
	# Label maps map indices to category names, so that when our convolution
	# network predicts `5`, we know that this corresponds to `king`.
	# Here we use internal utility functions, but anything that returns a
	# dictionary mapping integers to appropriate string labels would be fine
	# label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	# categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	# category_index = label_map_util.create_category_index(categories)

	# Load the Tensorflow model into memory.
	detection_graph = tf.Graph()
	with detection_graph.as_default():
	    od_graph_def = tf.GraphDef()
	    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
	        serialized_graph = fid.read()
	        od_graph_def.ParseFromString(serialized_graph)
	        tf.import_graph_def(od_graph_def, name='')
	    sess = tf.Session(graph=detection_graph)

	# Define input and output tensors (i.e. data) for the object detection classifier

	# Input tensor is the image
	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

	# Output tensors are the detection boxes, scores, and classes
	# Each box represents a part of the image where a particular object was detected
	detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

	# Each score represents level of confidence for each of the objects.
	# The score is shown on the result image, together with the class label.
	detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
	detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

	# Number of objects detected
	num_detections = detection_graph.get_tensor_by_name('num_detections:0')

	# Load image using OpenCV and
	# expand image dimensions to have shape: [1, None, None, 3]
	# i.e. a single-column array, where each item in the column has the pixel RGB value
	image = cv2.imread(PATH_TO_IMAGE)
	image_expanded = np.expand_dims(image, axis=0)

	# Perform the actual detection by running the model with the image as input.
	(boxes, scores, classes, num) = sess.run(
	    [detection_boxes, detection_scores, detection_classes, num_detections],
	    feed_dict={image_tensor: image_expanded})

	# Draw the results of the detection (aka 'visulaize the results')

	boxes = np.squeeze(boxes)
	classes = np.squeeze(classes).astype(np.int32)
	scores = np.squeeze(scores)
	count = 0
	rsBoxes = []
	rsScore = []
	for i in range(len(boxes)):
	# Class 1 represents human
		if classes[i] == 1 and scores[i] > THRESHOLD:
			box = boxes[i]
			rsBoxes.append(boxes[i].tolist())
			rsScore.append(scores[i])
			count += 1
			cv2.rectangle(image,(int(box[1]*image.shape[1]),int(box[0]*image.shape[0])),(int(box[3]*image.shape[1]),int(box[2]*image.shape[0])),(255,0,0),2)
			cv2.putText(image,str(int(scores[i]*100)),(int(box[1]*image.shape[1])-3,int(box[0]*image.shape[0])-3),cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,0,0),1,cv2.LINE_AA)
		else:
			break
	# print(rsBoxes)
	print(rsScore)
	# print(classes)
	# All the results have been drawn on image. Now display the image.
	# image = cv2.resize(image,(1366,768))
	# cv2.imshow('Object detector', image)
	cv2.imwrite('Result.jpg', image)
	# Press any key to close the image
	# cv2.waitKey(0)
	
	return rsBoxes,rsScore
	# # Clean up
	# cv2.destroyAllWindows()
# detect('test3.jpg')