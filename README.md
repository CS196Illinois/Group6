# Group6
Welcome to LCTRS! This our CS196@Illinois group project. We decided to create a tool to summarize lecture transcripts to assist students in online learning. Below, you can find instructions to use our project and get some insight into what we did.

## How to Run
To run our project, you will need to install our finetuned language model. Sadly, it is too large to store on GitHub, so you will need to follow the instructions below to install the model.

 1. Clone this repository.
 2. Download the language model. You must download the entire folder [from Google Drive](https://drive.google.com/drive/folders/1TTnF539398dDx8kxmE_14ZbcbGPnsmN2?usp=sharing). ***Note: you must have an Illinois email account to access it.***
3. Store the model under the path <path_to_project_folder>/Group6/app/t5-small-finetuned/ 
4. Navigate to this project folder.
5. Run the following command in your terminal/command prompt:
	* Unix/MacOS: `python3 -m pip install -r requirements.txt`
	* Windows: `py -m pip install -r requirements.txt`
6. Run the following command in your terminal/command prompt: `python3 app/app.py`.
7. Open a browser and go to your localhost site: `127.0.0.1`
8. Congrats! You can summarize your lectures!

## Limitations
Unfortunately we ran out of time to implement the conversion of video files to audio files and audio files to text. You will have to find a transcript of your lectures yourself. If your lectures are hosted on YouTube, you may be able to leverage  YouTube captions functionality. 

Feel free to play around with the `SpeechToText.py` file as well. 

You will also need to limit the size of the chunks of text you wish to summarize. Our language model is only able to handle up to 1024 words at a time at the moment. You can summarize one section of each lecture at a time to overcome this. You will have logical progressions of summaries as a result!

***NOTE: You will not be able to use the Google login functionality unless you contact us for the correct client keys.***
