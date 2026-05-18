from django.db import models


class CategoriaConocimiento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)

    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría de conocimiento"
        verbose_name_plural = "Categorías de conocimiento"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class RespuestaConocimiento(models.Model):

    categoria = models.ForeignKey(
        CategoriaConocimiento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="respuestas"
    )

    titulo = models.CharField(max_length=200)

    palabras_clave = models.TextField(
        help_text="Separar palabras clave con coma"
    )

    respuesta = models.TextField()

    prioridad = models.IntegerField(default=1)

    activa = models.BooleanField(default=True)

    veces_utilizada = models.IntegerField(default=0)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Respuesta IA"
        verbose_name_plural = "Respuestas IA"
        ordering = ["-prioridad", "titulo"]

    def __str__(self):
        return self.titulo


class PreguntaAprendida(models.Model):

    pregunta = models.TextField()

    respuesta_sugerida = models.TextField(
        blank=True
    )

    respondida = models.BooleanField(default=False)

    veces_preguntada = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    ultima_vez = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pregunta aprendida"
        verbose_name_plural = "Preguntas aprendidas"
        ordering = ["-veces_preguntada"]

    def __str__(self):
        return self.pregunta[:80]


class ConversacionAgente(models.Model):

    nombre = models.CharField(
        max_length=200,
        blank=True
    )

    empresa = models.CharField(
        max_length=200,
        blank=True
    )

    correo = models.EmailField(
        blank=True
    )

    telefono = models.CharField(
        max_length=50,
        blank=True
    )

    ip = models.CharField(
        max_length=100,
        blank=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversación IA"
        verbose_name_plural = "Conversaciones IA"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Conversación #{self.id}"


class MensajeAgente(models.Model):

    conversacion = models.ForeignKey(
        ConversacionAgente,
        on_delete=models.CASCADE,
        related_name="mensajes"
    )

    rol = models.CharField(
        max_length=20,
        choices=[
            ("user", "Usuario"),
            ("assistant", "Asistente"),
        ]
    )

    mensaje = models.TextField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje IA"
        verbose_name_plural = "Mensajes IA"
        ordering = ["fecha_creacion"]

    def __str__(self):
        return f"{self.rol} - {self.fecha_creacion}"