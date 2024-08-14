from data.neuro.balka_text_recognize_yolo import Balka_Text_Recognize_yolo
from data.neuro.local_models import *
from data.neuro.models import RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS, RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2
from data.neuro.text_recognize_yolo import Text_Recognize_yolo
from data.result import Rama_prod
from data.result.Class_text import Class_text
from data.result.Rect import Rect
from data.result.balka_prod import Balka_Prod
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

class Danila_balka_text_recognize_redone:
    def __init__(self, local,  yolov5_dir, balka_text_recognize_version):
        if local:
            if balka_text_recognize_version == 3:
                self.prod_coefficients = {
                    Balka_Prod.altai: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                 Text_coefficients(4, 64, 128),
                                                                 Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                     Text_coefficients(4, 64, 64),
                                                                     Text_coefficients(2, 64, 96)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                   Text_coefficients(4, 64, 64),
                                                                   Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                      Text_coefficients(4, 64, 96),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                  Text_coefficients(4, 64, 128),
                                                                  Text_coefficients(2, 64, 64))
                }
                print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
                self.text_recognize_model = Balka_Text_Recognize_yolo(local, LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS, yolov5_dir)
            elif balka_text_recognize_version == 4:
                self.prod_coefficients = {
                    Balka_Prod.altai: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                 Text_coefficients(4, 64, 128),
                                                                 Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                     Text_coefficients(4, 64, 64),
                                                                     Text_coefficients(2, 64, 96)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                   Text_coefficients(4, 64, 64),
                                                                   Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                      Text_coefficients(4, 64, 96),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                  Text_coefficients(4, 64, 128),
                                                                  Text_coefficients(2, 64, 64))
                }
                print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
                self.text_recognize_model = Balka_Text_Recognize_yolo(local, LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir)
            elif balka_text_recognize_version == 6:
                self.prod_coefficients = {
                    Balka_Prod.altai: Prod_coefficients(Text_coefficients(5, 128, 128),
                                                                 Text_coefficients(4, 128, 128),
                                                                 Text_coefficients(2, 32, 32)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(5, 160, 160),
                                                                     Text_coefficients(2, 64, 64),
                                                                     Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                   Text_coefficients(2, 128, 128),
                                                                   Text_coefficients(2, 32, 32)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 128, 128),
                                                                      Text_coefficients(4, 96, 96),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                  Text_coefficients(4, 96, 96),
                                                                  Text_coefficients(2, 64, 64))
                }
                print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
                self.text_recognize_model = Balka_Text_Recognize_yolo(local, LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir)
        else:
            if balka_text_recognize_version == 3:
                self.prod_coefficients = {
                    Balka_Prod.altai: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                 Text_coefficients(4, 64, 128),
                                                                 Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                     Text_coefficients(4, 64, 64),
                                                                     Text_coefficients(2, 64, 96)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                   Text_coefficients(4, 64, 64),
                                                                   Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                      Text_coefficients(4, 64, 96),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                  Text_coefficients(4, 64, 128),
                                                                  Text_coefficients(2, 64, 64))
                }
                print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
                self.text_recognize_model = Balka_Text_Recognize_yolo(local, RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS, yolov5_dir)
            elif balka_text_recognize_version == 4:
                self.prod_coefficients = {
                    Balka_Prod.altai: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                 Text_coefficients(4, 64, 128),
                                                                 Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                     Text_coefficients(4, 64, 64),
                                                                     Text_coefficients(2, 64, 96)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                   Text_coefficients(4, 64, 64),
                                                                   Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                      Text_coefficients(4, 64, 96),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                  Text_coefficients(4, 64, 128),
                                                                  Text_coefficients(2, 64, 64))
                }
                print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
                self.text_recognize_model = Balka_Text_Recognize_yolo(local, RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir)
            elif balka_text_recognize_version == 6:
                self.prod_coefficients = {
                    Balka_Prod.altai: Prod_coefficients(Text_coefficients(5, 128, 128),
                                                                 Text_coefficients(4, 128, 128),
                                                                 Text_coefficients(2, 32, 32)),
                    Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(5, 160, 160),
                                                                     Text_coefficients(2, 64, 64),
                                                                     Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                   Text_coefficients(2, 128, 128),
                                                                   Text_coefficients(2, 32, 32)),
                    Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 128, 128),
                                                                      Text_coefficients(4, 96, 96),
                                                                      Text_coefficients(2, 64, 64)),
                    Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 96, 96),
                                                                  Text_coefficients(4, 96, 96),
                                                                  Text_coefficients(2, 64, 64))
                }
                print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
                self.text_recognize_model = Balka_Text_Recognize_yolo(local, LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir)


    def balka_text_recognize(self, _balka_prod, img_cuts, image_text_areas_2_balkas):
        label_area = self.text_recognize_model.work_image_cut(
            _balka_prod=_balka_prod, image_text_areas_2_half_balkas=image_text_areas_2_balkas, image_balka_cuts=img_cuts
        )
        res_labels = {}
        (number_text, number_conf) = label_area.labels[Class_text.number]
        res_labels['number'] = (number_text, number_conf)
        (year_text, year_conf) = label_area.labels[Class_text.year]
        if (len(year_text) == 2) and (int(year_text) < 25):
            res_labels['year'] = (year_text, year_conf)
        else:
            res_labels['year'] = ('24', 0.25)
        (prod_text, prod_conf) = label_area.labels[Class_text.prod]
        res_labels['prod'] = (prod_text, prod_conf)
        return res_labels


