
from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponse,  HttpResponseRedirect,  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Doc,  Hos,  Bed,  Booking
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
import datetime
import time




#  region login


def index(request):
    return render(request,   'login/index.html')


def docli(request):
    return render(request,   'login/docli.html')


def hosli(request):
    return render(request,   'login/hosli.html')




def docli_check(request):
    uc = None
    for user in Doc.objects.all():
        if((user.user_name == request.POST['user_name']) and
           (user.user_pass == request.POST['user_pass'])):
            uc = user
    if(uc is None):
        return render(request,   'login/docli.html',   {

            'error_message': "Username/password incorrect.",
        })
    else:
        return HttpResponseRedirect(reverse('doc_home', args=(uc.id,)))


def hosli_check(request):
    mc = None
    for man in Hos.objects.all():
        if((man.hos_name == request.POST['hos_name']) and
           (man.hos_pass == request.POST['hos_pass'])):
            mc = man
    if(mc is None):
        return render(request, 'login/hosli.html',   {
            'error_message': "Username/password incorrect.",
        })
    else:
        return HttpResponseRedirect(reverse('hos_home', args=(mc.id,)))


# # endregion


# # region Home


def doc_home(request, doc_id):
    try:
        doc = Doc.objects.get(pk=doc_id)
    except Doc.DoesNotExist:
        raise Http404("Doctor does not exist")
    curr_list = Booking.objects.filter(doctor=doc). \
        order_by('-date')
    latest_list=[]
    
    latest_list = curr_list[: 5]
    context = {'doc': doc, 'latest_list': latest_list}
    return render(request, 'pages/dochome.html', context)


def hos_home(request, hos_id):
    try:
        hos = Hos.objects.get(pk=hos_id)
    except Hos.DoesNotExist:
        raise Http404("Hospital does not exist")
    hos_bed_list1 = Bed.objects.filter(hospital=hos).filter(bed_type= 1)
    hos_bed_list2 = Bed.objects.filter(hospital=hos).filter(bed_type= 2)
    hos_bed_list3 = Bed.objects.filter(hospital=hos).filter(bed_type= 3)
    context = {'hos':  hos,  'hos_bed_list1': hos_bed_list1 ,'hos_bed_list2': hos_bed_list2 ,'hos_bed_list3': hos_bed_list3}
    return render(request,   'pages/hoshome.html', context)

# # endregion

# # region Room-views


def bed_details(request,  bed_id):
    try:
        bed = Bed.objects.get(pk=bed_id)
    except Room.DoesNotExist:
        raise Http404("Bed does not exist")
    bookings_list = Booking.objects.filter(bed=bed)
    o=bed.occu
    
    context = {'bed': bed, 'bookings_list': bookings_list, 'occ': o}
    return render(request, 'pages/bdetailshos.html', context)


def add_bed(request, hos_id):
    try:
        hos = Hos.objects.get(pk=hos_id)
    except Hos.DoesNotExist:
        raise Http404("Hospital does not exist")
    context = {'hos': hos}
    return render(request, 'pages/addbed.html', context)


def add_bed_add(request, hos_id):
    id = request.POST['hos_id']
    hos = Hos.objects.get(pk=id)
    try:
        bt = (request.POST['bed_type'])
        oc= (request.POST['occ'])
        num= (request.POST['no_beds'])
        num=int(num)
    except ValueError as e:
        return render(request, 'pages/addbed.html', {
            'error_message':  "Wrong bed type", 'hos': hos
        })
  
    if(oc == "0"):
        o= False
    else:
        o= True
    for _ in range(num):
        r = Bed(hospital=hos, bed_type=bt, 
                    occu=o)
        r.save()
    hos_bed_list1 = Bed.objects.filter(hospital=hos).filter(bed_type= 1)
    hos_bed_list2 = Bed.objects.filter(hospital=hos).filter(bed_type= 2)
    hos_bed_list3 = Bed.objects.filter(hospital=hos).filter(bed_type= 3)
    context = {'hos':  hos,  'hos_bed_list1': hos_bed_list1 ,'hos_bed_list2': hos_bed_list2 ,'hos_bed_list3': hos_bed_list3}
    return render(request,   'pages/hoshome.html', context)


def edit_bed(request, bed_id):
    bed = Bed.objects.get(pk=bed_id)
    bookings_list = Booking.objects.filter(bed=bed)
    if(bed.occu==True):
        context = {'bed':  bed, 'bookings_list': bookings_list,
                   'error_message': "The bed is not empty."}

    if(bookings_list):
        context = {'bed':  bed, 'bookings_list': bookings_list,
                   'error_message': "There should not be any bookings to \
                    edit room"}
        return render(request, 'pages/bdetailshos.html', context)
    else:
        context = {'bed': bed}
        return render(request, 'pages/editbed.html', context)


def edit_bed_fun(request, bed_id):
    bed = Bed.objects.get(pk=bed_id)

    try:
        bt = (request.POST['bed_type'])
        oc = (request.POST['occ'])
    except ValueError as e:
        return render(request, 'pages/editbed.html', {
            'error_message':  "wrong bed type", 'bed': bed
        })
    if ( oc== "0"):
        o =False
    else:
        o = True
    r = Bed(id=bed.id, hospital=bed.hospital, bed_type=bt,
                occu=o)
    r.save()
    return HttpResponseRedirect(reverse('bdetails', args=( bed.id,)))


def delete_bed(request, bed_id):
    try:
        bed = Bed.objects.get(pk=bed_id)
    except Bed.DoesNotExist:
        raise Http404("Bed does not exist")
    bookings_list = Booking.objects.filter(bed=bed)
    if(bookings_list):
        st = "There should not be any bookings to remove bed"
        context = {'bed':  bed, 'bookings_list': bookings_list,
                   'error_message': st}
        return render(request, 'pages/bdetailshos.html', context)
    else:
        hos = bed.hospital
        bed.delete()
        hos_bed_list1 = Bed.objects.filter(hospital=hos).filter(bed_type= 1)
        hos_bed_list2 = Bed.objects.filter(hospital=hos).filter(bed_type= 2)
        hos_bed_list3 = Bed.objects.filter(hospital=hos).filter(bed_type= 3)
        context = {'hos':  hos,  'hos_bed_list1': hos_bed_list1 ,'hos_bed_list2': hos_bed_list2 ,'hos_bed_list3': hos_bed_list3}
        return render(request,   'pages/hoshome.html', context)
        
# # endregion
# # region Bookings


def book_details_hos(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    context = {'booking': booking}
    return render(request, 'pages/bookdetailshos.html', context)


def c_bookdetails_d(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    context = {'booking': booking}
    return render(request, 'pages/cbookdetailsd.html', context)


def deletebook(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    doc= booking.doctor
    bed= booking.bed
    booking.delete()
    bed.occu = False
    bed.save()
    latest_list = Booking.objects.filter(doctor=doc). \
        order_by('-date')
    if(len(latest_list) > 5):
        latest_list = latest_list[: 5]
    context = {'doc': doc, 'latest_list': latest_list}
    return render(request, 'pages/dochome.html', context)

def deletebookh(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    bed= booking.bed
    booking.delete()
    bed.occu = False
    bed.save()
    bookings_list = Booking.objects.filter(bed=bed)
    context = {'bed':  bed, 'bookings_list': bookings_list,
                }
    return render(request, 'pages/bdetailshos.html', context)

def currbook(request, doc_id):
    doc = Doc.objects.get(pk=doc_id)
    curr_list = Booking.objects.filter(doctor=doc). \
               order_by('-date')
    
    context = {'doc': doc, 'curr_list': curr_list,}
    return render(request, 'pages/currbook.html', context)





def newbook(request, doc_id):
    doc = Doc.objects.get(pk=doc_id)
    date = datetime.datetime.now()
    all_hos= Hos.objects.all()
    hos_names=[]
    for hos in all_hos:
        hos_names.append(hos.hos_name)

    context = {'doc': doc, 'today': date,'hos':hos_names}
    return render(request, 'pages/newbook.html', context)


def newbook_fun(request, doc_id):
    doc = Doc.objects.get(pk=doc_id)
    today = datetime.datetime.now()
    all_hos=Hos.objects.all()
    select_hos= all_hos[0]
    try:
        p_name = (request.POST['patient_name'])
        p_mob= (request.POST['patient_mob'])
        bt =   (request.POST['bed_type'])
        h= (request.POST['hospital'])
        for hos in all_hos:
            if(hos.hos_name==h):
                select_hos=hos

    except ValueError as e:
        context = {'doc': doc, 'today': today,
                   'error_message': "Incorrect bed type"}
        return render(request, 'pages/newbook.html', context)
    
    if(p_name==""):

        context = {'doc': doc, 'today': today,
                   'error_message': "Please enter patient name"}
        return render(request, 'pages/newbook.html', context)
    elif(p_mob==""):

        context = {'doc': doc, 'today': today,
                   'error_message': "Please enter patient Mobile number"}
        return render(request, 'pages/newbook.html', context)
    elif(bt==""):

        context = {'doc': doc, 'today': today,
                   'error_message': "Please enter type"}
        return render(request, 'pages/newbook.html', context)
    else:
        bed_list = []
        for bed in Bed.objects.filter(bed_type=bt).filter(hospital=select_hos):
            o= "0"
            if(bed.occu):
                o= "1"
            if(o == "0"):
                bed_list.append(bed)
        
        context = {'doc': doc, 'bed_list': bed_list, 'p_name':p_name, 'p_mob':p_mob,'bt':bt,
                   'today': today,}
        return render(request, 'pages/bedavai.html', context)


def bookroom(request, doc_id):
    doc = Doc.objects.get(pk=doc_id)

    bed = Bed.objects.get(pk=request.POST['bed_choice'])

    
    b = Booking(bed=bed, doctor=doc, date=datetime.datetime.now(),
                patient_name=request.POST['patient_name'], patient_mob=request.POST['patient_mob'],
                bed_type=request.POST['bed_type'])
    b.save()
    bed.occu= True
    bed.save()
    curr_list = Booking.objects.filter(doctor=doc). \
           order_by('-date')
    latest_list=[]
    latest_list = curr_list[: 5]
    context = {'doc':  doc, 'latest_list': latest_list}
    return render(request, 'pages/dochome.html', context)


# # endregion


# # region summery



def summery(request, hos_id):
    hos= Hos.objects.get(pk=hos_id)
    all_hos= Hos.objects.all()
    data=[]
    hospitals=[]
    for i in range(len(all_hos)):
        data.append([])
        hosp=all_hos[i]
        bed1=Bed.objects.filter(bed_type=1).filter(hospital=hosp)
        bed2=Bed.objects.filter(bed_type=2).filter(hospital=hosp)
        bed3=Bed.objects.filter(bed_type=3).filter(hospital=hosp)
        bed1_oc=Bed.objects.filter(bed_type=1).filter(hospital=hosp).filter(occu=True)
        bed2_oc=Bed.objects.filter(bed_type=2).filter(hospital=hosp).filter(occu=True)
        bed3_oc=Bed.objects.filter(bed_type=3).filter(hospital=hosp).filter(occu=True)
        hospitals.append(hosp.hos_name)
        data[i].append(hosp.hos_name)
        data[i].append(len(bed1)); data[i].append(len(bed2));data[i].append(len(bed3)) 
        data[i].append(len(bed1_oc));data[i].append(len(bed2_oc));data[i].append(len(bed3_oc))
    
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {'users': users, 
                'hos': hos}
    return render(request, 'pages/summery.html', context)

def summerydoc(request, doc_id):
    doc= Doc.objects.get(pk=doc_id)
    all_hos= Hos.objects.all()
    data=[]
    hospitals=[]
    for i in range(len(all_hos)):
        data.append([])
        hosp=all_hos[i]
        bed1=Bed.objects.filter(bed_type=1).filter(hospital=hosp)
        bed2=Bed.objects.filter(bed_type=2).filter(hospital=hosp)
        bed3=Bed.objects.filter(bed_type=3).filter(hospital=hosp)
        bed1_oc=Bed.objects.filter(bed_type=1).filter(hospital=hosp).filter(occu=True)
        bed2_oc=Bed.objects.filter(bed_type=2).filter(hospital=hosp).filter(occu=True)
        bed3_oc=Bed.objects.filter(bed_type=3).filter(hospital=hosp).filter(occu=True)
        hospitals.append(hosp.hos_name)
        data[i].append(hosp.hos_name)
        data[i].append(len(bed1)); data[i].append(len(bed2));data[i].append(len(bed3)) 
        data[i].append(len(bed1_oc));data[i].append(len(bed2_oc));data[i].append(len(bed3_oc))
    
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {'users': users, 
                'doc': doc}
    return render(request, 'pages/summerydoc.html', context)

def summeryindex(request):
    
    all_hos= Hos.objects.all()
    data=[]
    
    for i in range(len(all_hos)):
        data.append([])
        hosp=all_hos[i]
        bed1=Bed.objects.filter(bed_type=1).filter(hospital=hosp)
        bed2=Bed.objects.filter(bed_type=2).filter(hospital=hosp)
        bed3=Bed.objects.filter(bed_type=3).filter(hospital=hosp)
        bed1_oc=Bed.objects.filter(bed_type=1).filter(hospital=hosp).filter(occu=True)
        bed2_oc=Bed.objects.filter(bed_type=2).filter(hospital=hosp).filter(occu=True)
        bed3_oc=Bed.objects.filter(bed_type=3).filter(hospital=hosp).filter(occu=True)
        
        data[i].append(hosp.hos_name)
        data[i].append(len(bed1)); data[i].append(len(bed2));data[i].append(len(bed3)) 
        data[i].append(len(bed1_oc));data[i].append(len(bed2_oc));data[i].append(len(bed3_oc))
        
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        
    context = {'users': users, 
                }
    return render(request, 'pages/summeryindex.html', context)
# # endregion
# # region Availability


