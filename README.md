# ReMarkable Highlight Extractor

The ReMarkable is an E-Ink tablet that can be used for reading and note-taking. More about it can be found here: https://remarkable.com/

One of my main uses of the tablet is to load a PDF and use the snap-to-text highlighting feature. However, (as of now) there is no mainstream process to extract the text that has been highlighted. There have, however, been many GitHub repositories dedicated to extracting highlighted text by parsing the underlying files. 
Most of these methods worked flawlessly for older versions, but the most recent versions have changed the how the ReMarkable stores annotation information, rendering all previous methods useless.

This project aims to solve this problem for good.

In order to use this extractor, you must have two copies of the PDF in the same directory as this cloned repository:
- The original PDF
- The highlighted PDF

The highlighted PDF can be exported through two methods (that I know of):
1. Using the ReMarkable application, right click on the PDF and choose "Export" with the file format as PDF. However, PDFs will stop syncing through ReMarkable Connect after a certain amount of time, so this method may not be entirely feasible.
2. Using the reMarkable Connection Utilty (RCU) (can be bought for $12 at http://www.davisr.me/projects/rcu/), left click the PDF and press the "Export PDF" drop-down arrow at the bottom of the application. When the options pop up, make sure to check the "Annotated PDF" box and select "Export PDF (Web UI)". If this button is grayed out, make sure your tablet is directly connected with the cable and that the "USB web interface" slider is enabled (can be found at Menu -> Settings -> Storage on the tablet).

The extraction works by converting each page within the specified range into an image and then comparing the two images. If the page has highlights, the hightlighted text should be the only thing remaining after the comparison. At this point, the extractor attempts to read the text and enter it into a .txt file. This process is slow, but should be guaranteed to work regardless of ReMarkable version. (Do not be surprised if the text is not perfectly extracted, there are a lot of ways it can get it wrong)

Once both PDFs have been placed in the home directory, run the python code from the terminal and let the magic happen.
