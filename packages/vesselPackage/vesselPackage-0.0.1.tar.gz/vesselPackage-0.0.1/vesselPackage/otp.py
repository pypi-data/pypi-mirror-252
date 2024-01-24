# from datetime import datetime
# import uuid
# from time import time
# import base64
# import datetime
# from api.models import OTP


# def generateKey(email):
#     key_string = str(email) + "FGH#^&TYE&V*EV^&U#H$R*&H&*$F(Y*GHT$*O(GT$&)))"
#     return base64.b32encode(key_string.encode())


# def generate_OTP(request, user=None, email=None, template=None, subject=None):
#     key = generateKey(email)
#     otp_code = str(uuid.uuid1())[:6]

#     if OTP.objects.filter(key=key).exists():
#         OTP.objects.filter(key=key).delete()

#     try:

#         otp_model = OTP.objects.create(key=key, otp=otp_code)

#     except:
#         return None
    
#     return otp_model.otp


# def verify_OTP(otp, email):
#     key = generateKey(email)

#     if OTP.objects.filter(key=key).exists():
#         otpmodel = OTP.objects.get(key=key)
#         expire_time = otpmodel.created_date + datetime.timedelta(minutes=5)

#         if expire_time < datetime.datetime.now():
#             OTP.objects.filter(key=key).delete()
#             return {
#                 "is_verify": False,
#                 "message": "OTP has been Expired, generate new OTP",
#             }

#         elif otp == otpmodel.otp:

#             OTP.objects.filter(key=key).delete()
#             return {"is_verify": True, "message": "OTP verified"}

#         else:
#             return {"is_verify": False, "message": "Incorrect OTP"}
#     else:
#         return {"is_verify": False, "message": "Invalid OTP"}
