from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('docli/', views.docli, name='docli'),
    
    path('hosli/', views.hosli, name='hosli'),
    
    path('docli_check/', views.docli_check, name='docli_check'),
    path('hosli_check/', views.hosli_check, name='hosli_check'),
   
    path('<int:doc_id>/dochome/', views.doc_home, name='doc_home'),
    path('<int:hos_id>/hoshome/', views.hos_home, name='hos_home'),
    path('<int:bed_id>/bdetails/', views.bed_details, name='bdetails'),
    path('<int:hos_id>/addbed/', views.add_bed, name='addbed'),
    path('<int:hos_id>/addbedadd/', views.add_bed_add, name='addbedadd'),
    path('<int:booking_id>/bookdetailsh/', views.book_details_hos, name='bookdetailsh'),
    path('<int:bed_id>/editbed/', views.edit_bed, name='editbed'),
    path('<int:bed_id>/editbedf/', views.edit_bed_fun, name='editbedf'),
    path('<int:bed_id>/deletebed/', views.delete_bed, name='deletebed'),
    path('<int:booking_id>/cbookdetailsd/', views.c_bookdetails_d, name='cbookdetaild'),
    
    path('<int:booking_id>/deletebook/', views.deletebook, name='deletebook'),
    path('<int:booking_id>/deletebookh/', views.deletebookh, name='deletebookh'),
    path('<int:doc_id>/currbook/', views.currbook, name='currbook'),
    
    path('<int:doc_id>/newbook/', views.newbook, name='newbook'),
    path('<int:doc_id>/newbookfun/', views.newbook_fun, name='newbookfun'),
    path('<int:doc_id>/bookroom/', views.bookroom, name='bookroom'),
    path('<int:hos_id>/summery/', views.summery, name='summery'),
    path('<int:doc_id>/summerydoc/', views.summerydoc, name='summerydoc'),
    path('summeryindex/', views.summeryindex, name='summeryindex'),
    # path('<int:user_id>/available/', views.available, name='available'),
    # path('<int:user_id>/avachecke/', views.avacheck, name='avacheck'),
    
]
