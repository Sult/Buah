from django import forms


class HeroNameForm(forms.Form):
    """ change the name of a hero """
    
    name = forms.CharField(max_length=63, min_length=1, label="")

    def save(self, hero, commit=True):
        heroname = super(HeroNameForm, self)
        name = self.cleaned_data['name']
        hero.name = name
        
        if commit:
            hero.save()
        return heroname


