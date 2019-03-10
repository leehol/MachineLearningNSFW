from business_logic.nsfw_detection import is_nsfw



def test_is_nsfw():
    is_nsfw({"video_link": "http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"})
    is_nsfw({"video_link": "./test_images/240P_400K_199372161.mp4"})

test_is_nsfw()
