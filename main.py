import pytesseract as fourD, cv2 as cv, PySimpleGUI as gui

def newFile(plate, percentMatch):
    toWrite = "1. " + plate + " - " + str(percentMatch) + "% Match"
    with open("licensePlates.txt", "w") as w:
        w.write(toWrite)

def existingFile(plate, percentMatch, filepath):

    with open(filepath, "r+") as f:
        fContents = f.readlines()
        toWrite = str(len(fContents) + 1) + ". " + plate + " - " + str(percentMatch) + "% Match"
        fContents.append(toWrite)
        f.seek(0)
        f.truncate()
        for line in fContents:
            f.write(str.rstrip(line))
            f.write("\n")

# source = input("Enter path to file you would like to read. ")
gui.theme('DarkAmber')

layout =[
    [gui.Text("Please select the file from which you would like to read a license plate:")],
    [gui.Input("Paste path here or browse", key="-IN-"), gui.FileBrowse(file_types=(("JPG Image Files", "*.jpg"), ("PNG Image Files", "*.png")))],
    [gui.Button("Submit")]
]

window = gui.Window("bueno!", layout, size=(500, 100), element_justification='c')

window.read()

while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        source = values["-IN-"]
        window.close()
        break  

# source = str(Values["pathInput"])

# Open image
bueno = cv.imread(source)

# Grayscale and denoise image to make life easier for tesseract 
buenoGrayscale = cv.cvtColor(bueno, cv.COLOR_BGR2GRAY)
buenoDenoise = cv.GaussianBlur(buenoGrayscale,(5,5),5)

# Open the denoised grayscale image for the user to see
cv.imshow('gaming', buenoDenoise)
cv.waitKey(0)

# Tesseract Magic
string = fourD.image_to_string(buenoDenoise)

# Tesseract is too good it seems...
# Sometimes Tesseract picks up a |, a (, or a )
# The code below removes these
plate = ""
for char in string:
    if str.isalnum(char) == True:
        plate += str(char)
    else:
        pass

platelist = ["ERA87TL", "B2823PR", "IBS7470", "BX5438", "IAB12DL9"]
sameChar = 0
samePos = 0
most = []
mostChar = 0
mostCount = 0


for item in platelist:
    for char in item:
        # print(char)
        if char in plate:
            sameChar += 1   
        else:
            pass
        
        if item.find(char) == plate.find(char):
            samePos += 1
        else:
            pass

        if samePos > mostCount:
            most = []
            most.append(platelist.index(item))
            mostCount = samePos
            mostChar = sameChar
        elif samePos == mostCount:
            most.append(platelist.index(item))

        else:
            pass
    # print(sameChar, samePos)
    # print("gaming")
    # print(most, mostCount, mostChar)
    samePos = 0
    sameChar = 0

if mostCount != 0 and mostCount != 7:
    percentMatch = mostCount / 7 * 100
    
    # print(percentMatch)
elif mostCount == 7:
    percentMatch = 100
else:
    percentMatch = 0

if mostChar - mostCount <= 0:
    pass
else:
    gaming = (mostChar-mostCount) / 7 / 4 * 100
    # print(gaming)
    percentMatch += gaming

buenoo = str("License plate detected in image: " + plate)

percentMatch = float("{:.2f}".format(percentMatch))
if percentMatch == 0:
    buenoo2 = "No match to license plates in database found."
else:
    buenoo2 = str(percentMatch) + "% match found to authorized license plate: " + platelist[most[0]]

layout2 = [
    [gui.Text(buenoo)],
    [gui.Text(buenoo2)],
    [gui.Button("Continue")]
]    

window2 = gui.Window("bueno!", layout2, element_justification="c")
window2.read()

while True:
    event, values = window.Read()
    if event == gui.WIN_CLOSED or event=="Exit":
        break
    elif event == "Continue":
        window.close()
        break

layout3 = [
    [gui.Text("Would you like to save to an existing file or a new file?")],
    [gui.Button("New"), gui.Button("Existing")],
    [gui.Button("Close and Delete")]
]

window3 = gui.Window("bueno!", layout3, element_justification="c")
window3.read()

while True:
    event, values = window3.read()
    if event == gui.WIN_CLOSED or event=="Exit":
        break
    elif event == "New":
        # window.close()
        newFile(plate, percentMatch)
        print("Gaming")
        window.close()
        break  
    elif event == "Existing":
        layout4 =[
            [gui.Text("Please select the file that you would like to save the license plate to:")],
            [gui.Input("Paste path here or browse", key="-IN-"), gui.FileBrowse(file_types=(("JPG Image Files", "*.jpg"), ("PNG Image Files", "*.png")))],
            [gui.Button("Submit")]
        ]
        window4 = gui.Window("bueno!", layout4, size=(500, 100), element_justification='c')
        # existingFile(plate, percentMatch, savePath)
        while True:
            event, values = window4.read()
            if event == gui.WIN_CLOSED or event=="Exit":
                break
            elif event == "Submit":
                savePath = values["-IN-"]
                existingFile(plate, percentMatch, savePath)
                window.close()
                break
        # print("Gaming!")
        break
        # window.close()
        # layout4 = []
    elif event == "Close and Delete":
        window.close()
        break
