from django.shortcuts import render
from .forms import homeForm
from . import crypto
from django.contrib import messages

# Create your views here.
def home(request):
    form1 = homeForm()
    key_eff = ""
    changed = ""
    mylis = []
    diff = []
    roundKeys = []
    round_no_list = []
    data = {}
    if request.method == 'POST':
        form1 = homeForm(request.POST)
        if form1.is_valid():
            n = form1.cleaned_data['rounds']
            l = form1.cleaned_data['length']
            x = form1.cleaned_data['option']
            b = form1.cleaned_data['block'][:l]
            k = form1.cleaned_data['key'][:l]
            mylis = crypto.run(n, l, b, k, x)
            diff = mylis[0]
            roundKeys = mylis[1]
            key_eff = mylis[4]
            changed = mylis[5]
            print(diff)
            round_no_list = list(range(n+1))
            data = {
                "labels":round_no_list,
                "DefaultData":diff,
            }
             
        
    return render(request, 'index.html', {'form': form1, 'output':zip(diff, roundKeys), "data":data, 'key_eff':key_eff, 'alter':changed})
        