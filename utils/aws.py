import boto3
import random
import string
from PIL import Image
from io import BytesIO
import os
import copy


class S3Instance:
    aws = None

    class _S3Instance:
        def __init__(self, bucket):
            self.bucketName = bucket
            self.session = boto3.Session(aws_access_key_id=os.getenv(
                "AWS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))
            self.resource = boto3.resource("s3")
            self.bucket = self.resource.Bucket(name=bucket)

    def __init__(self):
        if not S3Instance.aws:
            S3Instance.aws = S3Instance._S3Instance(
                os.getenv("AWS_BUCKET_NAME"))

    def itemExists(self, itemName):
        for item in self.aws.bucket.objects.filter(Prefix="images/"):
            # Quitando el nombre de la carpeta y el formato
            objectName = item.key.split("/")[1:][0].split(".")[:1][0]
            if objectName == itemName:
                return True
        return False

    def randomString(self, size=40):
        # tomando 52 letras [A-Za-z] y 10 numeros [0-1]. Existen 2.276015817 E+28 posibles combinaciones. Muchas
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(size))

    def uploadImage(self, imageObject):
        urlPrefix = f'https://{os.getenv("AWS_BUCKET_NAME")}.s3-us-west-1.amazonaws.com'
        fileExtension = imageObject.filename.split(".")[1:][0]
        awsKey = self.randomString()
        while(self.itemExists(awsKey)):
            awsKey = self.randomString()
        newFileName = f'{awsKey}.{fileExtension}'
        # Image compression stuff
        byteStream = BytesIO(imageObject.stream.read())
        imgBig = Image.open(byteStream)
        width, height = imgBig.size
        if(width > height):
            factor = 200 / width
        else:
            factor = 200 / height

        imgSmall = imgBig.resize(
            (int(width*factor), int(height*factor)), Image.ANTIALIAS)
        print(f'Your image is {imgBig.size[0]}x{imgBig.size[1]}')
        print(f'Your thumbnail is {imgSmall.size[0]}x{imgSmall.size[1]}')

        imgBig.save("_"+newFileName)
        self.aws.bucket.upload_file("_"+newFileName, f'images/{newFileName}')
        os.remove("_"+newFileName)
        print(f'Saved images/{newFileName}')

        imgSmall.save(newFileName)
        self.aws.bucket.upload_file(newFileName, f'thumbnails/{newFileName}')
        os.remove(newFileName)
        print(f'Saved thumbnails/{newFileName}')

        urlImage = f'{urlPrefix}/images/{newFileName}'
        urlThumbnail = f'{urlPrefix}/thumbnails/{newFileName}'
        return [urlImage, urlThumbnail]
