import json
import oauth2
import argparse
import os
import subprocess

MAILDIR="/var/spool/imap"
JSON_DIR="/usr/local/lib/json"
#NO_MIGRAR = ["Junk","Sent","Trash","Drafts"]
NO_MIGRAR = ["Junk","Trash","Drafts"]

# PER REFRESCAR EL TOKEN:
#python /usr/local/bin/oauth2_test.py 
#           --client_id=808003594133-cb5igon9pdu51kb6tcmlvq56tc4nnp10.apps.googleusercontent.com 
#           --client_secret=qZx3ofzU1AIpmZxgd-nqDSmP 
#           --refresh_token=1//03o1QJDXSDvtPCgYIARAAGAMSNwF-L9IrUxTDYHH2D5jiD_s6V8q1toFqEW-GLW5TNy7VYGQzAhy98EBpYgyzLsPycgp6JUpC0qA
#
#  el modul oauth2 te la seguent funcio:
# def RefreshToken(client_id, client_secret, refresh_token):
#   retorna un dict (json) amb 'access_token', 'expires_in', and 'refresh_token'

MAIL2GMAIL="/usr/local/bin/maildir2gmail2.py"
#python /usr/local/bin/maildir2gmail2.py 
#      -u francesc.bassas@upc.edu 
#      -p ya29.a0AfH6SMCWKsBdyid8wbcmKKX6nFWMGOP2AnINsKINgCQH13fSkJG4wdnzSxcfIXQ3V7iZyyc17VJucY9q9spxM7twnKUOIeHx7O7clj_ioRT6DHfWQtAfri-Vj17iQR7XZEwAGtXNxBZt1REypJoOKaqxQJ5_a-hLgHrN 
#      --folder=Prisma Prisma

def get_refresh_token(usuari_local):
  fitxer = os.path.join(JSON_DIR,"{0}.json".format(usuari_local))
  with open(fitxer) as fitxer_json:
    data = json.load(fitxer_json)
    return data["refresh_token"]

def llegeix_json():
  with open(os.path.join(JSON_DIR,"client_secret.json")) as fitxer_json:
    data = json.load(fitxer_json)
    #print json.dumps(data)
    parametres = data["installed"]
    #print "client_id: {0}\n".format(parametres["client_id"])
    #print "client_secret: {0}\n".format(parametres["client_secret"])
    return parametres


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-l","--local",help="usuari local",required=True)
  parser.add_argument("-g","--gmail",help="correu gmail",required=True)
  arguments = parser.parse_args()

  primera_lletra = arguments.local[0]
  nom_bustia = arguments.local.replace(".","^")
  dir_bustia = os.path.join(MAILDIR,primera_lletra,"user",nom_bustia)
  print dir_bustia

  refresh_token = get_refresh_token(arguments.local)
  print refresh_token

  tokens_programa = llegeix_json() 

  # anem a generar tots els directoris
  els_dirs = []
  for root, dirs, files in os.walk(dir_bustia):
    print root
    for un_dir in dirs:
      print "{0}".format(os.path.join(root,un_dir))
      els_dirs.append(os.path.join(root,un_dir))

  ##dir_actual = os.getcwd()
  ##os.chdir(dir_bustia)
  #els_fitxers = [os.path.join(dir_bustia,f) for f in os.listdir(dir_bustia)]
  #els_dirs = [f for f in els_fitxers if os.path.isdir(f)]
  ##print els_dirs 
  ##dirs_migrar = [d for d in els_dirs if d not in NO_MIGRAR]

  # PROVA UN DIRECTORI
  #dirs_migrar = ["/var/spool/imap/f/user/frank/Leam"]
  #print dirs_migrar

  for el_dir in els_dirs:
    la_carpeta = el_dir.replace(dir_bustia + '/','')
    #la_carpeta = os.path.basename(el_dir)
    if la_carpeta not in NO_MIGRAR:
      tokens_nous = oauth2.RefreshToken(tokens_programa["client_id"],tokens_programa["client_secret"], refresh_token)
      print tokens_nous
      el_token = tokens_nous['access_token']
      #print el_token
      comanda = " ".join(["python",MAIL2GMAIL,"-u",arguments.gmail,"-p",el_token,"--folder=\"Correu CT/{0}\"".format(la_carpeta),"\"{1}\"".format(la_carpeta,el_dir)])
      print comanda
      subprocess.call(comanda, shell=True)

  # Falta migrar el INBOX
  tokens_nous = oauth2.RefreshToken(tokens_programa["client_id"],tokens_programa["client_secret"], refresh_token)
  el_token = tokens_nous['access_token']
  comanda = " ".join(["python",MAIL2GMAIL,"-u",arguments.gmail,"-p",el_token,"--folder=\"Correu CT/INBOX\"",dir_bustia])

  subprocess.call(comanda, shell=True)


  #os.chdir(dir_actual)



# Tipica invocacio
if __name__ == '__main__':
  main()

