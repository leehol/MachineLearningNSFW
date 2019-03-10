import os
import caffe
import cv2
import numpy as np
import logging
from response_class import MLResponse
from common.response_utils import make_success_response, make_error_response
from ml_model_config import PROTO_TXT_PATH
from ml_model_config import TRAINED_MODEL_PATH
from ml_model_config import OUTPUT_LAYERS
from ml_model_config import IMG_WRITE_DIR
from open_nsfw.classify_nsfw import caffe_preprocess_and_compute
from common.directory_utils import CURRENT_PATH, make_dir, del_dir

def __cut_video_to_frames(link, dir_name):
    vidcap = cv2.VideoCapture(link)
    success, image = vidcap.read()
    count = 0
    while success:
            if count % 200 == 0:
                cv2.imwrite(dir_name + "/" + "frame_%d.jpg" % count, image)
                print("Frame count is: {count}".format(count=count))

            success, image = vidcap.read()
            count += 1


def __iterate_through_directory(dir_name):
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for f in filenames:
            yield os.path.join(dirpath, f)


def __nsfw_detection(dir_name):
    scores = []
    
    nsfw_net = caffe.Net(PROTO_TXT_PATH, TRAINED_MODEL_PATH, caffe.TEST)
    caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
    caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
    caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
    caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
    caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR
    
    for image_path in __iterate_through_directory(dir_name):
        # Classify
        with open(image_path, 'rb') as f:
            image_data = f.read()
        score = caffe_preprocess_and_compute(image_data, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=['prob'])
        scores.append(score[1])
        print "NSFW score for image is: %s" % (score[1])

    return scores


def __rate_single_video(write_path):
    scores = __nsfw_detection(write_path)
    overall_score = 1
    print scores
    msg = "Content is clean."
    
    for score in scores:
        if score >= 0.8:
            msg = "Content is not suitable for work."
            overall_score = 0
            return MLResponse(msg, overall_score)
        elif score >= 0.4:
            overall_score = -1
            msg = "Content is somewhat graphic. Will be submitted for further review."

    return MLResponse(msg, overall_score)


def is_nsfw(data):
    video_link = data.get("video_link", "")
    if not video_link:
        return make_error_response("No video specified. Please specify a video_link")
    try:
        write_path = CURRENT_PATH + "/" +  IMG_WRITE_DIR
        
        make_dir(write_path)
        __cut_video_to_frames(video_link, write_path)
        content_rating = __rate_single_video(write_path)
        del_dir(write_path)
        print content_rating.code, content_rating.msg
        rating_response = {"content_rating": content_rating.code, "msg": content_rating.msg}
        return make_success_response(rating_response)

    except Exception as e:
        return make_error_response(e)


