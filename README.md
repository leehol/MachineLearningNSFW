# Build Instructions
```docker build -t [image_name]:[tag] .```

# Running Instructions
```docker run -it -d [image_id]```  
```docker exec -it [container_id] bash```  
```python rest_service.py```

# Endpoints and Usage
Server is up on port 4321. 
Endpoint is /video_check  
Query string will search for "video_link" in the html body and a URL to an mp4 file after that... example:  
```{"video_link": "sample.mp4"}```

# Return Codes for Content
1  -- clean content  
0  -- nsfw content  
-1 -- ambiguous; manual review is required


