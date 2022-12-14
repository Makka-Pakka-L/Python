import numpy as np
import cv2 as cv
import os
import time
from matplotlib import pyplot as plt

# YOLO文件路径
yolo_dir = './birdnest'  
#权重文件
weightsPath = os.path.join(yolo_dir,
 'yolov3-bdk2_1500.weights')     
configPath = os.path.join(yolo_dir, 'yolov3-bdk.cfg')  
# 配置文件
labelsPath = os.path.join(yolo_dir, 'mydata.names')  
# label名称
imgPath = os.path.join(yolo_dir, 'test1.jpg')  
# 测试图像

CONFIDENCE = 0.5  # 过滤弱检测的最小概率
THRESHOLD = 0.4  # 非最大值抑制阈值

net = cv.dnn.readNetFromDarknet(configPath, weightsPath)  
# 利用下载的文件
print("[INFO] loading YOLO from disk...")  
# 可以打印下信息
img = cv.imread(imgPath)
blobImg = cv.dnn.blobFromImage(img, 1.0/255.0, (416, 416), None, True, False)   
# net需要的输入是blob格式的，用blobFromImage这个函数来转格式
net.setInput(blobImg)  
# 调用setInput函数将图片送入输入层
outInfo = net.getUnconnectedOutLayersNames()
start = time.time()
layerOutputs = net.forward(outInfo)  
end = time.time()
print("[INFO] YOLO took {:.6f} seconds".format(end - start))
(H, W) = img.shape[:2] 
#获取图片shape
boxes = [] 
# 所有边界框
confidences = [] 
# 所有置信度
classIDs = [] 
# 所有分类ID

for out in layerOutputs:  # 各个输出层
    for detection in out:  # 各个框框
        # 拿到置信度
        scores = detection[5:]  # 各个类别的置信度
        classID = np.argmax(scores)  # 最高置信度的id即为分类id
        confidence = scores[classID]  # 拿到置信度

        # 根据置信度筛查
        if confidence > CONFIDENCE:
            box = detection[0:4] * np.array([W, H, W, H])  # 将边界框放会图片尺寸
            (centerX, centerY, width, height) = box.astype("int")
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)
idxs = cv.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD) # boxes中，保留的box的索引index存入idxs
with open(labelsPath, 'rt') as f:
    labels = f.read().rstrip('\n').split('\n')
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")  # 框框显示颜色，每一类有不同的颜色，每种颜色都是由RGB三个值组成的，所以size为(len(labels), 3)
if len(idxs) > 0:
    for i in idxs.flatten():  # indxs是二维的，第0维是输出层，所以这里把它展平成1维
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        color = [int(c) for c in COLORS[classIDs[i]]]
        cv.rectangle(img, (x, y), (x+w, y+h), color, 2)  # 线条粗细为2px
        text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
        cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
         # cv.FONT_HERSHEY_SIMPLEX字体风格、0.5字体大小、粗细2px

img3=img[:,:,::-1]
plt.figure(figsize=(20,20))
plt.imshow(img3)
plt.show()


































