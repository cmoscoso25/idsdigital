document.addEventListener("DOMContentLoaded", function () {
  const botonAbrir = document.getElementById("idsIaAbrir");
  const botonCerrar = document.getElementById("idsIaCerrar");
  const panel = document.getElementById("idsIaPanel");
  const form = document.getElementById("idsIaForm");
  const input = document.getElementById("idsIaInput");
  const mensajesBox = document.getElementById("idsIaMensajes");

  const nombreInput = document.getElementById("idsIaNombre");
  const empresaInput = document.getElementById("idsIaEmpresa");
  const emailInput = document.getElementById("idsIaEmail");
  const telefonoInput = document.getElementById("idsIaTelefono");
  const guardarBtn = document.getElementById("idsIaGuardar");
  const estado = document.getElementById("idsIaEstado");

  let historial = [
    {
      role: "assistant",
      content:
        "Hola, soy el asistente IA de IDS Digital. ¿Qué proceso, problema o necesidad tecnológica quieres resolver?",
    },
  ];

  function abrirPanel() {
    panel.classList.add("activo");
    panel.setAttribute("aria-hidden", "false");
    setTimeout(() => input.focus(), 150);
  }

  function cerrarPanel() {
    panel.classList.remove("activo");
    panel.setAttribute("aria-hidden", "true");
  }

  function agregarMensaje(tipo, texto) {
    const div = document.createElement("div");
    div.className =
      tipo === "user"
        ? "ids-ia-msg ids-ia-msg-user"
        : "ids-ia-msg ids-ia-msg-bot";
    div.textContent = texto;
    mensajesBox.appendChild(div);
    mensajesBox.scrollTop = mensajesBox.scrollHeight;
  }

  function obtenerCSRFToken() {
    const nombre = "csrftoken";
    const cookies = document.cookie ? document.cookie.split(";") : [];

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, nombre.length + 1) === nombre + "=") {
        return decodeURIComponent(cookie.substring(nombre.length + 1));
      }
    }

    return "";
  }

  async function enviarMensaje(mensaje) {
    const boton = form.querySelector("button");
    boton.disabled = true;
    boton.textContent = "Pensando...";

    try {
      const respuesta = await fetch("/agente-ia/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": obtenerCSRFToken(),
        },
        body: JSON.stringify({
          mensajes: historial,
        }),
      });

      const data = await respuesta.json();

      if (!respuesta.ok || !data.ok) {
        throw new Error(data.error || "No fue posible obtener respuesta.");
      }

      historial.push({
        role: "assistant",
        content: data.respuesta,
      });

      agregarMensaje("assistant", data.respuesta);
    } catch (error) {
      agregarMensaje(
        "assistant",
        "En este momento no pude generar el diagnóstico. Intenta nuevamente en unos minutos."
      );
    } finally {
      boton.disabled = false;
      boton.textContent = "Enviar";
    }
  }

  async function guardarDiagnostico() {
    const nombre = nombreInput.value.trim();
    const empresa = empresaInput.value.trim();
    const email = emailInput.value.trim();
    const telefono = telefonoInput.value.trim();

    if (!nombre || !email) {
      estado.textContent = "Debes ingresar al menos nombre y correo.";
      estado.style.color = "#e2001a";
      return;
    }

    guardarBtn.disabled = true;
    guardarBtn.textContent = "Guardando...";
    estado.textContent = "";

    const resumen = historial
      .map((m) => `${m.role === "user" ? "Usuario" : "Agente IDS"}: ${m.content}`)
      .join("\n\n");

    try {
      const respuesta = await fetch("/agente-ia/guardar/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": obtenerCSRFToken(),
        },
        body: JSON.stringify({
          nombre: nombre,
          empresa: empresa,
          email: email,
          telefono: telefono,
          resumen: resumen,
        }),
      });

      const data = await respuesta.json();

      if (!respuesta.ok || !data.ok) {
        throw new Error(data.error || "No fue posible guardar.");
      }

      estado.textContent =
        "Diagnóstico guardado correctamente. IDS Digital te contactará pronto.";
      estado.style.color = "#15803d";

      nombreInput.value = "";
      empresaInput.value = "";
      emailInput.value = "";
      telefonoInput.value = "";
    } catch (error) {
      estado.textContent =
        "No fue posible guardar el diagnóstico. Intenta nuevamente.";
      estado.style.color = "#e2001a";
    } finally {
      guardarBtn.disabled = false;
      guardarBtn.textContent = "Guardar diagnóstico";
    }
  }

  botonAbrir.addEventListener("click", abrirPanel);
  botonCerrar.addEventListener("click", cerrarPanel);

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const mensaje = input.value.trim();

    if (!mensaje) {
      return;
    }

    historial.push({
      role: "user",
      content: mensaje,
    });

    agregarMensaje("user", mensaje);
    input.value = "";

    enviarMensaje(mensaje);
  });

  guardarBtn.addEventListener("click", guardarDiagnostico);
});