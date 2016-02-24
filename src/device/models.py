import datetime
from daya import db


class DeviceModel(db.Document):
    hospital = db.StringField()
    device_model = db.StringField()
    device_index = db.StringField()
    owner = db.StringField()
    status = db.LongField(default=0)
    is_deleted = db.BooleanField(default=False)
    update_time = db.DateTimeField(default=datetime.datetime.now())
    update_user = db.StringField()


class Device(object):
    def __init__(self, hospital=None, device_model=None, device_index=None, owner=None):
        self.hospital = hospital
        self.device_model = device_model
        self.device_index = device_index
        self.owner = owner
        self.status = 0
        self.update_user = None
        self.id = None
        self.update_time = None

    def save(self):
        if self.id is None:
            db_device = DeviceModel(hospital=self.hospital, device_model=self.device_model,
                                    device_index=self.device_index, owner=self.owner, status=self.status,
                                    update_user=self.update_user)
        else:
            db_device = DeviceModel.objects.with_id(self.id)
            db_device.hospital = self.hospital
            db_device.device_model = self.device_model
            db_device.device_index = self.device_index
            db_device.owner = self.owner
            db_device.status = self.status
            db_device.update_user = self.update_user

        db_device.save()
        if self.id is None:
            self.id = db_device.id
        return self.id

    def get_by_id(self, device_id):
        db_device = DeviceModel.objects.with_id(device_id)
        if db_device:
            self.hospital = db_device.hospital
            self.device_model = db_device.device_model
            self.device_index = db_device.device_index
            self.owner = db_device.owner
            self.status = db_device.status
            self.update_user = db_device.update_user
            self.id = db_device.id
            self.update_time = db_device.update_time
            return self
        else:
            return None

    @staticmethod
    def delete(device_id):
        db_device = DeviceModel.objects.with_id(device_id)
        if db_device:
            db_device.is_deleted = True
            db_device.save()
            return True
        else:
            return False

    @staticmethod
    def get_count():
        return DeviceModel.objects(is_deleted=False).count()

    @staticmethod
    def paginate(page, per_page):
        return DeviceModel.objects(is_deleted=False).paginate(page=int(page), per_page=int(per_page))

    @staticmethod
    def get_devices():
        return DeviceModel.objects(is_deleted=False).order_by("-update_time")
