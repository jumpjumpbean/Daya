import datetime
from daya import db
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUserMixin,
                             confirm_login, fresh_login_required)


class UserModel(db.Document):
    account = db.StringField(default='')
    password = db.StringField(default='')
    name = db.StringField(default='')
    type = db.IntField(default=0)
    address = db.StringField(default='')
    telephone = db.StringField(default='')
    description = db.StringField(default='')
    active = db.BooleanField(default=True)
    is_admin = db.BooleanField(default=False)
    is_deleted = db.BooleanField(default=False)
    timestamp = db.DateTimeField(default=datetime.datetime.now())


class User(UserMixin):
    def __init__(self, account=None, name=None, password=None, user_type=None, active=True):
        self.account = account
        self.name = name
        self.password = password
        self.active = active
        self.type = user_type
        self.address = None
        self.telephone = None
        self.description = None
        self.is_admin = False
        self.id = None

    def save(self):
        if self.id is None:
            db_user = UserModel(account=self.account, name=self.name, password=self.password,
                                type=self.type, address=self.address, telephone=self.telephone,
                                description=self.description, active=self.active, is_admin=self.is_admin)
        else:
            db_user = UserModel.objects.with_id(self.id)
            db_user.name = self.name
            db_user.account = self.account
            db_user.password = self.password
            db_user.type = self.type
            db_user.address = self.address
            db_user.telephone = self.telephone
            db_user.description = self.description
            db_user.active = self.active
            db_user.is_admin = self.is_admin

        db_user.save()
        if self.id is None:
            self.id = db_user.id
        return self.id

    def get_by_name(self, name):
        db_user = UserModel.objects.get(name=name)
        if db_user:
            self.account = db_user.account
            self.name = db_user.name
            self.active = db_user.active
            self.password = db_user.password
            self.id = db_user.id
            self.type = db_user.type
            self.address = db_user.address
            self.telephone = db_user.telephone
            self.description = db_user.description
            self.is_admin = db_user.is_admin
            return self
        else:
            return None

    def get_by_name_w_password(self, name):
        try:
            db_user = UserModel.objects.get(name=name)

            if db_user:
                self.account = db_user.account
                self.name = db_user.name
                self.active = db_user.active
                self.password = db_user.password
                self.id = db_user.id
                self.type = db_user.type
                self.address = db_user.address
                self.telephone = db_user.telephone
                self.description = db_user.description
                self.is_admin = db_user.is_admin
                return self
            else:
                return None
        except Exception, e:
            print e
            #print "there was an error"
            return None

    def get_mongo_doc(self):
        if self.id:
            return UserModel.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, uid):
        db_user = UserModel.objects.with_id(uid)
        if db_user:
            self.account = db_user.account
            self.name = db_user.name
            self.active = db_user.active
            self.password = db_user.password
            self.id = db_user.id
            self.type = db_user.type
            self.address = db_user.address
            self.telephone = db_user.telephone
            self.description = db_user.description
            self.is_admin = db_user.is_admin
            return self
        else:
            return None

    def is_admin(self):
        return self.is_admin

    def is_valid(self):
        if self.active and self.type == 1 and self.is_active():
            return True
        else:
            return False

    @staticmethod
    def delete(user_id):
        db_user = UserModel.objects.with_id(user_id)
        if db_user and not db_user.is_admin:
            db_user.is_deleted = True
            db_user.save()
            return True
        else:
            return False

    @staticmethod
    def get_count():
        return UserModel.objects(is_deleted=False).count()

    @staticmethod
    def paginate(page, per_page):
        return UserModel.objects(is_deleted=False).paginate(page=int(page), per_page=int(per_page))

    @staticmethod
    def get_users():
        return UserModel.objects.order_by("name")


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
