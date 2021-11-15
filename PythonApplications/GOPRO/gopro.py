from datetime import datetime
import shutil
from goprocam import GoProCamera
# from goprocam import constants


class GoPro:
    def __init__(self):
        self.gopro = GoProCamera.GoPro()
        self.flag = False

    def take_photo_transfer_delete(self, timer, filename, filename_extension='jpg'):
        self.gopro.take_photo(timer=timer)
        # self.gopro.getStatusRaw()
        self.gopro.downloadLastMedia(custom_filename=f'{filename}.{filename_extension}')
        self.gopro.delete("last")

    def take_video_transfer_delete(self, timer, filename, filename_extension='jpg'):
        self.gopro.shoot_video(timer)
        # self.gopro.getStatusRaw()
        self.gopro.downloadLastMedia(custom_filename=f'{filename}.{filename_extension}')
        self.gopro.delete("last")

    def time_lapse(self, interval):
        while self.flag:
            self.gopro.downloadLastMedia(self.gopro.take_photo(timer=interval))
            self.gopro.downloadLastMedia()
            self.gopro.delete("last")

    def media_download_and_transfer_and_delete(self):
        media = self.gopro.downloadAll()
        for i in media:
            shutil.move('./100GOPRO-{}'.format(i), './images/100GOPRO-{}'.format(i))
        self.gopro.delete("all")


def get_current_time():
    return datetime.strftime(datetime.today(), "%Y_%m_%d")


if __name__ == '__main__':
    go_pro_obj = GoPro()  # WIFI password: mTM-9kx-Yyz
    go_pro_obj.gopro.listMedia(True)

    go_pro_obj.take_photo_transfer_delete(timer=2, filename=get_current_time())

    print()
