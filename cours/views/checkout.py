from django.shortcuts import render, redirect
from cours.models import Course, Video, Payment, UserCourse, CouponCode
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from sronou.settings import *
from time import time
import requests




@login_required(login_url='/login')
def checkout(request, slug,):
    course = Course.objects.get(slug=slug)
    user = request.user
    couponcode = request.GET.get('couponcode')
    coupon_code_message = None
    coupon = None
    order = None
    payment = None
    error = None
    url = requests.get('http://localhost:8000/verify_payment')
    
    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "You are Already Enrolled in this Course"
    except:
        pass
    amount = None
    if error is None:
        amount = int(
            (course.price - (course.price * course.discount * 0.01)) * 100)
   # if ammount is zero dont create paymenty , only save emrollment obbect

    if couponcode:
        print("COUPONCODE ", couponcode)
        try:
            coupon = CouponCode.objects.get(course=course, code=couponcode)
            amount = course.price - (course.price * coupon.discount * 0.01)
            amount = int(amount) * 100
            print("AMOUNT", amount)
        except:
            coupon_code_message = 'invalid Coupon Code'
            print('coupon code invalid')

    if amount == 0:
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()
        return redirect('my-courses')

        # enroll direct
    order=f"sronou-{int(time())}"
    
    
    payment = Payment()
    payment.user = user
    payment.course = course
    payment.order_id = order
    payment.save()

    context = {
        "course": course,
        "order": order,
        "payment": payment,
        "user": user,
        "error": error,
        'coupon': coupon,
        "coupon_code_message": coupon_code_message,
        'url':url,
       
        
    }
    return render(request, template_name="courses/checkout.html", context=context)


@login_required(login_url='/login')
@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:
            # client.utility.verify_payment_signature(data)
            paygate_tx_reference = data['tx_reference']
            paygate_payment_reference = data['payment_reference']

            payment = Payment.objects.get(order_id=paygate_tx_reference)
            payment.payment_id = paygate_payment_reference
            payment.status = True

            userCourse = UserCourse(user=payment.user, course=payment.course)
            userCourse.save()

            print("UserCourse",  userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return redirect('my-courses')

        except:
            return HttpResponse("Invalid Payment Details")
