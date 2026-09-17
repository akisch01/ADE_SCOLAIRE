# Image de base Nginx Alpine ultra-légère
FROM nginx:alpine

# Copier tous les fichiers statiques du projet dans le répertoire de Nginx
COPY . /usr/share/nginx/html

# Exposer le port 80 pour le serveur web
EXPOSE 80

# Commande par défaut pour exécuter Nginx au premier plan
CMD ["nginx", "-g", "daemon off;"]
