# 🖥️ Mise en place du serveur SQL — SAE203

> À faire à chaque début de séance sur la VM Debian dans VirtualBox.

---

## ⚙️ Prérequis VirtualBox

Dans les paramètres de la VM → **Réseau → Adaptateur 1** :
- Mode : **Accès par pont**
- Interface : carte réseau de la salle

---

## 🚀 Étapes dans la VM Debian

### 1. Tuer NetworkManager

```bash
systemctl stop NetworkManager
systemctl disable NetworkManager
```

### 1.1 S'affecter une IP via le DHCP 

```bash
nano /etc/newtork/interface
```
Souvent enp0s3
```bash
auto enp0s3
iface enp0s3 inet dhcp
```

Puis il faut restart

```bash
systemctl restart networking
```
---

### 2. Installer MariaDB

```bash
apt install mariadb-server -y
```

---

### 3. Modifier le bind-address

```bash
nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Trouver la ligne et la modifier :
```
bind-address = 0.0.0.0
```

---

### 4. Créer la base de données et l'utilisateur

```bash
mariadb -u root
```

```sql
CREATE DATABASE sae203 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'django'@'%' IDENTIFIED BY 'motdepasse';
GRANT ALL PRIVILEGES ON sae203.* TO 'django'@'%';
FLUSH PRIVILEGES;
EXIT;
```

---

### 5. Redémarrer MariaDB

```bash
systemctl restart mariadb
```

---

### 6. Installer SSH (pour le transfert de fichiers)

```bash
apt install openssh-server -y
systemctl enable ssh
systemctl start ssh
```

---

### 7. Récupérer l'IP de la VM

```bash
ip a
```

> Noter l'IP de l'interface `enp0s3` (ex: `10.128.x.x`) → à mettre dans `settings.py`

---

## 💾 Importer la base de données

### Depuis Windows → copier le backup vers la VM

```powershell
scp C:\Users\TON_USER\Desktop\sae203_backup.sql root@IP_DE_LA_VM:/tmp/
```

### Dans la VM → importer le backup

```bash
mysql -u django -p sae203 < /tmp/sae203_backup.sql
```

Mot de passe : `motdepasse`

---

## 🐍 Configurer Django (settings.py)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sae203',
        'USER': 'django',
        'PASSWORD': 'motdepasse',
        'HOST': 'IP_DE_LA_VM',  # ex: 10.128.207.87
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

---

## 💿 Exporter la base en fin de séance

Dans la VM :
```bash
mysqldump -u django -p sae203 > /tmp/sae203_backup.sql
```

Depuis Windows → récupérer le backup :
```powershell
scp root@IP_DE_LA_VM:/tmp/sae203_backup.sql C:\Users\TON_USER\Desktop\
```

> ⚠️ Pense à sauvegarder le fichier `sae203_backup.sql` sur ta clé USB ou GitHub à chaque fin de séance !

---

## ✅ Vérifications rapides

```bash
# MariaDB tourne ?
systemctl status mariadb

# La base est là ?
mariadb -u root -e "SHOW DATABASES;"

# Le bind-address est bon ?
grep bind-address /etc/mysql/mariadb.conf.d/50-server.cnf

# L'IP de la VM ?
ip a
```
