from data.neuro.local_models import *
from data.neuro.models import RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS, RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2
from data.neuro.text_recognize_yolo import Text_Recognize_yolo
from data.result import Rama_prod
from data.result.Class_text import Class_text
from data.result.Rect import Rect


class Prod_coefficients:
    def __init__(self, number_coefficients, prod_coefficients, year_coefficients):
        self.number_coefficients = number_coefficients
        self.prod_coefficients = prod_coefficients
        self.year_coefficients = year_coefficients

class Text_coefficients:
    def __init__(self, length, height, width):
        self.length = length
        self.height = height
        self.width = width

class Danila_rama_text_recognize_base:
    def __init__(self, local, yolov5_dir, rama_text_recognize_version):

        print('reading and loading - RAMA_TEXT_RECOGNIZE_MODEL')
        if local:
            if rama_text_recognize_version == 7:
                self.prod_coefficients = {
                    Rama_prod.Rama_Prod.altai: Prod_coefficients(Text_coefficients(5, 160, 160),
                                                                 Text_coefficients(4, 96, 96),
                                                                 Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.balakovo: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                    Text_coefficients(4, 96, 96),
                                                                    Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(6, 224, 224),
                                                                     Text_coefficients(2, 96, 96),
                                                                     Text_coefficients(2, 96, 96)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                   Text_coefficients(2, 96, 96),
                                                                   Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                      Text_coefficients(4, 128, 128),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 160, 160),
                                                                  Text_coefficients(4, 96, 96),
                                                                  Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.uralvagon: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                     Text_coefficients(1, 128, 128),
                                                                     Text_coefficients(2, 96, 96)),
                }
                self.text_recognize_model = Text_Recognize_yolo(local, LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2,
                                                                yolov5_dir)

        else:
            if rama_text_recognize_version == 7:
                self.prod_coefficients = {
                    Rama_prod.Rama_Prod.altai: Prod_coefficients(Text_coefficients(5, 160, 160),
                                                                 Text_coefficients(4, 96, 96),
                                                                 Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.balakovo: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                    Text_coefficients(4, 96, 96),
                                                                    Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(6, 224, 224),
                                                                     Text_coefficients(2, 96, 96),
                                                                     Text_coefficients(2, 96, 96)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                   Text_coefficients(2, 96, 96),
                                                                   Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                      Text_coefficients(4, 128, 128),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 160, 160),
                                                                  Text_coefficients(4, 96, 96),
                                                                  Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.uralvagon: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                     Text_coefficients(1, 128, 128),
                                                                     Text_coefficients(2, 96, 96)),
                }
                self.text_recognize_model = Text_Recognize_yolo(local, LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2,
                                                                yolov5_dir)



    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        label_area = self.text_recognize_model.work_image_cut(
            image_text_areas, img_cut,
            self.prod_coefficients[rama_prod].number_coefficients.length,
            self.prod_coefficients[rama_prod].number_coefficients.height,
            self.prod_coefficients[rama_prod].number_coefficients.width,
            self.prod_coefficients[rama_prod].prod_coefficients.length,
            self.prod_coefficients[rama_prod].prod_coefficients.height,
            self.prod_coefficients[rama_prod].prod_coefficients.width,
            self.prod_coefficients[rama_prod].year_coefficients.length,
            self.prod_coefficients[rama_prod].year_coefficients.height,
            self.prod_coefficients[rama_prod].year_coefficients.width
        )
        res_labels = {}
        (number_text, number_conf) = label_area.labels[Class_text.number]
        res_labels['number'] = (number_text, number_conf)
        (year_text, year_conf) = label_area.labels[Class_text.year]
        if (len(year_text) == 2) and (int(year_text) < 25):
            res_labels['year'] = (year_text, year_conf)
        else:
            res_labels['year'] = ('23', 0.25)
        return res_labels


