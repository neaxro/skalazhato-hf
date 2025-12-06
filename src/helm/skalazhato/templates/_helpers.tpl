{{- define "skalazhato.recipe-service.labelSelector" -}}
app: recipe-service
environment: {{ .Values.common.environment }}
{{- end -}}

{{- define "skalazhato.recipe-service.hpa.minReplicas" -}}
{{ max .Values.recipeService.replicaCount .Values.recipeService.horizontalScaler.minReplicas }}
{{- end -}}
