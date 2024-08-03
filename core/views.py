from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import DepositForm, RatingForm
from .models import Deposit, Book, Borrow, RatingModel
from django.contrib import messages
from accounts.models import UserAccountModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class DepositView(LoginRequiredMixin, CreateView):
    model = Deposit
    form_class = DepositForm
    template_name = 'deposit.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = UserAccountModel.objects.get(user=self.request.user)
        account.balance += amount
        account.save()

        # Create Deposit instance with the associated account
        deposit = form.save(commit=False)
        deposit.account = account
        deposit.save()

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        self.mail_sending(amount, account)
        return super().form_valid(form)

    def mail_sending(self, amount, account):
        mail_subject = 'Deposit'
        mail_message = render_to_string('deposit_mails.html', {
            'user': self.request.user,
            'amount': amount,
            'balance': account.balance
        })
        mail_from = settings.EMAIL_HOST_USER
        mail_to = [self.request.user.email]
        mail = EmailMultiAlternatives(mail_subject, mail_message, mail_from, mail_to)
        mail.attach_alternative(mail_message, 'text/html')
        mail.send()

class BorrowView(LoginRequiredMixin, CreateView):
    model = Book
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        account = get_object_or_404(UserAccountModel, user=request.user)
        
        if book.available_copies <= 0:
            messages.error(request, 'No available copies for this book')
            return render(request, 'books.html', {'books': Book.objects.all()})
        
        if account.balance < book.borrowing_price:
            messages.error(request, 'Insufficient balance')
            return render(request, 'books.html', {'books': Book.objects.all()})
        
        account.balance -= book.borrowing_price
        account.save()
        
        book.available_copies -= 1
        book.save()
        
        borrow, created = Borrow.objects.get_or_create(user=request.user, book=book)
        if not created:
            borrow.borrow_count += 1
            borrow.save()
        
        messages.success(request, f'You have successfully borrowed {book.title}')

        #send_maillllllllll
        mail_subject = 'Borrow'
        mail_message = render_to_string('borrow.html', {
            'user': self.request.user,
            'amount': book.borrowing_price,
            'balance': account.balance,
            'book' : book,
        })
        mail_from = settings.EMAIL_HOST_USER
        mail_to = [self.request.user.email]
        mail = EmailMultiAlternatives(mail_subject, mail_message, mail_from, mail_to)
        mail.attach_alternative(mail_message, 'text/html')
        mail.send()
        return render(request, 'books.html', {'books': Book.objects.all()})

class ReturnView(LoginRequiredMixin, CreateView):
    model = Book
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        account = get_object_or_404(UserAccountModel, user=request.user)
        
        account.balance += book.borrowing_price
        account.save()
        
        book.available_copies += 1
        book.save()
        
        try:
            borrow = Borrow.objects.get(user=request.user, book=book)
            if borrow.borrow_count > 1:
                borrow.borrow_count -= 1
                borrow.save()
            else:
                borrow.delete()
        except Borrow.DoesNotExist:
            messages.error(request, 'No borrow record found for this book')
            return render(request, 'books.html', {'books': Book.objects.all()})
        
        messages.success(request, f'You have successfully returned {book.title}')

        #send_maillllllllll
        mail_subject = 'Return'
        mail_message = render_to_string('return.html', {
            'user': self.request.user,
            'amount': book.borrowing_price,
            'balance': account.balance,
            'book' : book,
        })
        mail_from = settings.EMAIL_HOST_USER
        mail_to = [self.request.user.email]
        mail = EmailMultiAlternatives(mail_subject, mail_message, mail_from, mail_to)
        mail.attach_alternative(mail_message, 'text/html')
        mail.send()
        return render(request, 'books.html', {'books': Book.objects.all()})

class RatingView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = RatingForm
    template_name = 'rate.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        rating = form.cleaned_data.get('rate')
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        rating_obj, created = RatingModel.objects.update_or_create(user = self.request.user, book=book, defaults={'rate': rating})
        self.object = form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_details.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['rating'] = RatingModel.objects.filter(book=book)
        return context
