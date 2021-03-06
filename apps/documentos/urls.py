from django.conf.urls import url
from .views import (AnotacionGeneralView, AnotacionView, TerminarDocumentoView,
                    OracionViewSet, ParrafoViewSet, TAGSLeyesViewSet,
                    AnotacionViewSet, TAGPersonalViewSet, RevisionGeneralView, RevisionView, # despues de esta son mios
                    asigna_anotaciones_Bloque,asigna_Anotacion,
                    asigna_Revision,asigna_Revisiones,asigna_Revisiones_Auto,
                    revision,
                    anotacion_Parrafo,
                    estadisticas_Usuario,concordancia_Usuarios,
                    registro_Actividad,registro_Actividad_Administra_Revision,registro_Actividad_Administra_Etiquetado,
                    consulta_Documentos_Parrafo,)
from .cbv import (registra_Ley,lista_Leyes,actualiza_Ley,
					registra_Etiqueta,proponer_Etiqueta,lista_Etiquetas,lista_Etiquetas_Propuestas,actualiza_Etiqueta,elimina_Etiqueta,
					registra_Parrafos,registra_Parrafo,detalles_Parrafo,lista_Parrafos_Leyes,lista_Parrafos_Ley,actualiza_Parrafo,elimina_Parrafo,
					asigna_Anotacion_Leyes,lista_Anotaciones_Leyes,lista_Anotaciones_Ley,actualiza_Anotacion,elimina_Anotacion,
					asigna_Revision_Leyes,asigna_Revision_Ley,lista_Revisiones_Leyes,lista_Revisiones_Ley,actualiza_Revision,elimina_Revision,asigna_Revision_Usuarios,asigna_Revision_Usuario,
					anotacion_Leyes,anotacion_Ley,
					revision_Leyes,revision_Ley,
					descripcion_etiquetas,descripcion_etiqueta,
					estadisticas_Usuarios,
					registro_Actividad_Parrafos,registro_Actividad_Anotaciones,registro_Actividad_Revisiones,registro_Actividad_Administra_Parrafo,registro_Actividad_Administra_Anotacion,registro_Actividad_Elimina_Parrafo,registro_Actividad_Elimina_Anotacion,registro_Actividad_Elimina_Revision,registro_Actividad_Elimina_Etiquetado,
					consulta_Documentos,consulta_Documentos_Ley,consulta_Documentos_Titulo,consulta_Documentos_Capitulo,consulta_Documentos_Base,consulta_Documentos_Apartado,consulta_Documentos_Articulo,consulta_Documentos_Fraccion,consulta_Documentos_Inciso,)
guardar_anotacion = OracionViewSet.as_view({'post':'create'})
terminar_parrafo = ParrafoViewSet.as_view({'patch':'update'})
guardar_argumentacion_1 = ParrafoViewSet.as_view({'post':'guardar_argumentacion'})
terminar_anotacion = AnotacionViewSet.as_view({'patch':'update'})
listado_leyes = TAGSLeyesViewSet.as_view({'get':'list'})
tag_personal = TAGPersonalViewSet.as_view({'post':'create'})
documentos_urls = [
    url(r'^anotacion/(?P<anotacion_id>\d+)$', AnotacionGeneralView, name='anotacion-general'),
    url(r'^anotacion/(?P<anotacion_id>\d+)/parrafo/(?P<parrafo_id>\d+)$', AnotacionView, name='anotacion-especifica'),
    url(r'^anotacion/(?P<id>\d+)/complete$', TerminarDocumentoView, name='terminar_documento'),
    url(r'^anotacion/(?P<pk>\d+)/terminar$', terminar_anotacion, name='terminar_anotacion'),
    url(r'^guardar-anotacion', guardar_anotacion, name='guardar-anotacion'),
    url(r'^parrafo/(?P<pk>\d+)/guardar-argumentacion', guardar_argumentacion_1, name='guardar-argumentacion-1'),
    url(r'^parrafo/(?P<pk>\d+)', terminar_parrafo, name='terminar_parrafo'),
    url(r'^crear-tag', tag_personal, name='crear-tag'),
    url(r'^lista-leyes', listado_leyes, name='lista-leyes'),
    url(r'^lista-leyes', listado_leyes, name='lista-leyes'),
    url(r'^revision/(?P<anotacion_id>\d+)$', RevisionGeneralView, name='revision-general'),
    url(r'^revision/(?P<anotacion_id>\d+)/parrafo/(?P<parrafo_id>\d+)$', RevisionView, name='revision-especifica'),
	url(r'^registra_ley$', registra_Ley.as_view(success_url="/registra_ley"), name='registra_ley'),
	url(r'^administra_leyes$', lista_Leyes.as_view(), name='administra_leyes'),
	url(r'^administra_ley_(?P<pk>\d+)$', actualiza_Ley.as_view(success_url="/administra_leyes"), name='administra_ley'),
	url(r'^asigna_anotacion_leyes$', asigna_Anotacion_Leyes.as_view(), name='asigna_anotacion_leyes'),
	url(r'^asigna_anotaciones_bloque_(?P<pk>\d+)$', asigna_anotaciones_Bloque, name='asigna_anotaciones_bloque'),
	url(r'^asigna_anotacion_ley_(?P<pk>\d+)$', asigna_Anotacion, name='asigna_anotacion_ley'),
	url(r'^administra_anotaciones_leyes$', lista_Anotaciones_Leyes.as_view(), name='administra_anotaciones_leyes'),
	url(r'^administra_anotacion_ley_(?P<pk>\d+)$', lista_Anotaciones_Ley.as_view(), name='administra_anotaciones_ley'),
	url(r'^administra_anotacion_(?P<pk>\d+)$', actualiza_Anotacion.as_view(success_url="/administra_anotaciones_leyes"), name='administra_anotacion'),
	url(r'^elimina_anotacion_(?P<pk>\d+)$', elimina_Anotacion.as_view(success_url="/administra_anotaciones_leyes"), name='elimina_anotacion'),
	url(r'^asigna_revisiones$', asigna_Revisiones, name='asigna_revisiones'),
	url(r'^asigna_revisiones_auto$', asigna_Revisiones_Auto, name='asigna_revisiones_auto'),
	url(r'^asigna_revision_leyes$', asigna_Revision_Leyes.as_view(), name='asigna_revision_leyes'),
	url(r'^asigna_revision_ley_(?P<pk>\d+)$', asigna_Revision_Ley.as_view(), name='asigna_revision_ley'),
	url(r'^asigna_revision_usuarios$', asigna_Revision_Usuarios.as_view(), name='asigna_revision_usuarios'),
	url(r'^asigna_revision_usuario_(?P<pk>\d+)$', asigna_Revision_Usuario.as_view(), name='asigna_revision_usuario'),
	url(r'^asigna_revision_(?P<pk>\d+)$', asigna_Revision, name='asigna_revision'),
	url(r'^administra_revisiones_leyes$', lista_Revisiones_Leyes.as_view(), name='administra_revisiones_leyes'),
	url(r'^administra_revisiones_ley_(?P<pk>\d+)$', lista_Revisiones_Ley.as_view(), name='administra_revisiones_ley'),
	url(r'^administra_revision_(?P<pk>\d+)$', actualiza_Revision.as_view(success_url="/administra_revisiones_leyes"), name='administra_revision'),
	url(r'^elimina_revision_(?P<pk>\d+)$', elimina_Revision.as_view(success_url="/administra_revisiones_leyes"), name='elimina_revision'),
	url(r'^registra_etiqueta$', registra_Etiqueta.as_view(success_url="/registra_etiqueta"), name='registra_etiqueta'),
	url(r'^proponer_etiqueta$', proponer_Etiqueta.as_view(success_url="/proponer_etiqueta"), name='proponer_etiqueta'),
	url(r'^administra_etiquetas$', lista_Etiquetas.as_view(), name='administra_etiquetas'),
	url(r'^administra_etiquetas_propuestas$', lista_Etiquetas_Propuestas.as_view(), name='administra_etiquetas'),
	url(r'^administra_etiqueta_(?P<pk>\d+)$', actualiza_Etiqueta.as_view(success_url="/administra_etiquetas"), name='administra_etiqueta'),
	url(r'^elimina_etiqueta_(?P<pk>\d+)$', elimina_Etiqueta.as_view(success_url="/administra_etiquetas"), name='elimina_etiqueta'),
	url(r'^registra_parrafos$', registra_Parrafos.as_view(), name='registra_parrafos'),
	url(r'^registra_parrafo_ley_(?P<pk>\d+)$', registra_Parrafo.as_view(), name='registra_parrafo'),
	url(r'^detalles_parrafo_(?P<pk>\d+)$', detalles_Parrafo.as_view(), name='detalles_parrafo'),
	url(r'^administra_parrafos_leyes$', lista_Parrafos_Leyes.as_view(), name='administra_parrafos_leyes'),
	url(r'^administra_parrafos_ley_(?P<pk>\d+)$', lista_Parrafos_Ley.as_view(), name='administra_parrafos_ley'),
	url(r'^administra_parrafo_(?P<pk>\d+)$', actualiza_Parrafo.as_view(success_url="/administra_parrafos_leyes"), name='administra_parrafo'),
	url(r'^elimina_parrafo_(?P<pk>\d+)$', elimina_Parrafo.as_view(success_url="/administra_parrafos_leyes"), name='elimina_parrafo'),
	url(r'^anota_leyes$', anotacion_Leyes.as_view(), name='anota_leyes'),
	url(r'^anota_ley_(?P<pk>\d+)$', anotacion_Ley.as_view(), name='anota_ley'),
	url(r'^anota_parrafo_(?P<pk>\d+)$', anotacion_Parrafo, name='anota_parrafo'),
	url(r'^descripcion_etiquetas$', descripcion_etiquetas.as_view(), name='descripcion_etiquetas'),
	url(r'^descripcion_etiqueta_(?P<pk>\d+)$', descripcion_etiqueta.as_view(), name='descripcion_etiqueta'),
	url(r'^revisa_leyes$', revision_Leyes.as_view(), name='revisa_leyes'),
	url(r'^revisa_ley_(?P<pk>\d+)$', revision_Ley.as_view(), name='revisa_ley'),
	url(r'^revision_(?P<pk>\d+)$', revision, name='revision'),
	url(r'^estadisticas_usuarios$', estadisticas_Usuarios.as_view(), name='estadisticas_usuarios'),
	url(r'^estadisticas_usuario_(?P<pk>\d+)$', estadisticas_Usuario, name='estadisticas_usuario'),
	url(r'^concordancia_usuarios_(?P<pk1>\d+)_(?P<pk2>\d+)$', concordancia_Usuarios, name='concordancia_usuarios'),
	url(r'^registro_actividad$', registro_Actividad, name='registro_actividad'),
	url(r'^registro_actividad/parrafos$', registro_Actividad_Parrafos.as_view(), name='registro_actividad_parrafos'),
	url(r'^registro_actividad/administra_parrafo_(?P<pk>\d+)$', registro_Actividad_Administra_Parrafo.as_view(success_url="/registro_actividad_parrafos"), name='registro_actividad_administra_parrafo'),
	url(r'^registro_actividad/elimina_parrafo_(?P<pk>\d+)$', registro_Actividad_Elimina_Parrafo.as_view(success_url="/registro_actividad_parrafos"), name='registro_actividad_elimina_parrafo'),
	url(r'^registro_actividad/anotaciones$', registro_Actividad_Anotaciones.as_view(), name='registro_actividad_anotaciones'),
	url(r'^registro_actividad/administra_anotacion_(?P<pk>\d+)$', registro_Actividad_Administra_Anotacion.as_view(), name='registro_actividad_administra_anotacion'),
	url(r'^registro_actividad/elimina_anotacion_(?P<pk>\d+)$', registro_Actividad_Elimina_Anotacion.as_view(success_url="/registro_actividad_anotaciones"), name='registro_actividad_elimina_anotacion'),
	url(r'^registro_actividad/administra_etiquetado_(?P<pk>\d+)$', registro_Actividad_Administra_Etiquetado, name='registro_actividad_administra_etiquetado'),
	url(r'^registro_actividad/elimina_etiquetado_(?P<pk>\d+)$', registro_Actividad_Elimina_Etiquetado.as_view(success_url="/registro_actividad_anotaciones"), name='registro_actividad_elimina_etiquetado'),
	url(r'^registro_actividad/revisiones$', registro_Actividad_Revisiones.as_view(), name='registro_actividad_revisiones'),
	url(r'^registro_actividad/administra_revision_(?P<pk>\d+)$', registro_Actividad_Administra_Revision, name='registro_actividad_administra_revision'),
	url(r'^registro_actividad/elimina_revision_(?P<pk>\d+)$', registro_Actividad_Elimina_Revision.as_view(success_url="/registro_actividad_revisiones"), name='registro_actividad_elimina_revision'),
	url(r'^consulta_documentos$', consulta_Documentos.as_view(), name='consulta_documentos'),
	url(r'^consulta_documentos/ley_(?P<pk>\d+)$', consulta_Documentos_Ley.as_view(), name='consulta_documentos_ley'),
	url(r'^consulta_documentos/titulo_(?P<pk>\d+)$', consulta_Documentos_Titulo.as_view(), name='consulta_documentos_titulo'),
	url(r'^consulta_documentos/capitulo_(?P<pk>\d+)$', consulta_Documentos_Capitulo.as_view(), name='consulta_documentos_capitulo'),
	url(r'^consulta_documentos/base_(?P<pk>\d+)$', consulta_Documentos_Base.as_view(), name='consulta_documentos_base'),
	url(r'^consulta_documentos/apartado_(?P<pk>\d+)$', consulta_Documentos_Apartado.as_view(), name='consulta_documentos_apartado'),
	url(r'^consulta_documentos/articulo_(?P<pk>\d+)$', consulta_Documentos_Articulo.as_view(), name='consulta_documentos_articulo'),
	url(r'^consulta_documentos/fraccion_(?P<pk>\d+)$', consulta_Documentos_Fraccion.as_view(), name='consulta_documentos_fraccion'),
	url(r'^consulta_documentos/inciso_(?P<pk>\d+)$', consulta_Documentos_Inciso.as_view(), name='consulta_documentos_inciso'),
	url(r'^consulta_documentos/parrafo_(?P<pk>\d+)$', consulta_Documentos_Parrafo, name='consulta_documentos_parrafo'),
]
