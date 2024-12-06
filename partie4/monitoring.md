# **Monitoring et Alertes**


## **Log Analytics Workspace**


Creation de la ressource `Logs Analytics Workspace` dans mon groupe de ressource.
![log analytics workspace](01_log_analytics_workspace/ressource_log_analytics_w.png)

Capture du parametrage pour remonter les logs du `keyvault` dans le `Logs Analytics Workspace`.
![param log keyvault](01_log_analytics_workspace/param_log_keyvault.png)

Il faut effectuer ce parametrage sur les differentes ressources dont on veut remonter les logs dans le `Logs Analytics Workspace`. On peut visualiser ce parametrage  dans le groupe de ressource dans *Monitoring>Diagnostic settings*.
![diagnostic settings](01_log_analytics_workspace/diagnostic_setting.png)

On peut egalement visualiser les tables de logs qui sont crées dans le `Logs Analytics Workspace`. On pourra par la suite requeter ces tables.
![log table](01_log_analytics_workspace/log_table.png)


## **Metrics**


## **Insights**


## **Alerts**


Creation d `Alerts` dans le groupe de ressource dans *Monitoring>Alerts*.
![description](04_alerts/ressource_alerte.png)

Paramétrage d une alerte sur une `métrique`. 
![description](04_alerts/ingress_1G.png)

Paramétrage d une alerte sur les `Activity Logs`
![description](04_alerts/key_regen.png)

Paramétrage de la `gravité` d une alerte.
![config gravite](04_alerts/ex_config_gravite.png)

Creation d un `groupe d action` avec un mode de notification (sms, mail, ...) à attribuer à une alerte.
![description](04_alerts/action_group.png)