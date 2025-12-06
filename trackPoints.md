# Track Completed Points

Jegy 	Pont
5 	    80-100
4 	    67-79
3 	    54-66

- [X] BASE;24
- [] LANG2;5
- [] NOERR;5
- [] CACHE;5
- [X] HELM;10
- [X] K8SJOB;5
- [X] K8SCRONJOB;5      TODO: HOZZAADNI A CSV-HEZ!
- [X] K8SCMAP;5
- [X] K8SSECRET;3
- [X] K8SNS;7
- [] CICD;10
- [X] GW;5-10
- [X] CONTRIB;2
- [] Sum;86

24+10+3*5+3+7+5+2=66

{LANG2} Több programozási nyelv használata. A backend szolgáltatások legalább két különböző programozási nyelven készültek. (A frontend ebbe nem számít bele!): 5 pont

{NOERR} Hibatűrést növelő kommunikációs minták alkalmazása külső komponensek segítségével (pl. Polly, Resilience4j, Tenacity). 5 pont

{CACHE} Saját telepítésű (pl. Redis konténer) használata kifejezetten gyorsítótárazásra legalább egy művelet esetén: 5 pont

{HELM} A szolgáltatás Kubernetesen belül futó része Helm chart-on keresztül telepíthető. Szükséges demonstrálni a rendszer frissítését a chart segítségével: 10 pont

{K8SJOB} Kubernetes Job objektum használata, lefuttatása védéskor: 5 pont

{K8SCRONJOB} Kubernetes CronJob objektum használata, korábbi lefutás demonstrálása védéskor: 5 pont

{K8SCMAP} Kubernetes ConfigMap objektum használata valamely konfigurációs beállítás tárolására: 5 pont

{K8SSECRET} Kubernetes Secret objektum használata titok tárolására: 3 pont

{K8SNS} Több példány (verzió) telepítése ugyanabba a környezetbe K8S namespace-ek vagy Azure Function deployment slot-ok használatával. Azure Container Apps platform esetén külön Container Apps példány használható: 7 pont

{CICD} CI/CD folyamat implementálása valamely elterjedt DevOps eszközre építve (GitHub Actions, Azure DevOps). Git push-ra a backend új verziója felépül és kitelepül: 10-15 pont

    egy platformra telepít: 10 pont
    két platformra telepít 15 pont

{GW} Saját telepítésű (API/App) gateway használata. Kivéve self-hosted Azure API Management. 5-10 pont
    Traefik használata útvonalválasztásra: 5 pont
    Más, saját telepítésű (API/App) gateway használata: 10 pont

{CONTRIB} Visszacsatolás. A véglegesített pontrendszer vagy tananyag javítása, bővítése, módosítása pull request-tel. Helyesírási hiba is lehet, de az oktatók döntenek, hogy pontot ér-e a módosítás. Többször is megszerezhető. 0-2 pont, összesen max. 6 pont.
