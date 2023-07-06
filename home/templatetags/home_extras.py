from django import template
# from forex_python.converter import CurrencyRates
from currency_converter import CurrencyConverter

register = template.Library()


@register.filter()
def class_name(value):
    return value.__class__.__name__


@register.simple_tag
def country_currency(request, country):
    if request.session['currency']:
        request.session['currency'] = request.POST.get('currency')
        if country == request.session['currency']:
            return 'selected'
    elif request.user.is_authenticated:
        request.session['currency'] = request.user.currency
    else:
        request.session['currency'] = 'INR'
    return ''


@register.simple_tag
def currency(request, amt):
    # Forex code
    # converter = CurrencyRates()
    # try:
    #     amount = converter.convert('INR', 'USD', 1)
    # except:
    #     amount = amt

    # currency_converter code
    converter = CurrencyConverter()
    try:
        amount = converter.convert(amt, 'INR', request.session['currency'])
    except:
        amount = amt

    try:
        if request.session['currency'] == 'USD':
            currency_symbol = '$'
        elif request.session['currency'] == 'EUR':
            currency_symbol = '€'
        elif request.session['currency'] == 'AUD':
            currency_symbol = 'A$'
        elif request.session['currency'] == 'GBP':
            currency_symbol = '£'
        else:
            currency_symbol = '₹'
    except:
        currency_symbol = '₹'

    return f'{currency_symbol}{round(amount)}'

