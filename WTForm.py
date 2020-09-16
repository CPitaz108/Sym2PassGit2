from wtforms import Form, BooleanField, validators


class Sym2passForm(Form):
    coughing = BooleanField('Coughing?', [validators.InputRequired()])
    sore_throat = BooleanField('Sore Through?', [validators.InputRequired()])
    diarrhea = BooleanField('Diarrhea?', [validators.InputRequired()])
    fever = BooleanField('Fever?', [validators.InputRequired()])
    headache = BooleanField('Headache?', [validators.InputRequired()])
    loss_smell = BooleanField('Loss of Smell?', [validators.InputRequired()])
    loss_taste = BooleanField('Loss of Taste?', [validators.InputRequired()])
    shortness_breath = BooleanField('Shortness of Breath?', [validators.InputRequired()])
    fatigue = BooleanField('Fatigue?', [validators.InputRequired()])
    chest_pain = BooleanField('Chest Pain?', [validators.InputRequired()])
    loss_consciousness = BooleanField('Loss of Consciousness', [validators.InputRequired()])
    confusion = BooleanField('Confusion', [validators.InputRequired()])

    def register(request):
        form = Sym2passForm(request.POST);
        if request.method == 'POST' and form.validate():
            user = User();
            user.coughing = form.coughing.data;
            user.sore_throat = form.sore_throat.data;
            user.diarrhea = form.diarrhea.data;
            user.fever = form.fever.data;
            user.headache = form.headache.data;
            user.loss_smell = form.loss_smell.data;
            user.loss_taste = form.loss_taste.data;
            user.shortness_breath = form.shortness_breath.data;
            user.fatigue = form.fatigue.data;
            user.chest_pain = form.chest_pain.data;
            user.loss_consciousness = form.loss_consciousness.data;
            user.confusion = form.confusion.data;
            user.save();
            redirect('register');
        return render_response('register.html',form=form);