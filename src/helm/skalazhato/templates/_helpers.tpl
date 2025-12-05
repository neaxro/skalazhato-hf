{{- define "skalazhato.recipe-service.labelSelector" -}}
app: recipe-service
environment: {{ .Values.common.environment }}
{{- end -}}

