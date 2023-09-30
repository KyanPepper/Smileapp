from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Post,Tag,postTags

class PostForm(FlaskForm):

    def tag_query():
        return Tag.query.all()

    title = StringField('Title', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    body  = TextAreaField('Body',validators=[DataRequired(),Length(min=1, max=1500)])
    submit = SubmitField('Post')
    tag =  QuerySelectMultipleField( 'Tag', query_factory= tag_query, get_label=lambda tag: tag.name, widget=ListWidget(prefix_label=False),  option_widget=CheckboxInput())


class SortForm(FlaskForm):
   sort = SelectField('Sort',choices = [(1, 'Date'), (2, 'Title'), (3,'# of likes'),(4,'Happiness level')])
   userSort = BooleanField('Display my Posts only')
   submit =SubmitField('Refresh')
   
 