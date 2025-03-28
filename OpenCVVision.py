import cv2
import time
import mss
import numpy as np

class OpenCVVision():
    def __init__(self, screenWidth, screenHeight):
        self.lastBoxes = []
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.captureRegion = {"top" : int(11.5/100 * screenHeight), "left" : int(27.0/64.0 * screenWidth), "width" : int(10.0/64.0 * screenWidth), "height" : int(3.0/20.0 * screenHeight)}
        # Stores the x, y, w, h for each letter in the win/loss word
        self.wonArrays = [[9.37, 3.53, 1.83, 6.38], [7.25, 3.39, 1.90, 6.64], [4.32, 3.39, 2.78, 6.51]]
        self.lossArrays = [[9.74, 3.39, 1.61, 6.51], [7.83, 3.39, 1.68, 6.51], [5.71, 3.39, 1.83, 6.51], [4.32, 3.39, 1.17, 6.51]]
        self.lastWonLoss = False
        self.lastWon = False
        self.wonLossTime = 0

    def distance(self, arr1, arr2):
        '''Takes in 2, arrays formatted in x, y, width, height and returns the distance and size difference between the two'''
        distance = np.sqrt((arr1[0] - arr2[0]) ** 2 + (arr1[1] - arr2[1]) ** 2)
        sizeDiff = abs(arr1[2] - arr2[2]) + abs(arr1[3] - arr2[3])
        return distance, sizeDiff
    

    def mainLoop(self, startMusic):
        '''Takes in the startMusic function as the function to be called when the banner dissapears'''
        with mss.mss() as sct:
            key = cv2.waitKey(30)
            while not (key == ord('q') or key == 27):
                loss = False
                won = False
                print("frame")
                screenshot = sct.grab(self.captureRegion) # Takes Screenshot
                img = np.array(screenshot) # Convert to a usable format 
                imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Convert to HSV
                threshold = cv2.inRange(imgHSV, (0, 0, 228), (180, 36, 255)) # Threshold out evrything exept white
                blurred = cv2.GaussianBlur(threshold, (5, 5), 0)  # Reduce noise
                edges = cv2.Canny(blurred, threshold1=50, threshold2=150) # Finds edges
                boxes, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finds boxes

                currentBoxes = []

                for contour in boxes:
                    if cv2.contourArea(contour) > 100:  # Filter small contours
                        x, y, w, h = cv2.boundingRect(contour)

                        # Convert to percentage of screen size
                        x_pe = x / self.screenWidth
                        y_pe = y / self.screenHeight
                        w_pe = w / self.screenWidth
                        h_pe = h / self.screenHeight

                        currentBoxes.append((x_pe, y_pe, w_pe, h_pe))

                # Compare current boxes with previous boxes
                for (x, y, w, h) in currentBoxes:
                    sameBox = False
                    for (px, py, pw, ph) in self.lastBoxes:
                        # Calculate distance and size difference
                        distance, sizeDiff = self.distance([x, y, w, h], [px, py, pw, ph])

                        if distance < 0.02 and sizeDiff < 0.02: 
                            sameBox = True
                            break

                    if sameBox:
                        # Pixels
                        x_px, y_px, w_px, h_px = int(x * self.screenWidth), int(y * self.screenHeight), int(w * self.screenWidth), int(h * self.screenHeight)
                        # Percentage
                        x_pe, y_pe, w_pe, h_pe = x * 100, y * 100, w * 100, h * 100

                        for wonArr in self.wonArrays:
                            distance, sizeDiff = self.distance([x_pe, y_pe, w_pe, h_pe], wonArr)
                            if distance < 0.5 and sizeDiff < 0.5:
                                won = True
                                cv2.rectangle(img, (x_px, y_px), (x_px + w_px, y_px + h_px), (0, 255, 0), 2)  
                                print(x_px, y_px, w_px, h_px, sep = " ")                              
                                break
                        if won:
                            break
                        # Checking if the array is close to any of the loss arrays
                        for lossArr in self.lossArrays:
                            distance, sizeDiff = self.distance([x_pe, y_pe, w_pe, h_pe], lossArr)
                            if distance < 0.5 and sizeDiff < 0.5:
                                loss = True
                                cv2.rectangle(img, (x_px, y_px), (x_px + w_px, y_px + h_px), (0, 255, 0), 2)
                                print(x_px, y_px, w_px, h_px, sep = " ")
                                break
                        if loss:
                            break

                if not (won or loss) and self.lastWonLoss:
                    self.wonLossTime = time.time()
                
                if not (won or loss) and time.time() > self.wonLossTime + 1 and time.time() < self.wonLossTime + 2:
                    startMusic(self.lastWon)
                    self.lastWonLoss = False
                    cv2.imwrite('roundEnd.png', img)
                    self.wonLossTime = 0


                self.lastWonLoss = won or loss
                self.lastWon = won
                self.lastBoxes = currentBoxes 

                cv2.imshow('img', img)
                cv2.imshow('threshgold', edges)
                key = cv2.waitKey(30)


def DoOrDie(hasWon):
    if hasWon:
        print("HE DID")
    else:
        print("He ded")

opencv = OpenCVVision(1366, 768)
opencv.mainLoop(DoOrDie)