from danila.danila_rama_text_recognize_base import Danila_rama_text_recognize_base
from danila.danila_rama_text_recognize_redone import Danila_rama_text_recognize_redone


class Danila_rama_text_recognize:
    def __init__(self, local, yolov5_dir, danila_rama_text_recognize_params):
        self.danila_rama_text_recognize_params = danila_rama_text_recognize_params
        if (self.danila_rama_text_recognize_params.rama_text_recognize_version == 1) | (self.danila_rama_text_recognize_params.rama_text_recognize_version == 2) | (self.danila_rama_text_recognize_params.rama_text_recognize_version == 5):
            self.danila_rama_text_recognize = Danila_rama_text_recognize_base(local, yolov5_dir,
                                                                    self.danila_rama_text_recognize_params.rama_text_recognize_version
                                                                    )
        elif (self.danila_rama_text_recognize_params.rama_text_recognize_version == 3) | (self.danila_rama_text_recognize_params.rama_text_recognize_version == 4) | (self.danila_rama_text_recognize_params.rama_text_recognize_version == 6):
            self.danila_rama_text_recognize = Danila_rama_text_recognize_redone(local, yolov5_dir,
                                                                    self.danila_rama_text_recognize_params.rama_text_recognize_version
                                                                    )

    def rama_text_recognize(self, rama_prod, img_cut, img_text_areas):
        return self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, img_text_areas)