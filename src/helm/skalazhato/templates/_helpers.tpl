{{- define "skalazhato.recipe-service.labelSelector" -}}
app: recipe-service
release: {{ .Release.Name }}
chart: {{ .Chart.Name }}
environment: {{ .Values.common.environment }}
{{- end -}}

{{- define "skalazhato.mealplan-service.labelSelector" -}}
app: mealplan-service
release: {{ .Release.Name }}
chart: {{ .Chart.Name }}
environment: {{ .Values.common.environment }}
{{- end -}}

{{- define "skalazhato.recipe-service.hpa.minReplicas" -}}
{{ max .Values.recipeService.replicaCount .Values.recipeService.horizontalScaler.minReplicas }}
{{- end -}}
