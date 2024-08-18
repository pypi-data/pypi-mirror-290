import cv2


def printDer(height=512, width=512):
    black_image = cv2.UMat(height, width, cv2.CV_8UC3)
    cv2.imshow('Der', black_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def convert2Der(amount):
    converted = amount / 200.0
    print(str(converted) + " der")
    return converted
