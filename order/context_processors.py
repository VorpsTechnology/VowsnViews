from .models import Cart, Order


def cart_list(request):
    cart_count = 0
    cart = ''
    order = ''
    if request.user.is_authenticated:
        cart = Cart.objects.filter(ordered=False, user=request.user)
        order = Order.objects.filter(ordered=False, user=request.user).first()
        try:
            cart_count = cart.count()
        except:
            pass
    return {
        'cart': cart,
        'order': order,
        'cart_count': cart_count
    }


