import wx
import Object_detection_image as detect
import cv2


class Example(wx.Frame):
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, size=(960, 500))
		self.Centre()
		self.panel = wx.Panel(self)
		self.listImage = []
		vbox = wx.BoxSizer(wx.VERTICAL) 
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)


		self.btnFile = wx.Button(self.panel, -1, "Choose File")
		self.btnCreate = wx.Button(self.panel, -1, "Detect License Plate")
		self.textChoose = wx.StaticText(self.panel, -1,"Result: ")
		self.textLicense = wx.StaticText(self.panel, -1,"File choosen:")
		self.textCtrlLicense = wx.TextCtrl(self.panel, -1, value="", size=(150,40))
		

		image = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))
		imageBitmap.SetPosition((25,25))


		self.btnFile.Bind(wx.EVT_BUTTON, self.openFile)
		self.btnCreate.Bind(wx.EVT_BUTTON, self.detect)
		
		self.btnFile.SetPosition((115, 200))
		self.btnCreate.SetPosition((215, 200))
		self.btnCreate.Disable()
		self.textChoose.SetPosition((420, 25))
		self.textChoose.Hide()
		self.textLicense.SetPosition((70, 250))
		self.textLicense.Hide()
		self.textCtrlLicense.SetPosition((70, 390))
		self.textCtrlLicense.Hide()

		myFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
		self.textCtrlLicense.SetFont(myFont)


		hbox1.Add(self.btnFile)
		vbox.Add(hbox1)

	def openFile(self, event):
		openFileDialog = wx.FileDialog(self.panel, "Open", wildcard = "Image Files Only (*.jpg,*.png,*.jpeg)|*.jpg;*.png;*.jpeg")
		openFileDialog.ShowModal()
		path = openFileDialog.GetPath()
		self.listImage.append(path)
		self.textLicense.Show()
		
		openFileDialog.Destroy()
		image = wx.Image(path, wx.BITMAP_TYPE_ANY)
		image = image.Scale(300, 150, wx.IMAGE_QUALITY_HIGH)
		imageBitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))
		imageBitmap.SetPosition((70,270))
		self.btnCreate.Enable()

	def detect(self, event):
		boxes, score = detect.detect(self.listImage[0])

		if  len(boxes) != 0:
			image = wx.Image('Result.jpg', wx.BITMAP_TYPE_ANY)
			image = image.Scale(480, 360, wx.IMAGE_QUALITY_HIGH)
			imageBitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))

			# print(boxes)
			# textFile = ''.join(str(int(i*100))+'%' + '\t' for i in boxes)
			# with open('Result.txt','w') as fp:

			li2 = [ y for x in boxes for y in x]
			# for i in range(len(li2)):
			# 	if i%4 == 0:
			# 		temp2 = '\n'.join(map(str,li2))
			# 	else:
			# 		temp2 = '\t'.join(map(str,li2))
			temp2= ''
			for i in boxes:
				t = '\t'.join(str(int(j*100)) for j in i)
				temp2 += t +'\n'
			# print(temp2)
			with open("Result.txt", "w") as f:
				f = open("Result.txt", "w")
				f.write(temp2)
			imageBitmap.SetPosition((440,70))
			temp = ''.join(str(int(i*100))+'%' + '\t' for i in score)
			self.textResultScore = wx.StaticText(self.panel, -1,temp)
			self.textResultScore.SetPosition((500,25))
			self.textResultScore.SetSize((500,20))
			self.textChoose.Show()
		else:
			image = wx.Image('notfound.png', wx.BITMAP_TYPE_ANY)
			image = image.Scale(480, 360, wx.IMAGE_QUALITY_HIGH)
			imageBitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))
			imageBitmap.SetPosition((440,70))
		self.listImage = []

def main():

    app = wx.App()
    ex = Example(None, title = "License Plate Recognition")
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
