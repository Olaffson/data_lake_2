## **Veille sur les systèmes de securité**

### **1. Storage Access Keys**
Description : Ce sont des clés secrètes (Primary et Secondary Keys) générées pour accéder à un compte de stockage Azure. Elles permettent un contrôle total sur les ressources du compte de stockage (Data Lake inclus).
Usage principal : Fournir un moyen simple mais puissant d’accès pour des applications ou des scripts.
Limite : Manque de granularité et risque élevé en cas de compromission (pas d’expiration).

### **2. Shared Access Signatures (SAS) (Delegation Key)**
Description : Une SAS est un jeton temporaire qui accorde un accès limité et granulaire aux ressources Azure Storage. Il peut spécifier la durée de validité, les permissions (lecture/écriture/liste), et les IP autorisées.
Usage principal : Partager des ressources avec des utilisateurs externes ou applications de manière sécurisée.
Avantage : Meilleure granularité et sécurité qu’une clé d’accès, avec expiration intégrée.

### **3. Microsoft Entra ID (anciennement Azure Active Directory)**
Description : Plateforme d’identités sécurisée pour gérer les accès basés sur des identités (utilisateurs, groupes, ou applications). Elle repose sur des concepts comme le Service Principal pour autoriser les applications à interagir avec des services Azure.
Usage principal : Contrôle d’accès basé sur l’identité avec authentification forte et gestion centralisée.
Avantage : Intégration native avec d’autres services Azure et prise en charge des protocoles sécurisés (OAuth2, OpenID Connect).

### **4. Azure Key Vault**
Description : Service de gestion de secrets, clés et certificats. Il centralise et sécurise le stockage des clés d’accès, mots de passe, et autres secrets critiques nécessaires pour protéger les ressources Azure.
Usage principal : Protéger les secrets et permettre leur intégration sécurisée avec des applications et services.
Avantage : Protection renforcée grâce à un chiffrement matériel (HSM).

### **5. IAM et Role-Based Access Control (RBAC)**
Description : IAM (Identity and Access Management) sur Azure repose sur RBAC, un modèle qui attribue des rôles prédéfinis ou personnalisés aux utilisateurs, groupes ou applications pour restreindre leur accès à des ressources spécifiques.
Usage principal : Gérer qui peut faire quoi (lecture, écriture, gestion) sur quelles ressources, avec une granularité fine.
Avantage : Réduction du risque d’erreur ou d'accès non autorisé grâce à des permissions bien définies.


## **Synthèse**
Pour protéger les données d’un Data Lake, il est stratégique de combiner ces outils :

- Utiliser `IAM/RBAC` pour contrôler l’accès par rôle.  
- Adopter `Microsoft Entra ID` pour authentifier les utilisateurs et applications.  
- Stocker les clés et secrets dans `Azure Key Vault`.  
- Délivrer des accès temporaires et limités via `SAS`.  
- Éviter ou minimiser l’utilisation des `Storage Access Keys` en faveur de méthodes plus sécurisées.