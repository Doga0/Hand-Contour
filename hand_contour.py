import cv2

# resize the image automatically
def resize_(blur, height=None, width=None, inter=cv2.INTER_AREA):
    dimension = None
    h, w = img.shape[:2]

    if height is None and width is None:
        return blur
    if height is None:
        r = width/float(w)
        dimension = (int(h*r), width)
    else:
        r = height / float(h)
        dimension = (int(w*r), height)
    return cv2.resize(blur, dimension, interpolation=inter)


img = cv2.imread("hand.jpg")

# applying filters
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (1, 3))
_, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
cnt = contours[0]

# find the corners
hull = cv2.convexHull(cnt, returnPoints=False)
defects = cv2.convexityDefects(cnt, hull)

for i in range(defects.shape[0]):
    s, e, f, d = defects[i, 0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])

    # to connect the corners
    cv2.line(img, start, end, [200, 0, 0], 2)
    # draw circle to the corners
    cv2.circle(img, far, 3, [0, 0, 0], -1)

img1 = resize_(img, height=450, width=None, inter=cv2.INTER_AREA)

cv2.imshow("img", img1)
cv2.waitKey(0)
cv2.destroyAllWindows()

