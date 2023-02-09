import sqlite3, pandas
import streamlit as st

def ouvrirConnexion():
    conn = sqlite3.connect('data_biblio.db')
    cur=conn.cursor()
    return conn, cur

def executerRequete(requete):
    conn = sqlite3.connect('data_biblio.db')
    cur=conn.cursor()
    cur.execute(requete)
    
    # Fermeture de la connexion à la base de données
    conn.commit()
    conn.close()

def afficherRequete(requete):
    conn = sqlite3.connect('data_biblio.db')
    cur=conn.cursor()
    cur.execute(requete)
    
    # Récupération des résultats de la requête (s'il y en a)
    r = pandas.read_sql(requete, conn)
    # Fermeture de la connexion à la base de données
    conn.commit()
    conn.close()
    return r

def afficherTable(table):
    res = afficherRequete(f"SELECT * FROM {table}")
    return res

def ajouterTuple(table, attributs):
    # Construction de la requête d'insertion
    query = "INSERT INTO {} ({}) VALUES ({})".format(table, ', '.join(attributs.keys()), ', '.join(attributs.values()))
    
    # Exécution de la requête
    executerRequete(query)
    
def supprimerTuple(table, nomId, valeurId):
    # Construction de la requête de suppression
    req = "DELETE FROM " + table + " WHERE " + nomId + " = " + valeurId
    
    # Exécution de la requête de suppression
    executerRequete(req)

def terminerConnection(conn, cur):
    # Validation des modifications
    conn.commit()
    # Fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    
def empruntsAbonne(id):
    req = "SELECT livre.titre as 'Titre' FROM abonne INNER JOIN emprunte ON abonne.id_abonne = emprunte.id_abonne INNER JOIN exemplaire ON emprunte.id_exemplaire = exemplaire.id_exemplaire INNER JOIN livre ON exemplaire.id_livre = livre.id_livre WHERE emprunte.id_abonne =" + id 
    
    # Exécution de la requête 
    return afficherRequete(req)

def ajouterLivreAuteur(titre, date, nom, prenom):
    conn = sqlite3.connect('data_biblio.db')
    cur=conn.cursor()
    
    #Vérifions si le livre du même auteur existe déjà
    req1 = 'SELECT auteur.id_auteur FROM auteur INNER JOIN ecrit ON auteur.id_auteur = ecrit.id_auteur INNER JOIN livre ON ecrit.id_livre = livre.id_livre WHERE livre.titre= "{}" AND auteur.nom = "{}" AND auteur.prenom = "{}" AND livre.date_creation = {} '.format(titre, nom, prenom, date)
    res1 = pandas.read_sql(req1, conn)
    
    if res1.shape[0] == 0 :
        #On va insérer le livre 
        req2 = f'INSERT INTO livre (titre, date_creation) VALUES ("{titre}" , {date})'
        cur.execute(req2)
        id_liv = cur.lastrowid
        st.success(f"Le nouveau livre a été ajouté à la table LIVRE avec l\'id {id_liv}", icon="✅")
                
        req3 = f"SELECT id_auteur FROM auteur WHERE nom ='{nom}' AND prenom = '{prenom}' "
        res3 = pandas.read_sql(req3, conn)
        
        if res3.shape[0] == 1 :
            #L'auteur existe déjà
            id_aut = res3.at[0,'id_auteur']
            st.info(f"L\'auteur de ce livre existe déjà dans la base de donnée avec l\'id {id_aut}", icon="ℹ️")
            
        if res3.shape[0] == 0 :
            #On va insérer l'auteur 
            req4 = f"INSERT INTO auteur (nom, prenom) VALUES ('{nom}','{prenom}')"
            cur.execute(req4)
            id_aut = cur.lastrowid
            st.success(f"Le nouvel auteur a été ajouté à la table AUTEUR avec l\'id {id_aut}", icon="✅")
        
        req5 = f"INSERT INTO ecrit (id_auteur, id_livre) VALUES ('{id_aut}','{id_liv}')"
        cur.execute(req5)
        st.success("Un nouveau tuple a été inséré dans la table ECRIT !", icon="✅")
    else :
        st.warning("Ce livre de cet auteur existe déjà dans la base de donnée ! ", icon="⚠️")
    
    conn.commit()
    conn.close()

# Voici le programme principal 
st.title("Administration de la Bibliothèque")
st.sidebar.title("Voici le menu principal :")

if "bouton_clicked1" not in st.session_state:
    st.session_state.bouton_clicked1 = False

if "bouton_clicked2" not in st.session_state:
    st.session_state.bouton_clicked2 = False

if "bouton_clicked3" not in st.session_state:
    st.session_state.bouton_clicked3 = False

if "bouton_clicked4" not in st.session_state:
    st.session_state.bouton_clicked4 = False

if "bouton_clicked5" not in st.session_state:
    st.session_state.bouton_clicked5 = False
    
def callback1():
    st.session_state.bouton_clicked1 = True
    st.session_state.bouton_clicked2 = False
    st.session_state.bouton_clicked3 = False
    st.session_state.bouton_clicked4 = False
    st.session_state.bouton_clicked5 = False
    
def callback2():
    st.session_state.bouton_clicked1 = False
    st.session_state.bouton_clicked2 = True
    st.session_state.bouton_clicked3 = False
    st.session_state.bouton_clicked4 = False
    st.session_state.bouton_clicked5 = False

def callback3():
    st.session_state.bouton_clicked1 = False
    st.session_state.bouton_clicked2 = False
    st.session_state.bouton_clicked3 = True
    st.session_state.bouton_clicked4 = False
    st.session_state.bouton_clicked5 = False

def callback4():
    st.session_state.bouton_clicked1 = False
    st.session_state.bouton_clicked2 = False
    st.session_state.bouton_clicked3 = False
    st.session_state.bouton_clicked4 = True
    st.session_state.bouton_clicked5 = False

def callback5():
    st.session_state.bouton_clicked1 = False
    st.session_state.bouton_clicked2 = False
    st.session_state.bouton_clicked3 = False
    st.session_state.bouton_clicked4 = False
    st.session_state.bouton_clicked5 = True
    
if (st.sidebar.button('Afficher Table',on_click = callback1) or st.session_state.bouton_clicked1 ) :
    tab = st.sidebar.radio(
        "Quelle table souhaitez-vous afficher ?",
        ('abonne', 'auteur', 'correspond', 'decrit', 'ecrit', 'editeur',
         'emprunte', 'exemplaire','genre','livre','motcle'))    
    st.subheader(f"Voici la table {tab.upper()}")
    st.write(afficherTable(tab))

if (st.sidebar.button('Ajouter tuple', on_click = callback2) or st.session_state.bouton_clicked2 ):
    st.sidebar.write("*Nous allons ajouter un tuple dans la **table** de votre choix*")
    tu = st.sidebar.selectbox("**Choississez la table**", ('correspond', 'decrit', 'ecrit'), key='2')
    if tu =='correspond':
        gen1 = st.sidebar.text_input('**id_genre**')
        gen2 = st.sidebar.text_input('**id_livre**')
        etat=True
        if gen1 and gen2 :
            etat = False
        if st.sidebar.button('Ajouter', disabled=etat):
            att={"id_genre": gen1, "id_livre":gen2}
            try :
                ajouterTuple("correspond", att)
                st.success('Tuple ajouté', icon="✅")
                st.subheader("Table CORRESPOND")
                st.write(afficherTable("correspond"))
            except :
                st.warning('Ce Tuple existe déjà dans la table !!', icon="⚠️")
                st.write('Veuillez choisir un autre tuple.')
            
    if tu =='decrit':
        gen1 = st.sidebar.text_input('id_motcle')
        gen2 = st.sidebar.text_input('id_livre')
        etat=True
        if gen1 and gen2 :
            etat = False
        if st.sidebar.button('Ajouter', disabled=etat):
            att={"id_motcle": gen1, "id_livre":gen2}
            try :
                ajouterTuple("decrit", att)
                st.success('Tuple ajouté', icon="✅")
                st.subheader("Table DECRIT")
                st.write(afficherTable("decrit"))
            except :
                st.warning('Ce Tuple existe déjà dans la table !!', icon="⚠️")
                st.write('Veuillez choisir un autre tuple.')
            
    if tu =='ecrit':
        gen1 = st.sidebar.text_input('id_auteur')
        gen2 = st.sidebar.text_input('id_livre')
        etat=True
        if gen1 and gen2 :
            etat = False
        if st.sidebar.button('Ajouter', disabled=etat):
            att={"id_auteur": gen1, "id_livre":gen2}
            try :
                ajouterTuple("ecrit", att)
                st.success('Tuple ajouté', icon="✅")
                st.subheader("Table ECRIT")
                st.write(afficherTable("ecrit"))
            except :
                st.warning('Ce Tuple existe déjà dans la table !!', icon="⚠️")
                st.write('Veuillez choisir un autre tuple.')
            
if (st.sidebar.button('Supprimer tuple', on_click = callback3) or st.session_state.bouton_clicked3) :
    st.sidebar.write("*Nous allons supprimer un tuple dans la **table** de votre choix*")
    ch = st.sidebar.selectbox("Choississez la table", ('correspond', 'decrit', 'ecrit'), key='3')
    if ch == "correspond" :
        sch1 = st.sidebar.selectbox("Choississez le nom de l\'attribut à supprimer", ('id_genre', 'id_livre'))
        if sch1 :
            sch2 = st.sidebar.text_input(f'Entrez la valeur de {sch1}')
            etat=True
            if sch2 :
                etat = False
            if st.sidebar.button("Supprimer", disabled = etat):
                supprimerTuple("correspond", sch1, sch2)
                st.success('Tuple supprimé', icon="✅")
                st.subheader("Table CORRESPOND")
                st.write(afficherTable("correspond"))
    
    if ch == "decrit" :
        sch1 = st.sidebar.selectbox("Choississez le nom de l\'attribut à supprimer", ('id_motcle', 'id_livre'))
        if sch1 :
            sch2 = st.sidebar.text_input(f'Entrez la valeur de {sch1}')
            etat=True
            if sch2 :
                etat = False
            if st.sidebar.button("Supprimer", disabled = etat):
                supprimerTuple("decrit", sch1, sch2)
                st.success('Tuple supprimé', icon="✅")
                st.subheader("Table DECRIT")
                st.write(afficherTable("decrit"))
    
    if ch == "ecrit" :
        sch1 = st.sidebar.selectbox("Choississez le nom de l\'attribut à supprimer", ('id_auteur', 'id_livre'))
        if sch1 :
            sch2 = st.sidebar.text_input(f'Entrez la valeur de {sch1}')
            etat=True
            if sch2 :
                etat = False
            if st.sidebar.button("Supprimer", disabled = etat):
                supprimerTuple("ecrit", sch1, sch2)
                st.success('Tuple supprimé', icon="✅")
                st.subheader("Table ECRIT")
                st.write(afficherTable("ecrit"))
    
if (st.sidebar.button('Livre Emprunté', on_click = callback4) or st.session_state.bouton_clicked4) :
    st.sidebar.write("*Nous allons afficher la liste des livres empruntés par un abonné*")
    chox = st.sidebar.number_input("**Entrez l\'identifiant de l\'abonné**", min_value=1, step=1)
    etat = True
    if chox :
        etat = False
    if st.sidebar.button("Valider", disabled = etat):
        chox = f'{chox}'
        res = empruntsAbonne(chox)
        if res.shape[0] == 0:
            st.warning("Cet abonné n\'a emprunté aucun livre à la Bibliothèque ")
        else:
            st.subheader("Livres empruntés :")
            st.write(res)

if (st.sidebar.button('Ajouter un livre', on_click = callback5) or st.session_state.bouton_clicked5) :
    st.sidebar.write("*Nous allons ajouter un livre et son auteur dans la base de donnée*")
    inp1 = st.sidebar.text_input("**Entrez le titre du livre**")
    inp2 = st.sidebar.text_input("**Entrez la date de création du livre**")
    inp3 = st.sidebar.text_input("**Entrez le nom de l\'auteur**")
    inp4 = st.sidebar.text_input("**Entrez le prénom de l\'auteur**")
    etat = True 
    if inp1 and inp2 and inp3 and inp4 :
        etat = False
    if st.sidebar.button("Valider", disabled = etat) :
        ajouterLivreAuteur(inp1, inp2, inp3, inp4)


    
    