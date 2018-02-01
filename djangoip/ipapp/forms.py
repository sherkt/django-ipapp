from django import forms
from django.template.defaultfilters import striptags


class IpForm(forms.Form):
    ip = forms.GenericIPAddressField()


    def clean_ip(self):
        print("got here")
        ip = self.cleaned_data['ip']
        if striptags(ip) != ip:
            raise forms.ValidationError("You have some HTML code in there.")
        elif "()" in ip or ";" in ip:
            raise forms.ValidationError("You have code in there.")
        return ip
