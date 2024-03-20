# ReMarkable Highlight Extractor

The ReMarkable is an E-Ink tablet that can be used for reading and note-taking. More about it can be found here: https://remarkable.com/

One of my main uses of the tablet is to load a PDF and use the snap-to-text highlighting feature. However, (as of now) there is no mainstream process to extract the text that has been highlighted. There have, however, been many GitHub repositories dedicated to extracting highlighted text by parsing the underlying files. 
Most of these methods worked flawlessly for older versions, but the most recent versions have changed the how the ReMarkable stores annotation information, rendering all previous methods useless.

This project aims to solve this problem for good.

In order to use this extractor, all you need is a copy of the highlighted PDF from your ReMarkable tablet.

The highlighted PDF can be exported through two methods (that I know of):
1. Using the ReMarkable application, right click on the PDF and choose "Export" with the file format as PDF. Keep in mind that if you don't have a ReMarkable Connect subscription and you haven't opened/synced the PDF in 50 days it will stop syncing entirely. If this happens you can probably just export the file and re-upload it.
2. Using the reMarkable Connection Utility (RCU) (can be bought for $12 at http://www.davisr.me/projects/rcu/), left click the PDF and press the "Export PDF" drop-down arrow at the bottom of the application. When the options pop up, make sure to check the "Annotated PDF" box and select "Export PDF (Web UI)". If this button is grayed out, make sure your tablet is directly connected with the cable and that the "USB web interface" slider is enabled (can be found at Menu -> Settings -> Storage on the tablet).

The extraction works by converting each page within the specified range into an image and then searching for regions that have ReMarkable highlight colors (as of now, **only pink is supported**). Each different section of highlights are enclosed in a box and cropped into a separate image. Once they're separated, the text can be easily read and exported to a file as plaintext, although you can specify any file extension you want (.md, etc.). This process is somewhat slow, but should be guaranteed to work regardless of ReMarkable version. Do not be surprised if the text is not perfectly extracted; some PDFs might have lines close enough to cause their highlights to overlap and cause unintended consequences.

You can let the program run in the background and choose to trust the output, or only let it run page by page and observe/fix any formatting while it runs. One you're content, you can hit "Enter" and it will show the next page. I personally like to use this method with Obsidian so I can alternate between extracting highlights and then formatting the text at the same time.

Once the PDF has been placed in the home directory, run the python code from the terminal and let the magic happen.
