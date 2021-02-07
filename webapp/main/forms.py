from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from webapp.main.utils import get_team_list


eredivisie_list = get_team_list()

choices = [(i, c) for i, c in zip(range(1, 19), eredivisie_list)]


class EredivisieForm(FlaskForm):
    ed_1 = SelectField('1', choices=eredivisie_list)
    ed_2 = SelectField('2', choices=eredivisie_list)
    ed_3 = SelectField('3', choices=eredivisie_list)
    ed_4 = SelectField('4', choices=eredivisie_list)
    ed_5 = SelectField('5', choices=eredivisie_list)
    ed_6 = SelectField('6', choices=eredivisie_list)
    ed_7 = SelectField('7', choices=eredivisie_list)
    ed_8 = SelectField('8', choices=eredivisie_list)
    ed_9 = SelectField('9', choices=eredivisie_list)
    ed_10 = SelectField('10', choices=eredivisie_list)
    ed_11 = SelectField('11', choices=eredivisie_list)
    ed_12 = SelectField('12', choices=eredivisie_list)
    ed_13 = SelectField('13', choices=eredivisie_list)
    ed_14 = SelectField('14', choices=eredivisie_list)
    ed_15 = SelectField('15', choices=eredivisie_list)
    ed_16 = SelectField('16', choices=eredivisie_list)
    ed_17 = SelectField('17', choices=eredivisie_list)
    ed_18 = SelectField('18', choices=eredivisie_list)
    submit = SubmitField('Voorspelling Opslaan')

    def validate(self):
        rv = FlaskForm.validate(self)

        seen = set()
        for field in [self.ed_1, self.ed_2, self.ed_3, self.ed_4,
                      self.ed_5, self.ed_6, self.ed_7, self.ed_8,
                      self.ed_9, self.ed_10, self.ed_11, self.ed_12,
                      self.ed_13, self.ed_14, self.ed_15, self.ed_16,
                      self.ed_17, self.ed_18]:
            if field.data in seen:
                list(self.errors).append('Not unique')
                return False
            else:
                seen.add(field.data)
        return True
