from django.shortcuts import render ,redirect ,get_object_or_404
import braintree
from django.conf import settings
from orders.models import Order

# Create your views here.

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id =request.session.get('order_id') #get the current order from the order_id session key was stored by the order_create view
    order = get_object_or_404(Order , id= order_id) #You retrieve the Order object for the given ID or raise an Http404
    total_cost =order.get_total_cost()
    if request.method == 'POST':
        # retrieve nonce
        #When the view is loaded with a POST request, you retrieve the payment_method_nonce using gateway.transaction
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({'amount': f'{total_cost:.2f}',
                                                        'payment_method_nonce': nonce,
                                                        'options': {'submit_for_settlement': True}})

        if result.is_success :
            # mark the order as paid if transacion was success
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')

        else :
            return redirect('payment:canceled')    

#the view was loaded with a GET request, generate a client token with gateway.client_token.generate() 
# that you will use in the template
    else :
        # generate token
        #client_token = gateway.client_token.generate()
        
        #return render(request,'payment/process.html',{'order':order,'client_token':client_token})
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,'payment/process.html',{'order': order,'client_token': client_token})

#create basic views to redirect users when their payment has been successful
def payment_done(request):
    return render(request , 'payment/done.html')


def payment_canceled(request):
    return render (request , 'payment/canceled.html')