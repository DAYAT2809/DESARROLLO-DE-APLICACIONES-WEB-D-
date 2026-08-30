from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=2, max=100, message="Debe tener entre 2 y 100 caracteres.")
        ]
    )

    descripcion = StringField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(min=5, max=200, message="Debe tener entre 5 y 200 caracteres.")
        ]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0.")
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(min=0, message="El stock no puede ser negativo.")
        ]
    )

    submit = SubmitField("Guardar producto")