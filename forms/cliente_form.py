from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=2, max=100, message="Debe tener entre 2 y 100 caracteres.")
        ]
    )

    email = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=7, max=15, message="El teléfono debe tener entre 7 y 15 caracteres.")
        ]
    )

    direccion = StringField(
        "Dirección",
        validators=[
            DataRequired(message="La dirección es obligatoria."),
            Length(min=5, max=150, message="Debe tener entre 5 y 150 caracteres.")
        ]
    )

    submit = SubmitField("Guardar cliente")