from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import EmpresaNexa, MemoriaMarca, ContenidoGenerado, EstrategiaMensual
from .forms import EmpresaNexaForm, MemoriaMarcaForm, GenerarContenidoForm, GenerarEstrategiaForm
from .services.generador_contenido import generar_contenido
from .services.agentes.estratega import generar_estrategia
from .services.agentes.copywriter import generar_contenido_completo


@login_required
def dashboard(request):
    qs_empresas = EmpresaNexa.objects.filter(usuario=request.user)
    qs_contenidos = ContenidoGenerado.objects.filter(empresa__usuario=request.user)
    return render(request, "nexa/dashboard.html", {
        "total_empresas": qs_empresas.count(),
        "total_contenidos": qs_contenidos.count(),
        "borradores": qs_contenidos.filter(estado="borrador").count(),
        "aprobados": qs_contenidos.filter(estado="aprobado").count(),
        "contenidos_recientes": qs_contenidos.select_related("empresa")[:6],
        "empresas": qs_empresas[:6],
    })


@login_required
def empresa_list(request):
    empresas = EmpresaNexa.objects.filter(usuario=request.user)
    return render(request, "nexa/empresa_list.html", {"empresas": empresas})


@login_required
def empresa_nueva(request):
    if request.method == "POST":
        form = EmpresaNexaForm(request.POST, request.FILES)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.usuario = request.user
            empresa.save()
            return redirect("nexa:empresa_detalle", pk=empresa.pk)
    else:
        form = EmpresaNexaForm()
    return render(request, "nexa/empresa_form.html", {"form": form, "accion": "Registrar empresa"})


@login_required
def empresa_detalle(request, pk):
    empresa = get_object_or_404(EmpresaNexa, pk=pk, usuario=request.user)
    memoria = getattr(empresa, "memoria_marca", None)
    contenidos = empresa.contenidos.all()[:10]
    palabras_clave_lista = []
    if memoria and memoria.palabras_clave:
        palabras_clave_lista = [p.strip() for p in memoria.palabras_clave.split(",") if p.strip()]
    return render(request, "nexa/empresa_detalle.html", {
        "empresa": empresa,
        "memoria": memoria,
        "contenidos": contenidos,
        "palabras_clave_lista": palabras_clave_lista,
    })


@login_required
def memoria_editar(request, pk):
    empresa = get_object_or_404(EmpresaNexa, pk=pk, usuario=request.user)
    memoria = getattr(empresa, "memoria_marca", None)
    if request.method == "POST":
        form = MemoriaMarcaForm(request.POST, instance=memoria)
        if form.is_valid():
            mem = form.save(commit=False)
            mem.empresa = empresa
            mem.save()
            return redirect("nexa:empresa_detalle", pk=empresa.pk)
    else:
        form = MemoriaMarcaForm(instance=memoria)
    return render(request, "nexa/memoria_form.html", {"form": form, "empresa": empresa})


@login_required
def generar(request, pk):
    empresa = get_object_or_404(EmpresaNexa, pk=pk, usuario=request.user)
    memoria = getattr(empresa, "memoria_marca", None)
    if request.method == "POST":
        form = GenerarContenidoForm(request.POST)
        if form.is_valid():
            resultado = generar_contenido(
                empresa=empresa,
                memoria_marca=memoria,
                tipo_contenido=form.cleaned_data["tipo_contenido"],
                objetivo=form.cleaned_data["objetivo"],
                tema=form.cleaned_data["tema"],
            )
            contenido = ContenidoGenerado.objects.create(
                empresa=empresa,
                tipo_contenido=form.cleaned_data["tipo_contenido"],
                titulo=resultado["titulo"],
                copy=resultado["copy"],
                hashtags=resultado["hashtags"],
                cta=resultado["cta"],
                estructura_json=resultado["estructura_json"],
                estado="borrador",
            )
            return redirect("nexa:contenido_detalle", pk=contenido.pk)
    else:
        form = GenerarContenidoForm()
    return render(request, "nexa/generar.html", {
        "form": form,
        "empresa": empresa,
        "memoria": memoria,
    })


@login_required
def contenido_list(request):
    empresa_id = request.GET.get("empresa")
    estrategia_id = request.GET.get("estrategia")
    tipo_filtro = request.GET.get("tipo")
    estado_filtro = request.GET.get("estado")

    qs = ContenidoGenerado.objects.filter(
        empresa__usuario=request.user
    ).select_related("empresa", "estrategia")

    if empresa_id:
        qs = qs.filter(empresa_id=empresa_id)
    if estrategia_id:
        qs = qs.filter(estrategia_id=estrategia_id)
    if tipo_filtro:
        qs = qs.filter(tipo_contenido=tipo_filtro)
    if estado_filtro:
        qs = qs.filter(estado=estado_filtro)

    base_qs = ContenidoGenerado.objects.filter(empresa__usuario=request.user)
    return render(request, "nexa/contenido_list.html", {
        "contenidos": qs,
        "empresas": EmpresaNexa.objects.filter(usuario=request.user),
        "estrategias": EstrategiaMensual.objects.filter(empresa__usuario=request.user).select_related("empresa"),
        "empresa_id_filtro": empresa_id,
        "estrategia_id_filtro": estrategia_id,
        "tipo_filtro": tipo_filtro,
        "estado_filtro": estado_filtro,
        "tipos": ContenidoGenerado.TIPOS,
        "estados": ContenidoGenerado.ESTADOS,
        "kpi_total": base_qs.count(),
        "kpi_borradores": base_qs.filter(estado="borrador").count(),
        "kpi_aprobados": base_qs.filter(estado="aprobado").count(),
        "kpi_programados": base_qs.filter(estado="programado").count(),
        "kpi_publicados": base_qs.filter(estado="publicado").count(),
    })


@login_required
def estrategia_list(request):
    estrategias = EstrategiaMensual.objects.filter(
        empresa__usuario=request.user
    ).select_related("empresa")
    empresas = EmpresaNexa.objects.filter(usuario=request.user)
    return render(request, "nexa/estrategia_list.html", {
        "estrategias": estrategias,
        "empresas": empresas,
    })


@login_required
def estrategia_nueva(request, pk):
    empresa = get_object_or_404(EmpresaNexa, pk=pk, usuario=request.user)
    memoria = getattr(empresa, "memoria_marca", None)
    if request.method == "POST":
        resultado = generar_estrategia(empresa=empresa, memoria_marca=memoria)
        estrategia = EstrategiaMensual.objects.create(
            empresa=empresa,
            objetivo=resultado["objetivo"],
            pilares_contenido=resultado["pilares_contenido"],
            frecuencia_publicacion=resultado["frecuencia_publicacion"],
            publico_objetivo=resultado["publico_objetivo"],
            calendario_json=resultado["calendario_json"],
        )
        return redirect("nexa:estrategia_detalle", pk=estrategia.pk)
    return render(request, "nexa/estrategia_nueva.html", {
        "empresa": empresa,
        "memoria": memoria,
    })


@login_required
def estrategia_detalle(request, pk):
    estrategia = get_object_or_404(
        EstrategiaMensual, pk=pk, empresa__usuario=request.user
    )
    pilares_lista = [p.strip() for p in estrategia.pilares_contenido.split(",") if p.strip()]
    cal = estrategia.calendario_json
    planificados = sum(
        len(s.get("publicaciones", [])) for s in cal.get("semanas", [])
    )
    generados = estrategia.contenidos.count()
    avance = round(generados / planificados * 100) if planificados > 0 else 0
    return render(request, "nexa/estrategia_detalle.html", {
        "estrategia": estrategia,
        "pilares_lista": pilares_lista,
        "planificados": planificados,
        "generados": generados,
        "avance": avance,
    })


@login_required
def generar_contenido_mes(request, pk):
    """Genera automáticamente todos los contenidos del calendario mensual."""
    estrategia = get_object_or_404(
        EstrategiaMensual, pk=pk, empresa__usuario=request.user
    )
    if request.method != "POST":
        return redirect("nexa:estrategia_detalle", pk=pk)

    empresa = estrategia.empresa
    memoria = getattr(empresa, "memoria_marca", None)
    cal = estrategia.calendario_json
    creados = 0

    for semana in cal.get("semanas", []):
        for pub in semana.get("publicaciones", []):
            resultado = generar_contenido_completo(
                empresa=empresa,
                memoria_marca=memoria,
                tipo_contenido=pub["tipo"],
                pilar=pub["pilar"],
                objetivo=pub.get("descripcion", pub["pilar"]),
                semana=semana["semana"],
            )
            ContenidoGenerado.objects.create(
                empresa=empresa,
                estrategia=estrategia,
                tipo_contenido=pub["tipo"],
                titulo=resultado["titulo"],
                copy=resultado["copy"],
                hashtags=resultado["hashtags"],
                cta=resultado["cta"],
                estructura_json=resultado["estructura_json"],
                estado="borrador",
            )
            creados += 1

    mes = cal.get("mes", "este mes")
    messages.success(request, f"Se generaron {creados} contenidos para {mes}.")
    return redirect("nexa:estrategia_detalle", pk=pk)


@login_required
def contenido_detalle(request, pk):
    contenido = get_object_or_404(
        ContenidoGenerado, pk=pk, empresa__usuario=request.user
    )
    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in dict(ContenidoGenerado.ESTADOS):
            contenido.estado = nuevo_estado
            contenido.save(update_fields=["estado"])
        return redirect("nexa:contenido_detalle", pk=pk)
    return render(request, "nexa/contenido_detalle.html", {"contenido": contenido})
