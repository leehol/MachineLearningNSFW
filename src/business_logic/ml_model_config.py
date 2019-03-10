import os

__MODEL_DIR = "/home/ubuntu/nsfw_video_detection/src/business_logic/open_nsfw/nsfw_model/"
PROTO_TXT_PATH = __MODEL_DIR + "deploy.prototxt"
TRAINED_MODEL_PATH = __MODEL_DIR + "resnet_50_1by2_nsfw.caffemodel"
OUTPUT_LAYERS = ['prob']
IMG_WRITE_DIR = "check_image"
