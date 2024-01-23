# -*- coding: utf-8 -*-
# @Time    : 2024/1/23 上午9:22
# @Author  : sudoskys
# @File    : hash.py
# @Software: PyCharm
import base64
import hashlib
import hmac
import json
from typing import Union

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from loguru import logger
from pydantic import BaseModel


def sign_message(message, key):
    # 使用 HMAC 算法对消息进行哈希签名
    hmac_digest = hmac.new(key.encode(), message.encode(), hashlib.sha256).digest()
    signed_hash = base64.b64encode(hmac_digest).decode()
    return signed_hash


class NaiPic(BaseModel):
    title: str = "AI generated image"
    description: str
    comment: Union[dict, str] = {}

    def generate_exif(self):
        self.comment["signed_hash"] = sign_message(json.dumps(self.description), "novalai-bot")
        self.comment = json.dumps(self.comment)
        return {"Title": self.title, "Description": self.description, "Comment": self.comment}

    def generate_to_img_io(self, img_io):
        with Image.open(img_io) as img:
            metadata = PngInfo()
            _info = self.generate_exif()
            for k, v in _info.items():
                metadata.add_text(k, v)
            img.save(img_io, format="PNG", pnginfo=metadata)
            return img_io

    @classmethod
    def read_from_img(cls, image_io):
        with Image.open(image_io) as img:
            title = img.info.get("Title")
            if not title == 'AI generated image':
                raise ValueError("Not a NaiPic")
            prompt = img.info.get("Description")
            comment = img.info.get("Comment")
            try:
                comment = json.loads(comment)
            except Exception as e:
                logger.debug(e)
                comment = {}
            return cls(title=title, description=prompt, comment=comment)

    @classmethod
    def read_from_param(cls, prompt, neg_prompt, **kwargs):
        _comment = {"uc": neg_prompt}
        _comment.update(kwargs)
        return cls(title="AI generated image", description=prompt, comment=_comment)
