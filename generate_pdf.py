#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar PDF de documentación CI/CD
Museo de Dinosaurios FastAPI
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from datetime import datetime

# Configuración de estilos
styles = getSampleStyleSheet()

# Estilos personalizados
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#1a4d2e'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#2d6a4f'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#40916c'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    leading=16
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontSize=9,
    fontName='Courier',
    textColor=colors.HexColor('#555555'),
    leftIndent=20,
    rightIndent=20,
    spaceAfter=10,
    backColor=colors.HexColor('#f0f0f0')
)

def create_pdf():
    """Crea el PDF de documentación CI/CD"""
    
    filename = "CI_CD_Documentation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    # ============ PORTADA ============
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("🦖 Museo de Dinosaurios", title_style))
    story.append(Paragraph("FastAPI", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("CI/CD & DevOps", heading1_style))
    story.append(Paragraph("Pipeline de Integración Continua", styles['Normal']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
    story.append(Paragraph("<b>Versión:</b> 1.0", styles['Normal']))
    story.append(PageBreak())
    
    # ============ TABLA DE CONTENIDOS ============
    story.append(Paragraph("Tabla de Contenidos", heading1_style))
    toc_items = [
        "1. Introducción a DevOps",
        "2. Arquitectura CI/CD",
        "3. Docker - Containerización",
        "4. GitHub Actions - Pipeline",
        "5. Flujo de Trabajo",
        "6. Despliegue Automático",
        "7. Monitoreo y Mantenimiento",
        "8. Troubleshooting",
    ]
    for item in toc_items:
        story.append(Paragraph(item, normal_style))
    story.append(PageBreak())
    
    # ============ 1. INTRODUCCIÓN ============
    story.append(Paragraph("1. Introducción a DevOps", heading1_style))
    story.append(Paragraph(
        "DevOps es una metodología que combina desarrollo (Dev) y operaciones (Ops). "
        "Su objetivo es automatizar y optimizar el ciclo de vida del software, desde el desarrollo "
        "hasta la producción. En esta aplicación, hemos implementado un pipeline CI/CD completo "
        "que garantiza calidad, seguridad y velocidad de entrega.",
        normal_style
    ))
    
    story.append(Paragraph("Beneficios de CI/CD:", heading2_style))
    benefits = [
        "✅ <b>Automatización:</b> Eliminación de tareas manuales",
        "✅ <b>Calidad:</b> Tests automáticos en cada cambio",
        "✅ <b>Velocidad:</b> Despliegues más rápidos",
        "✅ <b>Confiabilidad:</b> Menos errores en producción",
        "✅ <b>Trazabilidad:</b> Registro completo de cambios",
        "✅ <b>Seguridad:</b> Análisis automático de vulnerabilidades",
    ]
    for benefit in benefits:
        story.append(Paragraph(benefit, normal_style))
    story.append(PageBreak())
    
    # ============ 2. ARQUITECTURA ============
    story.append(Paragraph("2. Arquitectura CI/CD", heading1_style))
    story.append(Paragraph(
        "La arquitectura implementada se compone de varios componentes que trabajan en conjunto:",
        normal_style
    ))
    
    story.append(Paragraph("Componentes Principales:", heading2_style))
    
    # Tabla de componentes
    components_data = [
        ["Componente", "Función", "Tecnología"],
        ["Control de Versiones", "Gestionar código fuente", "Git / GitHub"],
        ["CI/CD", "Automatizar pipeline", "GitHub Actions"],
        ["Containerización", "Empaquetar aplicación", "Docker"],
        ["Registro", "Almacenar imágenes", "Docker Hub"],
        ["Deployment", "Desplegar aplicación", "Docker / Cloud"],
    ]
    
    t = Table(components_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d6a4f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # ============ 3. DOCKER ============
    story.append(Paragraph("3. Docker - Containerización", heading1_style))
    story.append(Paragraph(
        "Docker es una plataforma que permite empaquetar la aplicación y todas sus dependencias "
        "en un contenedor, garantizando que funcione igual en desarrollo, testing y producción.",
        normal_style
    ))
    
    story.append(Paragraph("Dockerfile Multi-stage:", heading2_style))
    story.append(Paragraph(
        "Utilizamos un Dockerfile con dos etapas para optimizar el tamaño final de la imagen:",
        normal_style
    ))
    
    story.append(Paragraph("<b>Stage 1: Builder</b>", heading2_style))
    builder_points = [
        "• Imagen base: python:3.11-slim",
        "• Instala dependencias necesarias",
        "• Compila las librerías Python",
        "• Limpia archivos innecesarios",
    ]
    for point in builder_points:
        story.append(Paragraph(point, normal_style))
    
    story.append(Paragraph("<b>Stage 2: Runtime</b>", heading2_style))
    runtime_points = [
        "• Copia solo lo necesario del builder",
        "• Crea usuario no-root para mayor seguridad",
        "• Variables de entorno optimizadas",
        "• Health check configurado",
    ]
    for point in runtime_points:
        story.append(Paragraph(point, normal_style))
    
    story.append(Paragraph("<b>Ventajas:</b>", heading2_style))
    advantages = [
        "✅ Menor tamaño final (eliminamos herramientas de compilación)",
        "✅ Mayor seguridad (usuario no-root)",
        "✅ Mejor rendimiento",
        "✅ Cacheo eficiente de capas",
    ]
    for adv in advantages:
        story.append(Paragraph(adv, normal_style))
    story.append(PageBreak())
    
    # ============ 4. GITHUB ACTIONS ============
    story.append(Paragraph("4. GitHub Actions - Pipeline", heading1_style))
    story.append(Paragraph(
        "GitHub Actions es un servicio de integración continua integrado en GitHub. "
        "Ejecuta automáticamente tareas cuando ocurren eventos (push, pull request, etc.).",
        normal_style
    ))
    
    story.append(Paragraph("Jobs del Pipeline:", heading2_style))
    
    # Job 1
    story.append(Paragraph("<b>Job 1: Test</b>", heading2_style))
    job1_tasks = [
        "1. Checkout del código",
        "2. Setup Python 3.11",
        "3. Instala dependencias",
        "4. Ejecuta linting (Flake8)",
        "<b>Trigger:</b> En cada push o pull request",
        "<b>Obligatorio:</b> Sí (debe pasar para continuar)",
    ]
    for task in job1_tasks:
        story.append(Paragraph(task, normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Job 2
    story.append(Paragraph("<b>Job 2: Docker Build & Push</b>", heading2_style))
    job2_tasks = [
        "1. Setup Docker Buildx (herramienta de build mejorada)",
        "2. Login a Docker Hub",
        "3. Build imagen Docker",
        "4. Push a Docker Hub",
        "<b>Trigger:</b> Solo después de pasar tests",
        "<b>Solo en:</b> Push a main/develop (no en PRs)",
        "<b>Resultado:</b> Imagen disponible en Docker Hub",
    ]
    for task in job2_tasks:
        story.append(Paragraph(task, normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Job 3
    story.append(Paragraph("<b>Job 3: Notifications</b>", heading2_style))
    job3_tasks = [
        "1. Verifica estado de todos los jobs anteriores",
        "2. Notifica resultado final del pipeline",
        "<b>Útil para:</b> Alertas por email, Slack, etc.",
    ]
    for task in job3_tasks:
        story.append(Paragraph(task, normal_style))
    
    story.append(PageBreak())
    
    # ============ 5. FLUJO DE TRABAJO ============
    story.append(Paragraph("5. Flujo de Trabajo Completo", heading1_style))
    
    flow_steps = [
        "1. <b>Desarrollador</b> realiza cambios en el código",
        "2. <b>Git push</b> a GitHub (a rama main o develop)",
        "3. <b>GitHub detecta</b> el event (push) y dispara el workflow",
        "4. <b>Job Test</b> se ejecuta (validación de código)",
        "5. Si test <b>FALLA</b>: Pipeline se detiene, notifica error",
        "6. Si test <b>PASA</b>: Continúa al siguiente job",
        "7. <b>Job Build & Push</b> construye imagen Docker",
        "8. <b>Sube a Docker Hub</b> la imagen con tags automáticos",
        "9. <b>Job Notifications</b> notifica resultado final",
        "10. <b>Imagen disponible</b> para despliegue en producción",
    ]
    for step in flow_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Diagrama de Flujo:", heading2_style))
    
    diagram = """
    <font name="Courier" size="9">
    ┌─────────────┐<br/>
    │  Developer  │<br/>
    │   Pushes    │<br/>
    └──────┬──────┘<br/>
           │<br/>
           ▼<br/>
    ┌──────────────────┐<br/>
    │  GitHub Actions  │<br/>
    │   Triggered      │<br/>
    └──────┬───────────┘<br/>
           │<br/>
           ├──→ ┌──────────────────────┐ PASS ┌─────────────────┐<br/>
           │    │   TEST JOB          │─────→│  DOCKER BUILD   │<br/>
           │    │ (Lint, Tests)       │      │  & PUSH         │<br/>
           │    └──────────────────────┘ FAIL │                 │<br/>
           │         │                        └────────┬────────┘<br/>
           │         └───────────────────→ STOP        │<br/>
           │                                           ▼<br/>
           └───────────────────────────→ ┌───────────────────────┐<br/>
                                         │   Docker Hub  <br/>
                                         │   Image Stored<br/>
                                         └───────────────────────┘<br/>
    </font>
    """
    story.append(Paragraph(diagram, code_style))
    story.append(PageBreak())
    
    # ============ 6. DESPLIEGUE ============
    story.append(Paragraph("6. Despliegue Automático", heading1_style))
    
    story.append(Paragraph("Tagging Strategy:", heading2_style))
    story.append(Paragraph(
        "Las imágenes Docker se tagean automáticamente según la rama:",
        normal_style
    ))
    
    tags_data = [
        ["Tag", "Cuándo", "Ejemplo"],
        ["latest", "Rama main", "usuario/museo:latest"],
        ["develop", "Rama develop", "usuario/museo:develop"],
        ["rama-nombre", "Cualquier rama", "usuario/museo:feature-x"],
        ["main-sha", "Commit hash", "usuario/museo:main-a1b2c3d"],
    ]
    
    t_tags = Table(tags_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    t_tags.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d6a4f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(t_tags)
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Opciones de Deploy:", heading2_style))
    story.append(Paragraph("<b>Opción 1: Docker Hub (Recomendado)</b>", heading2_style))
    option1 = [
        "• Imagen se pushea automáticamente",
        "• Cualquiera puede descargarla",
        "• Bajo costo (gratuito para públicas)",
        "• Comando: docker pull usuario/museo:latest",
    ]
    for opt in option1:
        story.append(Paragraph(opt, normal_style))
    
    story.append(Paragraph("<b>Opción 2: Heroku</b>", heading2_style))
    option2 = [
        "• Deploy automático desde GitHub",
        "• Gratuito (con limitaciones)",
        "• Ideal para prototipo",
    ]
    for opt in option2:
        story.append(Paragraph(opt, normal_style))
    
    story.append(Paragraph("<b>Opción 3: AWS/Google Cloud</b>", heading2_style))
    option3 = [
        "• Máxima escalabilidad",
        "• Requiere configuración adicional",
        "• Costo variable según uso",
    ]
    for opt in option3:
        story.append(Paragraph(opt, normal_style))
    
    story.append(PageBreak())
    
    # ============ 7. MONITOREO ============
    story.append(Paragraph("7. Monitoreo y Mantenimiento", heading1_style))
    
    story.append(Paragraph("Verificar ejecución del Pipeline:", heading2_style))
    steps = [
        "1. Ir a GitHub → Tu repositorio → Actions",
        "2. Seleccionar el workflow 'FastAPI CI/CD Pipeline'",
        "3. Ver logs detallados de cada job",
        "4. Descargar artefactos si es necesario",
    ]
    for step in steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Métricas Importantes:", heading2_style))
    metrics = [
        "✅ Tasa de éxito de tests (ideal: 100%)",
        "📦 Tamaño de imagen Docker (menor es mejor)",
        "⏱️ Tiempo de ejecución del pipeline (< 10 min ideal)",
        "🔐 Auditoría de cambios (quién, qué, cuándo)",
        "🚀 Frecuencia de despliegues",
    ]
    for metric in metrics:
        story.append(Paragraph(metric, normal_style))
    
    story.append(PageBreak())
    
    # ============ 8. TROUBLESHOOTING ============
    story.append(Paragraph("8. Troubleshooting", heading1_style))
    
    issues = [
        ("El workflow no se ejecuta", [
            "• Revisar sintaxis del archivo YAML (validar en yamllint.com)",
            "• Verificar que el archivo esté en .github/workflows/",
            "• Confirmar que el trigger (push/PR) sea correcto",
        ]),
        ("Docker build falla", [
            "• Verificar que Dockerfile sea válido",
            "• Probar build localmente: docker build -t test .",
            "• Revisar logs en GitHub Actions",
        ]),
        ("Login a Docker Hub falla", [
            "• Verificar secrets configurados en GitHub Settings",
            "• Revisar que token no esté expirado",
            "• Regenerar token en Docker Hub si es necesario",
        ]),
        ("Imagen muy grande", [
            "• Usar multi-stage Dockerfile (ya implementado)",
            "• Limpiar archivos innecesarios",
            "• Usar imagen base más pequeña (python:3.11-slim)",
        ]),
    ]
    
    for issue, solutions in issues:
        story.append(Paragraph(f"<b>Problema: {issue}</b>", heading2_style))
        for solution in solutions:
            story.append(Paragraph(solution, normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # ============ CONCLUSIÓN ============
    story.append(Paragraph("Conclusión", heading1_style))
    story.append(Paragraph(
        "El pipeline CI/CD implementado proporciona una base sólida para el desarrollo, "
        "testing y despliegue automático de la aplicación. Permite a los equipos ser más "
        "productivos, garantiza la calidad del código y reduce significativamente el tiempo "
        "entre desarrollo e implementación en producción.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Checklist de Implementación:", heading2_style))
    checklist = [
        "☑ Dockerfile multi-stage creado",
        "☑ docker-compose.yml configurado",
        "☑ .gitignore y .dockerignore creados",
        "☑ GitHub Actions workflow configurado",
        "☑ Documentación DevOps completada",
        "☑ Secrets configurados en GitHub (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN)",
        "☑ Primer push a GitHub realizado",
        "☑ Workflow ejecutado exitosamente",
        "☑ Imagen subida a Docker Hub",
    ]
    for item in checklist:
        story.append(Paragraph(item, normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        f"<b>Documento generado:</b> {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}",
        styles['Normal']
    ))
    
    # Construir PDF
    doc.build(story)
    print(f"PDF generado: {filename}")

if __name__ == "__main__":
    create_pdf()
