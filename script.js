"use strict";

// Datos de práctica. NO son requisitos oficiales ni registran trámites reales.
const SERVICIOS = {
  agua: {
    titulo: "Agua y saneamiento", imagen: "agua.svg", alt: "Ícono de una gota de agua",
    resumen: "Orientación sobre suministro, incidencias y saneamiento.",
    descripcion: "Este ejemplo explica cómo un portal puede organizar solicitudes vinculadas con el suministro de agua, la atención de fugas y las consultas de saneamiento.",
    requisitos: ["Descripción de la consulta o incidencia.", "Referencia del sitio o zona afectada.", "Número de cuenta o comprobante, solo cuando el organismo oficial lo solicite."],
    pasos: ["Identifica si se trata de una consulta o un reporte.", "Prepara una descripción clara y la referencia de ubicación.", "Consulta los canales oficiales del organismo operador del agua."],
    nota: "Los formatos y tiempos de atención dependen de la autoridad responsable."
  },
  licencias: {
    titulo: "Licencias y permisos", imagen: "licencias.svg", alt: "Ícono de una credencial",
    resumen: "Información introductoria para permisos y licencias.",
    descripcion: "El servicio ilustra la presentación ordenada de información para gestionar licencias y permisos, como los relacionados con la conducción vehicular.",
    requisitos: ["Identificación y datos del solicitante.", "Comprobantes y constancias que establezca el procedimiento.", "Tipo de licencia o permiso que se pretende tramitar."],
    pasos: ["Determina el tipo de permiso requerido.", "Revisa en el portal oficial la lista vigente de documentos.", "Sigue el procedimiento oficial para realizar el trámite o agendar una cita."],
    nota: "No se incluyen costos, vigencias ni documentos obligatorios, pues cambian según la entidad y el trámite."
  },
  transporte: {
    titulo: "Movilidad y transporte", imagen: "transporte.svg", alt: "Ícono de un autobús",
    resumen: "Consultas orientativas relacionadas con servicios de movilidad.",
    descripcion: "Se muestra cómo estructurar solicitudes de orientación y reportes de movilidad, con una navegación sencilla entre el catálogo y el detalle de servicio.",
    requisitos: ["Nombre o referencia de la ruta o medio de transporte.", "Fecha, horario aproximado y ubicación, cuando aplique.", "Explicación de la solicitud o incidencia."],
    pasos: ["Identifica el tipo de servicio de transporte.", "Recopila la información relevante para tu consulta.", "Verifica los canales de atención de la autoridad de movilidad competente."],
    nota: "Las rutas, horarios y disposiciones deben consultarse en fuentes oficiales actualizadas."
  },
  reciclaje: {
    titulo: "Reciclaje y residuos", imagen: "reciclaje.svg", alt: "Ícono de reciclaje",
    resumen: "Guía informativa de separación y recolección de residuos.",
    descripcion: "Este apartado representa un servicio municipal o local de orientación sobre reciclaje, separación de materiales y reportes relacionados con residuos.",
    requisitos: ["Tipo de material o residuo al que se refiere la consulta.", "Colonia o zona aproximada.", "Motivo de la solicitud y descripción del caso."],
    pasos: ["Distingue los materiales y la necesidad de atención.", "Consulta los lineamientos locales de separación.", "Ubica el canal oficial de recolección o recepción de residuos."],
    nota: "La clasificación de residuos y los calendarios de recolección varían según la localidad."
  },
  alumbrado: {
    titulo: "Alumbrado público", imagen: "alumbrado.svg", alt: "Ícono de una luminaria",
    resumen: "Datos de referencia para reportes de iluminación pública.",
    descripcion: "Demuestra cómo presentar una guía breve para describir fallas de alumbrado en calles, andadores o espacios de uso común.",
    requisitos: ["Referencia de calle o zona donde se ubica la luminaria.", "Descripción de la falla y horario aproximado en el que se detectó.", "Referencia física adicional, cuando sea necesaria."],
    pasos: ["Describe la incidencia de manera concreta.", "Anota un punto de referencia del lugar.", "Envía el reporte por el mecanismo oficial de atención ciudadana."],
    nota: "No es posible generar folios ni reportes oficiales desde este proyecto."
  },
  atencion: {
    titulo: "Atención ciudadana", imagen: "atencion.svg", alt: "Ícono de personas dialogando",
    resumen: "Ejemplo de orientación y solicitud de atención.",
    descripcion: "Este módulo ilustra la captura responsable de una consulta en un formulario, con etiquetas, validación del navegador y un mensaje de confirmación local.",
    requisitos: ["Asunto y explicación de la consulta.", "Servicio sobre el que se requiere orientación.", "Datos de prueba sin información personal sensible."],
    pasos: ["Selecciona el servicio de interés.", "Llena los campos marcados como obligatorios.", "Observa la confirmación en pantalla: la solicitud no se envía."],
    nota: "El formulario es una simulación sin conexión a una base de datos o servidor de correo."
  }
};

function agregarElementosLista(lista, elementos) {
  lista.replaceChildren();
  for (const texto of elementos) {
    const li = document.createElement("li");
    li.textContent = texto; // Evita interpretar entradas como HTML.
    lista.appendChild(li);
  }
}

function configurarPaginaDetalle() {
  const titulo = document.getElementById("detalle-titulo");
  if (!titulo) return;
  const codigo = new URLSearchParams(window.location.search).get("servicio");
  const servicio = Object.prototype.hasOwnProperty.call(SERVICIOS, codigo) ? SERVICIOS[codigo] : null;
  if (!servicio) {
    titulo.textContent = "Servicio no encontrado";
    document.getElementById("detalle-resumen").textContent = "El servicio solicitado no está disponible en esta demostración. Vuelve al catálogo para elegir una opción.";
    document.getElementById("detalle-descripcion").textContent = "No se encontró información para esta dirección.";
    document.getElementById("detalle-imagen").alt = "Ícono de atención ciudadana";
    document.getElementById("migaja-actual").textContent = "No encontrado";
    return;
  }
  titulo.textContent = servicio.titulo;
  document.title = `${servicio.titulo} | Portal de Servicios Ciudadanos`;
  document.getElementById("migaja-actual").textContent = servicio.titulo;
  document.getElementById("detalle-resumen").textContent = servicio.resumen;
  document.getElementById("detalle-descripcion").textContent = servicio.descripcion;
  document.getElementById("detalle-nota").textContent = servicio.nota;
  const imagen = document.getElementById("detalle-imagen");
  imagen.src = `${servicio.imagen}`;
  imagen.alt = servicio.alt;
  agregarElementosLista(document.getElementById("detalle-requisitos"), servicio.requisitos);
  agregarElementosLista(document.getElementById("detalle-pasos"), servicio.pasos);
}

function configurarBusqueda() {
  const campo = document.getElementById("buscar-servicio");
  if (!campo) return;
  const tarjetas = Array.from(document.querySelectorAll(".tarjeta-servicio"));
  const resultados = document.getElementById("resultados-busqueda");
  const vacio = document.getElementById("sin-resultados");
  campo.addEventListener("input", () => {
    const consulta = campo.value.trim().toLocaleLowerCase("es");
    let visibles = 0;
    tarjetas.forEach(tarjeta => {
      const texto = `${tarjeta.dataset.nombre} ${tarjeta.textContent}`.toLocaleLowerCase("es");
      const coincide = texto.includes(consulta);
      tarjeta.hidden = !coincide;
      if (coincide) visibles++;
    });
    resultados.textContent = `${visibles} ${visibles === 1 ? "servicio disponible" : "servicios disponibles"} en esta guía.`;
    vacio.hidden = visibles !== 0;
  });
}

function configurarFormulario() {
  const formulario = document.getElementById("formulario-contacto");
  if (!formulario) return;
  const respuesta = document.getElementById("respuesta-formulario");
  formulario.addEventListener("submit", evento => {
    evento.preventDefault(); // No hay servidor, correo o guardado de datos.
    if (!formulario.reportValidity()) return;
    const servicio = document.getElementById("servicio-contacto").value;
    respuesta.hidden = false;
    respuesta.textContent = `Demostración realizada: se validó una consulta de ${servicio}. No se envió información ni se generó una cita real.`;
    formulario.reset();
    respuesta.focus();
  });
}

configurarPaginaDetalle();
configurarBusqueda();
configurarFormulario();
