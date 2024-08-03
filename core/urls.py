from django.urls import path
from .views import DepositView, BorrowView, ReturnView, RatingView, BookDetailView
urlpatterns = [
    path('deposit/', DepositView.as_view(), name = 'deposit'),
    path('borrow/<int:pk>/', BorrowView.as_view(), name = 'borrow'),
    path('return/<int:pk>/', ReturnView.as_view(), name = 'return'),
    path('rating/<int:pk>/', RatingView.as_view(), name = 'rating'),
    path('details/<int:pk>/', BookDetailView.as_view(), name = 'details'),
]
