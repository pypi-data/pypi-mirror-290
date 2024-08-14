from danila.danila_rama_base import Danila_rama_base
from danila.danila_rama_classify import Danila_rama_classify
from danila.danila_rama_redone import Danila_rama_redone
from danila.danila_rama_text_detect import Danila_rama_text_detect
from danila.danila_rama_text_recognize import Danila_rama_text_recognize
from data.neuro.prods import RAMA_PRODS
from data.result.Rama_prod import Rama_Prod
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_rama:
    def __init__(self, local, yolov5_dir, danila_rama_params):
        if (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version < 3) or (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version == 5):
            self.danila_rama = Danila_rama_base(local, yolov5_dir, danila_rama_params)
        else:
            self.danila_rama = Danila_rama_redone(local, yolov5_dir, danila_rama_params)

    def rama_classify(self,img, detail):
        return self.danila_rama.rama_classify(img, detail)

    def rama_text_detect(self, img):
        return self.danila_rama.rama_text_detect(img)

    def rama_text_recognize(self, img, detail):
        return self.danila_rama.rama_text_recognize(img, detail)