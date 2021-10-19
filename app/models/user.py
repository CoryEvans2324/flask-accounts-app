import mongoengine as db

class User(db.Document):
    email = db.StringField(max_length=300, required=True)
    role = db.StringField(default="normal")


    passwordHash = db.StringField()
    otpEnabled = db.BooleanField(default=False)
    otpSecret = db.StringField()

    @property
    def is_authenticated(self) -> bool:
        return not self.is_anonymous
    
    @property
    def is_active(self) -> bool:
        return True
    
    @property
    def is_anonymous(self) -> bool:
        return self.id == None

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        return User.objects(id=user_id).exclude('passwordHash').exclude('otpSecret').first()