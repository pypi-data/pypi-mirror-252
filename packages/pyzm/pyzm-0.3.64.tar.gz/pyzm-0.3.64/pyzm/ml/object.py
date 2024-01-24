import numpy as np

import sys
import cv2
import time
import datetime
import re
from pyzm.helpers.Base import Base
from pyzm.helpers.Media import MediaStream

import time
import requests
import pyzm.helpers.globals as g

# Class to instantiate a specific object detection implementation

class Object(Base):

    def __init__(self, options={}):

        self.model = None
        self.options = options

        if self.options.get('object_framework') == 'opencv':
            import pyzm.ml.yolo as yolo
            self.model =  yolo.Yolo(options=options)

        elif self.options.get('object_framework') == 'coral_edgetpu':
            import pyzm.ml.coral_edgetpu as tpu
            self.model = tpu.Tpu(options=options)

        elif self.options.get('object_framework') == 'aws_rekognition':
            try:
                import pyzm.ml.aws_rekognition as awsr
                self.model = awsr.AwsRekognition(options=options)
            except ModuleNotFoundError as e:
                g.logger.Error('Module {} not found. Please install with: sudo pip3 install {}'.format(e.name, e.name))
                raise e

        elif self.options.get('object_framework') == 'virelai':
            try:
                import pyzm.ml.virelai as virelai
                self.model = virelai.VirelAI(options=options)
            except ModuleNotFoundError as e:
                g.logger.Error('Module {} not found. Please install with: sudo pip3 install {}'.format(e.name, e.name))
                raise e

        else:
            raise ValueError ('Invalid object_framework:{}'.format(self.options.get('object_framework')))

    def get_options(self):
        return self.options
        
    def get_model(self):
        return self.model

    def get_classes(self):
        return self.model.get_classes()

    def acquire_lock(self):
        self.model.acquire_lock()

    def release_lock(self):
        self.model.release_lock()
 
    def get_detect_image(self, data=None):
        method = getattr(self.model, 'get_detect_image', None)
        if callable(method):
            return self.model.get_detect_image(data['image'])
        else:
            return pyzmutils.draw_bbox(image=data['image'], boxes=data['boxes'],
                                              labels=data['labels'], confidences=data['confidences'],
                                              polygons=data['polygons'], poly_thickness = g.config['poly_thickness'],
                                              write_conf=True if g.config['show_percent'] == 'yes' else False )

    def detect(self,image=None):
        h,w = image.shape[:2]
        b,l,c,_model_names = self.model.detect(image)
        g.logger.Debug(2, 'core model detection over, got {} objects. Now filtering'.format(len(b)))
        # Apply various object filtering rules
        max_object_area = 0
        if self.options.get('max_detection_size'):
                g.logger.Debug(2,'Max object size found to be: {}'.format(self.options.get('max_detection_size')))
                # Let's make sure its the right size
                m = re.match('(\d*\.?\d*)(px|%)?$', self.options.get('max_detection_size'),
                            re.IGNORECASE)
                if m:
                    max_object_area = float(m.group(1))
                    if m.group(2) == '%':
                        max_object_area = float(m.group(1))/100.0*(h * w)
                        g.logger.Debug (2,'Converted {}% to {}'.format(m.group(1), max_object_area))
                else:
                    g.logger.Error('max_object_area misformatted: {} - ignoring'.format(
                        self.options.get('max_object_area')))

        boxes=[]
        labels=[]
        confidences=[]
        model_names = []

        for idx,box in enumerate(b):
            (sX,sY,eX,eY) = box
            if max_object_area:
                object_area = abs((eX-sX)*(eY-sY))
                if (object_area > max_object_area):
                    g.logger.Debug(2, 'Ignoring object:{}, as it\'s area: {}px exceeds max_object_area of {}px'.format(l[idx], object_area, max_object_area))
                    continue
            if c[idx] >= self.options.get('object_min_confidence'):
                boxes.append([sX,sY,eX,eY])
                labels.append(l[idx])
                confidences.append(c[idx])
                model_names.append(_model_names[idx])
            else:
                g.logger.Debug(2, 'Ignoring {} {} as conf. level {} is lower than {}'.format(l[idx],box,c[idx],self.options.get('object_min_confidence')))
       
        g.logger.Debug(2, 'Returning filtered list of {} objects.'.format(len(boxes)))
        return boxes,labels,confidences,model_names
