# https://gist.github.com/MarcScott/2116aae340afef8bdccdd035d4e20c8b
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from PIL import Image as PilImage
from picamera import PiCamera
from time import sleep
from gpiozero import Button, LED
from twython import Twython

from auth import (
	consumer_key,
	consumer_secret,
	access_token,
	access_token_secret
	)

# add your clarifai keys here
CLARIFAI_APP_ID = " *****CHANGE ME***** "
CLARIFAI_APP_SECRET = " *****CHANGE ME***** "
ledR = LED(23)
ledG = LED(24)
camera = PiCamera()
button = Button(17)
twitter = Twython(
	consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
        )
ledG.on()

while True:
    
    print("Press the button to take your picture.")
    # wait for button press to take picture
    button.wait_for_press()
    ledG.off()
    ledR.on()

    # make image to file
    camera.start_preview(alpha=192)
    camera.annotate_text='3'
    sleep(1)
    camera.annotate_text='2'
    sleep(1)
    camera.annotate_text='1'
    sleep(1)
    camera.annotate_text=' '
    sleep(1)
    camera.capture("/home/pi/capture.jpg")
    camera.stop_preview()

    ##Grab the image from file
    the_image = '/home/pi/capture.jpg'

    # connect to Clarifai
    app = ClarifaiApp(CLARIFAI_APP_ID, CLARIFAI_APP_SECRET)

    #face recognition model
    model = app.models.get('a403429f2ddf4b49b307e318f00e528b')
    image = ClImage(filename=the_image)

    data = model.predict([image])
    ledG.on()
    ledR.off()


    #tweet if there is a face in the picture.
    try:
        box = data['outputs'][0]['data']['regions'][0]['region_info']['bounding_box']
    except IndexError:
        print("No face seen")
    else:
        print ("Face seen")
        message = "Hello world! #picademy"
        print("Tweeted: %s" % message)
        with open('/home/pi/capture.jpg', 'rb') as photo:
            twitter.update_status_with_media(status=message, media=photo)
