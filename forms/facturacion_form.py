from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio.")
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(message="El producto es obligatorio.")
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(min=1, message="La cantidad debe ser mayor a 0.")
        ]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0.")
        ]
    )

    submit = SubmitField("Generar factura")