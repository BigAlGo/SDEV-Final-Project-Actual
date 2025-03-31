import cv2
import time
import mss
import numpy as np
import threading
# Todo when flased it breakes
# todo when switching people it breaks
class OpenCVVision():
    def __init__(self, screenWidth, screenHeight, func):
        # Takes in the screen size and a function to be called on round start
        self.startMusic = func
        self.lastBoxes = []
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.captureRegion = {"top" : int(11.5/100 * screenHeight), "left" : int(27.0/64.0 * screenWidth), "width" : int(10.0/64.0 * screenWidth), "height" : int(3.0/20.0 * screenHeight)}
        # Stores the x, y, w, h for each letter in the win/loss word
        # Look for one of these then switch to unlimited fps 
        self.wonArrays = [[9.37, 3.53, 1.83, 6.38], [7.25, 3.39, 1.90, 6.64], [4.32, 3.39, 2.78, 6.51]]
        self.lossArrays = [[9.74, 3.39, 1.61, 6.51], [7.83, 3.39, 1.68, 6.51], [5.71, 3.39, 1.83, 6.51], [4.32, 3.39, 1.17, 6.51]]
        self.clutchArrays = [[11.46, 5.09, 1.93, 6.67], [7.71, 5.09, 1.67, 6.67], [5.68, 5.09, 1.93, 6.67], [4.22, 5.09, 1.30, 6.57], [9.43, 5.00, 1.88, 6.85], [2.24, 4.91, 1.82, 6.76]]
        self.teaAceArray = [[12.40, 5.74, 1.04, 5.09], [10.73, 5.74, 1.46, 5.09], [9.11, 5.74, 1.51, 5.09], [4.69, 5.74, 1.46, 5.09], [3.44, 5.65, 1.04, 5.19], [2.03, 5.65, 1.25, 5.19]]
        self.ace = [[9.11, 5.19, 1.35, 6.48], [5.05, 5.19, 1.82, 6.39], [7.08, 5.09, 1.77, 6.57]]
        self.flawless = [[10.68, 5.74, 1.41, 5.09], [12.29, 5.65, 1.35, 5.19], [9.38, 5.65, 1.15, 5.19], [8.23, 5.65, 1.04, 5.19], [5.89, 5.65, 2.24, 5.19], [4.27, 5.65, 1.51, 5.28], [3.18, 5.65, 0.99, 5.19], [1.93, 5.65, 1.04, 5.19]]
        self.thrifty = [[12.03, 5.00, 1.82, 6.48], [10.31, 5.00, 1.61, 6.48], [8.85, 5.00, 1.30, 6.48], [7.86, 5.00, 0.73, 6.48], [5.83, 5.00, 1.77, 6.48], [3.75, 5.00, 1.82, 6.48], [2.03, 5.00, 1.51, 6.48]]
        # But if you see the buy phase, instantly play music
        self.buyPhase = [[7.03, 11.85, 1.30, 2.31], [1.35, 4.54, 1.46, 5.19], [13.12, 4.44, 1.15, 5.28], [11.56, 4.44, 1.41, 5.28], [9.95, 4.44, 1.51, 5.28], [8.28, 4.44, 1.51, 5.28], [6.72, 4.44, 1.41, 5.28], [2.97, 4.44, 1.46, 5.28]]

        self.lastRoundEnd = False
        self.roundEndTime = 0

        self.running = False

    def startLoop(self):
        '''Starts looking already in a separate thread.'''
        self.running = True

    def stopLoop(self):
        '''Stops looking'''
        self.running = False

    def detectRoundType(self, x_pe, y_pe, w_pe, h_pe):
            '''Checks each banner type separately in its own loop.'''

            # Won
            for ref in self.wonArrays:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Won"

            # Loss
            for ref in self.lossArrays:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Loss"

            # Flawless
            for ref in self.flawless:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Flawless"

            # Clutch
            for ref in self.clutchArrays:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Clutch"

            # Ace
            for ref in self.ace:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Ace"

            # Team Ace
            for ref in self.teaAceArray:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Team Ace"

            # Thrifty
            for ref in self.thrifty:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Thrifty"
                
            # Buy Phase
            for ref in self.buyPhase:
                if self.isMatch(x_pe, y_pe, w_pe, h_pe, ref):
                    return "Buy Phase"

            return None
    
    def isMatch(self, x_pe, y_pe, w_pe, h_pe, ref):
        '''Helper function to check if a bounding box is close enough to a reference.'''
        distance, sizeDiff = self.distance([x_pe, y_pe, w_pe, h_pe], ref)
        return distance < 0.25 and sizeDiff < 0.25
    
    def distance(self, arr1, arr2):
        '''Takes in 2, arrays formatted in x, y, width, height and returns the distance and size difference between the two'''
        distance = np.sqrt((arr1[0] - arr2[0]) ** 2 + (arr1[1] - arr2[1]) ** 2)
        sizeDiff = abs(arr1[2] - arr2[2]) + abs(arr1[3] - arr2[3])
        return distance, sizeDiff
    
    def mainLoop(self):
        '''Takes in the startMusic function as the function to be called when the banner dissapears, calls that function when the next round starts, and then returns'''
        with mss.mss() as sct:
            while self.running:
                roundEnd = False
                screenshot = sct.grab(self.captureRegion) # Takes Screenshot
                img = np.array(screenshot) # Convert to a usable format 
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to HSV
                threshold = cv2.inRange(imgRGB, (234, 232, 237), (255, 255, 255)) # Threshold out evrything exept white
                edges = cv2.Canny(threshold, threshold1 = 50, threshold2 = 150) # Finds edges
                boxes, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finds boxes

                currentBoxes = []

                # Filters out small coutours and converts to percentage
                for contour in boxes:
                    if cv2.contourArea(contour) > 100:
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

                    # If the box was found last frame
                    if sameBox:
                        # Percentage
                        x_pe, y_pe, w_pe, h_pe = x * 100, y * 100, w * 100, h * 100

                        # Finds if the box is part of the banner
                        roundType = self.detectRoundType(x_pe, y_pe, w_pe, h_pe)
                        if roundType == "Buy Phase":
                            # PANIC This shouldnt happen as the program should already have returned
                            self.startMusic()
                            print("PANIC")
                            cv2.imwrite('buyroundEnd.png', img)
                            return
                        elif roundType:
                            print("roundEnd = True: " + str(roundType))
                            print(f"[{x_pe:.2f}", f"{y_pe:.2f}", f"{w_pe:.2f}", f"{h_pe:.2f}]", sep = ", ")
                            cv2.imwrite('roundEnd.png', img)

                            roundEnd = True
                            

                # Once the banner has disappeared
                if not roundEnd and self.lastRoundEnd:
                    self.roundEndTime = time.time()
                    print("No Mo Banner")
                
                # Once 1 second after the banner has disappeared
                if not roundEnd and time.time() > self.roundEndTime + 1 and time.time() < self.roundEndTime + 2:
                    self.startMusic()
                    cv2.imwrite('roundEnd.png', img)
                    self.roundEndTime = 0
                    self.running = False
                    self.stopLoop()
                    return

                # If the banner is not up, shoot at 1 fps
                if not roundEnd and not (time.time() > self.roundEndTime + 1 and time.time() < self.roundEndTime + 2):
                    time.sleep(1)
                    print("1 fps")

                # Sets variables for next loop
                self.lastRoundEnd = roundEnd
                self.lastBoxes = currentBoxes


    def debug(self):
        '''Takes in the startMusic function as the function to be called when the banner dissapears and prints some stuff'''
        with mss.mss() as sct:
            key = cv2.waitKey(30)
            while not (key == ord('q') or key == 27):
                roundEnd = False
                print("frame")
                screenshot = sct.grab(self.captureRegion) # Takes Screenshot
                img = np.array(screenshot) # Convert to a usable format 
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to HSV
                threshold = cv2.inRange(imgRGB, (234, 232, 237), (255, 255, 255)) # Threshold out evrything exept white
                edges = cv2.Canny(threshold, threshold1=50, threshold2=150) # Finds edges
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
                        # Percentage
                        x_pe, y_pe, w_pe, h_pe = x * 100, y * 100, w * 100, h * 100
                        print(f"[{x_pe:.2f}, " + f"{y_pe:.2f}", f"{w_pe:.2f}", f"{h_pe:.2f}]", sep = ", ")

                        x_px, y_px, w_px, h_px = int(x * self.screenWidth), int(y * self.screenHeight), int(w * self.screenWidth), int(h * self.screenHeight)
                        cv2.rectangle(img, (x_px, y_px), (x_px + w_px, y_px + h_px), (0, 255, 0), 2)



                        # Finds if the box is part of the banner
                        roundType = self.detectRoundType(x_pe, y_pe, w_pe, h_pe)
                        
                        if roundType == "Buy Phase":
                            # PANIC This shouldnt happen as the program should already have returned
                            self.startMusic()
                            print("PANIC")
                        elif roundType:
                            # Makes sure roundtype isnt null
                            print("roundEnd = True:" + str(roundType))
                            print("I Saw: " + f"[{x_pe:.2f}, " + f"{y_pe:.2f}", f"{w_pe:.2f}", f"{h_pe:.2f}]", sep = ", ")

                            roundEnd = True

                if not (roundEnd) and self.lastRoundEnd:
                    self.roundEndTime = time.time()
                
                if not (roundEnd) and time.time() > self.roundEndTime + 1 and time.time() < self.roundEndTime + 2:
                    self.startMusic(False)
                    self.lastRoundEnd = False
                    cv2.imwrite('roundEnd.png', img)
                    self.roundEndTime = 0


                self.lastRoundEnd = roundEnd
                self.lastBoxes = currentBoxes 

                cv2.imshow('img', img)
                cv2.imshow('threshgold', edges)
                key = cv2.waitKey(30)


def DoOrDie():
    print("HE DID")

if __name__ == "__main__":
    opencv = OpenCVVision(1920, 1080, DoOrDie)
    opencv.debug()